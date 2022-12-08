from fastapi import APIRouter, Depends, status, Response, HTTPException
import requests
import json
from enum import Enum
from models.propertiInputModels import Properties_Bank, Properties_Fix
from models.carInputModels import Car_Bank, Car_Fix
from controller.cars import *
from controller.properties import *
from controller.auth import format_get

def car_fix_properti_fix(car: Car_Fix, property: Properties_Fix):
    a = cars_cicilan(car.harga_mobil, car.jangka_waktu, car.bunga_per_tahun, car.persentase_uang_muka)
    b = kpr_calc(property.harga, property.jangka_waktu, property.suku_bunga_fixed, property.masa_kredit_fix, property.suku_bunga_floating)
    print(a)
    tm = (a["Informasi Pinjaman Anda"]["Tenor"].split())[0]
    taw = (b["Angsuran Termin 1"]["Masa Kredit Termin 1"].split())[0]
    tak = (b["Informasi Pinjaman Anda"]["Tenor"].split())[0]
    cm = (a["Informasi Kredit Anda"]["Total angsuran per bulan"].split())[1]
    caw = ((b["Angsuran Termin 1"]["Cicilan per Bulan Termin 1"].split())[1]).replace('.', '')
    cak = ((b["Angsuran Termin 2"]["Cicilan per Bulan Termin 2"].split())[1]).replace('.', '')
    tahun_mobil = int(tm)
    tahun_awal_prop = int(taw)
    tahun_akhir_prop = int(tak)
    cicilan_mobil = int(cm)
    cicilan_awal_prop = int(caw)
    cicilan_akhir_prop = int(cak)
    
    if (tahun_mobil > tahun_awal_prop and tahun_mobil < tahun_akhir_prop):
        tahun_1 = tahun_awal_prop
        tahun_2 = tahun_mobil
        tahun_3 = tahun_akhir_prop
        cicilan_1 = cicilan_mobil + cicilan_awal_prop
        cicilan_2 = cicilan_mobil + cicilan_akhir_prop
        cicilan_3 = cicilan_akhir_prop
    elif (tahun_mobil == tahun_awal_prop and tahun_mobil < tahun_akhir_prop):
        tahun_sep = tahun_mobil
    elif (tahun_mobil < tahun_awal_prop and tahun_mobil < tahun_akhir_prop):
        tahun_1 = tahun_mobil
        tahun_2 = tahun_awal_prop
        tahun_3 = tahun_akhir_prop
        cicilan_1 = cicilan_mobil + cicilan_awal_prop
        cicilan_2 = cicilan_awal_prop
        cicilan_3 = cicilan_akhir_prop
    elif (tahun_mobil > tahun_awal_prop and tahun_mobil > tahun_akhir_prop):
        tahun_1 = tahun_awal_prop
        tahun_2 = tahun_akhir_prop
        tahun_3 = tahun_mobil
        cicilan_1 = cicilan_awal_prop + cicilan_mobil
        cicilan_2 = cicilan_akhir_prop + cicilan_mobil
        cicilan_3 = cicilan_mobil
    elif (tahun_mobil > tahun_awal_prop and tahun_mobil == tahun_akhir_prop):
        tahun_sep = tahun_awal_prop

    if (tahun_mobil == tahun_awal_prop or tahun_mobil == tahun_akhir_prop):
        return {
            "Informasi Harga": {
                "Mobil bekas Anda": f"Rp {car.harga_mobil}",
                "Properti Anda": f"Rp {property.harga}",
                "Lama cicilan mobil": f"{tahun_mobil} tahun",
                "Lama cicilan properti termin 1": f"{tahun_awal_prop} tahun",
                "Lama cicilan properti termin 2": f"{tahun_akhir_prop-tahun_awal_prop} tahun",
            },
            "Informasi cicilan per bulan":{
                "Cicilan mobil bekas": f"Rp {cicilan_mobil}",
                "Cicilan properti termin 1": f"Rp {cicilan_awal_prop}",
                "Cicilan properti termin 2": f"Rp {cicilan_akhir_prop}",
            },
            "Informasi total cicilan per bulan Anda":{
                f"Cicilan tahun pertama sampai tahun ke-{tahun_sep}": f"Rp {cicilan_mobil + cicilan_awal_prop}",
                f"Cicilan tahun ke-{tahun_sep+1} sampai tahun ke-{tahun_akhir_prop}": f"Rp {cicilan_akhir_prop}"
            }
        }
    else:
        return {
            "Informasi Harga": {
                "Mobil bekas Anda": f"Rp {car.harga_mobil}",
                "Properti Anda": f"Rp {property.harga}",
                "Lama cicilan mobil": f"{tahun_mobil} tahun",
                "Lama cicilan properti termin 1": f"{tahun_awal_prop} tahun",
                "Lama cicilan properti termin 2": f"{tahun_akhir_prop-tahun_awal_prop} tahun",
            },
            "Informasi cicilan per bulan":{
                "Cicilan mobil bekas": f"Rp {cicilan_mobil}",
                "Cicilan properti termin 1": f"Rp {cicilan_awal_prop}",
                "Cicilan properti termin 2": f"Rp {cicilan_akhir_prop}",
            },
            "Informasi total cicilan per bulan Anda":{
                f"Cicilan tahun pertama sampai tahun ke-{tahun_1}": f"Rp {cicilan_1}",
                f"Cicilan tahun ke-{tahun_1+1} sampai tahun ke-{tahun_2}": f"Rp {cicilan_2}",
                f"Cicilan tahun ke-{tahun_2+1} sampai tahun ke-{tahun_3}": f"Rp {cicilan_3}"
            }
        }
        
