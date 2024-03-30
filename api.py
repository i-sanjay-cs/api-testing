from flask import Flask, jsonify, request, abort
from pyngrok import ngrok

app = Flask(__name__)

tasks = [
    {"id": 1, "title": "Task 1", "API Testing": "Consider any one repository of API services and create request with GET,POST,PUT and Delete", "completed": False},
    {"id": 2, "title": "Task 2", "Pareto task": "Create a diagram using the excel sheet", "completed": True}
]

# Route to get all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

# Route to get a single task by ID
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = next((task for task in tasks if task['id'] == task_id), None)
    if task is None:
        abort(404)  # Task not found
    return jsonify(task)

# Route to create a new task
@app.route('/tasks', methods=['POST'])
def create_task():
    if not request.json or 'title' not in request.json:
        abort(400)  # Bad request
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'completed': False
    }
    tasks.append(task)
    return jsonify(task), 201  # 201 status code indicates resource created

# Route to update an existing task
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = next((task for task in tasks if task['id'] == task_id), None)
    if task is None:
        abort(404)  # Task not found
    if not request.json:
        abort(400)  # Bad request
    task.update(request.json)
    return jsonify(task)

# Route to delete a task by ID
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task['id'] != task_id]
    return '', 204  # 204 status code indicates success with no content

# Expose the Flask app using ngrok
ngrok.set_auth_token("enter you tocken here")
public_url = ngrok.connect(5000)  # Assuming Flask is running on port 5000
print("Public URL:", public_url)

if __name__ == '__main__':
    app.run()  # By default, Flask runs on port 5000
