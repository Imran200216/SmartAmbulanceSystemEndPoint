from fastapi import APIRouter
from typing import List
from firebase_admin import firestore
from schemas.ambulance_status_records_model import AmbulanceStatusRecord

ambulance_status_records_router = APIRouter()

# Get Firestore client
db = firestore.client()


# ambulance status records end point
@ambulance_status_records_router.get(
    "/ambulance_status_records",
    response_model=List[AmbulanceStatusRecord]
)
async def fetch_ambulance_status_records():
    try:
        # Reference to collection
        collection_ref = db.collection('ambulance_status')

        # Fetch all documents
        docs = collection_ref.stream()

        ambulance_records = []
        for doc in docs:
            data = doc.to_dict()
            record = AmbulanceStatusRecord(
                employeeEmail=data.get("employeeEmail"),
                employeeId=data.get("employeeId"),
                hospitalAddress=data.get("hospitalAddress"),
                hospitalName=data.get("hospitalName"),
                isAmbulanceDriverSelectedHospital=data.get("isAmbulanceDriverSelectedHospital"),
                timestamp=data.get("timestamp")
            )
            ambulance_records.append(record)

        return ambulance_records

    except Exception as e:
        raise e
