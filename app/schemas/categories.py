# app/schemas/categories.py

from pydantic import BaseModel, Field



class CategoryCreate(BaseModel):
    name: str = Field(...)



class CategorySchema(BaseModel):
    id: int = Field(...)
    name: str = Field(...)

    # question_text: str = Field(...)
    # is_agree: bool = Field(...)
    # question_id: int = Field(...)
    # text: str | None = Field(default=None)
    # user_id: int | None = Field(default=None)
    # user_nickname: str | None = Field(default=None)


