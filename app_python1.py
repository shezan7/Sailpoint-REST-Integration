"""
IAM REST API - SQLite3 Version (No SQLAlchemy)
Works with Python 3.14+ without version conflicts
"""

from flask import Flask, request, jsonify
import sqlite3
import json
from datetime import datetime
import os

app = Flask(__name__)

# Database file path
DB_PATH = 'iam.db'

# ==================== DATABASE INITIALIZATION ====================

def init_db():
    """Initialize database with tables"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create tables if they don't exist
    cursor.executescript('''
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            is_enabled BOOLEAN DEFAULT 1,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS "group" (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            description TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS user_group (
            user_id INTEGER NOT NULL,
            group_id INTEGER NOT NULL,
            PRIMARY KEY (user_id, group_id),
            FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE,
            FOREIGN KEY (group_id) REFERENCES "group"(id) ON DELETE CASCADE
        );
    ''')
    
    conn.commit()
    conn.close()

# Initialize database on startup
init_db()

# ==================== DATABASE HELPER FUNCTIONS ====================

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def user_to_dict(row):
    """Convert user row to dictionary with groups"""
    if not row:
        return None
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT g.id, g.name FROM "group" g
        JOIN user_group ug ON g.id = ug.group_id
        WHERE ug.user_id = ?
    ''', (row['id'],))
    groups = [{'id': g['id'], 'name': g['name']} for g in cursor.fetchall()]
    conn.close()
    
    return {
        'id': row['id'],
        'username': row['username'],
        'email': row['email'],
        'is_enabled': bool(row['is_enabled']),
        'created_at': row['created_at'],
        'updated_at': row['updated_at'],
        'groups': groups
    }

def group_to_dict(row, include_members=False):
    """Convert group row to dictionary"""
    if not row:
        return None
    
    result = {
        'id': row['id'],
        'name': row['name'],
        'description': row['description'],
        'created_at': row['created_at'],
        'updated_at': row['updated_at']
    }
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) as count FROM user_group WHERE group_id = ?', (row['id'],))
    count = cursor.fetchone()['count']
    result['member_count'] = count
    
    if include_members:
        cursor.execute('''
            SELECT u.id, u.username, u.email, u.is_enabled, u.created_at, u.updated_at
            FROM user u
            JOIN user_group ug ON u.id = ug.user_id
            WHERE ug.group_id = ?
        ''', (row['id'],))
        members = [user_to_dict(m) for m in cursor.fetchall()]
        result['members'] = members
    
    conn.close()
    return result

# ==================== HOME ROUTE ====================

@app.route('/', methods=['GET'])
def get_home():
    return jsonify({"message": "IAM REST API", "version": "1.0"}), 200

# ==================== USER ENDPOINTS ====================

@app.route('/api/users', methods=['GET'])
def get_all_users():
    """Get all users"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM user')
        users = [user_to_dict(row) for row in cursor.fetchall()]
        conn.close()
        return jsonify(users), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_single_user(user_id):
    """Get single user by ID"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM user WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        conn.close()
        
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        return jsonify(user_to_dict(user)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/users', methods=['POST'])
def create_user():
    """Create a new user"""
    try:
        data = request.json
        print(data)
        
        if not data or not data.get('username') or not data.get('email'):
            return jsonify({"error": "Username and email are required"}), 400
        
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO user (username, email, is_enabled)
                VALUES (?, ?, ?)
            ''', (data['username'], data['email'], data.get('is_enabled', True)))
            conn.commit()
            
            user_id = cursor.lastrowid
            cursor.execute('SELECT * FROM user WHERE id = ?', (user_id,))
            user = cursor.fetchone()
            conn.close()
            
            return jsonify(user_to_dict(user)), 201
        except sqlite3.IntegrityError as e:
            conn.close()
            if 'username' in str(e):
                return jsonify({"error": "Username already exists"}), 409
            elif 'email' in str(e):
                return jsonify({"error": "Email already exists"}), 409
            return jsonify({"error": str(e)}), 409
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Update user information"""
    try:
        data = request.json
        conn = get_db()
        cursor = conn.cursor()
        
        # Check if user exists
        cursor.execute('SELECT * FROM user WHERE id = ?', (user_id,))
        if not cursor.fetchone():
            conn.close()
            return jsonify({"error": "User not found"}), 404
        
        # Update fields
        if 'username' in data:
            try:
                cursor.execute('UPDATE user SET username = ? WHERE id = ?', (data['username'], user_id))
            except sqlite3.IntegrityError:
                conn.close()
                return jsonify({"error": "Username already exists"}), 409
        
        if 'email' in data:
            try:
                cursor.execute('UPDATE user SET email = ? WHERE id = ?', (data['email'], user_id))
            except sqlite3.IntegrityError:
                conn.close()
                return jsonify({"error": "Email already exists"}), 409
        
        if 'is_enabled' in data:
            cursor.execute('UPDATE user SET is_enabled = ? WHERE id = ?', (data['is_enabled'], user_id))
        
        cursor.execute('UPDATE user SET updated_at = CURRENT_TIMESTAMP WHERE id = ?', (user_id,))
        conn.commit()
        
        cursor.execute('SELECT * FROM user WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        conn.close()
        
        return jsonify(user_to_dict(user)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete user"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM user WHERE id = ?', (user_id,))
        if not cursor.fetchone():
            conn.close()
            return jsonify({"error": "User not found"}), 404
        
        cursor.execute('DELETE FROM user WHERE id = ?', (user_id,))
        conn.commit()
        conn.close()
        
        return jsonify({"message": "User deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/users/<int:user_id>/enable', methods=['PATCH'])
def enable_user(user_id):
    """Enable user"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM user WHERE id = ?', (user_id,))
        if not cursor.fetchone():
            conn.close()
            return jsonify({"error": "User not found"}), 404
        
        cursor.execute('UPDATE user SET is_enabled = 1, updated_at = CURRENT_TIMESTAMP WHERE id = ?', (user_id,))
        conn.commit()
        
        cursor.execute('SELECT * FROM user WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        conn.close()
        
        return jsonify({
            "message": "User enabled successfully",
            "user": user_to_dict(user)
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/users/<int:user_id>/disable', methods=['PATCH'])
def disable_user(user_id):
    """Disable user"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM user WHERE id = ?', (user_id,))
        if not cursor.fetchone():
            conn.close()
            return jsonify({"error": "User not found"}), 404
        
        cursor.execute('UPDATE user SET is_enabled = 0, updated_at = CURRENT_TIMESTAMP WHERE id = ?', (user_id,))
        conn.commit()
        
        cursor.execute('SELECT * FROM user WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        conn.close()
        
        return jsonify({
            "message": "User disabled successfully",
            "user": user_to_dict(user)
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==================== GROUP ENDPOINTS ====================

@app.route('/api/groups', methods=['GET'])
def get_all_groups():
    """Get all groups"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM "group"')
        groups = [group_to_dict(row) for row in cursor.fetchall()]
        conn.close()
        return jsonify(groups), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/groups/<int:group_id>', methods=['GET'])
def get_single_group(group_id):
    """Get single group by ID with members"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM "group" WHERE id = ?', (group_id,))
        group = cursor.fetchone()
        conn.close()
        
        if not group:
            return jsonify({"error": "Group not found"}), 404
        
        return jsonify(group_to_dict(group, include_members=True)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/groups', methods=['POST'])
def create_group():
    """Create a new group"""
    try:
        data = request.json
        
        if not data or not data.get('name'):
            return jsonify({"error": "Group name is required"}), 400
        
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO "group" (name, description)
                VALUES (?, ?)
            ''', (data['name'], data.get('description', '')))
            conn.commit()
            
            group_id = cursor.lastrowid
            cursor.execute('SELECT * FROM "group" WHERE id = ?', (group_id,))
            group = cursor.fetchone()
            conn.close()
            
            return jsonify(group_to_dict(group)), 201
        except sqlite3.IntegrityError:
            conn.close()
            return jsonify({"error": "Group already exists"}), 409
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/groups/<int:group_id>', methods=['PUT'])
def update_group(group_id):
    """Update group information"""
    try:
        data = request.json
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM "group" WHERE id = ?', (group_id,))
        if not cursor.fetchone():
            conn.close()
            return jsonify({"error": "Group not found"}), 404
        
        if 'name' in data:
            try:
                cursor.execute('UPDATE "group" SET name = ? WHERE id = ?', (data['name'], group_id))
            except sqlite3.IntegrityError:
                conn.close()
                return jsonify({"error": "Group name already exists"}), 409
        
        if 'description' in data:
            cursor.execute('UPDATE "group" SET description = ? WHERE id = ?', (data['description'], group_id))
        
        cursor.execute('UPDATE "group" SET updated_at = CURRENT_TIMESTAMP WHERE id = ?', (group_id,))
        conn.commit()
        
        cursor.execute('SELECT * FROM "group" WHERE id = ?', (group_id,))
        group = cursor.fetchone()
        conn.close()
        
        return jsonify(group_to_dict(group)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/groups/<int:group_id>', methods=['DELETE'])
def delete_group(group_id):
    """Delete group"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM "group" WHERE id = ?', (group_id,))
        if not cursor.fetchone():
            conn.close()
            return jsonify({"error": "Group not found"}), 404
        
        cursor.execute('DELETE FROM "group" WHERE id = ?', (group_id,))
        conn.commit()
        conn.close()
        
        return jsonify({"message": "Group deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==================== USER-GROUP RELATIONSHIP ENDPOINTS ====================

@app.route('/api/users/<int:user_id>/groups/<int:group_id>', methods=['POST'])
def assign_group_to_user(user_id, group_id):
    """Assign group to user"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM user WHERE id = ?', (user_id,))
        if not cursor.fetchone():
            conn.close()
            return jsonify({"error": "User not found"}), 404
        
        cursor.execute('SELECT * FROM "group" WHERE id = ?', (group_id,))
        if not cursor.fetchone():
            conn.close()
            return jsonify({"error": "Group not found"}), 404
        
        try:
            cursor.execute('''
                INSERT INTO user_group (user_id, group_id)
                VALUES (?, ?)
            ''', (user_id, group_id))
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            return jsonify({"error": "User already assigned to this group"}), 409
        
        cursor.execute('SELECT * FROM user WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        conn.close()
        
        return jsonify({
            "message": "Group assigned to user successfully",
            "user": user_to_dict(user)
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/users/<int:user_id>/groups/<int:group_id>', methods=['DELETE'])
def remove_group_from_user(user_id, group_id):
    """Remove group from user"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM user WHERE id = ?', (user_id,))
        if not cursor.fetchone():
            conn.close()
            return jsonify({"error": "User not found"}), 404
        
        cursor.execute('SELECT * FROM "group" WHERE id = ?', (group_id,))
        if not cursor.fetchone():
            conn.close()
            return jsonify({"error": "Group not found"}), 404
        
        cursor.execute('''
            DELETE FROM user_group
            WHERE user_id = ? AND group_id = ?
        ''', (user_id, group_id))
        
        if cursor.rowcount == 0:
            conn.close()
            return jsonify({"error": "User is not assigned to this group"}), 404
        
        conn.commit()
        
        cursor.execute('SELECT * FROM user WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        conn.close()
        
        return jsonify({
            "message": "Group removed from user successfully",
            "user": user_to_dict(user)
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/users/<int:user_id>/groups', methods=['GET'])
def get_user_groups(user_id):
    """Get all groups assigned to a user"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM user WHERE id = ?', (user_id,))
        if not cursor.fetchone():
            conn.close()
            return jsonify({"error": "User not found"}), 404
        
        cursor.execute('''
            SELECT g.* FROM "group" g
            JOIN user_group ug ON g.id = ug.group_id
            WHERE ug.user_id = ?
        ''', (user_id,))
        groups = [group_to_dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return jsonify(groups), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/groups/<int:group_id>/members', methods=['GET'])
def get_group_members(group_id):
    """Get all members (users) of a group"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM "group" WHERE id = ?', (group_id,))
        if not cursor.fetchone():
            conn.close()
            return jsonify({"error": "Group not found"}), 404
        
        cursor.execute('''
            SELECT u.* FROM user u
            JOIN user_group ug ON u.id = ug.user_id
            WHERE ug.group_id = ?
        ''', (group_id,))
        users = [user_to_dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return jsonify(users), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

# ==================== RUN APPLICATION ====================

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
