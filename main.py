from fastapi import FastAPI, APIRouter
from auth.email_auth import email_auth_router
from ambulance_status_records.ambulance_status_records import ambulance_status_records_router

app = FastAPI(title="Smart Ambulance System Api 👽💻")

router = APIRouter()


# Hello endpoint directly on app
@app.get("/hello")
async def hello_world_endpoint():
    return {"message": "Hello world"}


# Include email auth router into the router
router.include_router(email_auth_router)

# Include ambulance status records router
router.include_router(ambulance_status_records_router)

app.include_router(router)
