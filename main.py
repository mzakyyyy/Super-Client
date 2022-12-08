from fastapi import FastAPI
import uvicorn
from routers import properties, cars, calculation

app = FastAPI(title="Super Client",)

# models.Base.metadata.create_all(bind=engine)

app.include_router(properties.router)
app.include_router(cars.router)
app.include_router(calculation.router)

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8092, reload=True)
