from pydantic import BaseModel, Field


# ==========================================
# PRODUCE LISTING SCHEMA
# ==========================================
from typing import List, Optional, Union
from enum import Enum


class CropType(str, Enum):
    ONION = "Onion"
    SOYBEAN = "Soybean"
    COTTON = "Cotton"


class QualityGrade(str, Enum):
    GRADE_A = "Grade A"
    GRADE_B = "Grade B"
    GRADE_C = "Grade C"


class GradeResult(BaseModel):
    crop_type: CropType
    grade: QualityGrade
    uniformity_score: float = Field(..., ge=0.0, le=100.0)
    defect_percentage: float = Field(..., ge=0.0, le=100.0)
    estimated_shelf_life_days: Union[int, str]
    rejection_reasons: List[str] = []
    agmarknet_compliant: bool = True


class ProduceListing(BaseModel):

    farmer_name: str

    phone: str = Field(
        ...,
        pattern=r"^\+?[0-9]{10,13}$",
        description="Valid contact phone number"
    )

    district: str

    crop_type: str

    quantity_quintals: float = Field(
        ...,
        gt=0,
        le=10000,
        description="Quantity must be positive and realistic"
    )

    expected_price_per_quintal: float = Field(
        ...,
        gt=100,
        le=100000,
        description="Price must be within realistic agricultural bounds"
    )

    grade: str = "Grade A"

    uniformity_score: float = 94.0

    defect_percentage: float = 3.2


# ==========================================
# BID SCHEMA
# ==========================================

class Bid(BaseModel):

    listing_id: str

    buyer_company: str

    bid_price_per_quintal: float = Field(
        ...,
        gt=100,
        le=100000
    )

    delivery_terms: str