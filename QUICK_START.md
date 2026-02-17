# IAM REST API - Quick Start Guide

## Overview
This is a complete Flask-based CRUD application for managing Users and Groups with SQLite database integration. The API provides comprehensive endpoints for full user and group management.

## Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

## Installation & Setup

### Step 1: Install Dependencies
Navigate to the project directory and install the required packages:

```bash
pip install -r requirements.txt
```

**Required Packages:**
- Flask 2.3.0 - Web framework
- Flask-SQLAlchemy 3.0.5 - ORM for database
- SQLAlchemy 2.0.0 - SQL toolkit and ORM
- Werkzeug 2.3.0 - WSGI utility library

### Step 2: Run the Application

```bash
python app_python1.py
```

**Expected Output:**
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://0.0.0.0:5000
```

The API will be available at:
- **Main Route:** http://localhost:5000
- **API Endpoints:** http://localhost:5000/api/...

### Step 3: Test the API

In a new terminal/command prompt, run the test script:

```bash
python test_api.py
```

This will:
- Create sample users
- Create sample groups
- Test all API endpoints
- Show responses and status codes
- Clean up with deletions

## File Structure

```
Sailpoint REST Integration/
├── app_python1.py              # Main Flask application
├── requirements.txt             # Python dependencies
├── test_api.py                 # API testing script
├── API_DOCUMENTATION.md         # Complete API documentation
├── QUICK_START.md              # This file
└── iam.db                       # SQLite database (auto-created)
```

## Key Features

### User Management
✅ Create users with username and email
✅ Retrieve all users
✅ Get individual user details
✅ Update user information
✅ Enable/Disable user accounts
✅ Delete users

### Group Management
✅ Create groups
✅ Retrieve all groups
✅ Get individual group details
✅ Update group information
✅ Delete groups

### User-Group Management
✅ Assign groups to users
✅ Remove groups from users
✅ View user's assigned groups
✅ View group members

### Data Persistence
✅ SQLite database integration
✅ Automatic timestamps (created_at, updated_at)
✅ Relationship tracking between users and groups

## Database

**Database File:** `iam.db` (automatically created in the project directory)

**Tables:**
- `user` - Stores user information
- `group` - Stores group information
- `user_group` - Association table linking users to groups

## API Examples

### Quick API Tests with cURL

**Get All Users:**
```bash
curl http://localhost:5000/api/users
```

**Create User:**
```bash
curl -X POST http://localhost:5000/api/users \
  -H "Content-Type: application/json" \
  -d '{"username":"john","email":"john@example.com"}'
```

**Create Group:**
```bash
curl -X POST http://localhost:5000/api/groups \
  -H "Content-Type: application/json" \
  -d '{"name":"Admins","description":"Admin Group"}'
```

**Assign Group to User (user_id=1, group_id=1):**
```bash
curl -X POST http://localhost:5000/api/users/1/groups/1
```

**Disable User (user_id=1):**
```bash
curl -X PATCH http://localhost:5000/api/users/1/disable
```

For more detailed examples and endpoint documentation, see [API_DOCUMENTATION.md](API_DOCUMENTATION.md)

## API Endpoints Summary

### Users
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/users` | Get all users |
| GET | `/api/users/<id>` | Get single user |
| POST | `/api/users` | Create user |
| PUT | `/api/users/<id>` | Update user |
| DELETE | `/api/users/<id>` | Delete user |
| PATCH | `/api/users/<id>/enable` | Enable user |
| PATCH | `/api/users/<id>/disable` | Disable user |

### Groups
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/groups` | Get all groups |
| GET | `/api/groups/<id>` | Get single group |
| POST | `/api/groups` | Create group |
| PUT | `/api/groups/<id>` | Update group |
| DELETE | `/api/groups/<id>` | Delete group |

### User-Group Relations
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/users/<user_id>/groups/<group_id>` | Assign group to user |
| DELETE | `/api/users/<user_id>/groups/<group_id>` | Remove group from user |
| GET | `/api/users/<user_id>/groups` | Get user's groups |
| GET | `/api/groups/<group_id>/members` | Get group members |

## Troubleshooting

### Port Already in Use
If port 5000 is already in use, modify `app_python1.py`:
```python
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)  # Change 5000 to another port
```

### Database Errors
To reset the database, delete `iam.db` file:
```bash
rm iam.db  # On Linux/Mac
del iam.db # On Windows
```
The database will be automatically recreated on next run.

### Module Not Found Errors
Make sure all dependencies are installed:
```bash
pip install --upgrade -r requirements.txt
```

### Connection Refused
Ensure the Flask app is running in a separate terminal before running tests:
```bash
# Terminal 1
python app_python1.py

# Terminal 2
python test_api.py
```

## Next Steps

1. **Test the API:** Run `python test_api.py`
2. **Explore Endpoints:** Check `API_DOCUMENTATION.md` for detailed endpoint descriptions
3. **Customize:** Modify `app_python1.py` to add more fields or endpoints as needed
4. **Deploy:** Consider using production WSGI servers like Gunicorn or uWSGI

## Support Points

- **SQLAlchemy ORM:** Database models and queries
- **Flask Routes:** All API endpoints with proper HTTP methods
- **Error Handling:** 400, 404, 409, 500 error responses
- **Data Validation:** Username/email uniqueness, required fields
- **Relationship Management:** Many-to-many user-group relationships

---

**Created:** February 17, 2026
**Technology Stack:** Flask + SQLAlchemy + SQLite
