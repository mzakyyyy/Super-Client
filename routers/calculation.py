from fastapi import APIRouter, Depends, status, Response, HTTPException
import requests
import json
from controller.properties import *
from controller.cars import *
from controller.calculation import *
from controller import properties
from enum import Enum
from models.propertiInputModels import Properties_Bank, Properties_Fix
from models.carInputModels import Car_Bank, Car_Fix
from auth import OAuth2
from schemas import schemas

router = APIRouter(
    tags=['Hitung pengeluaran per bulan']
)

@router.post('/car_fix_propery_fix')
def hitung_kredit_fix_kpr_fix(car: Car_Fix, property: Properties_Fix, get_current_user: schemas.User = Depends(OAuth2.get_current_user)):
    return car_fix_properti_fix(car, property)

@router.post('/car_fix_property_bank')
def hitung_kredit_fix_kpr_bank(car: Car_Fix, property: Properties_Bank, get_current_user: schemas.User = Depends(OAuth2.get_current_user)):
    return car_fix_properti_bank(car, property)

@router.post('/car_bank_property_fix')
def hitung_kredit_bank_kpr_fix(car: Car_Bank, property: Properties_Fix, get_current_user: schemas.User = Depends(OAuth2.get_current_user)):
    return car_bank_properti_fix(car, property)

@router.post('/car_bank_property_bank')
def hitung_kredit_bank_kpr_bank(car: Car_Bank, property: Properties_Bank, get_current_user: schemas.User = Depends(OAuth2.get_current_user)):
    return car_bank_properti_bank(car, property)