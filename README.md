# SportVibe 
**Sports, Food & Recreation Hub**
Built with: Flask (Python) · MongoDB · Vanilla JavaScript

## Project Structure
```
sportvibe/
├── app.py                  ← Flask backend + all API routes
├── requirements.txt        ← Python dependencies
├── templates/
│   └── index.html          ← Main HTML page
└── static/
    ├── css/style.css        ← All styling
    └── js/app.js            ← Frontend JS (fetch API, DOM)
```

## Setup (8 Steps, ~5 minutes)

### 1. Install MongoDB
- Download from https://www.mongodb.com/try/download/community
- Start the service: `mongod` (or use MongoDB Compass GUI)

### 2. Create & activate Python virtual environment
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Flask app
```bash
python app.py
```

### 5. Open your browser
```
http://localhost:5000
```

The database auto-seeds with 6 sample activities on first run.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/activities` | List all activities |
| GET | `/api/activities?category=Sports` | Filter by category |
| GET | `/api/activities?search=football` | Search by keyword |
| GET | `/api/activities/<id>` | Get single activity |
| POST | `/api/activities` | Add new activity |
| DELETE | `/api/activities/<id>` | Delete activity |
| GET | `/api/categories` | List all categories |
| GET | `/api/stats` | Dashboard stats |

## Features
- View activities by category (Sports, Food, Recreation, Fitness)
- Live search across name, description, and tags
- Add new activities via modal form
- Delete activities
- Stats dashboard (total, average rating, by category)
- Responsive design – works on mobile


## MongoDB Atlas (Optional – for online hosting)
Change line in `app.py`:
```python
app.config["MONGO_URI"] = "mongodb+srv://<user>:<pass>@cluster.mongodb.net/sportvibe"
```
