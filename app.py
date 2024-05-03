from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Define a hardcoded username and password for employees and managers
EMPLOYEE_USERNAME = "employee1"
EMPLOYEE_PASSWORD = "employee"
MANAGER_USERNAME = "manager1"
MANAGER_PASSWORD = "manager"

tasks = []

employees = ["employee1","employee2"]

failed_login_count = 0  # Initialize the failed login counter

@app.route('/', methods=['GET', 'POST'])
def login():
    global failed_login_count  # Access the global failed login counter
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == EMPLOYEE_USERNAME and password == EMPLOYEE_PASSWORD:
            failed_login_count = 0  # Reset failed login counter on successful login
            return redirect(url_for('employee_home', username=username))
        elif username == MANAGER_USERNAME and password == MANAGER_PASSWORD:
            failed_login_count = 0  # Reset failed login counter on successful login
            return redirect(url_for('manager_home', username=username))
        else:
            failed_login_count += 1  # Increment failed login counter
            if failed_login_count >= 3:
                return redirect(url_for('failed_login'))
            else:
                error = 'Invalid Credentials. Please try again.'
    return render_template('login.html', error=error)

@app.route('/failed_login')
def failed_login():
    return render_template('failed_login.html')


@app.route('/employee_home/<username>')
def employee_home(username):
    return render_template('employee_home.html', username=username)

@app.route('/manager_home/<username>')
def manager_home(username):
    return render_template('manager_home.html', username=username)

@app.route('/schedule')
def schedule():
    # Dummy schedule data, replace with actual data from database
    schedule_data = [
        {'date': '2024-04-15', 'time': '9:00 AM - 5:00 PM', 'task': 'Shift 1'},
        {'date': '2024-04-16', 'time': '10:00 AM - 6:00 PM', 'task': 'Shift 2'},
        # Add more schedule data as needed
    ]
    return render_template('schedule.html', schedule_data=schedule_data)

@app.route('/tasks_page')
def tasks_page():
    return render_template('tasks_page.html', tasks=tasks)
    # return render_template('tasks_page.html', task_data=task_data)

@app.route('/complete_task', methods=['POST'])
def complete_task():
    task_to_complete = request.form['task']
    tasks.remove(task_to_complete)
    return render_template('tasks_page.html', tasks=tasks)


@app.route('/schedule_management', methods=['GET', 'POST'])
def schedule_management():
    if request.method == 'POST':
        # Assuming the form has fields 'date', 'time_slot', and 'employee'
        employees = ["employee1", "employee2",]  # Replace with your list of employees
        return render_template('schedule_management.html', employees=employees)
        date = request.form.get('date')
        time_slot = request.form.get('time_slot')



        # Perform any necessary processing or validation here

        # Pass the data to the schedule.html template
        return render_template('schedule.html', date=date, time_slot=time_slot, employee=employee)
    else:
        # Render the schedule management form
        return render_template('schedule_management.html')

@app.route('/update_schedule', methods=['POST'])
def update_schedule():
    employee = request.form['employee']
    hours = request.form['hours']
    # Here, you can process the submitted data, such as updating the schedule
    # For demonstration purposes, let's print the data
    print(f"Employee: {employee}, Hours: {hours}")
    return "Schedule updated successfully"

@app.route('/task_management', methods=['GET', 'POST'])
def task_management():
    message = None
    if request.method == 'POST':
        description = request.form['description']
        tasks.append(description)
        message = "Task submitted"
    return render_template('task_management.html', message=message)

if __name__ == '__main__':
    app.run(debug=True)
