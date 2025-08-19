from fastapi import FastAPI
from app.api.routers import shipment_router, seller_router,delivery_partner
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.include_router(shipment_router.router)
app.include_router(seller_router.router)
app.include_router(delivery_partner.router)
@app.get("/")
def welcome():
    return {
        "Hey" : "Welcome to the delivery app service"
    }
