# app/schemas/categories.py

from pydantic import BaseModel, Field



class CategoryCreate(BaseModel):
    name: str = Field(...)



class CategorySchema(BaseModel):
    id: int = Field(...)
    name: str = Field(...)

