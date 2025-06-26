import json
from flask import Flask, request, redirect, url_for, render_template_string

app = Flask(__name__)

DATA_FILE = 'data.json'

# --- HTML Templates as Strings ---
INDEX_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SIMS Flask</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f4f7f6; color: #333; }
        .container { max-width: 800px; margin: 50px auto; padding: 30px; background-color: #fff; border-radius: 12px; box-shadow: 0 6px 20px rgba(0,0,0,0.08); }
        h1 { color: #2c3e50; text-align: center; margin-bottom: 30px; font-size: 2.5em; }
        nav { text-align: center; margin-top: 30px; }
        nav a {
            display: inline-block;
            background-color: #007bff;
            color: white;
            padding: 12px 25px;
            margin: 0 10px;
            border-radius: 8px;
            text-decoration: none;
            font-weight: bold;
            transition: background-color 0.3s ease, transform 0.2s ease;
            box-shadow: 0 4px 10px rgba(0, 123, 255, 0.2);
        }
        nav a:hover {
            background-color: #0056b3;
            transform: translateY(-3px);
        }
        p { text-align: center; margin-top: 20px; color: #555; line-height: 1.6; }
        .footer { text-align: center; margin-top: 40px; font-size: 0.9em; color: #888; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Selamat Datang di Sistem Informasi Manajemen Sekolah (SIMS)</h1>
        <nav>
            <a href="{{ url_for('students') }}">Manajemen Siswa</a>
            <!-- Anda bisa menambahkan link lain di sini, misal untuk guru, mata pelajaran, dll. -->
        </nav>
        <p>Ini adalah aplikasi SIMS dasar yang dibangun dengan Flask dan penyimpanan JSON.</p>
        <div class="footer">
            <p>&copy; 2025 SIMS App</p>
        </div>
    </div>
</body>
</html>
"""

STUDENTS_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Manajemen Siswa</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f4f7f6; color: #333; }
        .container { max-width: 900px; margin: 50px auto; padding: 30px; background-color: #fff; border-radius: 12px; box-shadow: 0 6px 20px rgba(0,0,0,0.08); }
        h1 { color: #2c3e50; text-align: center; margin-bottom: 30px; font-size: 2.2em; }
        .actions-top { text-align: center; margin-bottom: 20px; }
        .actions-top a {
            display: inline-block;
            background-color: #28a745;
            color: white;
            padding: 10px 20px;
            margin: 0 5px;
            border-radius: 8px;
            text-decoration: none;
            font-weight: bold;
            transition: background-color 0.3s ease, transform 0.2s ease;
            box-shadow: 0 4px 10px rgba(40, 167, 69, 0.2);
        }
        .actions-top a.back-link {
            background-color: #6c757d;
            box-shadow: 0 4px 10px rgba(108, 117, 125, 0.2);
        }
        .actions-top a:hover {
            background-color: #218838;
            transform: translateY(-3px);
        }
        .actions-top a.back-link:hover {
            background-color: #5a6268;
        }
        table { width: 100%; border-collapse: separate; border-spacing: 0; margin-top: 30px; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }
        th, td { border: 1px solid #e0e0e0; padding: 12px 15px; text-align: left; }
        th { background-color: #f8f9fa; color: #495057; font-weight: bold; text-transform: uppercase; font-size: 0.9em; }
        tr:nth-child(even) { background-color: #fcfcfc; }
        tr:hover { background-color: #f2f2f2; }
        .actions { white-space: nowrap; }
        .actions a {
            background-color: #007bff;
            color: white;
            padding: 6px 12px;
            border-radius: 5px;
            text-decoration: none;
            font-size: 0.85em;
            margin-right: 5px;
            transition: background-color 0.2s ease;
        }
        .actions a.delete { background-color: #dc3545; }
        .actions a:hover { background-color: #0056b3; }
        .actions a.delete:hover { background-color: #c82333; }
        .no-data { text-align: center; margin-top: 30px; color: #888; font-style: italic; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Manajemen Siswa</h1>
        <div class="actions-top">
            <a href="{{ url_for('add_student') }}">Tambah Siswa Baru</a>
            <a href="{{ url_for('index') }}" class="back-link">Kembali ke Beranda</a>
        </div>

        {% if students %}
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Nama</th>
                    <th>Usia</th>
                    <th>Kelas</th>
                    <th>Aksi</th>
                </tr>
            </thead>
            <tbody>
                {% for student in students %}
                <tr>
                    <td>{{ student.id }}</td>
                    <td>{{ student.name }}</td>
                    <td>{{ student.age }}</td>
                    <td>{{ student.grade }}</td>
                    <td class="actions">
                        <a href="{{ url_for('edit_student', student_id=student.id) }}">Edit</a>
                        <a href="{{ url_for('delete_student', student_id=student.id) }}" onclick="return confirm('Apakah Anda yakin ingin menghapus siswa ini?');" class="delete">Hapus</a>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
        {% else %}
        <p class="no-data">Belum ada data siswa.</p>
        {% endif %}
    </div>
</body>
</html>
"""

ADD_STUDENT_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tambah Siswa Baru</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f4f7f6; color: #333; }
        .container { max-width: 600px; margin: 50px auto; padding: 30px; background-color: #fff; border-radius: 12px; box-shadow: 0 6px 20px rgba(0,0,0,0.08); }
        h1 { color: #2c3e50; text-align: center; margin-bottom: 30px; font-size: 2.2em; }
        form div { margin-bottom: 15px; }
        label { display: block; margin-bottom: 8px; font-weight: bold; color: #555; }
        input[type="text"], input[type="number"] {
            width: calc(100% - 20px);
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 8px;
            font-size: 1em;
            box-sizing: border-box; /* Include padding in width */
        }
        button {
            padding: 12px 25px;
            background-color: #28a745;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1.1em;
            font-weight: bold;
            transition: background-color 0.3s ease, transform 0.2s ease;
            box-shadow: 0 4px 10px rgba(40, 167, 69, 0.2);
            display: block;
            width: 100%;
            margin-top: 20px;
        }
        button:hover {
            background-color: #218838;
            transform: translateY(-3px);
        }
        .back-link {
            display: block;
            text-align: center;
            margin-top: 20px;
            text-decoration: none;
            color: #007bff;
            font-weight: bold;
            transition: color 0.3s ease;
        }
        .back-link:hover {
            color: #0056b3;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Tambah Siswa Baru</h1>
        <form action="{{ url_for('add_student') }}" method="POST">
            <div>
                <label for="name">Nama:</label>
                <input type="text" id="name" name="name" required>
            </div>
            <div>
                <label for="age">Usia:</label>
                <input type="number" id="age" name="age" required min="1">
            </div>
            <div>
                <label for="grade">Kelas:</label>
                <input type="text" id="grade" name="grade" required>
            </div>
            <button type="submit">Tambah Siswa</button>
        </form>
        <a href="{{ url_for('students') }}" class="back-link">Kembali ke Daftar Siswa</a>
    </div>
</body>
</html>
"""

EDIT_STUDENT_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Edit Siswa</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f4f7f6; color: #333; }
        .container { max-width: 600px; margin: 50px auto; padding: 30px; background-color: #fff; border-radius: 12px; box-shadow: 0 6px 20px rgba(0,0,0,0.08); }
        h1 { color: #2c3e50; text-align: center; margin-bottom: 30px; font-size: 2.2em; }
        form div { margin-bottom: 15px; }
        label { display: block; margin-bottom: 8px; font-weight: bold; color: #555; }
        input[type="text"], input[type="number"] {
            width: calc(100% - 20px);
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 8px;
            font-size: 1em;
            box-sizing: border-box; /* Include padding in width */
        }
        button {
            padding: 12px 25px;
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1.1em;
            font-weight: bold;
            transition: background-color 0.3s ease, transform 0.2s ease;
            box-shadow: 0 4px 10px rgba(0, 123, 255, 0.2);
            display: block;
            width: 100%;
            margin-top: 20px;
        }
        button:hover {
            background-color: #0056b3;
            transform: translateY(-3px);
        }
        .back-link {
            display: block;
            text-align: center;
            margin-top: 20px;
            text-decoration: none;
            color: #007bff;
            font-weight: bold;
            transition: color 0.3s ease;
        }
        .back-link:hover {
            color: #0056b3;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Edit Siswa</h1>
        <form action="{{ url_for('edit_student', student_id=student.id) }}" method="POST">
            <div>
                <label for="name">Nama:</label>
                <input type="text" id="name" name="name" value="{{ student.name }}" required>
            </div>
            <div>
                <label for="age">Usia:</label>
                <input type="number" id="age" name="age" value="{{ student.age }}" required min="1">
            </div>
            <div>
                <label for="grade">Kelas:</label>
                <input type="text" id="grade" name="grade" value="{{ student.grade }}" required>
            </div>
            <button type="submit">Simpan Perubahan</button>
        </form>
        <a href="{{ url_for('students') }}" class="back-link">Kembali ke Daftar Siswa</a>
    </div>
</body>
</html>
"""


# --- Fungsi Bantuan untuk Membaca/Menulis JSON ---
def load_data():
    """Loads data from the JSON file."""
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Initialize with empty lists if file not found
        return {"students": [], "teachers": [], "courses": []}
    except json.JSONDecodeError:
        # Handle case where JSON file is empty or malformed
        print(f"Warning: {DATA_FILE} is empty or malformed. Initializing with empty data.")
        return {"students": [], "teachers": [], "courses": []}


def save_data(data):
    """Saves data to the JSON file."""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4) # Use indent for pretty printing


# --- Routes Aplikasi ---

@app.route('/')
def index():
    """Renders the main index page."""
    return render_template_string(INDEX_HTML)

@app.route('/students')
def students():
    """Displays a list of all students."""
    data = load_data()
    return render_template_string(STUDENTS_HTML, students=data.get('students', []))

@app.route('/students/add', methods=['GET', 'POST'])
def add_student():
    """Handles adding a new student."""
    if request.method == 'POST':
        data = load_data()
        students_list = data.get('students', [])
        
        # Simple ID generation: max existing ID + 1, or 1 if no students
        new_id = max([s['id'] for s in students_list]) + 1 if students_list else 1

        new_student = {
            'id': new_id,
            'name': request.form['name'],
            'age': int(request.form['age']),
            'grade': request.form['grade']
        }
        students_list.append(new_student)
        data['students'] = students_list
        save_data(data)
        return redirect(url_for('students'))
    return render_template_string(ADD_STUDENT_HTML)

@app.route('/students/edit/<int:student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    """Handles editing an existing student."""
    data = load_data()
    students_list = data.get('students', [])
    student_to_edit = next((s for s in students_list if s['id'] == student_id), None)

    if student_to_edit is None:
        return "Student not found", 404 # Return 404 if student doesn't exist

    if request.method == 'POST':
        student_to_edit['name'] = request.form['name']
        student_to_edit['age'] = int(request.form['age'])
        student_to_edit['grade'] = request.form['grade']
        save_data(data)
        return redirect(url_for('students'))
    
    # For GET request, render the form with existing student data
    return render_template_string(EDIT_STUDENT_HTML, student=student_to_edit)


@app.route('/students/delete/<int:student_id>')
def delete_student(student_id):
    """Handles deleting a student."""
    data = load_data()
    # Filter out the student with the given ID
    initial_student_count = len(data.get('students', []))
    data['students'] = [s for s in data.get('students', []) if s['id'] != student_id]
    
    if len(data['students']) < initial_student_count: # Check if a student was actually removed
        save_data(data)
    else:
        print(f"Warning: Student with ID {student_id} not found for deletion.")
    
    return redirect(url_for('students'))

if __name__ == '__main__':
    # Run the Flask application in debug mode
    app.run(debug=True)
