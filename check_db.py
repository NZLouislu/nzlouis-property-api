import asyncio
from sqlalchemy import text
from app.services.database import SessionLocal

def check_db():
    db = SessionLocal()
    try:
        print("--- Properties Table Cities ---")
        result = db.execute(text("SELECT city, COUNT(*) FROM properties GROUP BY city"))
        for row in result:
            print(f"City: '{row[0]}', Count: {row[1]}")
            
        print("\n--- Properties With Latest Status Cities ---")
        result = db.execute(text("SELECT city, COUNT(*) FROM properties_with_latest_status GROUP BY city"))
        for row in result:
            print(f"City: '{row[0]}', Count: {row[1]}")
            
        print("\n--- Properties With Latest Status Confidence Scores (Wellington City) ---")
        result = db.execute(text("SELECT confidence_score, COUNT(*) FROM properties_with_latest_status WHERE city = 'Wellington City' GROUP BY confidence_score ORDER BY confidence_score DESC LIMIT 5"))
        for row in result:
            print(f"Confidence: {row[0]}, Count: {row[1]}")
            
    finally:
        db.close()

if __name__ == "__main__":
    check_db()
