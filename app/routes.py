# #routes.py 
# from flask import render_template, request, redirect, url_for, session
# from app import app
# from app.models import get_patient_by_email

# @app.route('/')
# def home():
#     return redirect(url_for('login'))

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     msg = ''
#     if request.method == 'POST':
#         email = request.form['email']
#         patient = get_patient_by_email(email)
#         if patient:
#             session['patient_id'] = patient[0]  # Assuming id is the first column
#             session['patient_name'] = patient[1]
#             return redirect(url_for('dashboard'))
#         else:
#             msg = 'No patient found with this email.'
#     return render_template('login.html', msg=msg)

# @app.route('/dashboard')
# def dashboard():
#     if 'patient_id' not in session:
#         return redirect(url_for('login'))
#     return render_template('dashboard.html', patient_name=session['patient_name'])

# @app.route('/logout')
# def logout():
#     session.clear()
#     return redirect(url_for('login'))



# from flask import Flask, render_template, request, redirect, url_for, session, jsonify
# import requests
# from app import app
# from app.models import get_patient_by_email

# @app.route('/send_message', methods=['POST'])
# def send_message():
#     if 'patient_id' not in session:
#         return jsonify([{"text": "Please log in first."}])
    
#     data = request.get_json()
#     patient_id = session['patient_id']
#     message = data.get('message')

#     # Send message to Rasa REST API
#     url = "http://localhost:5005/webhooks/rest/webhook"
#     payload = {"sender": str(patient_id), "message": message}
#     response = requests.post(url, json=payload)
#     return jsonify(response.json())




















# ========================================================================================================================================



# routes.py


# from flask import render_template, request, redirect, url_for, session, jsonify
# from app import app, mysql
# from app.models import get_patient_by_email
# import MySQLdb.cursors

# # -------------------
# # Authentication Routes
# # -------------------
# @app.route('/')
# def home():
#     return redirect(url_for('login'))

# # @app.route('/login', methods=['GET', 'POST'])
# # def login():
# #     msg = ''
# #     if request.method == 'POST':
# #         email = request.form['email']
# #         patient = get_patient_by_email(email)
# #         if patient:
# #             session['patient_id'] = patient[0]  # id
# #             session['patient_name'] = patient[1]  # name
# #             return redirect(url_for('dashboard'))
# #         else:
# #             msg = 'No patient found with this email.'
# #     return render_template('login.html', msg=msg)
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     msg = ''
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']   # get password from form
#         patient = get_patient_by_email(email)

#         if patient and patient[6] == password:  # assuming password column index is 6
#             session['patient_id'] = patient[0]   # id
#             session['patient_name'] = patient[1] # name
#             return redirect(url_for('dashboard'))
#         else:
#             msg = 'Invalid email or password.'
#     return render_template('login.html', msg=msg)



# @app.route('/dashboard')
# def dashboard():
#     if 'patient_id' not in session:
#         return redirect(url_for('login'))
#     return render_template('dashboard.html', patient_name=session['patient_name'])

# @app.route('/logout')
# def logout():
#     session.clear()
#     return redirect(url_for('login'))

# # -------------------
# # Chatbot Route (Rasa)
# # -------------------
# import requests

# @app.route('/send_message', methods=['POST'])
# def send_message():
#     if 'patient_id' not in session:
#         return jsonify([{"text": "Please log in first."}])
    
#     data = request.get_json()
#     patient_id = session['patient_id']
#     message = data.get('message')

#     # Send to Rasa REST channel
#     url = "http://localhost:5005/webhooks/rest/webhook"
#     payload = {"sender": str(patient_id), "message": message}
#     response = requests.post(url, json=payload)
#     return jsonify(response.json())

# # -------------------
# # Appointment Booking APIs
# # -------------------

# @app.route('/therapies')
# def get_therapies():
#     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#     cursor.execute("SELECT id, name FROM therapies")
#     rows = cursor.fetchall()
#     cursor.close()
#     return jsonify(rows)

# @app.route('/doctors/<int:therapy_id>')
# def get_doctors(therapy_id):
#     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#     cursor.execute("""
#         SELECT d.id, d.name, d.specialization
#         FROM doctors d
#         JOIN doctor_therapies dt ON d.id = dt.doctor_id
#         WHERE dt.therapy_id = %s
#     """, (therapy_id,))
#     rows = cursor.fetchall()
#     cursor.close()
#     return jsonify(rows)

# @app.route('/slots/<int:doctor_id>/<date>')
# def get_slots(doctor_id, date):
#     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#     query = """
#         SELECT s.id, s.time_label
#         FROM slots s
#         WHERE s.doctor_id = %s
#           AND s.day_of_week = LEFT(DAYNAME(%s), 3)
#           AND s.id NOT IN (
#               SELECT a.slot_id
#               FROM appointments a
#               WHERE a.doctor_id = %s
#                 AND a.date = %s
#                 AND a.status = 'Scheduled'
#           )
#     """
#     cursor.execute(query, (doctor_id, date, doctor_id, date))
#     rows = cursor.fetchall()
#     cursor.close()
#     return jsonify(rows)

