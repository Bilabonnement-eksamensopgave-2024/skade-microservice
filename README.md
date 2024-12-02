# skade-microservice

# Endpoints

This API provides several endpoints for managing damage types. Each damage type contains information about the type of damage, its severity, and associated repair costs.

## Get All Damage Types
- **URL:** `/damage_types`
- **Method:** `GET`
- **Response:**
  ```json
  [
    {
      "id": 1,
      "damage_type": "Ridse",
      "severity": "Minor",
      "repair_cost": 500
    }
    // ... additional damage types
  ]
  ```
- **Success Response Code:** `200 OK`

## Get Damage Type by ID
- **URL:** `/damage_types/<id>`
- **Method:** `GET`
- **URL Parameters:** `id=[integer]` - ID of the damage type to retrieve
- **Response:**
  ```json
  {
    "id": 1,
    "damage_type": "Ridse",
    "severity": "Minor",
    "repair_cost": 500
  }
  ```
- **Success Response Code:** `200 OK`

## Update Damage Type
- **URL:** `/damage_types/<id>`
- **Method:** `PATCH`
- **URL Parameters:** `id=[integer]` - ID of the damage type to update
- **Request Body:**
  ```json
  {
    "id": 1,
    "damage_type": "Ridse",
    "severity": "Minor",
    "repair_cost": 500
  }
  ```
- **Success Response Code:** `200 OK`
- **Error Response Code:** `400 Bad Request` if no data is provided

## Add New Damage Type
- **URL:** `/damage_types`
- **Method:** `POST`
- **Request Body:**
  ```json
  {
    "damage_type": "Ridse",
    "severity": "Minor",
    "repair_cost": 500
  }
  ```
- **Success Response Code:** `200 OK`
- **Error Response Code:** `400 Bad Request` if no data is provided or if data is invalid

## Delete Damage Type
- **URL:** `/damage_types/<id>`
- **Method:** `DELETE`
- **URL Parameters:** `id=[integer]` - ID of the damage type to delete
- **Success Response Code:** `200 OK`

## Data Structure
Each damage type contains the following fields:
- `id`: Unique identifier for the damage type (integer)
- `damage_type`: Name/description of the damage type (string)
- `severity`: Severity level of the damage (Minor, Moderate, Severe)
- `repair_cost`: Estimated cost of repair in currency units (integer)


















