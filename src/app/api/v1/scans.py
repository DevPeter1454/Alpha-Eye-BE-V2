from typing import Annotated, Any

import fastapi
from fastapi import Depends, Request, UploadFile, Form, File
from sqlalchemy.ext.asyncio import AsyncSession

from ...api.dependencies import get_current_superuser, get_current_doctor_or_hospital, generate_doctor_id, get_current_user, generate_scan_id
import requests

from ...api.paginated import PaginatedListResponse, compute_offset, paginated_response
from ...core.db.database import async_get_db
from ...core.exceptions.http_exceptions import DuplicateValueException, ForbiddenException, NotFoundException
from ...core.security import blacklist_token, get_password_hash, oauth2_scheme
from ...api.paginated import PaginatedListResponse, compute_offset, paginated_response
from ...core.db.database import async_get_db
from ...core.exceptions.http_exceptions import DuplicateValueException, ForbiddenException, NotFoundException
from ...core.security import blacklist_token, get_password_hash, oauth2_scheme
from ...crud.crud_rate_limit import crud_rate_limits
from ...crud.crud_users import crud_users
from ...crud.crud_tier import crud_tiers
from ...crud.crud_scans import crud_scans
from ...schemas.scans import ScanCreate, ScanRead, ScanUpdate
from ...schemas.user import UserRead
from ...core.utils.cache import cache
from pydantic import EmailStr
from ...core.config import settings
import cloudinary
import cloudinary.uploader
import datetime


router = fastapi.APIRouter(prefix="/scans", tags=["scans"])

cloudinary.config(
    cloud_name=f"{settings.CLOUDINARY_CLOUD_NAME}",
    api_key=f"{settings.CLOUDINARY_API_KEY}",
    api_secret=f"{settings.CLOUDINARY_API_SECRET}"
)


@router.post("/upload")
async def upload_scan(
    db: Annotated[AsyncSession, Depends(async_get_db)],
    current_user: Annotated[UserRead, Depends(get_current_user)],
    request: Request,
    file: UploadFile = File(...),
):
    if current_user["role"] in ["Doctor", "Hospital"]:
        raise ForbiddenException("Not authorized")

    user_exists = await crud_users.exists(db=db, id=current_user["id"])

    if not user_exists:
        raise NotFoundException("User not found")

    response = cloudinary.uploader.upload(file.file)

    url = 'https://www.nyckel.com/v1/functions/7hdsc8b5br345bz3/invoke'

    data = {
        "data": response['url']
    }

    response_from_external_api = requests.post(url, json=data)

    label_name = response_from_external_api.json()['labelName']

    label_id = response_from_external_api.json()['labelId']

    label_confidence = response_from_external_api.json()['confidence']

    if label_name == "Normal":
        if label_confidence < 0.8:
            scan_response = {
                "label_name": label_name,
                "label_id": label_id,
                "label_confidence": int(label_confidence * 100),
                "detected_conditions": "None",
                "severity": "None",
                "health_status": "Not Normal",
                "scan_id": generate_scan_id(),
                "title": "None",
                "description": "The scan is not too good for normal. The confidence level is less than 80%.",
                "recommendations": "It is advisable to see a doctor for further diagnosis",
                "special_id": current_user["special_id"],
                "created_at": datetime.datetime.now(),
            }
            scan_internal_create = ScanCreate(**scan_response)

            created_scan = await crud_scans.create(db=db, object=scan_internal_create)
            return {
                "scan": created_scan,
                "detailed_description": {
                    "title": created_scan.title,
                    "description": created_scan.description,
                    "recommendation": created_scan.recommendations
                }
            }
    else:
        scan_response = {
            "label_name": label_name,
            "label_id": label_id,
            "label_confidence": int(label_confidence * 100),
            "detected_conditions": "None",
            "severity": "None",
            "health_status": "Normal",
            "scan_id": generate_scan_id(),
            "title": "None",
            "description": "The scan is good for normal. The confidence level is greater than 80%.",
            "recommendations": "It's good to always do a regular checkup. Please see a doctor for further diagnosis.",
            "special_id": current_user["special_id"],
            "created_at": datetime.datetime.now(),
        }
        scan_internal_create = ScanCreate(**scan_response)

        created_scan = await crud_scans.create(db=db, object=scan_internal_create)

        return {
            "scan": created_scan,
            "detailed_description": {
                "title": created_scan.title,
                "description": created_scan.description,
                "recommendation": created_scan.recommendations
            }
        }

    if label_name == "Cataracts":
        if label_confidence < 0.70:
            scan_response = {
                "label_name": label_name,
                "label_id": label_id,
                "label_confidence": int(label_confidence * 100),
                "detected_conditions": "Cataracts",
                "severity": "Mild",
                "health_status": "Not Normal",
                "scan_id": generate_scan_id(),
                "title": "What are Cataracts?",
                "description": "Cataracts are a common eye condition that often develops with age. They occur when the clear lens in your eye becomes cloudy, leading to blurred or dimmed vision. Cataracts can impact your daily life and well-being, making it essential to understand your specific condition and explore treatment options.",
                "recommendations": "It is strongly recommended to schedule an appointment with an ophthalmologist for a comprehensive eye examination. They will assess the extent of your cataracts and discuss treatment options.",
                "special_id": current_user["special_id"],
                "created_at": datetime.datetime.now(),
            }
            scan_internal_create = ScanCreate(**scan_response)
            created_scan = await crud_scans.create(db=db, object=scan_internal_create)
            return {
                "scan": created_scan,
                "detailed_description": {
                    "title": created_scan.title,
                    "description": created_scan.description,
                    "recommendation": created_scan.recommendations
                }
            }
        else:
            scan_response = {
                "label_name": label_name,
                "label_id": label_id,
                "label_confidence": int(label_confidence * 100),
                "detected_conditions": "Cataracts",
                "severity": "Mild",
                "health_status": "Not Normal",
                "scan_id": generate_scan_id(),
                "title": "What are Cataracts?",
                "description": "Cataracts are a common eye condition that often develops with age. They occur when the clear lens in your eye becomes cloudy, leading to blurred or dimmed vision. Cataracts can impact your daily life and well-being, making it essential to understand your specific condition and explore treatment options.",
                "recommendations": "Your cataracts are in an advanced stage, affecting your vision significantly. This means that you may have trouble reading, driving, or performing other daily activities.Also you may experience blurred or cloudy vision. Difficulty seeing in low light conditions.Colors may appear faded. Glare from bright lights can be bothersome. It is strongly recommended to schedule an appointment with an ophthalmologist for a comprehensive eye examination. They will assess the extent of your cataracts and discuss treatment options.",
                "special_id": current_user["special_id"],
                "created_at": datetime.datetime.now(),
            }
            scan_internal_create = ScanCreate(**scan_response)
            created_scan = await crud_scans.create(db=db, object=scan_internal_create)
            return {
                "scan": created_scan,
                "detailed_description": {
                    "title": created_scan.title,
                    "description": created_scan.description,
                    "recommendation": created_scan.recommendations
                }
            }


@router.get("/history", status_code = 200)
async def read_user_scan_history(
    request:Request,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    current_user: Annotated[UserRead, Depends(get_current_user)],
):
    pass