from fastapi import APIRouter
from app.services.tourism_service import tourism_service

router = APIRouter(tags=["Tourism Data"])

@router.get("/tourist-places")
async def get_tourist_places():
    destinations = tourism_service.get_dataset("destinations")
    heritage = tourism_service.get_dataset("heritage_sites")
    temples = tourism_service.get_dataset("temples")
    beaches = tourism_service.get_dataset("beaches")
    return {"success": True, "data": destinations + heritage + temples + beaches}

@router.get("/restaurants")
async def get_restaurants():
    return {"success": True, "data": tourism_service.get_dataset("restaurants")}

@router.get("/hotels")
async def get_hotels():
    # Return accommodation data from provinces/destinations
    items = tourism_service.search_keyword("hotel resort accommodation lodge", limit=10)
    return {"success": True, "data": items}

@router.get("/events")
async def get_events():
    return {"success": True, "data": tourism_service.get_dataset("festivals")}

@router.get("/categories")
async def get_categories():
    categories = [
        {"id": "heritage", "name": "Heritage & Temples", "name_km": "បេតិកភណ្ឌ និងប្រាសាទ"},
        {"id": "beach", "name": "Beaches & Islands", "name_km": "ឆ្នេរ និងកោះ"},
        {"id": "nature", "name": "Nature & Waterfalls", "name_km": "ធម្មជាតិ និងទឹកធ្លាក់"},
        {"id": "food", "name": "Cambodian Food & Dining", "name_km": "ម្ហូប និងអាហារខ្មែរ"},
        {"id": "transport", "name": "Transportation & Travel", "name_km": "មធ្យោបាយធ្វើដំណើរ"},
        {"id": "culture", "name": "Culture & Festivals", "name_km": "វប្បធម៌ និងពិធីបុណ្យ"}
    ]
    return {"success": True, "data": categories}