# @app.route('/book', methods=['POST'])
# def book():
#     data = request.get_json()
#     patient_id = session.get('patient_id')  # always take from session
#     doctor_id = data.get('doctor_id')
#     therapy_id = data.get('therapy_id')
#     slot_id = data.get('slot_id')
#     date = data.get('date')

#     if not patient_id or not doctor_id or not therapy_id or not slot_id or not date:
#         return jsonify({"message": "Missing required fields."}), 400

#     cursor = mysql.connection.cursor()

#     # Check if slot is already booked
#     cursor.execute("""
#         SELECT id FROM appointments
#         WHERE doctor_id = %s AND slot_id = %s AND date = %s AND status = 'Scheduled'
#     """, (doctor_id, slot_id, date))
#     conflict = cursor.fetchone()

#     if conflict:
#         cursor.close()
#         return jsonify({"message": "This slot is already booked."}), 400

#     # Insert appointment
#     cursor.execute("""
#         INSERT INTO appointments (patient_id, doctor_id, therapy_id, slot_id, date, status)
#         VALUES (%s, %s, %s, %s, %s, 'Scheduled')
#     """, (patient_id, doctor_id, therapy_id, slot_id, date))
#     mysql.connection.commit()
#     cursor.close()

#     return jsonify({"message": "Appointment booked successfully!"})



































# 


# routes.py

# from flask import render_template, request, redirect, url_for, session, jsonify
# from app import app, mysql
# import MySQLdb.cursors
# import requests

# # -------------------
# # Database helper (moved from models.py)
# # -------------------
# def get_patient_by_email(email):
#     cursor = mysql.connection.cursor()
#     cursor.execute("SELECT * FROM patients WHERE email=%s", (email,))
#     patient = cursor.fetchone()
#     cursor.close()
#     return patient

# # -------------------
# # Authentication Routes
# # -------------------
# @app.route('/')
# def home():
#     return redirect(url_for('login'))

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     msg = ''
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']   # get password from form
#         patient = get_patient_by_email(email)

#         if patient and patient[6] == password:  # assuming password column index is 6
#             session['patient_id'] = patient[0]   # id
#             session['patient_name'] = patient[1] # name
#             return redirect(url_for('dashboard'))
#         else:
#             msg = 'Invalid email or password.'
#     return render_template('login.html', msg=msg)

# @app.route('/dashboard')
# def dashboard():
#     if 'patient_id' not in session:
#         return redirect(url_for('login'))
#     return render_template('dashboard.html', patient_name=session['patient_name'])

# @app.route('/logout')
# def logout():
#     session.clear()
#     return redirect(url_for('login'))

# # -------------------
# # Chatbot Route (Rasa)
# # -------------------
# @app.route('/send_message', methods=['POST'])
# def send_message():
#     if 'patient_id' not in session:
#         return jsonify([{"text": "Please log in first."}])
    
#     data = request.get_json()
#     patient_id = session['patient_id']
#     message = data.get('message')

#     # Send to Rasa REST channel
#     url = "http://localhost:5005/webhooks/rest/webhook"
#     payload = {"sender": str(patient_id), "message": message}
#     response = requests.post(url, json=payload)
#     return jsonify(response.json())

# # -------------------
# # Appointment Booking APIs
# # -------------------
# @app.route('/therapies')
# def get_therapies():
#     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#     cursor.execute("SELECT id, name FROM therapies")
#     rows = cursor.fetchall()
#     cursor.close()
#     return jsonify(rows)

# @app.route('/doctors/<int:therapy_id>')
# def get_doctors(therapy_id):
#     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#     cursor.execute("""
#         SELECT d.id, d.name, d.specialization
#         FROM doctors d
#         JOIN doctor_therapies dt ON d.id = dt.doctor_id
#         WHERE dt.therapy_id = %s
#     """, (therapy_id,))
#     rows = cursor.fetchall()
#     cursor.close()
#     return jsonify(rows)

# @app.route('/slots/<int:doctor_id>/<date>')
# def get_slots(doctor_id, date):
#     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#     query = """
#         SELECT s.id, s.time_label
#         FROM slots s
#         WHERE s.doctor_id = %s
#           AND s.day_of_week = LEFT(DAYNAME(%s), 3)
#           AND s.id NOT IN (
#               SELECT a.slot_id
#               FROM appointments a
#               WHERE a.doctor_id = %s
#                 AND a.date = %s
#                 AND a.status = 'Scheduled'
#           )
#     """
#     cursor.execute(query, (doctor_id, date, doctor_id, date))
#     rows = cursor.fetchall()
#     cursor.close()
#     return jsonify(rows)

# @app.route('/book', methods=['POST'])
# def book():
#     data = request.get_json()
#     patient_id = session.get('patient_id')  # always take from session
#     doctor_id = data.get('doctor_id')
#     therapy_id = data.get('therapy_id')
#     slot_id = data.get('slot_id')
#     date = data.get('date')

