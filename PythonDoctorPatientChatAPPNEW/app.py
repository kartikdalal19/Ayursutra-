# from flask import Flask, render_template, request, redirect, session, url_for
# from flask_socketio import SocketIO, join_room, leave_room, emit
# import mysql.connector

# app = Flask(__name__)
# app.secret_key = 'test1234'
# socketio = SocketIO(app)

# # Database connection (update with your config)
# db_config = {
#     'host': 'localhost',
#     'user': 'root',
#     'password': '1234',
#     'database': 'ayursutra'
# }

# def get_db_connection():
#     return mysql.connector.connect(**db_config)

# # Simple login (no hashing, just dummy check)
# @app.route('/', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']
#         user_type = request.form['user_type']  # 'doctor' or 'patient'

#         conn = get_db_connection()
#         cursor = conn.cursor(dictionary=True)
#         if user_type == 'doctor':
#             cursor.execute("SELECT * FROM doctors WHERE email=%s AND password=%s", (email, password))
#         else:
#             cursor.execute("SELECT * FROM patients WHERE email=%s AND password=%s", (email, password))

#         user = cursor.fetchone()
#         cursor.close()
#         conn.close()

#         if user:
#             session['user_id'] = user['id']
#             session['user_name'] = user['name']
#             session['user_type'] = user_type

#             # Redirect to select chat partner page
#             return redirect(url_for('select_chat'))
#         else:
#             return render_template('login.html', error="Invalid credentials")

#     return render_template('login.html')

# # Select chat partner page
# @app.route('/select_chat')
# def select_chat():
#     if 'user_id' not in session:
#         return redirect(url_for('login'))

#     user_type = session['user_type']
#     user_id = session['user_id']

#     conn = get_db_connection()
#     cursor = conn.cursor(dictionary=True)

#     if user_type == 'doctor':
#         # Fetch patients associated with this doctor
#         cursor.execute("""
#             SELECT p.id, p.name FROM patients p
#             JOIN doctor_patient dp ON p.id = dp.patient_id
#             WHERE dp.doctor_id = %s
#         """, (user_id,))
#         partners = cursor.fetchall()
#     else:
#         # Fetch doctors associated with this patient
#         cursor.execute("""
#             SELECT d.id, d.name FROM doctors d
#             JOIN doctor_patient dp ON d.id = dp.doctor_id
#             WHERE dp.patient_id = %s
#         """, (user_id,))
#         partners = cursor.fetchall()

#     cursor.close()
#     conn.close()

#     return render_template('select_chat.html', partners=partners, user_type=user_type)

# # Chat page
# @app.route('/chat/<int:partner_id>')
# def chat(partner_id):
#     if 'user_id' not in session:
#         return redirect(url_for('login'))

#     user_type = session['user_type']
#     user_id = session['user_id']
#     username = session['user_name']

#     # Determine who is doctor and who is patient
#     if user_type == 'doctor':
#         doctor_id = user_id
#         patient_id = partner_id
#     else:
#         patient_id = user_id
#         doctor_id = partner_id

#     # Create a unique room ID
#     room_id = f"doctor_{doctor_id}_patient_{patient_id}"

#     return render_template('chat.html', username=username, room_id=room_id)

# # SocketIO events
# @socketio.on('join')
# def on_join(data):
#     room = data['room_id']
#     username = data['username']
#     join_room(room)
#     emit('message', {'msg': f"{username} has joined the chat."}, room=room)

# @socketio.on('send_message')
# def handle_send_message(data):
#     room = data['room_id']
#     username = data['username']
#     message = data['message']
#     emit('message', {'msg': f"{username}: {message}"}, room=room)

# @socketio.on('leave')
# def on_leave(data):
#     room = data['room_id']
#     username = data['username']
#     leave_room(room)
#     emit('message', {'msg': f"{username} has left the chat."}, room=room)

# if __name__ == '__main__':
#     socketio.run(app, debug=True)

















from flask import Flask, render_template, request, redirect, session, url_for
from flask_socketio import SocketIO, join_room, emit
import pymysql

app = Flask(__name__)
app.secret_key = 'test1234'
socketio = SocketIO(app)

# In-memory message history
chat_history = {}

