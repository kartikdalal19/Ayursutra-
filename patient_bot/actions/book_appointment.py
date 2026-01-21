import MySQLdb

def book_appointment(therapy_id, doctor_id, appointment_date, slot_id, patient_id):
    db = MySQLdb.connect(host="localhost", user="root", passwd="your_password", db="ayursutra")
    cursor = db.cursor()
    
    try:
        # Check if slot is already booked
        cursor.execute("""
            SELECT * FROM appointments 
            WHERE doctor_id=%s AND appointment_date=%s AND slot_id=%s
        """, (doctor_id, appointment_date, slot_id))
        
        if cursor.fetchone():
            return "❌ Sorry, this slot is already booked. Please choose another slot."
        
        # Insert patient if not exists
        cursor.execute("SELECT id FROM patients WHERE id=%s", (patient_id,))
        if not cursor.fetchone():
            cursor.execute("INSERT INTO patients (id) VALUES (%s)", (patient_id,))
            db.commit()

        # Insert appointment
        cursor.execute("""
            INSERT INTO appointments (therapy_id, doctor_id, appointment_date, slot_id, patient_id, status)
            VALUES (%s, %s, %s, %s, %s, 'Scheduled')
        """, (therapy_id, doctor_id, appointment_date, slot_id, patient_id))
        db.commit()
        
        return "✅ Appointment booked successfully!"
    
    except Exception as e:
        return f"⚠️ Error while booking: {str(e)}"
    
    finally:
        db.close()
