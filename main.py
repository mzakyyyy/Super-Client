from fastapi import FastAPI
import uvicorn
from routers import authentication,users,properties, cars, calculation
from models import models
from config.database import engine, SessionLocal

description = """
Super API ini merupakan gabungan layanan **API mobil bekas** dan **API properti**. Fungsi-fungsi yang terdapat di dalam API mobil bekas dan API properti juga dapat dilakukan di Super API ini. Sebelum dapat melakukan request pada endpoints API ini, pastikan Anda telah terautorisasi dengan cara **Registrasion** dan **Login** atau melalui tombol **Authorize** pada API ini. Setelah terauthorize, Anda dapat melakukan request pada beberapa endpoints yang terdapat pada API ini, yaitu:

## Users
Anda dapat:
1. Melakukan registrasi
2. Melakukan login
3. Menghapus akun

## Properti
Anda dapat:
1. Mendapatkan seluruh data properti
2. Mendapatkan seluruh data properti berdasarkan **filter yang ditentukan**
3. Mendapatkan data properti berdasarkan ID
4. Menghitung kredit KPR berdasarkan **persentase bunga fix, janga waktu, masa kredit bunga fix,** dan **persentase bunga floating** yang Anda input
5. Menghitung kredit KPR berdasarkan **bank** yang Anda pilih
6. Melihat rekomendasi properti pada _database_ kami berdasarkan **jangka waktu, harga maksimal,** dan **cicilan maksimal** yang Anda inginkan
7. Melakukan prediksi harga properti yang diestimasi berdasarkan **nama kota, jumlah kamar tidur, jumlah kamar mandi, jumlah car port, luas tanah,** dan **luas bangunan**

## Cars
Anda dapat:
1. Mendapatkan seluruh data mobil
2. Mendapatkan seluruh data mobil berdasarkan **nama**
3. Mendapatkan seluruh data mobil berdasarkan **tahun**
4. Mendapatkan seluruh data mobil berdasarkan **nama perusahaan**
5. Mendapatkan seluruh data mobil berdasarkan **jenis transmisi**
6. Mendapatkan seluruh data mobil berdasarkan **rentang harganya**
7. Mendapatkan seluruh data mobil berdasarkan **filter yang ditentukan**
8. Melakukan perhitungan kredit mobil berdasarkan **bunga fix**, **jangka waktu**, dan **persentase pembayaran uang muka** yang Anda masukkan
9. Melakukan perhitungan kredit mobil berdasarkan **bank yang Anda pilih** serta **persentase pembayaran uang muka**
10. Melihat rekomendasi mobil bekas pada _database_ kami berdasarkan **bank pilihan, harga,** dan **cicilan maksimal** yang Anda inginkan
11. Melakukan prediksi harga mobil bekas yang diestimasi berdasarkan **nama mobil, tahun, odo,** dan **jenis transmisinya**

## Menghitung total pengeluaran per bulan dari kredit KPR dan kredit KKB
Anda dapat:
1. Menghitung total cicilan kredit KPR dengan jangka waktu dan bunga yang ditentukan sendiri serta kredit KKB dengan jangka waktu dan bunga yang ditentukan sendiri
2. Menghitung total cicilan kredit KPR dengan jangka waktu dan bunga yang ditentukan sendiri serta kredit KKB dengan jangka waktu dan bunga sesuai dengan kebijakan bank
3. Menghitung total cicilan kredit KPR dengan jangka waktu dan bunga sesuai dengan kebijakan bank serta kredit KKB dengan jangka waktu dan bunga yang ditentukan sendiri
4. Menghitung total cicilan kredit KPR dengan jangka waktu dan bunga sesuai dengan kebijakan bank serta kredit KKB dengan jangka waktu dan bunga sesuai dengan kebijakan bank

"""

app = FastAPI(
    title="Super API",
    description=description
)

models.Base.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(authentication.router)
app.include_router(properties.router)
app.include_router(cars.router)
app.include_router(calculation.router)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8092, reload=True)
