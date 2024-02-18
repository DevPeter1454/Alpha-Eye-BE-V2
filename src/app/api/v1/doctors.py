from typing import Annotated, Any

import fastapi
from fastapi import Depends, Request, UploadFile, Form, File
from sqlalchemy.ext.asyncio import AsyncSession

from ...api.dependencies import get_current_superuser, get_current_doctor_or_hospital, generate_doctor_id
from ...api.paginated import PaginatedListResponse, compute_offset, paginated_response
from ...core.db.database import async_get_db
from ...core.exceptions.http_exceptions import DuplicateValueException, ForbiddenException, NotFoundException
from ...core.security import blacklist_token, get_password_hash, oauth2_scheme
from ...crud.crud_rate_limit import crud_rate_limits
from ...crud.crud_tier import crud_tiers
from ...crud.crud_doctors import crud_doctors
from ...models.tier import Tier
from ...schemas.tier import TierRead
from ...schemas.hospital import HospitalRead
from ...schemas.doctor import DoctorCreate, DoctorCreateInternal, DoctorRead, DoctorUpdate
from ...core.utils.cache import cache
from pydantic import EmailStr
from ...core.config import settings
import cloudinary
import cloudinary.uploader

router = fastapi.APIRouter(tags=["doctors"])

cloudinary.config(
    cloud_name=f"{settings.CLOUDINARY_CLOUD_NAME}",
    api_key=f"{settings.CLOUDINARY_API_KEY}",
    api_secret=f"{settings.CLOUDINARY_API_SECRET}"
)


@router.post("/doctor", status_code=201, response_model=DoctorRead)
async def write_doctor(
    request: Request,

        db: Annotated[AsyncSession, Depends(async_get_db)],
        current_user: Annotated[HospitalRead, Depends(get_current_doctor_or_hospital)],
        doctor: DoctorCreate = Depends(),
        file: UploadFile = File(...), ) -> DoctorRead:
    doctor_row = await crud_doctors.get(db=db, email=doctor.email)
    if doctor_row is not None:
        raise DuplicateValueException("Doctor is already registered")

    response = cloudinary.uploader.upload(file.file)

    # print(current_user)

    doctor_internal_dict = doctor.model_dump()
    doctor_internal_dict["hashed_password"] = get_password_hash(
        password=doctor_internal_dict["password"])
    doctor_internal_dict["doctor_id"] = generate_doctor_id()
    doctor_internal_dict["profile_image_url"] = response["url"]
    doctor_internal_dict["hospital_id"] = current_user["hospital_id"]
    del doctor_internal_dict["password"]
    doctor_internal = DoctorCreateInternal(
        **doctor_internal_dict)
    created_doctor: DoctorRead = await crud_doctors.create(db=db, object=doctor_internal)
    return created_doctor
