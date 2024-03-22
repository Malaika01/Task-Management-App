from flask import Flask, render_template,request,redirect,url_for
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    # conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/add')
def render_add_html():
    return render_template('add.html')

# @app.route('/edit')
# def render_add_html():
#     return render_template('edit.html')

@app.route('/add_task', methods=['POST'])
def add_task():
    if request.method == 'POST':
        task_id = request.form['Id']
        task_title = request.form['Title']
        task_desc = request.form['Desc']
        task_date = request.form['Date']
        task_priority = request.form['Priority']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO tasks (Id, Title, Desc, Date, Priority) VALUES (?, ?, ?, ?, ?)',
                       (task_id, task_title, task_desc, task_date, task_priority))
        print("data added")
        conn.commit()
        conn.close()

        return redirect(url_for('index'))


@app.route('/view_tasks')
def view_tasks():
    # Fetch tasks from the database
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()
    conn.close()

    return render_template('view.html', tasks=tasks)


@app.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    if request.method == 'POST':
        # Update task in the database
        task_title = request.form['Title']
        task_desc = request.form['Desc']
        task_date = request.form['Date']
        task_priority = request.form['Priority']
        cursor.execute('UPDATE tasks SET Title=?, Desc=?, Date=?, Priority=? WHERE Id=?',
                       (task_title, task_desc, task_date, task_priority, task_id))
        conn.commit()
        conn.close()
        return redirect(url_for('view_tasks'))
    else:
        cursor.execute('SELECT * FROM tasks WHERE Id = ?', (task_id,))
        task = cursor.fetchone()
        conn.close()
        if task:
            return render_template('edit_task.html', task=task)
        else:
            return 'Task not found', 404


if __name__ == '__main__':
    app.run(debug=True)
