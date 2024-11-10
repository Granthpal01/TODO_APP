from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

tasks = []

@app.route('/')
def home():
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    task = request.form.get('task')
    priority = request.form.get('priority')
    due_date = request.form.get('due_date')
    if task:
        tasks.append({
            'task': task,
            'priority': priority,
            'due_date': due_date,
            'status': 'Incomplete'
        })
    return redirect(url_for('home'))

@app.route('/delete/<int:task_id>')
def delete(task_id):
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
    return redirect(url_for('home'))

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit(task_id):
    if request.method == 'POST':
        new_task = request.form.get('task')
        priority = request.form.get('priority')
        due_date = request.form.get('due_date')
        status = request.form.get('status')
        if new_task and 0 <= task_id < len(tasks):
            tasks[task_id] = {
                'task': new_task,
                'priority': priority,
                'due_date': due_date,
                'status': status
            }
        return redirect(url_for('home'))
    return render_template('edit.html', task=tasks[task_id], task_id=task_id)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