def car_fix_properti_bank(car: Car_Fix, property: Properties_Bank):
    a = cars_cicilan(car.harga_mobil, car.jangka_waktu, car.bunga_per_tahun, car.persentase_uang_muka)
    b = bank_calc(property.harga, property.bank, property.jangka_waktu, property.suku_bunga_floating)
    
    tm = (a["Informasi Pinjaman Anda"]["Tenor"].split())[0]
    taw = (b["Angsuran Termin 1"]["Masa Kredit Termin 1"].split())[0]
    tak = (b["Informasi Pinjaman Anda"]["Tenor"].split())[0]
    cm = (a["Informasi Kredit Anda"]["Total angsuran per bulan"].split())[1]
    caw = ((b["Angsuran Termin 1"]["Cicilan per Bulan Termin 1"].split())[1]).replace('.', '')
    cak = ((b["Angsuran Termin 2"]["Cicilan per Bulan Termin 2"].split())[1]).replace('.', '')
    
    tahun_mobil = int(tm)
    tahun_awal_prop = int(taw)
    tahun_akhir_prop = int(tak)
    cicilan_mobil = int(cm)
    cicilan_awal_prop = int(caw)
    cicilan_akhir_prop = int(cak)
    
    if (tahun_mobil > tahun_awal_prop and tahun_mobil < tahun_akhir_prop):
        tahun_1 = tahun_awal_prop
        tahun_2 = tahun_mobil
        tahun_3 = tahun_akhir_prop
        cicilan_1 = cicilan_mobil + cicilan_awal_prop
        cicilan_2 = cicilan_mobil + cicilan_akhir_prop
        cicilan_3 = cicilan_akhir_prop
    elif (tahun_mobil == tahun_awal_prop and tahun_mobil < tahun_akhir_prop):
        tahun_sep = tahun_mobil
    elif (tahun_mobil < tahun_awal_prop and tahun_mobil < tahun_akhir_prop):
        tahun_1 = tahun_mobil
        tahun_2 = tahun_awal_prop
        tahun_3 = tahun_akhir_prop
        cicilan_1 = cicilan_mobil + cicilan_awal_prop
        cicilan_2 = cicilan_awal_prop
        cicilan_3 = cicilan_akhir_prop
    elif (tahun_mobil > tahun_awal_prop and tahun_mobil > tahun_akhir_prop):
        tahun_1 = tahun_awal_prop
        tahun_2 = tahun_akhir_prop
        tahun_3 = tahun_mobil
        cicilan_1 = cicilan_awal_prop + cicilan_mobil
        cicilan_2 = cicilan_akhir_prop + cicilan_mobil
        cicilan_3 = cicilan_mobil
    elif (tahun_mobil > tahun_awal_prop and tahun_mobil == tahun_akhir_prop):
        tahun_sep = tahun_awal_prop

    if (tahun_mobil == tahun_awal_prop or tahun_mobil == tahun_akhir_prop):
        return {
            "Informasi Harga": {
                "Mobil bekas Anda": f"Rp {car.harga_mobil}",
                "Properti Anda": f"Rp {property.harga}",
                "Lama cicilan mobil": f"{tahun_mobil} tahun",
                "Lama cicilan properti termin 1": f"{tahun_awal_prop} tahun",
                "Lama cicilan properti termin 2": f"{tahun_akhir_prop-tahun_awal_prop} tahun",
            },
            "Informasi cicilan per bulan":{
                "Cicilan mobil bekas": f"Rp {cicilan_mobil}",
                "Cicilan properti termin 1": f"Rp {cicilan_awal_prop}",
                "Cicilan properti termin 2": f"Rp {cicilan_akhir_prop}",
            },
            "Informasi cicilan per bulan Anda":{
                f"Cicilan tahun pertama sampai tahun ke-{tahun_sep}": f"Rp {cicilan_mobil + cicilan_awal_prop}",
                f"Cicilan tahun ke-{tahun_sep+1} sampai tahun ke-{tahun_akhir_prop}": f"Rp {cicilan_akhir_prop}"
            }
        }
    else:
        return {
            "Informasi Harga": {
                "Mobil bekas Anda": f"Rp {car.harga_mobil}",
                "Properti Anda": f"Rp {property.harga}",
                "Lama cicilan mobil": f"{tahun_mobil} tahun",
                "Lama cicilan properti termin 1": f"{tahun_awal_prop} tahun",
                "Lama cicilan properti termin 2": f"{tahun_akhir_prop-tahun_awal_prop} tahun",
            },
            "Informasi cicilan per bulan":{
                "Cicilan mobil bekas": f"Rp {cicilan_mobil}",
                "Cicilan properti termin 1": f"Rp {cicilan_awal_prop}",
                "Cicilan properti termin 2": f"Rp {cicilan_akhir_prop}"
            },
            "Informasi total cicilan per bulan Anda":{
                f"Cicilan tahun pertama sampai tahun ke-{tahun_1}": f"Rp {cicilan_1}",
                f"Cicilan tahun ke-{tahun_1+1} sampai tahun ke-{tahun_2}": f"Rp {cicilan_2}",
                f"Cicilan tahun ke-{tahun_2+1} sampai tahun ke-{tahun_3}": f"Rp {cicilan_3}"
            }
        }
        
