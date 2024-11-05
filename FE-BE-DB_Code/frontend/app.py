from flask import Flask, request, jsonify, render_template_string
import requests

app = Flask(__name__)

# HTML template for the student form and list view
form_template = """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Student Attendance System</title>
    <style>
      /* Basic Reset */
      * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
      }

      body {
        font-family: Arial, sans-serif;
        background-color: #f4f4f9;
        color: #333;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
      }

      /* Container */
      .container {
        background: #ffffff;
        width: 80%;
        max-width: 500px;
        padding: 20px;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
        border-radius: 8px;
        text-align: center;
      }

      /* Header */
      h1 {
        color: #4a90e2;
        font-size: 1.8em;
        margin-bottom: 10px;
      }

      h2 {
        color: #333;
        font-size: 1.4em;
        margin: 20px 0 10px;
      }

      /* Form */
      form {
        display: flex;
        flex-direction: column;
        align-items: center;
      }

      label {
        font-weight: bold;
        margin-bottom: 5px;
        color: #555;
      }

      input[type="text"], input[type="number"] {
        width: 90%;
        padding: 10px;
        margin: 10px 0;
        border: 1px solid #ddd;
        border-radius: 5px;
      }

      input[type="submit"] {
        width: 100%;
        padding: 10px;
        background-color: #4a90e2;
        color: white;
        font-size: 1em;
        font-weight: bold;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        transition: background-color 0.3s;
      }

      input[type="submit"]:hover {
        background-color: #357abd;
      }

      /* View Students Link */
      .view-link {
        margin-top: 20px;
        font-size: 1em;
      }

      .view-link a {
        text-decoration: none;
        color: #4a90e2;
        font-weight: bold;
        transition: color 0.3s;
      }

      .view-link a:hover {
        color: #357abd;
      }
    </style>
  </head>
  <body>
    <div class="container">
      <h1>Welcome to the Student Attendance System</h1>

      <!-- Form to add student -->
      <h2>Add Student</h2>
      <form action="/submit_student" method="post">
        <label for="name">Name:</label>
        <input type="text" id="name" name="name" required>

        <label for="age">Age:</label>
        <input type="number" id="age" name="age" required>

        <input type="submit" value="Add Student">
      </form>
      
      <!-- Link to view students -->
      <div class="view-link">
        <h2><a href="/view_students">View All Students</a></h2>
      </div>
    </div>
  </body>
</html>

"""

@app.route('/')
def home():
    return render_template_string(form_template)

@app.route('/submit_student', methods=['POST'])
def submit_student():
    # Collect data from the form
    name = request.form.get('name')
    age = request.form.get('age')
    data = {'name': name, 'age': age}

    # Send data to the backend service
    response = requests.post('http://backend:5001/store_student', json=data)
    
    # Return response to user
    if response.status_code == 200:
        return "Student added successfully! <a href='/'>Go Back</a>"
    else:
        return "Error adding student."

@app.route('/view_students')
def view_students():
    # Request the list of students from the backend
    response = requests.get('http://backend:5001/get_students')
    students = response.json() if response.status_code == 200 else []

    # HTML template to display students
    student_list_html = """
    <h1>Student List</h1>
    <ul>
    {% for student in students %}
      <li>{{ student['name'] }} - Age: {{ student['age'] }} - Date: {{ student['date'] }}</li>
    {% endfor %}
    </ul>
    <a href="/">Go Back</a>
    """
    return render_template_string(student_list_html, students=students)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
