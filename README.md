# skade-microservice

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.x-green.svg)
![SQLite](https://img.shields.io/badge/SQLite-3-blue.svg)

## Overview

The **Damage Management System** microservice manages damage-related information, including damage types and individual damage reports. This service provides RESTful endpoints for managing damage types and reports, with integrated SQLite database storage.

## Project Structure

```
skade-microservice/
├── app.py                 # Main Flask application
├── damage_type.py         # Damage types database operations
├── damage_reports.py      # Damage reports database operations
├── swagger/              # Swagger documentation
└── damage.db             # SQLite database
```

## Setup and Installation

1. **Environment Setup**
   ```bash
   # Create and configure .env file
   DB_PATH=damage.db
   PORT=5000
   ```

2. **Install Dependencies**
   ```bash
   pip install flask sqlite3 python-dotenv flasgger
   ```

3. **Initialize Database**
   ```bash
   python app.py
   ```

## API Documentation

### Damage Types API

#### Get All Damage Types
- **URL:** `/damage-types`
- **Method:** `GET`
- **Response Codes:**
  - `200`: Success
  - `204`: No content
  - `500`: Server error
- **Response Format:**
  ```json
  [
    {
      "id": 1,
      "damage_type": "Ridse",
      "severity": "Minor",
      "repair_cost": 500
    }
  ]
  ```

#### Get Damage Type by ID
- **URL:** `/damage-types/<id>`
- **Method:** `GET`
- **Response Codes:**
  - `200`: Success
  - `404`: Not found
  - `500`: Server error

#### Add New Damage Type
- **URL:** `/damage-types`
- **Method:** `POST`
- **Request Body:**
  ```json
  {
    "damage_type": "Ridse",
    "severity": "Minor",
    "repair_cost": 500
  }
  ```
- **Response Codes:**
  - `201`: Created successfully
  - `400`: Bad request
  - `409`: Conflict
  - `500`: Server error

#### Update Damage Type
- **URL:** `/damage-types/<id>`
- **Method:** `PATCH`
- **Response Codes:**
  - `200`: Success
  - `400`: Bad request
  - `404`: Not found
  - `500`: Server error

#### Delete Damage Type
- **URL:** `/damage-types/<id>`
- **Method:** `DELETE`
- **Response Codes:**
  - `204`: Deleted successfully
  - `404`: Not found
  - `500`: Server error

### Damage Reports API

#### Get All Damage Reports
- **URL:** `/damage-reports`
- **Method:** `GET`
- **Response Codes:**
  - `200`: Success
  - `204`: No content
  - `500`: Server error
- **Response Format:**
  ```json
  [
    {
      "damagereportid": 1,
      "carid": 123,
      "subscriptionid": 456,
      "reportdate": "2024-01-01",
      "description": "Front bumper damage",
      "damagetypeid": 1
    }
  ]
  ```

#### Get Reports by Filters
| Endpoint | Description |
|----------|-------------|
| `/damage-reports/<id>` | Get report by ID |
| `/damage-reports/cars/<id>` | Get reports by car ID |
| `/damage-reports/subscriptions/<id>` | Get reports by subscription ID |
| `/damage-reports/subscriptions/<id>/total-damage` | Get total repair cost |

#### Add New Damage Report
- **URL:** `/damage-reports`
- **Method:** `POST`
- **Request Body:**
  ```json
  {
    "carid": 123,
    "subscriptionid": 456,
    "reportdate": "2024-01-01",
    "description": "Front bumper damage",
    "damagetypeid": 1
  }
  ```
- **Response Codes:**
  - `200`: Success
  - `400`: Bad request
  - `409`: Conflict
  - `500`: Server error

#### Update Damage Report
- **URL:** `/damage-reports/<id>`
- **Method:** `PATCH`
- **Response Codes:**
  - `200`: Success
  - `404`: Not found
  - `500`: Server error

#### Delete Damage Report
- **URL:** `/damage-reports/<id>`
- **Method:** `DELETE`
- **Response Codes:**
  - `200`: Success
  - `404`: Not found
  - `500`: Server error

## Database Schema

### Damage Types Table
```sql
CREATE TABLE damage_type (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    damage_type TEXT NOT NULL,
    severity TEXT NOT NULL,
    repair_cost INTEGER NOT NULL
)
```

### Damage Reports Table
```sql
CREATE TABLE damage_reports (
    damagereportid INTEGER PRIMARY KEY AUTOINCREMENT,
    carid INTEGER NOT NULL,
    subscriptionid INTEGER NOT NULL,
    reportdate DATE NOT NULL,
    description TEXT NOT NULL,
    damagetypeid INTEGER NOT NULL
)
```

## Development Guidelines

1. **Environment Variables**
   - Always use the `.env` file for configuration
   - Required variables: `DB_PATH`, `PORT`

2. **API Responses**
   - All endpoints return JSON responses
   - Include appropriate HTTP status codes
   - Handle errors consistently

3. **Database Operations**
   - Use context managers for database connections
   - Implement proper error handling
   - Validate input data before database operations
