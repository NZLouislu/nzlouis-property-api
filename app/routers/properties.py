from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from app.models.property import PropertyBase
from app.services.supabase_client import get_supabase_client
from supabase import Client

router = APIRouter(prefix="/property", tags=["Properties"])

@router.get("", response_model=List[PropertyBase])
async def get_properties(
    city: Optional[str] = Query(None, description="City name"),
    page: int = Query(0, ge=0, description="Page number (0-indexed)"),
    page_size: int = Query(9, ge=1, le=50, description="Items per page"),
    suburbs: Optional[str] = Query(None, description="Comma-separated suburbs"),
    search: Optional[str] = Query(None, description="Address search keyword"),
    exact: bool = Query(False, description="Exact search mode"),
    id: Optional[str] = Query(None, description="Property ID"),
    supabase: Client = Depends(get_supabase_client)
) -> List[PropertyBase]:
    if not id and not exact and not city:
        return []

    try:
        table_check = supabase.table('properties').select('id').limit(1).execute()
        table_name = 'properties_view' if table_check.data is None else 'properties'

        query = supabase.table(table_name).select("""
            id,
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
            region,
            cover_image_url
        """)

        if id:
            query = query.eq("id", id)
        else:
            if not exact and city:
                query = query.eq("city", city)

            if not exact and suburbs:
                suburb_list = [s.strip() for s in suburbs.split(',') if s.strip()]
                if suburb_list:
                    query = query.in_("suburb", suburb_list)

            if search:
                if exact:
                    street_address = search.split(',')[0].strip()
                    query = query.ilike('address', f'{street_address}%').limit(1)
                else:
                    if search[0].isdigit():
                        query = query.ilike('address', f'{search}%')
                    else:
                        query = query.ilike('address', f'%{search}%')

            if not exact and not id:
                query = query.order("id")

            start = page * page_size
            end = start + page_size - 1
            query = query.range(start, end)

        response = query.execute()

        if response.data is None:
            raise HTTPException(status_code=500, detail="Database query failed")

        return response.data

    except Exception as e:
        if 'timeout' in str(e).lower() or '57014' in str(e):
            raise HTTPException(
                status_code=500,
                detail={
                    "error": f"Database query timeout. City '{city}' has too much data.",
                    "code": "TIMEOUT",
                    "suggestion": "Please select specific suburbs to narrow the search. Maximum 2 pages (18 items) to prevent timeout"
                }
            )
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/autocomplete", response_model=List[str])
async def autocomplete_properties(
    query: str = Query(..., min_length=1, description="Search keyword"),
    city: Optional[str] = Query(None, description="City filter"),
    limit: int = Query(10, ge=1, le=20, description="Result limit"),
    supabase: Client = Depends(get_supabase_client)
) -> List[str]:
    try:
        db_query = supabase.table('properties').select('address')

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
