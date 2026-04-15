from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json, os, uuid
from datetime import datetime

app = Flask(__name__)
CORS(app)

DATA_FILE = "data/db.json"

def load_db():
    if not os.path.exists(DATA_FILE):
        return {"users": [], "reports": [], "alerts": [], "teams": [], "resources": []}
    with open(DATA_FILE) as f:
        return json.load(f)

def save_db(db):
    os.makedirs("data", exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(db, f, indent=2)

def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# ── Seed demo data ──────────────────────────────────────────────────────────
def seed():
    db = load_db()
    if not db["users"]:
        db["users"] = [
            {"id":"u1","name":"Ravi Sharma","email":"ravi@demo.com","password":"1234","role":"citizen","phone":"9876543210","registered":now()},
            {"id":"u2","name":"Admin","email":"admin@demo.com","password":"admin","role":"admin","phone":"9999999999","registered":now()},
        ]
        db["reports"] = [
            {"id":"r1","user_id":"u1","type":"Flood","location":"Haridwar Ghat","severity":"High","description":"Water level rising rapidly near the Ghat area.","status":"Active","timestamp":now()},
            {"id":"r2","user_id":"u1","type":"Earthquake","location":"Rishikesh","severity":"Medium","description":"Tremors felt for ~30 seconds.","status":"Resolved","timestamp":now()},
        ]
        db["alerts"] = [
            {"id":"a1","type":"Flood","message":"Red alert: Haridwar Ghat flooding — evacuate immediately.","severity":"Critical","issued_by":"Admin","timestamp":now()},
        ]
        db["teams"] = [
            {"id":"t1","name":"Alpha Rescue","leader":"Capt. Mehta","members":8,"specialization":"Flood Rescue","status":"Deployed","location":"Haridwar"},
            {"id":"t2","name":"Beta Medical","leader":"Dr. Priya","members":5,"specialization":"Medical Aid","status":"Standby","location":"Rishikesh"},
        ]
        db["resources"] = [
            {"id":"res1","name":"Inflatable Boats","category":"Equipment","quantity":12,"available":8,"location":"NDRF Depot, Haridwar"},
            {"id":"res2","name":"Medical Kits","category":"Medical","quantity":100,"available":75,"location":"Civil Hospital"},
            {"id":"res3","name":"Food Packets","category":"Relief","quantity":5000,"available":4200,"location":"Relief Camp 1"},
        ]
        save_db(db)

seed()

# ──────────────────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")

# USERS
@app.route("/api/register", methods=["POST"])
def register():
    db = load_db()
    d = request.json
    if any(u["email"] == d["email"] for u in db["users"]):
        return jsonify({"error": "Email already registered"}), 400
    user = {"id": str(uuid.uuid4())[:8], "name": d["name"], "email": d["email"],
            "password": d["password"], "role": "citizen",
            "phone": d.get("phone",""), "registered": now()}
    db["users"].append(user)
    save_db(db)
    return jsonify({"message": "Registered successfully", "user": {k:v for k,v in user.items() if k!="password"}})

@app.route("/api/login", methods=["POST"])
def login():
    db = load_db()
    d = request.json
    user = next((u for u in db["users"] if u["email"]==d["email"] and u["password"]==d["password"]), None)
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401
    return jsonify({"message": "Login successful", "user": {k:v for k,v in user.items() if k!="password"}})

@app.route("/api/users", methods=["GET"])
def get_users():
    db = load_db()
    return jsonify([{k:v for k,v in u.items() if k!="password"} for u in db["users"]])

# REPORTS
@app.route("/api/reports", methods=["GET","POST"])
def reports():
    db = load_db()
    if request.method == "POST":
        d = request.json
        r = {"id": str(uuid.uuid4())[:8], "user_id": d.get("user_id","anonymous"),
             "type": d["type"], "location": d["location"], "severity": d["severity"],
             "description": d["description"], "status": "Active", "timestamp": now()}
        db["reports"].append(r)
        save_db(db)
        return jsonify({"message": "Report submitted", "report": r})
    return jsonify(db["reports"])

@app.route("/api/reports/<rid>", methods=["PUT","DELETE"])
def report_detail(rid):
    db = load_db()
    r = next((x for x in db["reports"] if x["id"]==rid), None)
    if not r: return jsonify({"error":"Not found"}), 404
    if request.method == "PUT":
        r.update(request.json)
        save_db(db)
        return jsonify({"message":"Updated","report":r})
    db["reports"] = [x for x in db["reports"] if x["id"]!=rid]
    save_db(db)
    return jsonify({"message":"Deleted"})

# ALERTS
@app.route("/api/alerts", methods=["GET","POST"])
def alerts():
    db = load_db()
    if request.method == "POST":
        d = request.json
        a = {"id": str(uuid.uuid4())[:8], "type": d["type"], "message": d["message"],
             "severity": d["severity"], "issued_by": d.get("issued_by","Admin"), "timestamp": now()}
        db["alerts"].append(a)
        save_db(db)
        return jsonify({"message":"Alert issued","alert":a})
    return jsonify(db["alerts"])

@app.route("/api/alerts/<aid>", methods=["DELETE"])
def delete_alert(aid):
    db = load_db()
    db["alerts"] = [x for x in db["alerts"] if x["id"]!=aid]
    save_db(db)
    return jsonify({"message":"Alert removed"})

# TEAMS
@app.route("/api/teams", methods=["GET","POST"])
def teams():
    db = load_db()
    if request.method == "POST":
        d = request.json
        t = {"id": str(uuid.uuid4())[:8], **d, "timestamp": now()}
        db["teams"].append(t)
        save_db(db)
        return jsonify({"message":"Team added","team":t})
    return jsonify(db["teams"])

@app.route("/api/teams/<tid>", methods=["PUT","DELETE"])
def team_detail(tid):
    db = load_db()
    t = next((x for x in db["teams"] if x["id"]==tid), None)
    if not t: return jsonify({"error":"Not found"}), 404
    if request.method == "PUT":
        t.update(request.json)
        save_db(db)
        return jsonify({"message":"Updated","team":t})
    db["teams"] = [x for x in db["teams"] if x["id"]!=tid]
    save_db(db)
    return jsonify({"message":"Deleted"})

# RESOURCES
@app.route("/api/resources", methods=["GET","POST"])
def resources():
    db = load_db()
    if request.method == "POST":
        d = request.json
        r = {"id": str(uuid.uuid4())[:8], **d, "timestamp": now()}
        db["resources"].append(r)
        save_db(db)
        return jsonify({"message":"Resource added","resource":r})
    return jsonify(db["resources"])

@app.route("/api/resources/<rid>", methods=["PUT","DELETE"])
def resource_detail(rid):
    db = load_db()
    r = next((x for x in db["resources"] if x["id"]==rid), None)
    if not r: return jsonify({"error":"Not found"}), 404
    if request.method == "PUT":
        r.update(request.json)
        save_db(db)
        return jsonify({"message":"Updated","resource":r})
    db["resources"] = [x for x in db["resources"] if x["id"]!=rid]
    save_db(db)
    return jsonify({"message":"Deleted"})

# DASHBOARD STATS
@app.route("/api/stats", methods=["GET"])
def stats():
    db = load_db()
    return jsonify({
        "total_users": len(db["users"]),
        "active_reports": sum(1 for r in db["reports"] if r["status"]=="Active"),
        "total_reports": len(db["reports"]),
        "active_alerts": len(db["alerts"]),
        "teams_deployed": sum(1 for t in db["teams"] if t["status"]=="Deployed"),
        "total_teams": len(db["teams"]),
        "critical_resources": sum(1 for r in db["resources"] if r.get("available",0) < r.get("quantity",1)*0.2),
        "total_resources": len(db["resources"]),
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)