#     if not patient_id or not doctor_id or not therapy_id or not slot_id or not date:
#         return jsonify({"message": "Missing required fields."}), 400

#     cursor = mysql.connection.cursor()

#     # Check if slot is already booked
#     cursor.execute("""
#         SELECT id FROM appointments
#         WHERE doctor_id = %s AND slot_id = %s AND date = %s AND status = 'Scheduled'
#     """, (doctor_id, slot_id, date))
#     conflict = cursor.fetchone()

#     if conflict:
#         cursor.close()
#         return jsonify({"message": "This slot is already booked."}), 400

#     # Insert appointment
#     cursor.execute("""
#         INSERT INTO appointments (patient_id, doctor_id, therapy_id, slot_id, date, status)
#         VALUES (%s, %s, %s, %s, %s, 'Scheduled')
#     """, (patient_id, doctor_id, therapy_id, slot_id, date))
#     mysql.connection.commit()
#     cursor.close()

#     return jsonify({"message": "Appointment booked successfully!"})



























# # routes.py

# from flask import render_template, request, redirect, url_for, session, jsonify
# from app import app, mysql
# import MySQLdb.cursors
# import requests

# def get_patient_by_email(email):
#     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#     cursor.execute("SELECT * FROM patients WHERE email=%s", (email,))
#     patient = cursor.fetchone()
#     cursor.close()
#     return patient


# # Helper for doctors with password
# def get_doctor_by_email(email):
#     cursor = mysql.connection.cursor()
#     # Explicitly select id, name, email, password (and any other needed columns)
#     cursor.execute("SELECT id, name, email, password FROM doctors WHERE email=%s", (email,))
#     doctor = cursor.fetchone()
#     cursor.close()
#     return doctor

# # -------------------
# # Authentication Routes
# # -------------------
# @app.route('/')
# def home():
#     return render_template('index.html')  # serve main page



# # -------------------
# # Patient Login
# # -------------------
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     msg = ''
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']
#         patient = get_patient_by_email(email)

#         if patient and patient['password'] == password:
#          session['patient_id'] = patient['id']
#          session['patient_name'] = patient['name']
#          return redirect(url_for('patient_portal'))
#         else:
#             msg = 'Invalid email or password.'
#     return render_template('login.html', msg=msg)


# # -------------------
# # Doctor Login
# # -------------------
# @app.route('/doctorLogin', methods=['GET', 'POST'])
# def doctor_login():
#     msg = ''
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']
#         doctor = get_doctor_by_email(email)

#         if doctor and doctor['password'] == password:
#            session['doctor_id'] = doctor['id']
#            session['doctor_name'] = doctor['name']
#            return redirect(url_for('doctor_dashboard'))

#         else:
#             msg = 'Invalid email or password.'
#     return render_template('doctorLogin.html', msg=msg)


# @app.route('/dashboard')
# def dashboard():
#     if 'patient_id' not in session:
#         return redirect(url_for('login'))
#     return render_template('dashboard.html', patient_name=session['patient_name'])

# @app.route('/logout')
# def logout():
#     session.clear()
#     return redirect(url_for('login'))


# @app.route('/patientPortal')
# def patient_portal():
#     if 'patient_id' not in session:
#         return redirect(url_for('login'))

#     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#     cursor.execute("""
#         SELECT 
#             a.id AS appointment_id,
#             a.date,
#             a.status,
#             d.name AS doctor_name,
#             t.name AS therapy_name,
#             s.time_label
#         FROM appointments a
#         JOIN doctors d ON a.doctor_id = d.id
#         JOIN therapies t ON a.therapy_id = t.id
#         JOIN slots s ON a.slot_id = s.id
#         WHERE a.patient_id = %s
#           AND a.status = 'Scheduled'
#         ORDER BY a.date ASC
#     """, (session['patient_id'],))
#     appointments = cursor.fetchall()
#     cursor.close()

#     return render_template(
#         'patientPortal.html',
#         patient_name=session['patient_name'],
#         appointments=appointments
#     )




# @app.route('/signUp')
# def sign_up():
#     return render_template('signUp.html')

# @app.route('/facts')
# def facts():
#     return render_template('facts.html')

# @app.route('/bookAppointment')
# def book_appointment():
#     return render_template('bookAppointment.html')


# # -------------------
# # Chatbot Route (Rasa)
# # -------------------
# @app.route('/send_message', methods=['POST'])
# def send_message():
#     if 'patient_id' not in session:
#         return jsonify([{"text": "Please log in first."}])
    
#     data = request.get_json()
#     patient_id = session['patient_id']
#     message = data.get('message')

#     # Send to Rasa REST channel
#     url = "http://localhost:5005/webhooks/rest/webhook"
#     payload = {"sender": str(patient_id), "message": message}
#     response = requests.post(url, json=payload)
#     return jsonify(response.json())

