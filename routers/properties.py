from fastapi import APIRouter, Depends, status, Response, HTTPException
import requests
import json
from controller.properties import *

router = APIRouter()

@router.get('/property/all', tags=["Properties"])
def get_all():
    return showall()

@router.get('/property', tags=["Properties"])
def get_filtered_properties(min_kamar_tidur: int, min_kamar_mandi: int, min_car_port: int, luas_tanah: int, luas_bangunan: int, minimal_harga: int, maksimal_harga: int):
    return get_filtered(min_kamar_tidur, min_kamar_mandi, min_car_port, luas_tanah, luas_bangunan, minimal_harga, maksimal_harga)

@router.get('/property/{id}', tags=["Properties"])
def get_by_id(id: int):
    return get_id(id)

@router.get('/kpr/property/{id}', tags=["KPR Calculator"])
def kpr_property_calculator(id: int, jangka_waktu: int, suku_bunga_fixed: float, masa_kredit_fix: int, suku_bunga_floating: float):
    return prop_calc(id, jangka_waktu, suku_bunga_fixed, masa_kredit_fix, suku_bunga_floating)

@router.get('/kpr', tags=["KPR Calculator"])
def kpr_calculator(harga: int, jangka_waktu: int, suku_bunga_fixed: float, masa_kredit_fix: int, suku_bunga_floating: float):
    return kpr_calc(harga, jangka_waktu, suku_bunga_fixed, masa_kredit_fix, suku_bunga_floating)