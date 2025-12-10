from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import date

class PropertyBase(BaseModel):
    id: str
    property_url: str
    address: str
    suburb: str
    city: str
    region: str

    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    car_spaces: Optional[int] = None
    land_area: Optional[float] = None

    last_sold_price: Optional[int] = None
    last_sold_date: Optional[date] = None
    cover_image_url: Optional[str] = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "property_url": "https://homes.co.nz/address/auckland/...",
                "address": "123 Queen Street",
                "suburb": "Auckland Central",
                "city": "Auckland",
                "region": "Auckland",
                "bedrooms": 3,
                "bathrooms": 2,
                "car_spaces": 1,
                "land_area": 350.5,
                "last_sold_price": 850000,
                "last_sold_date": "2023-06-15",
                "cover_image_url": "https://..."
            }
        }

class ForecastProperty(PropertyBase):
    confidence_score: float = Field(ge=0.0, le=1.0)
    predicted_status: str
    predicted_price: Optional[int] = None

    @field_validator('confidence_score')
    @classmethod
    def validate_confidence(cls, v):
        if not 0 <= v <= 1:
            raise ValueError('Confidence score must be between 0 and 1')
        return v

class PropertyQueryParams(BaseModel):
    city: Optional[str] = None
    page: int = Field(default=0, ge=0)
    page_size: int = Field(default=9, ge=1, le=50)
    suburbs: Optional[str] = None
    search: Optional[str] = None
    exact: bool = False
    id: Optional[str] = None

    @field_validator('suburbs')
    @classmethod
    def parse_suburbs(cls, v):
        if v:
            return [s.strip() for s in v.split(',') if s.strip()]
        return []
