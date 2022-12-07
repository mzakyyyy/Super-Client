from fastapi import FastAPI
from models import models
from config.database import engine, SessionLocal
import uvicorn

from routers import users, authentication

app = FastAPI(title="Super Client",)

models.Base.metadata.create_all(bind=engine)

app.include_router(users.router)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)














