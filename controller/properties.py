from fastapi import APIRouter, Depends, status, Response, HTTPException
import requests
import json
from enum import Enum


class BankName(str, Enum):
    bca = "BCA"
    mandiri = "Mandiri"
    btn = "BTN"


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
    url = 'https://property-kpr.azurewebsites.net/property/all'
    return format_get(url)


def get_filtered(min_kamar_tidur: int, min_kamar_mandi: int, min_car_port: int, luas_tanah: int, luas_bangunan: int, minimal_harga: int, maksimal_harga: int):
    url = f'https://property-kpr.azurewebsites.net/property?min_kamar_tidur={min_kamar_tidur}&min_kamar_mandi={min_kamar_mandi}&min_car_port={min_car_port}&luas_tanah={luas_tanah}&luas_bangunan={luas_bangunan}&minimal_harga={minimal_harga}&maksimal_harga={maksimal_harga}'
    return format_get(url)


def get_id(id: int):
    url = f'https://property-kpr.azurewebsites.net/property/{id}'
    return format_get(url)


def prop_calc(id: int, jangka_waktu: int, suku_bunga_fixed: float, masa_kredit_fix: int, suku_bunga_floating: float):
    url = f'https://property-kpr.azurewebsites.net/kpr/property/{id}?jangka_waktu={jangka_waktu}&suku_bunga_fixed={suku_bunga_fixed}&masa_kredit_fix={masa_kredit_fix}&suku_bunga_floating={suku_bunga_floating}'
    return format_get(url)


def kpr_calc(harga: int, jangka_waktu: int, suku_bunga_fixed: float, masa_kredit_fix: int, suku_bunga_floating: float):
    url = f'https://property-kpr.azurewebsites.net/kpr?harga={harga}&jangka_waktu={jangka_waktu}&suku_bunga_fixed={suku_bunga_fixed}&masa_kredit_fix={masa_kredit_fix}&suku_bunga_floating={suku_bunga_floating}'
    return format_get(url)


def prop_bank_calc(id: int, bank: BankName, jangka_waktu: int, suku_bunga_floating: float):
    url = f'https://property-kpr.azurewebsites.net/kpr/property/{id}/bank/{bank}?jangka_waktu={jangka_waktu}&suku_bunga_floating={suku_bunga_floating}'
    return format_get(url)


def bank_calc(harga: int, bank: BankName, jangka_waktu: int, suku_bunga_floating: float):
    url = f'https://property-kpr.azurewebsites.net/kpr/bank/{bank}?harga={harga}&jangka_waktu={jangka_waktu}&suku_bunga_floating={suku_bunga_floating}'
    return format_get(url)


def kpr_properties(jangka_waktu: int, max_cicilan_awal: int, max_cicilan_akhir: int):
    url = f'https://property-kpr.azurewebsites.net/get-properties-kpr?jangka_waktu={jangka_waktu}&max_cicilan_awal={max_cicilan_awal}&max_cicilan_akhir={max_cicilan_akhir}'
    return format_get(url)

def get_estimated_propertiy_price(kota: str, kamar_tidur: int, kamar_mandi: int, car_port: int, luas_tanah: int, luas_bangunan: int):
    url = f'https://property-kpr.azurewebsites.net/predict?kota={kota}&kamar_tidur={kamar_tidur}&kamar_mandi={kamar_mandi}&car_port={car_port}&luas_tanah={luas_tanah}&luas_bangunan={luas_bangunan}'
    return format_get(url)