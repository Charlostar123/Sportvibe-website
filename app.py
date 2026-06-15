from flask import Flask, jsonify, request, render_template
from flask_pymongo import PyMongo
from bson import ObjectId
from datetime import datetime
import json

app = Flask(__name__)

# MongoDB config - change URI if using Atlas
app.config["MONGO_URI"] = "mongodb://localhost:27017/sportvibe"
mongo = PyMongo(app)


def serialize(doc):
    """Convert MongoDB document to JSON-serializable dict."""
    doc["_id"] = str(doc["_id"])
    return doc


# ── Seed data ────────────────────────────────────────────────────────────────

SEED_ACTIVITIES = [
    {
        "name": "Premier League Match",
        "category": "Sports",
        "description": "Manchester City vs Arsenal – top-of-table clash.",
        "location": "Etihad Stadium, Manchester",
        "date": "2026-06-01",
        "rating": 4.8,
        "image_emoji": "⚽",
        "tags": ["football", "premier league", "live"],
    },
    {
        "name": "Trail Running – Karura Forest",
        "category": "Recreation",
        "description": "5 km scenic trail through Nairobi's green lung.",
        "location": "Karura Forest, Nairobi",
        "date": "2026-05-25",
        "rating": 4.5,
        "image_emoji": "🏃",
        "tags": ["running", "nature", "fitness"],
    },
    {
        "name": "Nyama Choma Cook-Off",
        "category": "Food",
        "description": "Community BBQ competition – best roast wins a trophy!",
        "location": "Uhuru Park, Nairobi",
        "date": "2026-05-30",
        "rating": 4.9,
        "image_emoji": "🍖",
        "tags": ["food", "BBQ", "competition"],
    },
    {
        "name": "Basketball Street League",
        "category": "Sports",
        "description": "3-on-3 street basketball tournament open to all.",
        "location": "Ruiru Sports Ground",
        "date": "2026-06-07",
        "rating": 4.3,
        "image_emoji": "🏀",
        "tags": ["basketball", "street", "tournament"],
    },
    {
        "name": "Cycling – Thika Road Rally",
        "category": "Recreation",
        "description": "40 km road cycling event, all skill levels welcome.",
        "location": "Thika Superhighway, Kenya",
        "date": "2026-06-14",
        "rating": 4.6,
        "image_emoji": "🚴",
        "tags": ["cycling", "outdoor", "fitness"],
    },
    {
        "name": "Sushi & Sake Night",
        "category": "Food",
        "description": "Curated Japanese dining experience with live sushi bar.",
        "location": "The Alchemist, Westlands",
        "date": "2026-06-03",
        "rating": 4.7,
        "image_emoji": "🍣",
        "tags": ["food", "japanese", "dining"],
    },
]


@app.before_request
def seed_db():
    """Seed the DB once if empty."""
    if mongo.db.activities.count_documents({}) == 0:
        mongo.db.activities.insert_many(
            [{**a, "created_at": datetime.utcnow()} for a in SEED_ACTIVITIES]
        )


# ── Routes ────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


# GET all activities (optional ?category= or ?search= filter)
@app.route("/api/activities", methods=["GET"])
def get_activities():
    query = {}
    category = request.args.get("category")
    search = request.args.get("search")

    if category and category != "All":
        query["category"] = category
    if search:
        query["$or"] = [
            {"name": {"$regex": search, "$options": "i"}},
            {"description": {"$regex": search, "$options": "i"}},
            {"tags": {"$regex": search, "$options": "i"}},
        ]

    docs = list(mongo.db.activities.find(query).sort("rating", -1))
    return jsonify([serialize(d) for d in docs])


# GET single activity
@app.route("/api/activities/<id>", methods=["GET"])
def get_activity(id):
    doc = mongo.db.activities.find_one({"_id": ObjectId(id)})
    if not doc:
        return jsonify({"error": "Not found"}), 404
    return jsonify(serialize(doc))


# POST – add new activity
@app.route("/api/activities", methods=["POST"])
def add_activity():
    data = request.get_json()
    required = ["name", "category", "description", "location", "date"]
    for field in required:
        if not data.get(field):
            return jsonify({"error": f"Missing field: {field}"}), 400

    data["rating"] = float(data.get("rating", 4.0))
    data["image_emoji"] = data.get("image_emoji", "🎯")
    data["tags"] = data.get("tags", [])
    data["created_at"] = datetime.utcnow()

    result = mongo.db.activities.insert_one(data)
    data["_id"] = str(result.inserted_id)
    return jsonify(data), 201


# DELETE activity
@app.route("/api/activities/<id>", methods=["DELETE"])
def delete_activity(id):
    result = mongo.db.activities.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        return jsonify({"error": "Not found"}), 404
    return jsonify({"message": "Deleted successfully"})


# GET categories
@app.route("/api/categories", methods=["GET"])
def get_categories():
    cats = mongo.db.activities.distinct("category")
    return jsonify(["All"] + sorted(cats))


# GET stats
@app.route("/api/stats", methods=["GET"])
def get_stats():
    total = mongo.db.activities.count_documents({})
    pipeline = [{"$group": {"_id": "$category", "count": {"$sum": 1}}}]
    by_cat = {d["_id"]: d["count"] for d in mongo.db.activities.aggregate(pipeline)}
    avg_pipeline = [{"$group": {"_id": None, "avg": {"$avg": "$rating"}}}]
    avg_res = list(mongo.db.activities.aggregate(avg_pipeline))
    avg_rating = round(avg_res[0]["avg"], 1) if avg_res else 0
    return jsonify({"total": total, "by_category": by_cat, "avg_rating": avg_rating})


@app.route("/admin")
def admin():
    activities = list(mongo.db.activities.find().sort("created_at", -1))
    for a in activities:
        a["_id"] = str(a["_id"])
    return render_template("admin.html", activities=activities)


if __name__ == "__main__":
    app.run(debug=True, port=5000)

