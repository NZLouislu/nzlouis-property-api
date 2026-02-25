from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.models.property import ForecastProperty
from app.services.database import get_db

router = APIRouter(prefix="/forecast", tags=["Forecast"])

@router.get("", response_model=List[ForecastProperty])
async def get_forecast_properties(
    city: str = Query(..., description="City name"),
    page: int = Query(0, ge=0, description="Page number"),
    page_size: int = Query(9, ge=1, le=50, description="Items per page"),
    suburbs: Optional[str] = Query(None, description="Comma-separated suburbs"),
    db: Session = Depends(get_db)
) -> List[ForecastProperty]:
    try:
        sql = """
            SELECT 
                property_url, last_sold_price, address, suburb, city, 
                bedrooms, bathrooms, car_spaces, land_area, last_sold_date, 
                cover_image_url, confidence_score, predicted_status
            FROM properties_with_latest_status
            WHERE city = :city
        """
        params = {"city": city}

        if suburbs:
            suburb_list = [s.strip() for s in suburbs.split(',') if s.strip()]
            if suburb_list:
                sql += " AND suburb = ANY(:suburbs)"
                params["suburbs"] = suburb_list

        sql += " ORDER BY confidence_score DESC LIMIT :limit OFFSET :offset"
        params["limit"] = page_size
        params["offset"] = page * page_size

        result = db.execute(text(sql), params)
        rows = result.mappings().all()

        if rows:
            return [dict(row) for row in rows]

        print(f"[INFO] No forecast data for {city}, falling back to properties table")

        fallback_sql = """
            SELECT 
                property_url, last_sold_price, address, suburb, city, 
                bedrooms, bathrooms, car_spaces, land_area, last_sold_date, 
                cover_image_url
            FROM properties
            WHERE city = :city
        """
        if suburbs:
            if suburb_list:
                fallback_sql += " AND suburb = ANY(:suburbs)"

        fallback_sql += " LIMIT :limit OFFSET :offset"
        
        fallback_result = db.execute(text(fallback_sql), params)
        fallback_rows = fallback_result.mappings().all()

        return [
            {**dict(row), 'confidence_score': 0.0, 'predicted_status': 'Unknown', 'predicted_price': 0}
            for row in fallback_rows
        ]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/autocomplete", response_model=List[str])
async def autocomplete_forecast(
    query: str = Query(..., min_length=1, description="Search keyword"),
    city: Optional[str] = Query(None, description="City filter"),
    limit: int = Query(10, ge=1, le=20, description="Result limit"),
    db: Session = Depends(get_db)
) -> List[str]:
    try:
        sql = "SELECT address FROM properties_with_latest_status WHERE 1=1"
        params = {"limit": limit}

        if city:
            sql += " AND city = :city"
            params["city"] = city

        if query[0].isdigit():
            sql += " AND address ILIKE :query_start"
            params["query_start"] = f"{query}%"
        else:
            sql += " AND address ILIKE :query_contains"
            params["query_contains"] = f"%{query}%"

        sql += " LIMIT :limit"
        result = db.execute(text(sql), params)
        return [row[0] for row in result.all()]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
