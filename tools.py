
import json, random, os

DATA_PATH = os.path.join(os.path.dirname(__file__), "mock_data.json")
with open(DATA_PATH, "r") as f:
    DATA = json.load(f)

def get_merchant_status(merchant_id=None):
    if merchant_id:
        merchant = next((m for m in DATA["merchants"] if m["id"] == merchant_id), None)
    else:
        merchant = random.choice(DATA["merchants"])
    if merchant:
        return {"ok": True, "merchant_id": merchant["id"], "name": merchant["name"], "prep_time_min": merchant["prep_time_min"], "status": merchant["status"]}
    return {"ok": False, "error": "Merchant not found"}

def get_nearby_merchants(cuisine, max_wait_min):
    matches = [m for m in DATA["merchants"] if m["cuisine"].lower() == cuisine.lower() and m["prep_time_min"] <= max_wait_min]
    return {"ok": True, "alternatives": matches}

def re_route_driver(driver_id=None, interim_job=None):
    if driver_id:
        driver = next((d for d in DATA["drivers"] if d["id"] == driver_id), None)
    else:
        driver = random.choice(DATA["drivers"])
    if driver:
        driver["current_status"] = "On Interim Job" if interim_job else "Idle"
        return {"ok": True, "driver_id": driver["id"], "assigned_job": interim_job}
    return {"ok": False, "error": "Driver not found"}

def notify_customer(order_id, message, voucher=False):
    return {"ok": True, "order_id": order_id, "message": message, "voucher_issued": voucher}

def check_traffic(route=None):
    if route:
        t = next((r for r in DATA["traffic"] if r["route"] == route), None)
    else:
        t = random.choice(DATA["traffic"])
    if t:
        return {"ok": True, "route": t["route"], "status": t["status"], "delay_min": t["delay_min"]}
    return {"ok": False, "error": "Route not found"}

def calculate_alternative_route(origin, destination):
    normal_route = f"{origin}-{destination}"
    for t in DATA["traffic"]:
        if t["route"] != normal_route and t["status"] == "Normal":
            return {"ok": True, "new_route": t["route"], "eta_min": 30}
    return {"ok": False, "error": "No alternative found"}

def find_nearby_locker(location=None):
    available = [l for l in DATA["lockers"] if l["available_slots"] > 0]
    if available:
        return {"ok": True, "lockers": [random.choice(available)]}
    return {"ok": False, "error": "No available lockers"}

def initiate_mediation_flow(order_id):
    return {"ok": True, "order_id": order_id, "mediation_started": True}

def collect_evidence(order_id):
    return {"ok": True, "order_id": order_id, "photos": ["photo1.jpg", "photo2.jpg"]}

def analyze_evidence(payload):
    return {"ok": True, "result": random.choice(["Merchant fault", "No fault"])}

def issue_instant_refund(order_id, amount):
    return {"ok": True, "order_id": order_id, "refunded_amount": amount}

def exonerate_driver(driver_id=None):
    if driver_id:
        driver = next((d for d in DATA["drivers"] if d["id"] == driver_id), None)
    else:
        driver = random.choice(DATA["drivers"])
    if driver:
        return {"ok": True, "driver_id": driver["id"], "status": "Cleared"}
    return {"ok": False, "error": "Driver not found"}

def log_merchant_packaging_feedback(merchant_id, report):
    return {"ok": True, "merchant_id": merchant_id, "feedback": report}

def contact_recipient_via_chat(job_id, message):
    return {"ok": True, "job_id": job_id, "response": random.choice(["No answer", "Confirmed"])}