def car_bank_properti_fix(car: Car_Bank, property: Properties_Fix):
    a = cars_cicilan_bank(car.harga_mobil, car.persentase_uang_muka, car.bank)
    b = kpr_calc(property.harga, property.jangka_waktu, property.suku_bunga_fixed, property.masa_kredit_fix, property.suku_bunga_floating)
    print(a)
    tam = (a["Angsuran Termin 1"]["Lama termin 1"].split())[0]
    tzm = (a["Angsuran Termin 2"]["Lama termin 2"].split())[0]
    taw = (b["Angsuran Termin 1"]["Masa Kredit Termin 1"].split())[0]
    tak = (b["Informasi Pinjaman Anda"]["Tenor"].split())[0]
    
    cam = (a["Angsuran Termin 1"]["Angsuran per bulan termin 1"].split())[1]
    czm = (a["Angsuran Termin 2"]["Angsuran per bulan termin 2"].split())[1]
    caw = ((b["Angsuran Termin 1"]["Cicilan per Bulan Termin 1"].split())[1]).replace('.', '')
    cak = ((b["Angsuran Termin 2"]["Cicilan per Bulan Termin 2"].split())[1]).replace('.', '')
    
    tahun_awal_mobil = int(tam)
    tahun_akhir_mobil = int(tam) + int(tzm)
    tahun_awal_prop = int(taw)
    tahun_akhir_prop = int(tak)
    cicilan_awal_mobil = int(cam)
    cicilan_akhir_mobil = int(czm)
    cicilan_awal_prop = int(caw)
    cicilan_akhir_prop = int(cak)
    
    tahun_empat = False
    tahun_tiga = False
    tahun_dua = False
    
    # Empat
    if (tahun_awal_mobil < tahun_awal_prop and tahun_akhir_mobil < tahun_awal_prop):
        tahun_empat_1 = tahun_awal_mobil
        tahun_empat_2 = tahun_akhir_mobil
        tahun_empat_3 = tahun_awal_prop
        tahun_empat_4 = tahun_akhir_prop
        cicilan_1 = cicilan_awal_mobil + cicilan_awal_prop
        cicilan_2 = cicilan_akhir_mobil + cicilan_awal_prop
        cicilan_3 = cicilan_awal_prop
        cicilan_4 = cicilan_akhir_prop
        tahun_empat = True
    
    elif (tahun_awal_mobil < tahun_awal_prop and tahun_akhir_mobil > tahun_akhir_prop and tahun_akhir_mobil < tahun_akhir_prop):
        tahun_empat_1 = tahun_awal_mobil
        tahun_empat_2 = tahun_awal_prop
        tahun_empat_3 = tahun_akhir_mobil
        tahun_empat_4 = tahun_akhir_prop
        cicilan_1 = cicilan_awal_mobil + cicilan_awal_prop
        cicilan_2 = cicilan_akhir_mobil + cicilan_awal_prop
        cicilan_3 = cicilan_akhir_mobil + cicilan_akhir_prop
        cicilan_4 = cicilan_akhir_prop
        tahun_empat = True
        
    elif (tahun_awal_mobil < tahun_awal_prop and tahun_akhir_mobil > tahun_akhir_prop and tahun_akhir_mobil > tahun_akhir_prop):
        tahun_empat_1 = tahun_awal_mobil
        tahun_empat_2 = tahun_awal_prop
        tahun_empat_3 = tahun_akhir_prop
        tahun_empat_4 = tahun_akhir_mobil
        cicilan_1 = cicilan_awal_mobil + cicilan_awal_prop
        cicilan_2 = cicilan_awal_prop
        cicilan_3 = cicilan_akhir_mobil + cicilan_akhir_prop
        cicilan_4 = cicilan_akhir_mobil
        tahun_empat = True
        
    elif (tahun_awal_mobil > tahun_awal_prop and tahun_akhir_prop < tahun_awal_mobil):
        tahun_empat_1 = tahun_awal_prop
        tahun_empat_2 = tahun_akhir_prop
        tahun_empat_3 = tahun_awal_mobil
        tahun_empat_4 = tahun_akhir_mobil
        cicilan_1 = cicilan_awal_prop + cicilan_awal_mobil
        cicilan_2 = cicilan_akhir_prop + cicilan_awal_mobil
        cicilan_3 = cicilan_awal_mobil
        cicilan_4 = cicilan_akhir_mobil
        tahun_empat = True
        
    elif (tahun_awal_prop < tahun_awal_mobil and tahun_akhir_prop > tahun_akhir_mobil and tahun_akhir_prop < tahun_akhir_mobil):
        tahun_empat_1 = tahun_awal_prop
        tahun_empat_2 = tahun_awal_mobil
        tahun_empat_3 = tahun_akhir_prop
        tahun_empat_4 = tahun_akhir_mobil
        cicilan_1 = cicilan_awal_prop + cicilan_awal_mobil
        cicilan_2 = cicilan_akhir_prop + cicilan_awal_mobil
        cicilan_3 = cicilan_akhir_prop + cicilan_akhir_mobil
        cicilan_4 = cicilan_akhir_mobil
        tahun_empat = True
    
    elif (tahun_awal_prop < tahun_awal_mobil and tahun_akhir_prop > tahun_akhir_mobil and tahun_akhir_prop > tahun_akhir_mobil):
        tahun_empat_1 = tahun_awal_prop
        tahun_empat_2 = tahun_awal_mobil
        tahun_empat_3 = tahun_akhir_mobil
        tahun_empat_4 = tahun_akhir_prop
        cicilan_1 = cicilan_awal_prop + cicilan_awal_mobil
        cicilan_2 = cicilan_awal_mobil
        cicilan_3 = cicilan_akhir_prop + cicilan_akhir_mobil
        cicilan_4 = cicilan_akhir_prop
        tahun_empat = True
        
    # Tiga
    elif (tahun_awal_mobil == tahun_akhir_prop):
        tahun_tiga_1 = tahun_awal_prop
        tahun_tiga_2 = tahun_awal_mobil
        tahun_tiga_3 = tahun_akhir_mobil
        cicilan_1 = cicilan_awal_mobil + cicilan_awal_prop
        cicilan_2 = cicilan_awal_mobil + cicilan_akhir_prop
        cicilan_3 = cicilan_akhir_mobil
        cicilan_1 = cicilan_awal_mobil + cicilan_awal_prop
        cicilan_2 = cicilan_awal_mobil + cicilan_akhir_prop
        cicilan_3 = cicilan_akhir_mobil
        tahun_tiga = True
        
    elif (tahun_akhir_mobil == tahun_awal_prop):
        tahun_tiga_1 = tahun_awal_mobil
        tahun_tiga_2 = tahun_awal_prop
        tahun_tiga_3 = tahun_akhir_prop
        cicilan_1 = cicilan_awal_prop + cicilan_awal_mobil
        cicilan_2 = cicilan_awal_prop + cicilan_akhir_mobil
        cicilan_3 = cicilan_akhir_prop
        tahun_tiga = True
    
    # Dua
    elif (tahun_awal_mobil==tahun_awal_prop and tahun_akhir_mobil==tahun_akhir_prop):
        tahun_dua_1 = tahun_awal_prop
        tahun_dua_2 = tahun_akhir_prop
        cicilan_1 = cicilan_awal_mobil + cicilan_awal_prop
        cicilan_2 = cicilan_akhir_mobil + cicilan_akhir_prop
        tahun_dua = True
    
    if tahun_empat:
        return {
            "Informasi Harga": {
                "Mobil bekas Anda": f"Rp {car.harga_mobil}",
                "Properti Anda": f"Rp {property.harga}",
                "Lama cicilan mobil termin 1": f"{tahun_awal_mobil} tahun",
                "Lama cicilan mobil termin 2": f"{tahun_akhir_mobil} tahun",
                "Lama cicilan properti termin 1": f"{tahun_awal_prop} tahun",
                "Lama cicilan properti termin 2": f"{tahun_akhir_prop-tahun_awal_prop} tahun"
            },
            "Informasi cicilan":{
                "Cicilan mobil bekas termin 1": f"Rp {cicilan_awal_mobil}",
                "Cicilan mobil bekas termin 2": f"Rp {cicilan_akhir_mobil}",
                "Cicilan properti termin 1": f"Rp {cicilan_awal_prop}",
                "Cicilan properti termin 2": f"Rp {cicilan_akhir_prop}"
            },
            "Informasi total cicilan per bulan Anda":{
                f"Cicilan tahun pertama sampai tahun ke-{tahun_empat_1}": f"Rp {cicilan_1}",
                f"Cicilan tahun ke-{tahun_empat_1+1} sampai tahun ke-{tahun_empat_2}": f"Rp {cicilan_2}",
                f"Cicilan tahun ke-{tahun_empat_2+1} sampai tahun ke-{tahun_empat_3}": f"Rp {cicilan_3}",
                f"Cicilan tahun ke-{tahun_empat_3+1} sampai tahun ke-{tahun_empat_4}": f"Rp {cicilan_4}"
            }
        }
    
    if tahun_tiga:
        return {
            "Informasi Harga": {
                "Mobil bekas Anda": f"Rp {car.harga_mobil}",
                "Properti Anda": f"Rp {property.harga}",
                "Lama cicilan mobil termin 1": f"{tahun_awal_mobil} tahun",
                "Lama cicilan mobil termin 2": f"{tahun_akhir_mobil} tahun",
                "Lama cicilan properti termin 1": f"{tahun_awal_prop} tahun",
                "Lama cicilan properti termin 2": f"{tahun_akhir_prop-tahun_awal_prop} tahun"
            },
            "Informasi cicilan":{
                "Cicilan mobil bekas termin 1": f"Rp {cicilan_awal_mobil}",
                "Cicilan mobil bekas termin 2": f"Rp {cicilan_akhir_mobil}",
                "Cicilan properti termin 1": f"Rp {cicilan_awal_prop}",
                "Cicilan properti termin 2": f"Rp {cicilan_akhir_prop}"
            },
            "Informasi total cicilan per bulan Anda":{
                f"Cicilan tahun pertama sampai tahun ke-{tahun_tiga_1}": f"Rp {cicilan_1}",
                f"Cicilan tahun ke-{tahun_tiga_1+1} sampai tahun ke-{tahun_tiga_2}": f"Rp {cicilan_2}",
                f"Cicilan tahun ke-{tahun_tiga_2+1} sampai tahun ke-{tahun_tiga_3}": f"Rp {cicilan_3}"
            }
        }
        
    if tahun_dua:
        return {
            "Informasi Harga": {
                "Mobil bekas Anda": f"Rp {car.harga_mobil}",
                "Properti Anda": f"Rp {property.harga}",
                "Lama cicilan mobil termin 1": f"{tahun_awal_mobil} tahun",
                "Lama cicilan mobil termin 2": f"{tahun_akhir_mobil} tahun",
                "Lama cicilan properti termin 1": f"{tahun_awal_prop} tahun",
                "Lama cicilan properti termin 2": f"{tahun_akhir_prop-tahun_awal_prop} tahun",
            },
            "Informasi cicilan":{
                "Cicilan mobil bekas termin 1": f"Rp {cicilan_awal_mobil}",
                "Cicilan mobil bekas termin 2": f"Rp {cicilan_akhir_mobil}",
                "Cicilan properti termin 1": f"Rp {cicilan_awal_prop}",
                "Cicilan properti termin 2": f"Rp {cicilan_akhir_prop}"
            },
            "Informasi total cicilan per bulan Anda":{
                f"Cicilan tahun pertama sampai tahun ke-{tahun_dua_1}": f"Rp {cicilan_1}",
                f"Cicilan tahun ke-{tahun_dua_1+1} sampai tahun ke-{tahun_dua_2}": f"Rp {cicilan_2}"
            }
        }
        
