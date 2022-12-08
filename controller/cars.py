from fastapi import APIRouter, Depends, status, Response, HTTPException
import requests
import json
from enum import Enum

def get_bearer_token():
    url = 'https://property-kpr.azurewebsites.net/login'
    data = {"username": "zaky@mail.com", "password": "password"}
    response = requests.post(url, data=data)
    jsonresponse = response.json()
    bearertoken = str(jsonresponse['access_token'])
    return bearertoken


def format_get(url: str):
    link = url
    headers = {"Authorization": f'Bearer {get_bearer_token()}'}
    response = requests.get(link, headers=headers)
    jsonresponse = response.json()
    return jsonresponse

def showall():
    url = 'https://tst-price-prediction.azurewebsites.net/cars'
    return format_get(url)

def cars_nama(nama_mobil: str):
    url = f'https://tst-price-prediction.azurewebsites.net/cars/search-nama/{nama_mobil}'
    return format_get(url)

def cars_tahun(tahun: int):
    url = f'https://tst-price-prediction.azurewebsites.net/cars/search/tahun/{tahun}'
    return format_get(url)

def cars_perusahaan(nama_perusahaan: str):
    url = f'https://tst-price-prediction.azurewebsites.net/cars/search-perusahaan/{nama_perusahaan}'
    return format_get(url)

def cars_transmisi(transmisi: str):
    url = f'https://tst-price-prediction.azurewebsites.net/cars/search-transmisi/{transmisi}'
    return format_get(url)

def cars_harga(harga_min: int, harga_max: int):
    url = f'https://tst-price-prediction.azurewebsites.net/cars/search-harga?harga_min={harga_min}&harga_max={harga_max}'
    return format_get(url)

def cars_filter(nama_mobil: str, odo_min: int, odo_max: int, tahun_min: int, tahun_max: int, harga_min: int, harga_max: int, transmisi: str):
    url = f'https://tst-price-prediction.azurewebsites.net/cars/filter?nama_mobil={nama_mobil}&odo_min={odo_min}&odo_max={odo_max}&tahun_min={tahun_min}&tahun_max={tahun_max}&harga_min={harga_min}&harga_max={harga_max}&transmisi={transmisi}'
    return format_get(url)

def cars_cicilan(harga_mobil: int, jangka_waktu: int, bunga_per_tahun: float, persentase_uang_muka: float):
    url = f'https://tst-price-prediction.azurewebsites.net/cicilan?harga_mobil={harga_mobil}&jangka_waktu={jangka_waktu}&bunga_per_tahun={bunga_per_tahun}&persentase_uang_muka={persentase_uang_muka}'
    return format_get(url)

def cars_cicilan_bank(harga_mobil: int, persentase_uang_muka: float, bank: str):
    url = f'https://tst-price-prediction.azurewebsites.net/cicilan-by-bank?harga_mobil={harga_mobil}&persentase_uang_muka={persentase_uang_muka}&bank={bank}'
    return format_get(url)

def cars_recommendation(max_harga_mobil: int, max_cicilan_per_bulan: int, bank: str):
    url = f'https://tst-price-prediction.azurewebsites.net/rekomendasi?max_harga_mobil={max_harga_mobil}&max_cicilan_per_bulan={max_cicilan_per_bulan}&bank={bank}'
    return format_get(url)

def cars_predict(nama_mobil: str, tahun: int, odo: int, transmisi: str):
    url = f'https://tst-price-prediction.azurewebsites.net/predict_car?nama_mobil={nama_mobil}&tahun={tahun}&odo={odo}&transmisi={transmisi}'
    return format_get(url)