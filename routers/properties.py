from fastapi import APIRouter, Depends, status, Response, HTTPException
import requests
import json
from controller.properties import *
from controller import properties
from enum import Enum

router = APIRouter(tags=["Properties"])


@router.get('/property/all')
def get_all():
    return showall()


@router.get('/property')
def get_filtered_properties(min_kamar_tidur: int, min_kamar_mandi: int, min_car_port: int, luas_tanah: int, luas_bangunan: int, minimal_harga: int, maksimal_harga: int):
    return get_filtered(min_kamar_tidur, min_kamar_mandi, min_car_port, luas_tanah, luas_bangunan, minimal_harga, maksimal_harga)


@router.get('/property/{id}')
def get_by_id(id: int):
    return get_id(id)


@router.get('/kpr/property/{id}')
def kpr_property_calculator(id: int, jangka_waktu: int, suku_bunga_fixed: float, masa_kredit_fix: int, suku_bunga_floating: float):
    return prop_calc(id, jangka_waktu, suku_bunga_fixed, masa_kredit_fix, suku_bunga_floating)


@router.get('/kpr')
def kpr_calculator(harga: int, jangka_waktu: int, suku_bunga_fixed: float, masa_kredit_fix: int, suku_bunga_floating: float):
    return kpr_calc(harga, jangka_waktu, suku_bunga_fixed, masa_kredit_fix, suku_bunga_floating)



# Need to fix for Enum
@router.get('/kpr/property/{id}/bank/{bank}')
def kpr_property_bank_calculator(id: int, bank: str, jangka_waktu: int, suku_bunga_floating: float):
    return prop_bank_calc(id, bank, jangka_waktu, suku_bunga_floating)


# Need to fix for Enum
@router.get('/kpr/property/bank/{bank}')
def kpr_bank_calculator(harga: int, bank: str, jangka_waktu: int, suku_bunga_floating: float):
    return bank_calc(harga, bank, jangka_waktu, suku_bunga_floating)


@router.get('/get-properties-kpr')
def get_properties_by_kpr(jangka_waktu: int, max_cicilan_awal: int, max_cicilan_akhir: int):
    return kpr_properties(jangka_waktu, max_cicilan_awal, max_cicilan_akhir)

@router.get('/predict')
def get_prediction(kota: str, kamar_tidur: int, kamar_mandi: int, car_port: int, luas_tanah: int, luas_bangunan: int):
    return get_estimated_propertiy_price(kota, kamar_tidur, kamar_mandi, car_port, luas_tanah, luas_bangunan)