# # -------------------
# # Appointment Booking APIs
# # -------------------
# @app.route('/therapies')
# def get_therapies():
#     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#     cursor.execute("SELECT id, name FROM therapies")
#     rows = cursor.fetchall()
#     cursor.close()
#     return jsonify(rows)

# @app.route('/doctors/<int:therapy_id>')
# def get_doctors(therapy_id):
#     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#     cursor.execute("""
#         SELECT d.id, d.name, d.specialization
#         FROM doctors d
#         JOIN doctor_therapies dt ON d.id = dt.doctor_id
#         WHERE dt.therapy_id = %s
#     """, (therapy_id,))
#     rows = cursor.fetchall()
#     cursor.close()
#     return jsonify(rows)

# @app.route('/slots/<int:doctor_id>/<date>')
# def get_slots(doctor_id, date):
#     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#     query = """
#         SELECT s.id, s.time_label
#         FROM slots s
#         WHERE s.doctor_id = %s
#           AND s.day_of_week = LEFT(DAYNAME(%s), 3)
#           AND s.id NOT IN (
#               SELECT a.slot_id
#               FROM appointments a
#               WHERE a.doctor_id = %s
#                 AND a.date = %s
#                 AND a.status = 'Scheduled'
#           )
#     """
#     cursor.execute(query, (doctor_id, date, doctor_id, date))
#     rows = cursor.fetchall()
#     cursor.close()
#     return jsonify(rows)



# @app.route('/book', methods=['POST'])
# def book():
#     data = request.get_json()
#     patient_id = session.get('patient_id')
#     doctor_id = data.get('doctor_id')
#     therapy_id = data.get('therapy_id')
#     slot_id = data.get('slot_id')
#     date = data.get('date')

#     if not patient_id or not doctor_id or not therapy_id or not slot_id or not date:
#         return jsonify({"message": "Missing required fields."}), 400

#     cursor = mysql.connection.cursor()

#     # Check for conflicts
#     cursor.execute("""
#         SELECT id FROM appointments
#         WHERE doctor_id = %s AND slot_id = %s AND date = %s AND status = 'Scheduled'
#     """, (doctor_id, slot_id, date))
#     conflict = cursor.fetchone()
#     if conflict:
#         cursor.close()
#         return jsonify({"message": "This slot is already booked."}), 400

#     # Insert appointment
#     cursor.execute("""
#         INSERT INTO appointments (patient_id, doctor_id, therapy_id, slot_id, date, status)
#         VALUES (%s, %s, %s, %s, %s, 'Scheduled')
#     """, (patient_id, doctor_id, therapy_id, slot_id, date))
#     mysql.connection.commit()
#     appointment_id = cursor.lastrowid

#     # Get doctor, therapy, slot details
#     cursor.execute("SELECT name FROM doctors WHERE id=%s", (doctor_id,))
#     doctor_name = cursor.fetchone()[0]

#     cursor.execute("SELECT name FROM therapies WHERE id=%s", (therapy_id,))
#     therapy_name = cursor.fetchone()[0]

#     cursor.execute("SELECT time_label FROM slots WHERE id=%s", (slot_id,))
#     time_label = cursor.fetchone()[0]

#     # Insert notification
#     message = f"Appointment booked: {therapy_name} with Dr. {doctor_name} on {date} at {time_label}."
#     cursor.execute("""
#         INSERT INTO notifications (patient_id, appointment_id, type, message, channel)
#         VALUES (%s, %s, %s, %s, %s)
#     """, (patient_id, appointment_id, 'Pre-Procedure', message, 'InApp'))
#     mysql.connection.commit()
#     cursor.close()

#     return jsonify({"message": "Appointment booked successfully!"})



# @app.route('/cancel/<int:appointment_id>', methods=['POST'])
# def cancel_appointment(appointment_id):
#     if 'patient_id' not in session:
#         return redirect(url_for('login'))

#     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

#     # Get appointment details first
#     cursor.execute("""
#         SELECT a.date, a.therapy_id, a.doctor_id, s.time_label
#         FROM appointments a
#         JOIN slots s ON a.slot_id = s.id
#         WHERE a.id=%s AND a.patient_id=%s
#     """, (appointment_id, session['patient_id']))
#     appt = cursor.fetchone()
#     if not appt:
#         cursor.close()
#         return redirect(url_for('patient_portal'))

#     # Get doctor & therapy names
#     cursor.execute("SELECT name FROM doctors WHERE id=%s", (appt['doctor_id'],))
#     doctor_name = cursor.fetchone()['name']

#     cursor.execute("SELECT name FROM therapies WHERE id=%s", (appt['therapy_id'],))
#     therapy_name = cursor.fetchone()['name']

#     # Cancel appointment
#     cursor.execute("""
#         UPDATE appointments
#         SET status='Cancelled'
#         WHERE id=%s AND patient_id=%s
#     """, (appointment_id, session['patient_id']))
#     mysql.connection.commit()

