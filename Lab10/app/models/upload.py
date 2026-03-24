from sqlmodel import Field, SQLModel
from typing import Optional

class Upload(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    filename: str = Field(index=True, unique=True)
    original_filename: str = Field(index=True)