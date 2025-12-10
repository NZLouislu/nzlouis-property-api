from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from app.models.property import ForecastProperty
from app.services.supabase_client import get_supabase_client
from supabase import Client

router = APIRouter(prefix="/forecast", tags=["Forecast"])

@router.get("", response_model=List[ForecastProperty])
async def get_forecast_properties(
    city: str = Query(..., description="City name"),
    page: int = Query(0, ge=0, description="Page number"),
    page_size: int = Query(9, ge=1, le=50, description="Items per page"),
    suburbs: Optional[str] = Query(None, description="Comma-separated suburbs"),
    supabase: Client = Depends(get_supabase_client)
) -> List[ForecastProperty]:
    try:
        query = supabase.table('properties_with_latest_status').select("""
            property_url,
            last_sold_price,
            address,
            suburb,
            city,
            bedrooms,
            bathrooms,
            car_spaces,
            land_area,
            last_sold_date,
            cover_image_url,
            confidence_score,
            predicted_status
        """).eq("city", city).order("confidence_score", desc=True)

        if suburbs:
            suburb_list = [s.strip() for s in suburbs.split(',') if s.strip()]
            if suburb_list:
                query = query.in_("suburb", suburb_list)

        start = page * page_size
        end = start + page_size - 1
        query = query.range(start, end)

        response = query.execute()

        if response.data:
            return response.data

        print(f"[INFO] No forecast data for {city}, falling back to properties table")

        fallback_query = supabase.table('properties').select("""
            property_url,
            last_sold_price,
            address,
            suburb,
            city,
            bedrooms,
            bathrooms,
            car_spaces,
            land_area,
            last_sold_date,
            cover_image_url
        """).eq("city", city)

        if suburbs:
            suburb_list = [s.strip() for s in suburbs.split(',') if s.strip()]
            if suburb_list:
                fallback_query = fallback_query.in_("suburb", suburb_list)

        fallback_query = fallback_query.range(start, end)
        fallback_response = fallback_query.execute()

        if fallback_response.data:
            return [
                {**item, 'confidence_score': 0.0, 'predicted_status': 'Unknown', 'predicted_price': 0}
                for item in fallback_response.data
            ]

        return []

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/autocomplete", response_model=List[str])
async def autocomplete_forecast(
    query: str = Query(..., min_length=1, description="Search keyword"),
    city: Optional[str] = Query(None, description="City filter"),
    limit: int = Query(10, ge=1, le=20, description="Result limit"),
    supabase: Client = Depends(get_supabase_client)
) -> List[str]:
    try:
        db_query = supabase.table('properties_with_latest_status').select('address')

        if city:
            db_query = db_query.eq('city', city)

        if query[0].isdigit():
            db_query = db_query.ilike('address', f'{query}%')
        else:
            db_query = db_query.ilike('address', f'%{query}%')

        db_query = db_query.limit(limit)
        response = db_query.execute()

        return [item['address'] for item in response.data] if response.data else []

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
