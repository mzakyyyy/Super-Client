from enum import Enum
from models.bankModels import Bank_Car
from pydantic import BaseModel, Field

class Transmisi(Enum):
    Manual = 'Manual'
    Automatic = 'Automatic'

class Car_Fix(BaseModel):
    harga_mobil: int = Field(default=None)
    jangka_waktu: int = Field(default=None)
    bunga_per_tahun: int = Field(default=None)
    persentase_uang_muka: int = Field(default=None)
    class Config:
        schema_extra = {
            "car_input_demo" : {
                "harga_mobil": 100000000,
                "jangka_waktu": 10,
                "bunga_per_tahun": 10,
                "persentase_uang_muka": 30
            }
        }
        
class Car_Bank(BaseModel):
    harga_mobil: int = Field(default=None)
    persentase_uang_muka: int = Field(default=None)
    bank: str = Field(default=None)
    # bank: Bank_Car = Field(default=None)
    class Config:
        schema_extra = {
            "car_bank_demo" : {
                "harga_mobil": 100000000,
                "persentase_uang_muka": 30,
                "bank": "BCA"
            }
        }