from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

tasks = []

@app.route('/')
def home():
    current_date = datetime.now().date()
    return render_template('index.html', tasks=tasks, current_date=current_date)

@app.route('/add', methods=['POST'])
def add():
    task_name = request.form.get('task')
    priority = request.form.get('priority')
    due_date_str = request.form.get('due_date')

    if task_name:
        task = {
            'name': task_name,
            'priority': priority,
            'due_date': datetime.strptime(due_date_str, '%Y-%m-%d').date() if due_date_str else None,
            'completed': False
        }
        tasks.append(task)

    return redirect(url_for('home'))

@app.route('/delete/<int:task_id>')
def delete(task_id):
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
    return redirect(url_for('home'))

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit(task_id):
    if request.method == 'POST':
        new_task_name = request.form.get('task')
        new_priority = request.form.get('priority')
        new_due_date_str = request.form.get('due_date')

        if new_task_name and 0 <= task_id < len(tasks):
            tasks[task_id]['name'] = new_task_name
            tasks[task_id]['priority'] = new_priority
            tasks[task_id]['due_date'] = datetime.strptime(new_due_date_str, '%Y-%m-%d').date() if new_due_date_str else None

        return redirect(url_for('home'))
    
    return render_template('edit.html', task=tasks[task_id], task_id=task_id)

@app.route('/complete/<int:task_id>')
def complete(task_id):
    if 0 <= task_id < len(tasks):
        tasks[task_id]['completed'] = True
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
