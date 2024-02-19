from datetime import datetime
from typing import Annotated, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, UUID4

from ..core.schemas import PersistentDeletion, TimestampSchema, UUIDSchema


class ScanBase(BaseModel):
    label_name: Annotated[str, Field(
        min_length=2, max_length=30, examples=["User"])]
    label_id: Annotated[str, Field(
        min_length=2, max_length=30, examples=["123abc"])]
    label_confidence: int
    detected_conditions: Annotated[str, Field(
        min_length=2, max_length=30, examples=["User"])]
    
    scan_id:str

    severity: Annotated[str, Field(examples=["Low"])]
    health_status: Annotated[str, Field(examples=["Good"])]
    title: Annotated[str, Field(
        min_length=2, max_length=30, examples=["User"])]
    description: Annotated[str, Field(
        None, min_length=5, max_length=100)] 
    special_id: Annotated[str, Field(None, alias="specialId")]
    created_at: datetime
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]
    is_deleted: bool = False
    uuid: UUID4


class ScanCreate(ScanBase):
    model_config = ConfigDict(extra="forbid")


class ScanRead(BaseModel):
    scan: dict
    detailed_description: dict

class ScanUpdate(BaseModel):
    pass

class Scan(ScanBase, TimestampSchema, UUIDSchema, PersistentDeletion):
    pass

class ScanCreateInternal(ScanBase):
    model_config = ConfigDict(extra="forbid")


class ScanDelete(BaseModel):
    model_config = ConfigDict(extra="forbid")
    deleted_at: datetime
    is_deleted: bool = True
