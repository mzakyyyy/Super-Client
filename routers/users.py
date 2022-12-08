# from fastapi import APIRouter, Depends, status, Response, HTTPException
# from schemas import schemas
# from config import database
# from sqlalchemy.orm import Session
# from controller import users
# import requests
# import json
# from auth import OAuth2

# router = APIRouter(
#     tags=["User"]
# )

# get_db = database.get_db


# @router.post('/user')
# def create_user(request: schemas.User, db: Session = Depends(get_db)):

#     return users.create(request, db)

# @router.get('/user')
# def show_user(db: Session = Depends(get_db)):
#     return users.retrieve_user(db)

# def get_bearer_token():
#     url = 'https://property-kpr.azurewebsites.net/login'
#     data = {"username": email, "password": password}
#     response = requests.post(url, data=data)
#     jsonresponse = response.json()
#     bearertoken = str(jsonresponse['access_token'])

# @router.get('/prop')
# def get_all(get_current_user: schemas.User = Depends(OAuth2.get_current_user)):
#     url = 'https://property-kpr.azurewebsites.net/property/all'
#     response = requests.get(url)
#     jsonresponse = response.json()
#     return jsonresponse

# @router.get('/alluser')
# def get_all_user():
#     url = 'https://property-kpr.azurewebsites.net/user'
#     response = requests.get(url)
#     jsonresponse = response.json()
#     listuser = [d['email'] for d in jsonresponse]
#     return listuser

# @router.get('/predict')
# def get_prediction(kota: str, kamar_tidur: int, kamar_mandi: int, car_port: int, luas_tanah: int, luas_bangunan: int):
#     url = f'https://property-kpr.azurewebsites.net/predict?kota={kota}&kamar_tidur={kamar_tidur}&kamar_mandi={kamar_mandi}&car_port={car_port}&luas_tanah={luas_tanah}&luas_bangunan={luas_bangunan}'
#     token = get_from_test()
#     headers = {"Authorization":f'Bearer {token}'}
#     response = requests.get(url, headers=headers)
#     jsonresponse = response.json()
#     return jsonresponse

# @router.get('/currentuser')
# def get_cur_user():
#     return get_from_test()