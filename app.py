from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

tasks = []

@app.route('/')
def home():
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    task = {
        'title': request.form.get('task'),
        'priority': request.form.get('priority', 'Medium'),
        'due_date': request.form.get('due_date'),
        'subtasks': [],
        'completed': False
    }
    if task['title']:
        tasks.append(task)
    tasks.sort(key=lambda x: x['priority'], reverse=True)  # Sort tasks by priority
    return redirect(url_for('home'))

@app.route('/delete/<int:task_id>')
def delete(task_id):
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
    return redirect(url_for('home'))

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit(task_id):
    if request.method == 'POST':
        new_task_title = request.form.get('task')
        new_due_date = request.form.get('due_date')
        new_priority = request.form.get('priority', 'Medium')
        if new_task_title and 0 <= task_id < len(tasks):
            tasks[task_id]['title'] = new_task_title
            tasks[task_id]['due_date'] = new_due_date
            tasks[task_id]['priority'] = new_priority
        return redirect(url_for('home'))
    return render_template('edit.html', task=tasks[task_id], task_id=task_id)

@app.route('/add_subtask/<int:task_id>', methods=['POST'])
def add_subtask(task_id):
    subtask = request.form.get('subtask')
    if subtask and 0 <= task_id < len(tasks):
        tasks[task_id]['subtasks'].append({'title': subtask, 'completed': False})
    return redirect(url_for('home'))

@app.route('/toggle_complete/<int:task_id>')
def toggle_complete(task_id):
    if 0 <= task_id < len(tasks):
        tasks[task_id]['completed'] = not tasks[task_id]['completed']
    return redirect(url_for('home'))

@app.route('/toggle_subtask_complete/<int:task_id>/<int:subtask_id>')
def toggle_subtask_complete(task_id, subtask_id):
    if 0 <= task_id < len(tasks) and 0 <= subtask_id < len(tasks[task_id]['subtasks']):
        tasks[task_id]['subtasks'][subtask_id]['completed'] = not tasks[task_id]['subtasks'][subtask_id]['completed']
    return redirect(url_for('home'))

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '').lower()
    filtered_tasks = [task for task in tasks if query in task['title'].lower()]
    return render_template('index.html', tasks=filtered_tasks)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
