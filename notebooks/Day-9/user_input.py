from pydantic import BaseModel, Field, field_validator, computed_field
from typing import Literal, Annotated

from config.city_tier import tier_1_cities, tier_2_cities

class UserInput(BaseModel):
age: Annotated[
int,
Field(gt=0, lt=120, description=“Age of the user”)
]

weight: Annotated[
    float,
    Field(gt=0, description="Weight in kilograms")
]
height: Annotated[
    float,
    Field(gt=0, lt=2.5, description="Height in meters")
]
income_lpa: Annotated[
    float,
    Field(gt=0, description="Annual income in Lakhs Per Annum")
]
smoker: bool
city: Annotated[
    str,
    Field(min_length=2, description="City name")
]
occupation: Literal[
    "retired",
    "freelancer",
    "student",
    "government_job",
    "business_owner",
    "unemployed",
    "private_job"
]
@field_validator("city")
@classmethod
def normalize_city(cls, value: str) -> str:
    return value.strip().title()
@computed_field
@property
def bmi(self) -> float:
    return round(self.weight / (self.height ** 2), 2)
@computed_field
@property
def lifestyle_risk(self) -> str:
    if self.smoker and self.bmi > 30:
        return "high"
    elif self.smoker or self.bmi > 27:
        return "medium"
    return "low"
@computed_field
@property
def age_group(self) -> str:
    if self.age < 25:
        return "young"
    elif self.age < 45:
        return "adult"
    elif self.age < 60:
        return "middle_aged"
    return "senior"
@computed_field
@property
def city_tier(self) -> int:
    if self.city in tier_1_cities:
        return 1
    elif self.city in tier_2_cities:
        return 2
    return 3