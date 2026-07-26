from pydantic import BaseModel, Field

class PropertyCreate(BaseModel):
    title: str
    district: str
    address: str
    monthly_rent: int = Field(gt=0)
    area: float = Field(gt=0)
    bedroom_count: int = Field(ge=0)
    commute_minutes: int = Field(ge=0)
    allows_pet: bool = False
    pet_deposit: int = Field(default=0, ge=0)
    floor: str
    deposit_months: int = Field(default=1, ge=0)
    description: str = ""

class PropertyUpdate(BaseModel):
    title:str | None =None
    district: str | None = None
    address: str | None = None
    monthly_rent: int | None = Field(default=None, gt=0)
    area: float | None = Field(default=None, gt=0)
    bedroom_count: int | None = Field(default=None, ge=0)
    commute_minutes: int | None = Field(default=None, ge=0)
    allows_pet: bool | None = None
    pet_deposit: int | None = Field(default=None, ge=0)
    floor: str | None = None
    deposit_months: int | None = Field(default=None, ge=0)
    description: str | None = None