from fastapi import APIRouter
from app.services.tourism_service import tourism_service

router = APIRouter(tags=["Tourism Data"])

@router.get("/tourist-places")
@router.get("/places")
@router.get("/travel/places")
async def get_tourist_places():
    destinations = tourism_service.get_dataset("destinations")
    heritage = tourism_service.get_dataset("heritage_sites")
    temples = tourism_service.get_dataset("temples")
    beaches = tourism_service.get_dataset("beaches")
    places = destinations + heritage + temples + beaches
    return {
        "success": True,
        "message": "Tourist places retrieved successfully.",
        "data": places
    }

@router.get("/provinces")
@router.get("/travel/provinces")
async def get_provinces():
    provinces = [
        {"id": 1, "name": "Siem Reap", "name_km": "សៀមរាប", "code": "SR", "description": "Home of Angkor Wat and ancient Khmer history."},
        {"id": 2, "name": "Phnom Penh", "name_km": "ភ្នំពេញ", "code": "PP", "description": "Capital city of Cambodia."},
        {"id": 3, "name": "Preah Sihanouk", "name_km": "ព្រះសីហនុ", "code": "SHV", "description": "Coastal province with beautiful islands."},
        {"id": 4, "name": "Kampot", "name_km": "កំពត", "code": "KP", "description": "Famous for black pepper, caves, and Bokor Mountain."},
        {"id": 5, "name": "Battambang", "name_km": "បាត់ដំបង", "code": "BB", "description": "Rich culture, colonial buildings, and bamboo train."},
        {"id": 6, "name": "Kep", "name_km": "កែប", "code": "KEP", "description": "Quiet seaside town famous for crab market."},
        {"id": 7, "name": "Mondulkiri", "name_km": "មណ្ឌលគិរី", "code": "MK", "description": "Highland nature, waterfalls, and elephant sanctuaries."},
        {"id": 8, "name": "Ratanakiri", "name_km": "រតនគិរី", "code": "RK", "description": "Volcanic lake Yeak Laom and lush jungles."},
        {"id": 9, "name": "Koh Kong", "name_km": "កោះកុង", "code": "KK", "description": "Mangrove forests and Cardamom mountains."}
    ]
    return {
        "success": True,
        "message": "Provinces retrieved successfully.",
        "data": provinces
    }

@router.get("/restaurants")
async def get_restaurants():
    return {
        "success": True,
        "message": "Restaurants retrieved successfully.",
        "data": tourism_service.get_dataset("restaurants")
    }

@router.get("/hotels")
async def get_hotels():
    items = tourism_service.search_keyword("hotel resort accommodation lodge", limit=10)
    return {
        "success": True,
        "message": "Hotels retrieved successfully.",
        "data": items
    }

@router.get("/events")
@router.get("/travel/events")
async def get_events():
    return {
        "success": True,
        "message": "Events retrieved successfully.",
        "data": tourism_service.get_dataset("festivals")
    }

@router.get("/categories")
@router.get("/travel/categories")
async def get_categories():
    categories = [
        {"id": "heritage", "name": "Heritage & Temples", "name_km": "បេតិកភណ្ឌ និងប្រាសាទ"},
        {"id": "beach", "name": "Beaches & Islands", "name_km": "ឆ្នេរ និងកោះ"},
        {"id": "nature", "name": "Nature & Waterfalls", "name_km": "ធម្មជាតិ និងទឹកធ្លាក់"},
        {"id": "food", "name": "Cambodian Food & Dining", "name_km": "ម្ហូប និងអាហារខ្មែរ"},
        {"id": "transport", "name": "Transportation & Travel", "name_km": "មធ្យោបាយធ្វើដំណើរ"},
        {"id": "culture", "name": "Culture & Festivals", "name_km": "វប្បធម៌ និងពិធីបុណ្យ"}
    ]
    return {
        "success": True,
        "message": "Categories retrieved successfully.",
        "data": categories
    }
