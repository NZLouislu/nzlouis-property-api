from pydantic import BaseModel
from typing import List

class Suburb(BaseModel):
    id: str
    name: str

class City(BaseModel):
    id: str
    name: str
    suburbs: List[Suburb]

class Region(BaseModel):
    id: str
    name: str
    cities: List[City]
