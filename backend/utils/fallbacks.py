FALLBACKS = {
    "search": {
        "error": True,
        "message": "Could not search your transactions right now. Try a more specific merchant name.",
        "data": []
    },
    "analytics": {
        "error": True,
        "message": "Could not calculate your spending summary. Please try again.",
        "data": {}
    },
    "anomaly": {
        "error": True,
        "message": "Could not scan for anomalies right now.",
        "data": []
    },
    "categorization": {
        "error": True,
        "message": "Could not categorize transactions right now.",
        "data": []
    },
    "projection": {
        "error": True,
        "message": "Could not calculate projection. Please check your goal and try again.",
        "data": {}
    }
}

def get_fallback(specialist: str) -> dict:
    return FALLBACKS.get(specialist, {"error": True, "message": "Something went wrong.", "data": None})