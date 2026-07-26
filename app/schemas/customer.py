from pydantic import BaseModel,Field

class CustomerNeed(BaseModel):
    budget : int | None= Field(default=None,gt=0)
    district: str | None = None
    bedroom_count: int | None = Field(default=None,ge=0)
    has_pet: bool | None=None
    workplace:str | None=None
    max_commute_minutes: int | None =Field(default=None,gt=0)
