import mysql.connector
from datetime import datetime, timedelta

# 1️⃣ Connect to your MySQL database
db = mysql.connector.connect(
    host="",
    user="",
    password="",
    database=""
)
import mysql.connector


cursor = db.cursor()

# 2️⃣ Populate patients
patients = [
    ("Alice", 30, "Female", "9876543210", "alice@mail.com", "123 Main St", "English"),
    ("Bob", 40, "Male", "9123456780", "bob@mail.com", "456 Elm St", "Hindi"),
    ("Charlie", 35, "Other", "9012345678", "charlie@mail.com", "789 Pine St", "English")
]

cursor.executemany(
    "INSERT INTO patients (name, age, gender, phone, email, address, preferred_language) VALUES (%s,%s,%s,%s,%s,%s,%s)",
    patients
)

# 3️⃣ Populate doctors
doctors = [
    ("Dr. Sharma", "Ayurveda", "Healing Center", 28.6139, 77.2090, 4.5, "Mon,Tue,Wed"),
    ("Dr. Mehta", "Panchakarma", "Wellness Hub", 28.7041, 77.1025, 4.7, "Thu,Fri,Sat"),
    ("Dr. Singh", "Yoga Therapy", "Zen Studio", 28.5355, 77.3910, 4.3, "Mon,Thu,Sun")
]

cursor.executemany(
    "INSERT INTO doctors (name, specialization, center, latitude, longitude, rating, available_days) VALUES (%s,%s,%s,%s,%s,%s,%s)",
    doctors
)

# 4️⃣ Populate therapies
therapies = [
    ("Abhyanga", "Full body oil massage", 60, 1200.0, "Avoid heavy meals", "Rest for 1 hour"),
    ("Shirodhara", "Oil poured on forehead", 45, 1500.0, "Avoid caffeine", "Drink warm water"),
    ("Panchakarma Detox", "Cleansing therapy", 120, 3000.0, "Fasting recommended", "Follow post-therapy diet")
]

cursor.executemany(
    "INSERT INTO therapies (name, description, duration_minutes, cost, precautions_pre, precautions_post) VALUES (%s,%s,%s,%s,%s,%s)",
    therapies
)

# 5️⃣ Populate slots
# For simplicity, assign 2 slots per doctor per day
slots = []
time_labels = ["10:00 AM - 11:00 AM", "11:30 AM - 12:30 PM"]
doctor_ids = [1,2,3]
days = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]

for doc_id in doctor_ids:
    for day in days:
        for time_label in time_labels:
            slots.append((doc_id, day, time_label, True))

cursor.executemany(
    "INSERT INTO slots (doctor_id, day_of_week, time_label, is_available) VALUES (%s,%s,%s,%s)",
    slots
)

# 6️⃣ Populate appointments
# Simple mapping: patient 1 with doctor 1 and therapy 1, etc.
appointments = [
    (1, 1, 1, 1, (datetime.today() + timedelta(days=1)).date(), "Scheduled"),
    (2, 2, 2, 3, (datetime.today() + timedelta(days=2)).date(), "Scheduled"),
    (3, 3, 3, 5, (datetime.today() + timedelta(days=3)).date(), "Scheduled")
]

cursor.executemany(
    "INSERT INTO appointments (patient_id, doctor_id, therapy_id, slot_id, date, status) VALUES (%s,%s,%s,%s,%s,%s)",
    appointments
)

# 7️⃣ Populate therapy_progress
therapy_progress = [
    (1, 1, "Feeling relaxed", 8, None, datetime.now()),
    (2, 1, "Mild headache", 6, "Headache", datetime.now()),
    (3, 2, "Better sleep", 9, None, datetime.now())
]

cursor.executemany(
    "INSERT INTO therapy_progress (appointment_id, session_number, patient_feedback, improvement_score, side_effects, recorded_at) VALUES (%s,%s,%s,%s,%s,%s)",
    therapy_progress
)

# 8️⃣ Populate notifications
notifications = [
    (1, 1, "Pre-Procedure", "Reminder: Your therapy is tomorrow", "SMS", None),
    (2, 2, "Post-Procedure", "Please follow post-therapy diet", "Email", None)
]

cursor.executemany(
    "INSERT INTO notifications (patient_id, appointment_id, type, message, channel, sent_at) VALUES (%s,%s,%s,%s,%s,%s)",
    notifications
)

# 9️⃣ Populate feedback
feedback = [
    (1, 1, 5, "Excellent service", datetime.now()),
    (2, 2, 4, "Very good", datetime.now()),
    (3, 3, 3, "Average experience", datetime.now())
]

cursor.executemany(
    "INSERT INTO feedback (patient_id, doctor_id, rating, comments, created_at) VALUES (%s,%s,%s,%s,%s)",
    feedback
)

# Commit and close
db.commit()
cursor.close()
db.close()

print("All tables populated with sample data successfully!")





