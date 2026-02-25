from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.services.database import get_db

router = APIRouter(prefix="/database-analysis", tags=["Analysis"])

@router.get("")
async def get_database_analysis(db: Session = Depends(get_db)):
    try:
        sql = """
            SELECT
                (SELECT COUNT(*) FROM properties WHERE city ILIKE 'Wellington%') as wellington_properties,
                (SELECT COUNT(*) FROM properties WHERE city ILIKE 'Auckland%') as auckland_properties,
                
                (SELECT COUNT(*) FROM properties_with_latest_status WHERE city ILIKE 'Wellington%') as wellington_forecast_total,
                (SELECT COUNT(*) FROM properties_with_latest_status WHERE city ILIKE 'Auckland%') as auckland_forecast_total,
                
                (SELECT COUNT(*) FROM properties_with_latest_status WHERE city ILIKE 'Auckland%' AND confidence_score >= 0.9) as auckland_forecast_90_percent,
                (SELECT COUNT(*) FROM properties_with_latest_status WHERE city ILIKE 'Auckland%' AND confidence_score >= 0.8) as auckland_forecast_80_percent,
                (SELECT COUNT(*) FROM properties_with_latest_status WHERE city ILIKE 'Auckland%' AND confidence_score >= 0.6) as auckland_forecast_60_percent,
                
                (SELECT COUNT(*) FROM properties_with_latest_status WHERE city ILIKE 'Wellington%' AND confidence_score >= 0.9) as wellington_forecast_90_percent,
                (SELECT COUNT(*) FROM properties_with_latest_status WHERE city ILIKE 'Wellington%' AND confidence_score >= 0.8) as wellington_forecast_80_percent,
                (SELECT COUNT(*) FROM properties_with_latest_status WHERE city ILIKE 'Wellington%' AND confidence_score >= 0.6) as wellington_forecast_60_percent
        """
        result = db.execute(text(sql))
        row = result.mappings().first()

        if row:
            return dict(row)
            
        return {
            "wellington_properties": 0,
            "auckland_properties": 0,
            "wellington_forecast_total": 0,
            "auckland_forecast_total": 0,
            "auckland_forecast_90_percent": 0,
            "auckland_forecast_80_percent": 0,
            "auckland_forecast_60_percent": 0,
            "wellington_forecast_90_percent": 0,
            "wellington_forecast_80_percent": 0,
            "wellington_forecast_60_percent": 0
        }

    except Exception as e:
        print(f"Error fetching database analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
