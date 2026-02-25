import json
from sqlalchemy import text
from app.services.database import SessionLocal

def check_db():
    db = SessionLocal()
    output = {"properties": [], "forecast": []}
    try:
        result = db.execute(text("SELECT city, COUNT(*) FROM properties GROUP BY city"))
        for row in result:
            output["properties"].append({"city": row[0], "count": row[1]})
            
        result = db.execute(text("SELECT city, COUNT(*) FROM properties_with_latest_status GROUP BY city"))
        for row in result:
            output["forecast"].append({"city": row[0], "count": row[1]})
            
        with open("db_output.json", "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2)
            
    finally:
        db.close()

if __name__ == "__main__":
    check_db()
