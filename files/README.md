# ResQ — Disaster Management & Emergency Response System
### Project_SEEVEN2026

---

## 📁 Project Structure

```
disaster_mgmt/
├── app.py               ← Python Flask backend (REST API)
├── requirements.txt     ← Python dependencies
├── data/
│   └── db.json          ← JSON file-based database (auto-created)
├── templates/
│   └── index.html       ← Frontend (HTML/CSS/JS)
└── README.md
```

---

## ⚙️ How to Run

### 1. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the Flask server
```bash
python app.py
```

### 3. Open browser
```
http://localhost:5000
```

---

## 🔐 Demo Login Credentials

| Role    | Email              | Password |
|---------|--------------------|----------|
| Admin   | admin@demo.com     | admin    |
| Citizen | ravi@demo.com      | 1234     |

---

## 📦 Modules

| Module                        | Features                                                   |
|-------------------------------|------------------------------------------------------------|
| User Registration & Login     | Register, Login, Role-based access (Admin / Citizen)       |
| Incident Reporting            | Submit flood/earthquake/fire reports with severity         |
| Emergency Alert System        | Admin issues/deletes alerts; visible to all users          |
| Rescue Team Management        | View/Add/Delete rescue teams with status tracking          |
| Resource Allocation           | Track equipment, medical kits, relief materials            |
| Disaster Monitoring Dashboard | Live stats, recent reports, active alerts                  |
| Admin Panel                   | Manage all reports, users, alerts, teams                   |

---

## 🌐 REST API Endpoints

| Method | Endpoint              | Description                      |
|--------|-----------------------|----------------------------------|
| POST   | /api/register         | Register new user                |
| POST   | /api/login            | Login                            |
| GET    | /api/users            | List all users                   |
| GET    | /api/reports          | Get all reports                  |
| POST   | /api/reports          | Submit new report                |
| PUT    | /api/reports/<id>     | Update report (e.g. status)      |
| DELETE | /api/reports/<id>     | Delete report                    |
| GET    | /api/alerts           | Get all alerts                   |
| POST   | /api/alerts           | Issue new alert                  |
| DELETE | /api/alerts/<id>      | Remove alert                     |
| GET    | /api/teams            | Get all rescue teams             |
| POST   | /api/teams            | Add team                         |
| PUT    | /api/teams/<id>       | Update team                      |
| DELETE | /api/teams/<id>       | Delete team                      |
| GET    | /api/resources        | Get all resources                |
| POST   | /api/resources        | Add resource                     |
| PUT    | /api/resources/<id>   | Update resource                  |
| DELETE | /api/resources/<id>   | Delete resource                  |
| GET    | /api/stats            | Dashboard statistics             |

---

## 🧰 Technologies Used

| Layer     | Technology                          |
|-----------|-------------------------------------|
| Frontend  | HTML5, CSS3, Vanilla JavaScript     |
| Backend   | Python 3, Flask, Flask-CORS         |
| Database  | JSON flat-file (data/db.json)       |
| Fonts     | Bebas Neue, DM Sans, JetBrains Mono |

---

## 📝 Notes
- Data is persisted in `data/db.json` across restarts.
- Admin role can issue alerts, manage teams/resources, and update report statuses.
- Citizens can register, report incidents, and view alerts.
