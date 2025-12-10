
from pydantic import BaseModel, ValidationError, field_validator
from typing import Optional

# 1. Define the current problematic model (mimicking app/models/property.py)
class PropertyOriginal(BaseModel):
    land_area: Optional[float] = None

# 2. Define the fixed model
class PropertyFixed(BaseModel):
    land_area: Optional[float] = None

    @field_validator('land_area', mode='before')
    @classmethod
    def parse_land_area(cls, v):
        if isinstance(v, str):
            # Handle cases like "433 m2", "541 m2", "-"
            clean_v = v.lower().replace('m2', '').replace(',', '').strip()
            if clean_v == '-' or not clean_v:
                return None
            try:
                return float(clean_v)
            except ValueError:
                return None  # Fallback to None if parsing fails
        return v

# 3. Test Cases from the log
test_inputs = [
    "433 m2",
    "541 m2", 
    "84 m2",
    "-",
    "2295 m2",
    424  # Should still work
]

print("--- Testing Original Model (Expected to Fail) ---")
for input_val in test_inputs:
    try:
        PropertyOriginal(land_area=input_val)
        print(f"✅ Original Model accepted: '{input_val}' (Unexpected)")
    except ValidationError as e:
        print(f"❌ Original Model failed on: '{input_val}'")

print("\n--- Testing Fixed Model (Expected to Succeed) ---")
for input_val in test_inputs:
    try:
        obj = PropertyFixed(land_area=input_val)
        print(f"✅ Fixed Model parsed '{input_val}' -> {obj.land_area}")
    except ValidationError as e:
        print(f"❌ Fixed Model failed on: '{input_val}'")
        print(e)