#     # Insert notification
#     message = f"Appointment cancelled: {therapy_name} with Dr. {doctor_name} on {appt['date']} at {appt['time_label']}."
#     cursor.execute("""
#         INSERT INTO notifications (patient_id, appointment_id, type, message, channel)
#         VALUES (%s, %s, %s, %s, %s)
#     """, (session['patient_id'], appointment_id, 'Pre-Procedure', message, 'InApp'))
#     mysql.connection.commit()
#     cursor.close()

#     return redirect(url_for('patient_portal'))


# @app.route('/edit/<int:appointment_id>')
# def edit_appointment(appointment_id):
#     if 'patient_id' not in session:
#         return redirect(url_for('login'))
    
#     # You can fetch details of the appointment here
#     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#     cursor.execute("""
#         SELECT a.id, a.date, a.slot_id, a.therapy_id, a.doctor_id
#         FROM appointments a
#         WHERE a.id = %s AND a.patient_id = %s
#     """, (appointment_id, session['patient_id']))
#     appointment = cursor.fetchone()
#     cursor.close()

#     if not appointment:
#         return redirect(url_for('patient_portal'))

#     # For now, just render a page with appointment info
#     return render_template("editAppointment.html", appointment=appointment)









# @app.route('/notifications/<int:patient_id>')
# def notifications(patient_id):
#     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#     cursor.execute("""
#         SELECT id, appointment_id, type, message, channel, sent_at
#         FROM notifications
#         WHERE patient_id = %s
#         ORDER BY sent_at DESC, id DESC
#     """, (patient_id,))
#     notifications = cursor.fetchall()
#     cursor.close()
#     return render_template('notifications.html', notifications=notifications)





# @app.route('/notifications/count/<int:patient_id>')
# def notifications_count(patient_id):
#     cursor = mysql.connection.cursor()
#     cursor.execute("""
#         SELECT COUNT(*) FROM notifications
#         WHERE patient_id = %s AND is_read = 0
#     """, (patient_id,))
#     count = cursor.fetchone()[0]
#     cursor.close()
#     return jsonify({"count": count})




# @app.route('/notifications/mark_read/<int:patient_id>', methods=['POST'])
# def mark_notifications_read(patient_id):
#     cursor = mysql.connection.cursor()
#     cursor.execute("""
#         UPDATE notifications
#         SET is_read = 1
#         WHERE patient_id = %s
#     """, (patient_id,))
#     mysql.connection.commit()
#     cursor.close()
#     return '', 204












# ------------------------------------------------------------------------














# routes.py

from flask import render_template, request, redirect, url_for, session, jsonify
from app import app, mysql
import MySQLdb.cursors
import requests






def get_patient_by_email(email):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM patients WHERE email=%s", (email,))
    patient = cursor.fetchone()
    cursor.close()
    return patient


# Helper for doctors with password
def get_doctor_by_email(email):
    cursor = mysql.connection.cursor()
    # Explicitly select id, name, email, password (and any other needed columns)
    cursor.execute("SELECT id, name, email, password FROM doctors WHERE email=%s", (email,))
    doctor = cursor.fetchone()
    cursor.close()
    return doctor

# -------------------
# Authentication Routes
# -------------------
@app.route('/')
def home():
    return render_template('index.html')  # serve main page



# -------------------
# Patient Login
# -------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        patient = get_patient_by_email(email)

        if patient and patient['password'] == password:
         session['patient_id'] = patient['id']
         session['patient_name'] = patient['name']
         return redirect(url_for('patient_portal'))
        else:
            msg = 'Invalid email or password.'
    return render_template('login.html', msg=msg)


# -------------------
# Doctor Login
# -------------------
@app.route('/doctorLogin', methods=['GET', 'POST'])
def doctor_login():
    msg = ''
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        doctor = get_doctor_by_email(email)

        if doctor and doctor['password'] == password:
           session['doctor_id'] = doctor['id']
           session['doctor_name'] = doctor['name']
           return redirect(url_for('doctor_dashboard'))

        else:
            msg = 'Invalid email or password.'
    return render_template('doctorLogin.html', msg=msg)


@app.route('/dashboard')
def dashboard():
    if 'patient_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', patient_name=session['patient_name'])

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/patientPortal')
def patient_portal():
    if 'patient_id' not in session:
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("""
        SELECT 
            a.id AS appointment_id,
            a.date,
            a.status,
            d.name AS doctor_name,
            t.name AS therapy_name,
            s.time_label
        FROM appointments a
        JOIN doctors d ON a.doctor_id = d.id
        JOIN therapies t ON a.therapy_id = t.id
        JOIN slots s ON a.slot_id = s.id
        WHERE a.patient_id = %s
          AND a.status = 'Scheduled'
        ORDER BY a.date ASC
    """, (session['patient_id'],))
    appointments = cursor.fetchall()
    cursor.close()

    return render_template(
        'patientPortal.html',
        patient_name=session['patient_name'],
        appointments=appointments
    )




@app.route('/signUp')
def sign_up():
    return render_template('signUp.html')