# MySQL Connection
db = pymysql.connect(
    host="localhost",
    user="root",
    password="1234",
    database="ayursutra",
    cursorclass=pymysql.cursors.DictCursor
)


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = None
        role = None

        with db.cursor() as cursor:
            # Check patient
            cursor.execute("SELECT * FROM patients WHERE email=%s AND password=%s", (email, password))
            patient = cursor.fetchone()
            if patient:
                user = patient
                role = 'patient'

            # Check doctor
            if not user:
                cursor.execute("SELECT * FROM doctors WHERE email=%s AND password=%s", (email, password))
                doctor = cursor.fetchone()
                if doctor:
                    user = doctor
                    role = 'doctor'

        if user:
            session['user_id'] = user['id']
            session['username'] = user['name']
            session['role'] = role
            return redirect(url_for('select_chat'))

        return render_template('login.html', error="Invalid credentials")

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/select_chat')
def select_chat():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    with db.cursor() as cursor:
        if session['role'] == 'patient':
            cursor.execute("""
                SELECT d.id, d.name FROM doctors d
                JOIN doctor_patient dp ON d.id = dp.doctor_id
                WHERE dp.patient_id = %s
            """, (session['user_id'],))
            users = cursor.fetchall()
        else:
            cursor.execute("""
                SELECT p.id, p.name FROM patients p
                JOIN doctor_patient dp ON p.id = dp.patient_id
                WHERE dp.doctor_id = %s
            """, (session['user_id'],))
            users = cursor.fetchall()

    # users is a list of dicts, which works well in Jinja2 for user.id and user.name
    return render_template('select_chat.html', users=users)


# @app.route('/chat/<int:partner_id>')
# def chat(partner_id):
#     if 'user_id' not in session:
#         return redirect(url_for('login'))

#     user_id = session['user_id']
#     role = session['role']

#     if role == 'patient':
#         doctor_id = partner_id
#         patient_id = user_id
#     else:
#         doctor_id = user_id
#         patient_id = partner_id

#     # Generate a consistent room id
#     room_id = f"doctor_{doctor_id}_patient_{patient_id}"

#     # Fetch partner name for display
#     with db.cursor() as cursor:
#         if role == 'patient':
#             cursor.execute("SELECT name FROM doctors WHERE id=%s", (partner_id,))
#         else:
#             cursor.execute("SELECT name FROM patients WHERE id=%s", (partner_id,))
#         partner = cursor.fetchone()

#     partner_name = partner['name'] if partner else 'Unknown'

#     return render_template('chat.html', room_id=room_id, username=session['username'], partner_name=partner_name)



@app.route('/chat/<int:partner_id>')
def chat(partner_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    role = session['role']

    with db.cursor() as cursor:
        if role == 'patient':
            cursor.execute("SELECT name FROM doctors WHERE id = %s", (partner_id,))
        else:
            cursor.execute("SELECT name FROM patients WHERE id = %s", (partner_id,))
        partner = cursor.fetchone()

    if role == 'patient':
        doctor_id = partner_id
        patient_id = user_id
    else:
        doctor_id = user_id
        patient_id = partner_id

    room_id = f"doctor_{doctor_id}_patient_{patient_id}"
    return render_template('chat.html',
                           room_id=room_id,
                           username=session['username'],
                           partner_name=partner['name'])


@socketio.on('join')
def on_join(data):
    room = data['room_id']
    username = data['username']
    join_room(room)

    # Send previous messages
    messages = chat_history.get(room, [])
    for msg in messages:
        emit('message', {'msg': f"{msg['username']}: {msg['msg']}", 'time': msg.get('time', '')}, room=request.sid)

    # (Optional) notify room user joined
    # emit('message', {'msg': f"{username} has joined the chat."}, room=room)


@socketio.on('send_message')
def handle_send_message(data):
    from datetime import datetime

    room = data['room_id']
    username = data['username']
    message = data['message']

    timestamp = datetime.now().strftime('%H:%M')  # Hour:Minute for chat time display

    # Store in memory
    if room not in chat_history:
        chat_history[room] = []
    chat_history[room].append({'username': username, 'msg': message, 'time': timestamp})

    emit('message', {'msg': f"{username}: {message}", 'time': timestamp}, room=room)


if __name__ == '__main__':
    socketio.run(app, debug=True)
