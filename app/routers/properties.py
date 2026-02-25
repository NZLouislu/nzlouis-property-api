from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.models.property import PropertyBase
from app.services.database import get_db

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
    db: Session = Depends(get_db)
) -> List[PropertyBase]:
    if not id and not exact and not city:
        return []

    try:
        table_name = 'properties'
        
        sql = f"""
            SELECT 
                id, property_url, last_sold_price, address, suburb, city, 
                bedrooms, bathrooms, car_spaces, land_area, last_sold_date, 
                region, cover_image_url
            FROM {table_name}
            WHERE 1=1
        """
        params = {}

        if id:
            sql += " AND id = :id"
            params["id"] = id
        else:
            if not exact and city:
                sql += " AND city = :city"
                params["city"] = city

            if not exact and suburbs:
                suburb_list = [s.strip() for s in suburbs.split(',') if s.strip()]
                if suburb_list:
                    sql += " AND suburb = ANY(:suburbs)"
                    params["suburbs"] = suburb_list

            if search:
                if exact:
                    street_address = search.split(',')[0].strip()
                    sql += " AND address ILIKE :search_exact"
                    params["search_exact"] = f"{street_address}%"
                else:
                    if search[0].isdigit():
                        sql += " AND address ILIKE :search_start"
                        params["search_start"] = f"{search}%"
                    else:
                        sql += " AND address ILIKE :search_contains"
                        params["search_contains"] = f"%{search}%"

            if not exact and not id:
                sql += " ORDER BY id"

            sql += " LIMIT :limit OFFSET :offset"
            params["limit"] = page_size
            params["offset"] = page * page_size

        result = db.execute(text(sql), params)
        rows = result.mappings().all()
        
        return [dict(row) for row in rows]

    except Exception as e:
        print(f"Error fetching properties: {str(e)}")
        if 'timeout' in str(e).lower() or '57014' in str(e):
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "Database query timeout.",
                    "code": "TIMEOUT"
                }
            )
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/autocomplete", response_model=List[str])
async def autocomplete_properties(
    query: str = Query(..., min_length=1, description="Search keyword"),
    city: Optional[str] = Query(None, description="City filter"),
    limit: int = Query(10, ge=1, le=20, description="Result limit"),
    db: Session = Depends(get_db)
) -> List[str]:
    try:
        sql = "SELECT address FROM properties WHERE 1=1"
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
