from fastapi import FastAPI
from pymongo import MongoClient
from dotenv import dotenv_values
from routes import routes

config = dotenv_values(".env")

app = FastAPI()


@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(config["MONGODB_URL_KEY"])
    app.database = app.mongodb_client[config["DATABASE_NAME"]]


@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()


app.include_router(routes.router)
