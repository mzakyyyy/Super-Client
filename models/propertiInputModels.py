from models.bankModels import Bank_Properties
from pydantic import BaseModel, Field

class Properties_Fix(BaseModel):
    harga: int = Field(default=None)
    jangka_waktu: int = Field(default=None)
    suku_bunga_fixed: float = Field(default=None)
    masa_kredit_fix: int = Field(default=None)
    suku_bunga_floating: float = Field(default=None)
    class Config:
        schema_extra = {
            "property_input_demo": {
                "harga": 1000000000,
                "janga_waktu": 15,
                "suku_bunga_fixed": 5,
                "masa_kredit_fix": 5,
                "suku_bunga_floating": 10
            }
        }

class Properties_Bank(BaseModel):
    # bank: Bank_Properties = Field(default=None)
    bank: str = Field(default=None)
    harga: int = Field(default=None)
    jangka_waktu: int = Field(default=None)
    suku_bunga_floating: int = Field(default=None)
    class Config:
        schema_extra = {
            "property_fix_demo": {
                "bank": "BCA",
                "harga": 1000000000,
                "janga_waktu": 15,
                "suku_bunga_floating": 10
            }
        }