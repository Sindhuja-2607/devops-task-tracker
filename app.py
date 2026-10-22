
from flask import Flask, jsonify, request

app = Flask(__name__)

tasks = [
    {
        "id": 1,
        "title": "Validate healthcare data",
        "status": "To Do"
    }
]

next_id = 2


@app.route("/")
def home():
    return jsonify({
        "message": "DevOps Task Tracker API is running"
    })


@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks)


@app.route("/tasks", methods=["POST"])
def create_task():
    global next_id

    data = request.get_json(silent=True) or {}
    title = data.get("title", "").strip()

    if not title:
        return jsonify({"error": "Task title is required"}), 400

    task = {
        "id": next_id,
        "title": title,
        "status": "To Do"
    }

    tasks.append(task)
    next_id += 1

    return jsonify(task), 201


@app.route("/tasks/<int:task_id>", methods=["PATCH"])
def update_task(task_id):
    data = request.get_json(silent=True) or {}
    status = data.get("status", "")

    allowed_statuses = ["To Do", "In Progress", "Done"]

    if status not in allowed_statuses:
        return jsonify({
            "error": "Status must be To Do, In Progress, or Done"
        }), 400

    for task in tasks:
        if task["id"] == task_id:
            task["status"] = status
            return jsonify(task)

    return jsonify({"error": "Task not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
