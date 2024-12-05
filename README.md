# skade-microservice

# Endpoints

This API provides several endpoints for managing damage types. Each damage type contains information about the type of damage, its severity, and associated repair costs.s

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


# Damage Reports API Documentation

## Base URL
`/damage-reports`

## Endpoints

### Get All Damage Reports
Get a list of all damage reports in the system.

**Request**
```http
GET /damage-reports
```

**Response**
- `200 OK`: Successfully retrieved damage reports
  ```json
  [
    {
      "damagereportid": integer,
      "carid": integer,
      "subscriptionid": integer,
      "reportdate": string,
      "description": string,
      "damagetypeid": integer
    }
  ]
  ```
- `204 No Content`: No damage reports found
- `500 Internal Server Error`: Server error

### Get Damage Report by ID
Retrieve a specific damage report by its ID.

**Request**
```http
GET /damage-reports/{id}
```

**Response**
- `200 OK`: Successfully retrieved damage report
- `404 Not Found`: Damage report not found
- `500 Internal Server Error`: Server error

### Get Damage Reports by Car ID
Retrieve all damage reports for a specific car.

**Request**
```http
GET /damage-reports/cars/{id}
```

**Response**
- `200 OK`: Successfully retrieved damage reports
- `404 Not Found`: No damage reports found for the car
- `500 Internal Server Error`: Server error

### Get Damage Reports by Subscription ID
Retrieve all damage reports for a specific subscription.

**Request**
```http
GET /damage-reports/subscriptions/{id}
```

**Response**
- `200 OK`: Successfully retrieved damage reports
- `404 Not Found`: No damage reports found for the subscription
- `500 Internal Server Error`: Server error

### Get Total Repair Cost by Subscription ID
Calculate the total repair cost for a specific subscription.

**Request**
```http
GET /damage-reports/subscriptions/{id}/total-damage
```

**Response**
- `200 OK`:
  ```json
  {
    "subscriptionid": integer,
    "total_amount": number
  }
  ```
- `404 Not Found`: No damages found for the subscription
- `500 Internal Server Error`: Server error

### Update Damage Report
Update an existing damage report by ID.

**Request**
```http
PATCH /damage-reports/{id}
```

**Request Body**
```json
{
  "field_name": "new_value"
}
```

**Response**
- `200 OK`: Successfully updated damage report
- `404 Not Found`: Damage report not found
- `500 Internal Server Error`: Server error

### Add New Damage Report
Create a new damage report.

**Request**
```http
POST /damage-reports
```

**Request Body**
```json
{
  "carid": integer,
  "subscriptionid": integer,
  "reportdate": string,
  "description": string,
  "damagetypeid": integer
}
```

**Response**
- `200 OK`: Successfully created damage report
- `400 Bad Request`: Missing required fields
- `409 Conflict`: Damage report already exists
- `500 Internal Server Error`: Server error

### Delete Damage Report
Delete a damage report by ID.

**Request**
```http
DELETE /damage-reports/{id}
```

**Response**
- `200 OK`: Successfully deleted damage report
- `404 Not Found`: Damage report not found
- `500 Internal Server Error`: Server error















