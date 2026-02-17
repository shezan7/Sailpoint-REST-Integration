from flask import Flask, request, jsonify

app = Flask(__name__)

users = [
    {"id": "1", "username": "john", "email": "john@test.com", "active": True},
    {"id": "2", "username": "alice", "email": "alice@test.com", "active": True}
]

groups = [
    {
        "id": "g1",
        "name": "Admins",
        "description": "Administrator Group",
        "members": ["1"]
    },
    {
        "id": "g2",
        "name": "Developers",
        "description": "Developer Group",
        "members": ["2"]
    }
]


@app.route('/', methods=['GET'])
def get_home():
    return jsonify({"message":"Main Route"})

@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users)

@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    users.append(data)
    return jsonify(data), 201

@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    for user in users:
        if user["id"] == id:
            user.update(request.json)
            return jsonify(user)
    return {"error": "User not found"}, 404

@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    global users
    users = [user for user in users if user["id"] != id]
    return {"message": "Deleted"}, 200


@app.route('/groups', methods=['GET'])
def get_groups():
    return jsonify(groups)

@app.route('/groups/<id>', methods=['GET'])
def get_group(id):
    for group in groups:
        if group["id"] == id:
            return jsonify(group)
    return {"error": "Group not found"}, 404

@app.route('/groups/<group_id>/members', methods=['POST'])
def add_member(group_id):
    data = request.json
    user_id = data.get("userId")

    for group in groups:
        if group["id"] == group_id:
            if user_id not in group["members"]:
                group["members"].append(user_id)
                return jsonify(group)

    return {"error": "Group not found"}, 404

@app.route('/groups/<group_id>/members/<user_id>', methods=['DELETE'])
def remove_member(group_id, user_id):
    for group in groups:
        if group["id"] == group_id:
            if user_id in group["members"]:
                group["members"].remove(user_id)
                return jsonify(group)

    return {"error": "Group not found"}, 404


if __name__ == '__main__':
    app.run(port=5000)
