# IAM REST API Documentation

## Overview
A comprehensive Flask-based REST API for managing users and groups with SQLite database integration.

## Installation

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Run the application:**
```bash
python app_python1.py
```

The API will be available at `http://localhost:5000`

## Database
- **Type:** SQLite
- **File:** `iam.db` (created automatically on first run)
- **Tables:** User, Group, user_group (association table)

---

## API Endpoints

### Home Route
**`GET /`**
- Returns API information

**Response (200):**
```json
{
  "message": "IAM REST API",
  "version": "1.0"
}
```

---

## USER ENDPOINTS

### Get All Users
**`GET /api/users`**
- Retrieve all users from the system

**Response (200):**
```json
[
  {
    "id": 1,
    "username": "john",
    "email": "john@example.com",
    "is_enabled": true,
    "created_at": "2026-02-17T10:30:00.000000",
    "updated_at": "2026-02-17T10:30:00.000000",
    "groups": [
      {"id": 1, "name": "Admins"}
    ]
  }
]
```

---

### Get Single User
**`GET /api/users/<user_id>`**
- Retrieve a specific user by ID

**Parameters:**
- `user_id` (integer): User ID

**Response (200):**
```json
{
  "id": 1,
  "username": "john",
  "email": "john@example.com",
  "is_enabled": true,
  "created_at": "2026-02-17T10:30:00.000000",
  "updated_at": "2026-02-17T10:30:00.000000",
  "groups": [
    {"id": 1, "name": "Admins"}
  ]
}
```

**Response (404):**
```json
{"error": "User not found"}
```

---

### Create User
**`POST /api/users`**
- Create a new user

**Request Body:**
```json
{
  "username": "alice",
  "email": "alice@example.com",
  "is_enabled": true
}
```

**Required Fields:** `username`, `email`

**Response (201):**
```json
{
  "id": 2,
  "username": "alice",
  "email": "alice@example.com",
  "is_enabled": true,
  "created_at": "2026-02-17T10:30:00.000000",
  "updated_at": "2026-02-17T10:30:00.000000",
  "groups": []
}
```

**Error Responses:**
- 400: Missing required fields
- 409: Username or email already exists

---

### Update User
**`PUT /api/users/<user_id>`**
- Update user information

**Parameters:**
- `user_id` (integer): User ID

**Request Body:**
```json
{
  "username": "new_username",
  "email": "new_email@example.com",
  "is_enabled": false
}
```

**Response (200):**
```json
{
  "id": 1,
  "username": "new_username",
  "email": "new_email@example.com",
  "is_enabled": false,
  "created_at": "2026-02-17T10:30:00.000000",
  "updated_at": "2026-02-17T10:31:00.000000",
  "groups": []
}
```

**Error Responses:**
- 404: User not found
- 409: New username or email already existed

---

### Delete User
**`DELETE /api/users/<user_id>`**
- Delete a user from the system

**Parameters:**
- `user_id` (integer): User ID

**Response (200):**
```json
{"message": "User deleted successfully"}
```

**Response (404):**
```json
{"error": "User not found"}
```

---

### Enable User
**`PATCH /api/users/<user_id>/enable`**
- Enable a disabled user

**Parameters:**
- `user_id` (integer): User ID

**Response (200):**
```json
{
  "message": "User enabled successfully",
  "user": {
    "id": 1,
    "username": "john",
    "email": "john@example.com",
    "is_enabled": true,
    ...
  }
}
```

---

### Disable User
**`PATCH /api/users/<user_id>/disable`**
- Disable an enabled user

**Parameters:**
- `user_id` (integer): User ID

**Response (200):**
```json
{
  "message": "User disabled successfully",
  "user": {
    "id": 1,
    "username": "john",
    "email": "john@example.com",
    "is_enabled": false,
    ...
  }
}
```

---

## GROUP ENDPOINTS

### Get All Groups
**`GET /api/groups`**
- Retrieve all groups from the system

**Response (200):**
```json
[
  {
    "id": 1,
    "name": "Admins",
    "description": "Administrator Group",
    "created_at": "2026-02-17T10:30:00.000000",
    "updated_at": "2026-02-17T10:30:00.000000",
    "member_count": 2
  }
]
```

---

### Get Single Group
**`GET /api/groups/<group_id>`**
- Retrieve a specific group by ID

**Parameters:**
- `group_id` (integer): Group ID

**Response (200):**
```json
{
  "id": 1,
  "name": "Admins",
  "description": "Administrator Group",
  "created_at": "2026-02-17T10:30:00.000000",
  "updated_at": "2026-02-17T10:30:00.000000",
  "member_count": 2,
  "members": [
    {
      "id": 1,
      "username": "john",
      "email": "john@example.com",
      ...
    }
  ]
}
```

---

### Create Group
**`POST /api/groups`**
- Create a new group

**Request Body:**
```json
{
  "name": "Developers",
  "description": "Developer Group"
}
```

**Required Fields:** `name`

**Response (201):**
```json
{
  "id": 2,
  "name": "Developers",
  "description": "Developer Group",
  "created_at": "2026-02-17T10:30:00.000000",
  "updated_at": "2026-02-17T10:30:00.000000",
  "member_count": 0
}
```

---

