from fastapi import APIRouter, Depends, status, Response, HTTPException
import requests
import json
from controller.cars import *
from enum import Enum
from models.carInputModels import Transmisi

router = APIRouter(tags=["Cars"])

@router.get('/cars')
def get_all():
    return showall()


@router.get('/cars/search-nama/{nama_mobil}')
def get_cars_by_name(nama_mobil: str):
    return cars_nama(nama_mobil)

@router.get('/cars/search/tahun/{tahun}')
def get_cars_by_tahun(tahun: int):
    return cars_tahun(tahun)

@router.get('/cars/search-perusahaan/{nama_perusahaan}')
def get_cars_by_perusahaan(nama_perusahaan: str):
    return cars_perusahaan(nama_perusahaan)

# Need to fix enum
@router.get('/cars/search-trasmisi/{transmisi}')
def get_cars_by_transmisi(transmisi: Transmisi):
    return cars_transmisi(transmisi)

@router.get('/cars/search-harga')
def get_cars_by_harga(harga_min: int, harga_max: int):
    return cars_harga(harga_min, harga_max)

# Need to fix enum
@router.get('/cars/filter')
def get_filtered_cars(nama_mobil: str, odo_min: int, odo_max: int, tahun_min: int, tahun_max: int, harga_min: int, harga_max: int, transmisi: str):
    return cars_filter(nama_mobil, odo_min, odo_max, tahun_min, tahun_max, harga_min, harga_max, transmisi)

@router.get('/cicilan')
def hitung_cicilan_menggunakan_bunga_fix(harga_mobil: int, jangka_waktu: int, bunga_per_tahun: float, persentase_uang_muka: float):
    return cars_cicilan(harga_mobil, jangka_waktu, bunga_per_tahun, persentase_uang_muka)

# Need to fix enum
@router.get('/cicilan-by-bank')
def hitung_cicilan_menggunakan_kebijakan_kkb_bank(harga_mobil: int, persentase_uang_muka: float, bank: str):
    return cars_cicilan_bank(harga_mobil, persentase_uang_muka, bank)

# Need to fix enum
@router.get('/rekomendasi')
def rekomendasi_mobil_bekas(max_harga_mobil: int, max_cicilan_per_bulan: int, bank: str):
    return cars_recommendation(max_harga_mobil, max_cicilan_per_bulan, bank)

# Need to fix enum
@router.get('/predict_car')
def prediksi_harga_mobil(nama_mobil: str, tahun: int, odo: int, transmisi: str):
    return cars_predict(nama_mobil, tahun, odo, transmisi)