@app.route('/facts')
def facts():
    return render_template('facts.html')

@app.route('/bookAppointment')
def book_appointment():
    return render_template('bookAppointment.html')


# -------------------
# Chatbot Route (Rasa)
# -------------------
@app.route('/send_message', methods=['POST'])
def send_message():
    if 'patient_id' not in session:
        return jsonify([{"text": "Please log in first."}])
    
    data = request.get_json()
    patient_id = session['patient_id']
    message = data.get('message')

    # Send to Rasa REST channel
    url = "http://localhost:5005/webhooks/rest/webhook"
    payload = {"sender": str(patient_id), "message": message}
    response = requests.post(url, json=payload)
    return jsonify(response.json())

# -------------------
# Appointment Booking APIs
# -------------------
@app.route('/therapies')
def get_therapies():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT id, name FROM therapies")
    rows = cursor.fetchall()
    cursor.close()
    return jsonify(rows)

@app.route('/doctors/<int:therapy_id>')
def get_doctors(therapy_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("""
        SELECT d.id, d.name, d.specialization
        FROM doctors d
        JOIN doctor_therapies dt ON d.id = dt.doctor_id
        WHERE dt.therapy_id = %s
    """, (therapy_id,))
    rows = cursor.fetchall()
    cursor.close()
    return jsonify(rows)

@app.route('/slots/<int:doctor_id>/<date>')
def get_slots(doctor_id, date):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    query = """
        SELECT s.id, s.time_label
        FROM slots s
        WHERE s.doctor_id = %s
          AND s.day_of_week = LEFT(DAYNAME(%s), 3)
          AND s.id NOT IN (
              SELECT a.slot_id
              FROM appointments a
              WHERE a.doctor_id = %s
                AND a.date = %s
                AND a.status = 'Scheduled'
          )
    """
    cursor.execute(query, (doctor_id, date, doctor_id, date))
    rows = cursor.fetchall()
    cursor.close()
    return jsonify(rows)



@app.route('/book', methods=['POST'])
def book():
    data = request.get_json()
    patient_id = session.get('patient_id')
    doctor_id = data.get('doctor_id')
    therapy_id = data.get('therapy_id')
    slot_id = data.get('slot_id')
    date = data.get('date')

    if not patient_id or not doctor_id or not therapy_id or not slot_id or not date:
        return jsonify({"message": "Missing required fields."}), 400

    cursor = mysql.connection.cursor()

    # Check for conflicts
    cursor.execute("""
        SELECT id FROM appointments
        WHERE doctor_id = %s AND slot_id = %s AND date = %s AND status = 'Scheduled'
    """, (doctor_id, slot_id, date))
    conflict = cursor.fetchone()
    if conflict:
        cursor.close()
        return jsonify({"message": "This slot is already booked."}), 400

    # Insert appointment
    cursor.execute("""
        INSERT INTO appointments (patient_id, doctor_id, therapy_id, slot_id, date, status)
        VALUES (%s, %s, %s, %s, %s, 'Scheduled')
    """, (patient_id, doctor_id, therapy_id, slot_id, date))
    mysql.connection.commit()
    appointment_id = cursor.lastrowid

    # Get doctor, therapy, slot details
    cursor.execute("SELECT name FROM doctors WHERE id=%s", (doctor_id,))
    doctor_name = cursor.fetchone()[0]

    cursor.execute("SELECT name FROM therapies WHERE id=%s", (therapy_id,))
    therapy_name = cursor.fetchone()[0]

    cursor.execute("SELECT time_label FROM slots WHERE id=%s", (slot_id,))
    time_label = cursor.fetchone()[0]

    # Insert notification
    message = f"Appointment booked: {therapy_name} with Dr. {doctor_name} on {date} at {time_label}."
    cursor.execute("""
        INSERT INTO notifications (patient_id, appointment_id, type, message, channel)
        VALUES (%s, %s, %s, %s, %s)
    """, (patient_id, appointment_id, 'Pre-Procedure', message, 'InApp'))
    mysql.connection.commit()
    cursor.close()

    return jsonify({"message": "Appointment booked successfully!"})



@app.route('/cancel/<int:appointment_id>', methods=['POST'])
def cancel_appointment(appointment_id):
    if 'patient_id' not in session:
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    # Get appointment details first
    cursor.execute("""
        SELECT a.date, a.therapy_id, a.doctor_id, s.time_label
        FROM appointments a
        JOIN slots s ON a.slot_id = s.id
        WHERE a.id=%s AND a.patient_id=%s
    """, (appointment_id, session['patient_id']))
    appt = cursor.fetchone()
    if not appt:
        cursor.close()
        return redirect(url_for('patient_portal'))

    # Get doctor & therapy names
    cursor.execute("SELECT name FROM doctors WHERE id=%s", (appt['doctor_id'],))
    doctor_name = cursor.fetchone()['name']

    cursor.execute("SELECT name FROM therapies WHERE id=%s", (appt['therapy_id'],))
    therapy_name = cursor.fetchone()['name']

    # Cancel appointment
    cursor.execute("""
        UPDATE appointments
        SET status='Cancelled'
        WHERE id=%s AND patient_id=%s
    """, (appointment_id, session['patient_id']))
    mysql.connection.commit()

    # Insert notification
    message = f"Appointment cancelled: {therapy_name} with Dr. {doctor_name} on {appt['date']} at {appt['time_label']}."
    cursor.execute("""
        INSERT INTO notifications (patient_id, appointment_id, type, message, channel)
        VALUES (%s, %s, %s, %s, %s)
    """, (session['patient_id'], appointment_id, 'Pre-Procedure', message, 'InApp'))
    mysql.connection.commit()
    cursor.close()

    return redirect(url_for('patient_portal'))


@app.route('/edit/<int:appointment_id>')
def edit_appointment(appointment_id):
    if 'patient_id' not in session:
        return redirect(url_for('login'))
    
    # You can fetch details of the appointment here
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("""
        SELECT a.id, a.date, a.slot_id, a.therapy_id, a.doctor_id
        FROM appointments a
        WHERE a.id = %s AND a.patient_id = %s
    """, (appointment_id, session['patient_id']))
    appointment = cursor.fetchone()
    cursor.close()

    if not appointment:
        return redirect(url_for('patient_portal'))

    # For now, just render a page with appointment info
    return render_template("editAppointment.html", appointment=appointment)









@app.route('/notifications/<int:patient_id>')
def notifications(patient_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("""
        SELECT id, appointment_id, type, message, channel, sent_at
        FROM notifications
        WHERE patient_id = %s
        ORDER BY sent_at DESC, id DESC
    """, (patient_id,))
    notifications = cursor.fetchall()
    cursor.close()
    return render_template('notifications.html', notifications=notifications)





# @app.route('/notifications/count/<int:patient_id>')
# def notifications_count(patient_id):
#     cursor = mysql.connection.cursor()
#     cursor.execute("""
#         SELECT COUNT(*) FROM notifications
#         WHERE patient_id = %s AND is_read = 0
#     """, (patient_id,))
#     count = cursor.fetchone()[0]
#     cursor.close()
#     return jsonify({"count": count})




# @app.route('/notifications/mark_read/<int:patient_id>', methods=['POST'])
# def mark_notifications_read(patient_id):
#     cursor = mysql.connection.cursor()
#     cursor.execute("""
#         UPDATE notifications
#         SET is_read = 1
#         WHERE patient_id = %s
#     """, (patient_id,))
#     mysql.connection.commit()
#     cursor.close()
#     return '', 204




@app.route('/progress/<int:patient_id>')
def treatment_progress(patient_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    # Count all sessions
    cursor.execute("SELECT COUNT(*) AS total FROM appointments WHERE patient_id=%s", (patient_id,))
    total = cursor.fetchone()['total']

    # Count by status
    cursor.execute("""
        SELECT status, COUNT(*) as count 
        FROM appointments 
        WHERE patient_id=%s 
        GROUP BY status
    """, (patient_id,))
    status_counts = cursor.fetchall()

    # Default values
    completed = scheduled = cancelled = 0
    for row in status_counts:
        if row['status'] == 'Completed':
            completed = row['count']
        elif row['status'] == 'Scheduled':
            scheduled = row['count']
        elif row['status'] == 'Cancelled':
            cancelled = row['count']

    return jsonify({
        "total": total,
        "completed": completed,
        "scheduled": scheduled,
        "cancelled": cancelled
    })








# --- Submit general doctor feedback ---
@app.route('/submit-feedback', methods=['POST'])
def submit_feedback():
    data = request.json
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("""
            INSERT INTO feedback (patient_id, doctor_id, rating, comments)
            VALUES (%s, %s, %s, %s)
        """, (
            data['patient_id'],
            data['doctor_id'],
            data['rating'],
            data.get('comments', '')
        ))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Feedback saved'}), 200
    except Exception as e:
        print(f"Error saving feedback: {e}")
        return jsonify({'error': 'Failed to save feedback'}), 500


# --- Submit detailed patient feedback ---
@app.route('/submit_patient_feedback', methods=['POST'])
def submit_patient_feedback():
    if 'patient_id' not in session:
        return jsonify({'error': 'User not logged in'}), 401

    data = request.json
    patient_id = session['patient_id']

    try:
        cursor = mysql.connection.cursor()
        cursor.execute("""
            INSERT INTO patient_feedback 
            (patient_id, energy_level, digestion, sleep_quality, stress_level, mood, overall_wellness)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            patient_id,
            data['energy_level'],
            data['digestion'],
            data['sleep_quality'],
            data['stress_level'],
            data['mood'],
            data['overall_wellness']
        ))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Patient feedback saved'}), 200
    except Exception as e:
        print(f"Error saving patient feedback: {e}")
        return jsonify({'error': 'Failed to save patient feedback'}), 500


# # --- API: Last 7 days patient feedback ---
# @app.route('/api/last-7-days-feedback')
# def last_7_days_feedback():
#     if 'patient_id' not in session:
#         return jsonify({'error': 'User not logged in'}), 401

#     patient_id = session['patient_id']

#     try:
#         cursor = mysql.connection.cursor(dictionary=True)
#         cursor.execute("""
#             SELECT pf.*
#             FROM patient_feedback pf
#             INNER JOIN (
#                 SELECT DATE(timestamp) AS feedback_date,
#                        MAX(timestamp) AS latest_time
#                 FROM patient_feedback
#                 WHERE patient_id = %s
#                   AND timestamp >= CURDATE() - INTERVAL 7 DAY
#                 GROUP BY DATE(timestamp)
#             ) latest
#             ON DATE(pf.timestamp) = latest.feedback_date
#             AND pf.timestamp = latest.latest_time
#             WHERE pf.patient_id = %s
#             ORDER BY pf.timestamp
#         """, (patient_id, patient_id))
#         rows = cursor.fetchall()
#         cursor.close()

#         dates = [row['timestamp'].strftime('%Y-%m-%d') for row in rows]
#         energy = [row['energy_level'] for row in rows]
#         digestion = [row['digestion'] for row in rows]
#         sleep = [row['sleep_quality'] for row in rows]
#         stress = [row['stress_level'] for row in rows]
#         mood = [row['mood'] for row in rows]
#         wellness = [row['overall_wellness'] for row in rows]

#         return jsonify({
#             'dates': dates,
#             'energy': energy,
#             'digestion': digestion,
#             'sleep': sleep,
#             'stress': stress,
#             'mood': mood,
#             'overall_wellness': wellness
#         })

#     except Exception as e:
#         print(f"Error in /api/last-7-days-feedback: {e}")
#         return jsonify({'error': 'Internal server error'}), 500











# from datetime import datetime, timedelta

# @app.route('/api/last-7-days-feedback')
# def last_7_days_feedback():
#     try:
#         # Get patientId from query params or session
#         patient_id = request.args.get('patientId') or session.get('patient_id')
#         if not patient_id:
#             return jsonify({'error': 'Missing patientId'}), 400

#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

#         # Build last 7 days list
#         today = datetime.today().date()
#         last_7_days = [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(6, -1, -1)]

#         # Query feedback for last 7 days
#         query = """
#             SELECT DATE(created_at) AS date, energy, digestion, sleep, stress
#             FROM patient_feedback
#             WHERE patient_id = %s
#               AND DATE(created_at) BETWEEN DATE_SUB(CURDATE(), INTERVAL 6 DAY) AND CURDATE()
#         """
#         cursor.execute(query, (patient_id,))
#         rows = cursor.fetchall()

#         # Convert to dict for quick lookup
#         data_map = {str(row['date']): row for row in rows}

#         # Build response ensuring 7 days of data (default 0 if missing)
#         result = {
#             'dates': [],
#             'energy': [],
#             'digestion': [],
#             'sleep': [],
#             'stress': []
#         }
#         for d in last_7_days:
#             result['dates'].append(d)
#             result['energy'].append(data_map.get(d, {}).get('energy', 0))
#             result['digestion'].append(data_map.get(d, {}).get('digestion', 0))
#             result['sleep'].append(data_map.get(d, {}).get('sleep', 0))
#             result['stress'].append(data_map.get(d, {}).get('stress', 0))

#         return jsonify(result)

#     except Exception as e:
#         print("Error in /api/last-7-days-feedback:", e)
#         return jsonify({'error': str(e)}), 500

















@app.route('/notifications/count/<int:patient_id>')
def notifications_count(patient_id):
    try:
        # TODO: Replace with real DB query later
        # Example: SELECT COUNT(*) FROM notifications WHERE patient_id = %s AND is_read = 0
        return jsonify({"count": 0})
    except Exception as e:
        print("Error in /notifications/count:", e)
        return jsonify({"error": str(e), "count": 0}), 500




@app.route('/api/last-7-days-feedback')
def last_7_days_feedback():
    patient_id = request.args.get('patientId', type=int)

    if not patient_id:
        return jsonify({"error": "Missing patientId"}), 400

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("""
        SELECT 
            timestamp,
            energy_level,
            digestion,
            sleep_quality,
            stress_level
        FROM patient_feedback
        WHERE patient_id = %s
        ORDER BY timestamp DESC
        LIMIT 7
    """, (patient_id,))
    rows = cursor.fetchall()
    cursor.close()

    # Reverse so oldest → newest
    rows = rows[::-1]

    dates = [r['timestamp'].strftime("%Y-%m-%d") for r in rows]
    energy = [r['energy_level'] for r in rows]
    digestion = [r['digestion'] for r in rows]
    sleep = [r['sleep_quality'] for r in rows]
    stress = [r['stress_level'] for r in rows]

    return jsonify({
        "dates": dates,
        "energy": energy,
        "digestion": digestion,
        "sleep": sleep,
        "stress": stress
    })