### Update Group
**`PUT /api/groups/<group_id>`**
- Update group information

**Parameters:**
- `group_id` (integer): Group ID

**Request Body:**
```json
{
  "name": "Senior Developers",
  "description": "Senior Developer Group"
}
```

**Response (200):**
```json
{
  "id": 2,
  "name": "Senior Developers",
  "description": "Senior Developer Group",
  "created_at": "2026-02-17T10:30:00.000000",
  "updated_at": "2026-02-17T10:31:00.000000",
  "member_count": 1
}
```

---

### Delete Group
**`DELETE /api/groups/<group_id>`**
- Delete a group from the system

**Parameters:**
- `group_id` (integer): Group ID

**Response (200):**
```json
{"message": "Group deleted successfully"}
```

---

## USER-GROUP RELATIONSHIP ENDPOINTS

### Assign Group to User
**`POST /api/users/<user_id>/groups/<group_id>`**
- Assign a group to a user

**Parameters:**
- `user_id` (integer): User ID
- `group_id` (integer): Group ID

**Response (200):**
```json
{
  "message": "Group assigned to user successfully",
  "user": {
    "id": 1,
    "username": "john",
    "email": "john@example.com",
    "is_enabled": true,
    "created_at": "2026-02-17T10:30:00.000000",
    "updated_at": "2026-02-17T10:30:00.000000",
    "groups": [
      {"id": 1, "name": "Admins"},
      {"id": 2, "name": "Developers"}
    ]
  }
}
```

**Error Responses:**
- 404: User or Group not found
- 409: User already assigned to this group

---

### Remove Group from User
**`DELETE /api/users/<user_id>/groups/<group_id>`**
- Remove a group from a user

**Parameters:**
- `user_id` (integer): User ID
- `group_id` (integer): Group ID

**Response (200):**
```json
{
  "message": "Group removed from user successfully",
  "user": {
    "id": 1,
    "username": "john",
    "email": "john@example.com",
    "is_enabled": true,
    "created_at": "2026-02-17T10:30:00.000000",
    "updated_at": "2026-02-17T10:30:00.000000",
    "groups": [
      {"id": 1, "name": "Admins"}
    ]
  }
}
```

---

### Get User Groups
**`GET /api/users/<user_id>/groups`**
- Get all groups assigned to a user

**Parameters:**
- `user_id` (integer): User ID

**Response (200):**
```json
[
  {
    "id": 1,
    "name": "Admins",
    "description": "Administrator Group",
    "created_at": "2026-02-17T10:30:00.000000",
    "updated_at": "2026-02-17T10:30:00.000000",
    "member_count": 2
  }
]
```

---

### Get Group Members
**`GET /api/groups/<group_id>/members`**
- Get all members (users) of a group

**Parameters:**
- `group_id` (integer): Group ID

**Response (200):**
```json
[
  {
    "id": 1,
    "username": "john",
    "email": "john@example.com",
    "is_enabled": true,
    "created_at": "2026-02-17T10:30:00.000000",
    "updated_at": "2026-02-17T10:30:00.000000",
    "groups": [
      {"id": 1, "name": "Admins"}
    ]
  }
]
```

---

## Testing with cURL

### Get All Users
```bash
curl -X GET http://localhost:5000/api/users
```

### Create User
```bash
curl -X POST http://localhost:5000/api/users \
  -H "Content-Type: application/json" \
  -d '{
    "username": "bob",
    "email": "bob@example.com",
    "is_enabled": true
  }'
```

### Update User
```bash
curl -X PUT http://localhost:5000/api/users/1 \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newemail@example.com"
  }'
```

### Delete User
```bash
curl -X DELETE http://localhost:5000/api/users/1
```

### Enable/Disable User
```bash
curl -X PATCH http://localhost:5000/api/users/1/enable
curl -X PATCH http://localhost:5000/api/users/1/disable
```

### Create Group
```bash
curl -X POST http://localhost:5000/api/groups \
  -H "Content-Type: application/json" \
  -d '{
    "name": "QA Team",
    "description": "QA Engineers"
  }'
```

### Assign Group to User
```bash
curl -X POST http://localhost:5000/api/users/1/groups/1 \
  -H "Content-Type: application/json"
```

### Remove Group from User
```bash
curl -X DELETE http://localhost:5000/api/users/1/groups/1
```

---

## HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request |
| 404 | Not Found |
| 409 | Conflict |
| 500 | Internal Server Error |

---

## Database Schema

### User Table
- `id` (Integer, Primary Key)
- `username` (String, Unique)
- `email` (String, Unique)
- `is_enabled` (Boolean, Default: True)
- `created_at` (DateTime)
- `updated_at` (DateTime)

### Group Table
- `id` (Integer, Primary Key)
- `name` (String, Unique)
- `description` (String)
- `created_at` (DateTime)
- `updated_at` (DateTime)

### user_group (Association Table)
- `user_id` (Foreign Key)
- `group_id` (Foreign Key)

---

## Notes

- All timestamps are in ISO 8601 format
- Usernames and emails must be unique
- Group names must be unique
- Users can be assigned to multiple groups
- Groups can have multiple users
- Deleting a user automatically removes it from all groups
- Deleting a group automatically removes it from all users