def car_bank_properti_bank(car: Car_Bank, property: Properties_Bank):
    a = cars_cicilan_bank(car.harga_mobil, car.persentase_uang_muka, car.bank)
    b = bank_calc(property.harga, property.bank, property.jangka_waktu, property.suku_bunga_floating)
    
    tam = (a["Angsuran Termin 1"]["Lama termin 1"].split())[0]
    tzm = (a["Angsuran Termin 2"]["Lama termin 2"].split())[0]
    taw = (b["Angsuran Termin 1"]["Masa Kredit Termin 1"].split())[0]
    tak = (b["Informasi Pinjaman Anda"]["Tenor"].split())[0]
    
    cam = (a["Angsuran Termin 1"]["Angsuran per bulan termin 1"].split())[1]
    czm = (a["Angsuran Termin 2"]["Angsuran per bulan termin 2"].split())[1]
    caw = ((b["Angsuran Termin 1"]["Cicilan per Bulan Termin 1"].split())[1]).replace('.', '')
    cak = ((b["Angsuran Termin 2"]["Cicilan per Bulan Termin 2"].split())[1]).replace('.', '')
    
    tahun_awal_mobil = int(tam)
    tahun_akhir_mobil = int(tam) + int(tzm)
    tahun_awal_prop = int(taw)
    tahun_akhir_prop = int(tak)
    cicilan_awal_mobil = int(cam)
    cicilan_akhir_mobil = int(czm)
    cicilan_awal_prop = int(caw)
    cicilan_akhir_prop = int(cak)
    
    tahun_empat = False
    tahun_tiga = False
    tahun_dua = False
    
    # Empat
    if (tahun_awal_mobil < tahun_awal_prop and tahun_akhir_mobil < tahun_awal_prop):
        tahun_empat_1 = tahun_awal_mobil
        tahun_empat_2 = tahun_akhir_mobil
        tahun_empat_3 = tahun_awal_prop
        tahun_empat_4 = tahun_akhir_prop
        cicilan_1 = cicilan_awal_mobil + cicilan_awal_prop
        cicilan_2 = cicilan_akhir_mobil + cicilan_awal_prop
        cicilan_3 = cicilan_awal_prop
        cicilan_4 = cicilan_akhir_prop
        tahun_empat = True
    
    elif (tahun_awal_mobil < tahun_awal_prop and tahun_akhir_mobil > tahun_akhir_prop and tahun_akhir_mobil < tahun_akhir_prop):
        tahun_empat_1 = tahun_awal_mobil
        tahun_empat_2 = tahun_awal_prop
        tahun_empat_3 = tahun_akhir_mobil
        tahun_empat_4 = tahun_akhir_prop
        cicilan_1 = cicilan_awal_mobil + cicilan_awal_prop
        cicilan_2 = cicilan_akhir_mobil + cicilan_awal_prop
        cicilan_3 = cicilan_akhir_mobil + cicilan_akhir_prop
        cicilan_4 = cicilan_akhir_prop
        tahun_empat = True
        
    elif (tahun_awal_mobil < tahun_awal_prop and tahun_akhir_mobil > tahun_akhir_prop and tahun_akhir_mobil > tahun_akhir_prop):
        tahun_empat_1 = tahun_awal_mobil
        tahun_empat_2 = tahun_awal_prop
        tahun_empat_3 = tahun_akhir_prop
        tahun_empat_4 = tahun_akhir_mobil
        cicilan_1 = cicilan_awal_mobil + cicilan_awal_prop
        cicilan_2 = cicilan_awal_prop
        cicilan_3 = cicilan_akhir_mobil + cicilan_akhir_prop
        cicilan_4 = cicilan_akhir_mobil
        tahun_empat = True
        
    elif (tahun_awal_mobil > tahun_awal_prop and tahun_akhir_prop < tahun_awal_mobil):
        tahun_empat_1 = tahun_awal_prop
        tahun_empat_2 = tahun_akhir_prop
        tahun_empat_3 = tahun_awal_mobil
        tahun_empat_4 = tahun_akhir_mobil
        cicilan_1 = cicilan_awal_prop + cicilan_awal_mobil
        cicilan_2 = cicilan_akhir_prop + cicilan_awal_mobil
        cicilan_3 = cicilan_awal_mobil
        cicilan_4 = cicilan_akhir_mobil
        tahun_empat = True
        
    elif (tahun_awal_prop < tahun_awal_mobil and tahun_akhir_prop > tahun_akhir_mobil and tahun_akhir_prop < tahun_akhir_mobil):
        tahun_empat_1 = tahun_awal_prop
        tahun_empat_2 = tahun_awal_mobil
        tahun_empat_3 = tahun_akhir_prop
        tahun_empat_4 = tahun_akhir_mobil
        cicilan_1 = cicilan_awal_prop + cicilan_awal_mobil
        cicilan_2 = cicilan_akhir_prop + cicilan_awal_mobil
        cicilan_3 = cicilan_akhir_prop + cicilan_akhir_mobil
        cicilan_4 = cicilan_akhir_mobil
        tahun_empat = True
    
    elif (tahun_awal_prop < tahun_awal_mobil and tahun_akhir_prop > tahun_akhir_mobil and tahun_akhir_prop > tahun_akhir_mobil):
        tahun_empat_1 = tahun_awal_prop
        tahun_empat_2 = tahun_awal_mobil
        tahun_empat_3 = tahun_akhir_mobil
        tahun_empat_4 = tahun_akhir_prop
        cicilan_1 = cicilan_awal_prop + cicilan_awal_mobil
        cicilan_2 = cicilan_awal_mobil
        cicilan_3 = cicilan_akhir_prop + cicilan_akhir_mobil
        cicilan_4 = cicilan_akhir_prop
        tahun_empat = True
        
    # Tiga
    elif (tahun_awal_mobil == tahun_akhir_prop):
        tahun_tiga_1 = tahun_awal_prop
        tahun_tiga_2 = tahun_awal_mobil
        tahun_tiga_3 = tahun_akhir_mobil
        cicilan_1 = cicilan_awal_mobil + cicilan_awal_prop
        cicilan_2 = cicilan_awal_mobil + cicilan_akhir_prop
        cicilan_3 = cicilan_akhir_mobil
        cicilan_1 = cicilan_awal_mobil + cicilan_awal_prop
        cicilan_2 = cicilan_awal_mobil + cicilan_akhir_prop
        cicilan_3 = cicilan_akhir_mobil
        tahun_tiga = True
        
    elif (tahun_akhir_mobil == tahun_awal_prop):
        tahun_tiga_1 = tahun_awal_mobil
        tahun_tiga_2 = tahun_awal_prop
        tahun_tiga_3 = tahun_akhir_prop
        cicilan_1 = cicilan_awal_prop + cicilan_awal_mobil
        cicilan_2 = cicilan_awal_prop + cicilan_akhir_mobil
        cicilan_3 = cicilan_akhir_prop
        tahun_tiga = True
    
    # Dua
    elif (tahun_awal_mobil==tahun_awal_prop and tahun_akhir_mobil==tahun_akhir_prop):
        tahun_dua_1 = tahun_awal_prop
        tahun_dua_2 = tahun_akhir_prop
        cicilan_1 = cicilan_awal_mobil + cicilan_awal_prop
        cicilan_2 = cicilan_akhir_mobil + cicilan_akhir_prop
        tahun_dua = True
    
    if tahun_empat:
        return {
            "Informasi Harga": {
                "Mobil bekas Anda": f"Rp {car.harga_mobil}",
                "Properti Anda": f"Rp {property.harga}",
                "Lama cicilan mobil termin 1": f"{tahun_awal_mobil} tahun",
                "Lama cicilan mobil termin 2": f"{tahun_akhir_mobil} tahun",
                "Lama cicilan properti termin 1": f"{tahun_awal_prop} tahun",
                "Lama cicilan properti termin 2": f"{tahun_akhir_prop-tahun_awal_prop} tahun"
            },
            "Informasi cicilan per bulan":{
                "Cicilan mobil bekas termin 1": f"Rp {cicilan_awal_mobil}",
                "Cicilan mobil bekas termin 2": f"Rp {cicilan_akhir_mobil}",
                "Cicilan properti termin 1": f"Rp {cicilan_awal_prop}",
                "Cicilan properti termin 2": f"Rp {cicilan_akhir_prop}"
            },
            "Informasi total cicilan per bulan Anda":{
                f"Cicilan tahun pertama sampai tahun ke-{tahun_empat_1}": f"Rp {cicilan_1}",
                f"Cicilan tahun ke-{tahun_empat_1+1} sampai tahun ke-{tahun_empat_2}": f"Rp {cicilan_2}",
                f"Cicilan tahun ke-{tahun_empat_2+1} sampai tahun ke-{tahun_empat_3}": f"Rp {cicilan_3}",
                f"Cicilan tahun ke-{tahun_empat_3+1} sampai tahun ke-{tahun_empat_4}": f"Rp {cicilan_4}"
            }
        }
    
    if tahun_tiga:
        return {
            "Informasi Harga": {
                "Mobil bekas Anda": f"Rp {car.harga_mobil}",
                "Properti Anda": f"Rp {property.harga}",
                "Lama cicilan mobil termin 1": f"{tahun_awal_mobil} tahun",
                "Lama cicilan mobil termin 2": f"{tahun_akhir_mobil} tahun",
                "Lama cicilan properti termin 1": f"{tahun_awal_prop} tahun",
                "Lama cicilan properti termin 2": f"{tahun_akhir_prop-tahun_awal_prop} tahun"
            },
            "Informasi cicilan per bulan":{
                "Cicilan mobil bekas termin 1": f"Rp {cicilan_awal_mobil}",
                "Cicilan mobil bekas termin 2": f"Rp {cicilan_akhir_mobil}",
                "Cicilan properti termin 1": f"Rp {cicilan_awal_prop}",
                "Cicilan properti termin 2": f"Rp {cicilan_akhir_prop}"
            },
            "Informasi total cicilan per bulan Anda":{
                f"Cicilan tahun pertama sampai tahun ke-{tahun_tiga_1}": f"Rp {cicilan_1}",
                f"Cicilan tahun ke-{tahun_tiga_1+1} sampai tahun ke-{tahun_tiga_2}": f"Rp {cicilan_2}",
                f"Cicilan tahun ke-{tahun_tiga_2+1} sampai tahun ke-{tahun_tiga_3}": f"Rp {cicilan_3}"
            }
        }
        
    if tahun_dua:
        return {
            "Informasi Harga": {
                "Mobil bekas Anda": f"Rp {car.harga_mobil}",
                "Properti Anda": f"Rp {property.harga}",
                "Lama cicilan mobil termin 1": f"{tahun_awal_mobil} tahun",
                "Lama cicilan mobil termin 2": f"{tahun_akhir_mobil} tahun",
                "Lama cicilan properti termin 1": f"{tahun_awal_prop} tahun",
                "Lama cicilan properti termin 2": f"{tahun_akhir_prop-tahun_awal_prop} tahun"
            },
            "Informasi cicilan per bulan":{
                "Cicilan mobil bekas termin 1": f"Rp {cicilan_awal_mobil}",
                "Cicilan mobil bekas termin 2": f"Rp {cicilan_akhir_mobil}",
                "Cicilan properti termin 1": f"Rp {cicilan_awal_prop}",
                "Cicilan properti termin 2": f"Rp {cicilan_akhir_prop}"
            },
            "Informasi total cicilan per bulan Anda":{
                f"Cicilan tahun pertama sampai tahun ke-{tahun_dua_1}": f"Rp {cicilan_1}",
                f"Cicilan tahun ke-{tahun_dua_1+1} sampai tahun ke-{tahun_dua_2}": f"Rp {cicilan_2}"
            }
        }