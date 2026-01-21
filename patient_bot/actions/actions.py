# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []












# # Phase - 1 

# # rasa/actions/actions.py
# from typing import Any, Text, Dict, List
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
# import MySQLdb

# class ActionUserInfo(Action):
#     def name(self) -> Text:
#         return "action_user_info"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         # sender_id is patient_id from Flask
#         patient_id = tracker.sender_id

#         conn = MySQLdb.connect(host="localhost", user="root", passwd="-", db="ayursutra")
#         cursor = conn.cursor()
#         cursor.execute("SELECT name, email, age, gender, phone FROM patients WHERE id=%s", (patient_id,))
#         result = cursor.fetchone()
#         cursor.close()
#         conn.close()

#         if result:
#             name, email, age, gender, phone = result
#             dispatcher.utter_message(text=f"Hello {name}! Your details:\nEmail: {email}\nAge: {age}\nGender: {gender}\nPhone: {phone}")
#         else:
#             dispatcher.utter_message(text="I could not find your details.")

#         return []













# # Phase - 2 

# #  actions.py

# from typing import Any, Text, Dict, List
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
# import MySQLdb

# # ----- Greetings -----
# class ActionGreet(Action):
#     def name(self) -> Text:
#         return "action_greet"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         dispatcher.utter_message(text="Hello! Welcome to Ayursutra. How can I help you today?")
#         return []

# # ----- User Info -----
# class ActionUserInfo(Action):
#     def name(self) -> Text:
#         return "action_user_info"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         patient_id = tracker.sender_id

#         conn = MySQLdb.connect(host="localhost", user="root", passwd="-", db="ayursutra")
#         cursor = conn.cursor()
#         cursor.execute(
#             "SELECT name, email, age, gender, phone FROM patients WHERE id=%s",
#             (patient_id,)
#         )
#         result = cursor.fetchone()
#         cursor.close()
#         conn.close()

#         if result:
#             name, email, age, gender, phone = result
#             dispatcher.utter_message(
#                 text=f"Hello {name}! Your details:\nEmail: {email}\nAge: {age}\nGender: {gender}\nPhone: {phone}"
#             )
#         else:
#             dispatcher.utter_message(text="I could not find your details.")

#         return []

# # ----- Show Upcoming Appointments -----
# class ActionShowAppointments(Action):
#     def name(self) -> Text:
#         return "action_show_appointments"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         patient_id = tracker.sender_id

#         conn = MySQLdb.connect(host="localhost", user="root", passwd="-", db="ayursutra")
#         cursor = conn.cursor()
        
#         query = """
#         SELECT 
#             a.id AS appointment_id,
#             a.date,
#             s.time_label,
#             d.name AS doctor_name,
#             t.name AS therapy_name,
#             a.status
#         FROM appointments a
#         JOIN doctors d ON a.doctor_id = d.id
#         JOIN therapies t ON a.therapy_id = t.id
#         JOIN slots s ON a.slot_id = s.id
#         WHERE a.patient_id = %s
#           AND a.date >= CURDATE()
#           AND a.status = 'Scheduled'
#         ORDER BY a.date, s.time_label;
#         """

#         cursor.execute(query, (patient_id,))
#         appointments = cursor.fetchall()
#         cursor.close()
#         conn.close()

#         if appointments:
#             text = "Here are your upcoming appointments:\n"
#             for appt in appointments:
#                 appt_id, date, time_label, doctor_name, therapy_name, status = appt
#                 text += f"- {date} {time_label} with {doctor_name} ({therapy_name})\n"
#             dispatcher.utter_message(text=text)
#         else:
#             dispatcher.utter_message(text="You have no upcoming appointments.")

#         return []












# Phase - 3 




# actions.py
# from typing import Any, Text, Dict, List
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
# import MySQLdb

# class ActionCancelAppointment(Action):
#     def name(self) -> Text:
#         return "action_cancel_appointment"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         patient_id = tracker.sender_id

#         conn = MySQLdb.connect(
#             host="localhost",
#             user="root",
#             passwd="-",
#             db="ayursutra"
#         )
#         cursor = conn.cursor()

#         cancel_query = """
#         UPDATE appointments
#         SET status = 'Cancelled'
#         WHERE id = (
#             SELECT id FROM (
#                 SELECT id
#                 FROM appointments
#                 WHERE patient_id = %s AND status = 'Scheduled'
#                 ORDER BY date DESC, slot_id DESC
#                 LIMIT 1
#             ) AS subquery
#         )
#         """
#         cursor.execute(cancel_query, (patient_id,))
#         conn.commit()
#         rows_updated = cursor.rowcount
#         cursor.close()
#         conn.close()

#         if rows_updated > 0:
#             dispatcher.utter_message(text="Your latest appointment has been cancelled.")
#         else:
#             dispatcher.utter_message(text="You have no scheduled appointments to cancel.")

#         return []


















# Phase - 4 integrate




# from typing import Any, Text, Dict, List
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
# import MySQLdb

# # ----- Greetings -----
# class ActionGreet(Action):
#     def name(self) -> Text:
#         return "action_greet"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         dispatcher.utter_message(text="Hello! Welcome to Ayursutra. How can I help you today?")
#         return []

# # ----- User Info -----
# class ActionUserInfo(Action):
#     def name(self) -> Text:
#         return "action_user_info"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         patient_id = tracker.sender_id

#         conn = MySQLdb.connect(host="localhost", user="root", passwd="-", db="ayursutra")
#         cursor = conn.cursor()
#         cursor.execute(
#             "SELECT name, email, age, gender, phone FROM patients WHERE id=%s",
#             (patient_id,)
#         )
#         result = cursor.fetchone()
#         cursor.close()
#         conn.close()

#         if result:
#             name, email, age, gender, phone = result
#             dispatcher.utter_message(
#                 text=f"Hello {name}! Your details:\nEmail: {email}\nAge: {age}\nGender: {gender}\nPhone: {phone}"
#             )
#         else:
#             dispatcher.utter_message(text="I could not find your details.")

#         return []

# # ----- Show Upcoming Appointments -----
# class ActionShowAppointments(Action):
#     def name(self) -> Text:
#         return "action_show_appointments"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         patient_id = tracker.sender_id

#         conn = MySQLdb.connect(host="localhost", user="root", passwd="-", db="ayursutra")
#         cursor = conn.cursor()
        
#         query = """
#         SELECT 
#             a.id AS appointment_id,
#             a.date,
#             s.time_label,
#             d.name AS doctor_name,
#             t.name AS therapy_name,
#             a.status
#         FROM appointments a
#         JOIN doctors d ON a.doctor_id = d.id
#         JOIN therapies t ON a.therapy_id = t.id
#         JOIN slots s ON a.slot_id = s.id
#         WHERE a.patient_id = %s
#           AND a.date >= CURDATE()
#           AND a.status = 'Scheduled'
#         ORDER BY a.date, s.time_label;
#         """

#         cursor.execute(query, (patient_id,))
#         appointments = cursor.fetchall()
#         cursor.close()
#         conn.close()

#         if appointments:
#             text = "Here are your upcoming appointments:\n"
#             for appt in appointments:
#                 appt_id, date, time_label, doctor_name, therapy_name, status = appt
#                 text += f"- {date} {time_label} with {doctor_name} ({therapy_name})\n"
#             dispatcher.utter_message(text=text)
#         else:
#             dispatcher.utter_message(text="You have no upcoming appointments.")

#         return []


# class ActionCancelAppointment(Action):
#     def name(self) -> Text:
#         return "action_cancel_appointment"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         patient_id = tracker.sender_id

#         conn = MySQLdb.connect(
#             host="localhost",
#             user="root",
#             passwd="-",
#             db="ayursutra"
#         )
#         cursor = conn.cursor()

#         cancel_query = """
#         UPDATE appointments
#         SET status = 'Cancelled'
#         WHERE id = (
#             SELECT id FROM (
#                 SELECT id
#                 FROM appointments
#                 WHERE patient_id = %s AND status = 'Scheduled'
#                 ORDER BY date DESC, slot_id DESC
#                 LIMIT 1
#             ) AS subquery
#         )
#         """
#         cursor.execute(cancel_query, (patient_id,))
#         conn.commit()
#         rows_updated = cursor.rowcount
#         cursor.close()
#         conn.close()

#         if rows_updated > 0:
#             dispatcher.utter_message(text="Your latest appointment has been cancelled.")
#         else:
#             dispatcher.utter_message(text="You have no scheduled appointments to cancel.")

#         return []





































# Phase - 5 


# actions.py 

# from typing import Any, Text, Dict, List
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
# import MySQLdb


# # -------------------------------------------------------------------
# # Helper: Database Connection
# # -------------------------------------------------------------------
# def get_db_connection():
#     return MySQLdb.connect(
#         host="localhost",
#         user="root",
#         passwd="-",
#         db="ayursutra"
#     )


# # -------------------------------------------------------------------
# #  Greeting
# # -------------------------------------------------------------------
# class ActionGreet(Action):
#     def name(self) -> Text:
#         return "action_greet"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         dispatcher.utter_message(
#             text="👋 Hello! Welcome to *Ayursutra*.\n\nHow can I help you today?"
#         )
#         return []


# # -------------------------------------------------------------------
# #  User Info
# # -------------------------------------------------------------------
# class ActionUserInfo(Action):
#     def name(self) -> Text:
#         return "action_user_info"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         patient_id = tracker.sender_id

#         conn = get_db_connection()
#         cursor = conn.cursor()
#         cursor.execute(
#             "SELECT name, email, age, gender, phone FROM patients WHERE id=%s",
#             (patient_id,)
#         )
#         result = cursor.fetchone()
#         cursor.close()
#         conn.close()

#         if result:
#             name, email, age, gender, phone = result
#             response = (
#                 f"🧑 **Your Profile**\n\n"
#                 f"• 🔹 Name: {name}\n"
#                 f"• 📧 Email: {email}\n"
#                 f"• 🎂 Age: {age}\n"
#                 f"•  ⚧ Gender: {gender}\n"
#                 f"• 📱 Phone: {phone}\n"
#             )
#             dispatcher.utter_message(text=response)
#         else:
#             dispatcher.utter_message(text="❌ I could not find your details.")

#         return []


# # -------------------------------------------------------------------
# #  Show Upcoming Appointments
# # -------------------------------------------------------------------
# class ActionShowAppointments(Action):
#     def name(self) -> Text:
#         return "action_show_appointments"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         patient_id = tracker.sender_id
#         conn = get_db_connection()
#         cursor = conn.cursor()

#         query = """
#         SELECT 
#             a.id AS appointment_id,
#             a.date,
#             s.time_label,
#             d.name AS doctor_name,
#             t.name AS therapy_name,
#             a.status
#         FROM appointments a
#         JOIN doctors d ON a.doctor_id = d.id
#         JOIN therapies t ON a.therapy_id = t.id
#         JOIN slots s ON a.slot_id = s.id
#         WHERE a.patient_id = %s
#           AND a.date >= CURDATE()
#           AND a.status = 'Scheduled'
#         ORDER BY a.date, s.time_label;
#         """
#         cursor.execute(query, (patient_id,))
#         appointments = cursor.fetchall()
#         cursor.close()
#         conn.close()

#         if appointments:
#             text = "📅 **Your Upcoming Appointments**\n\n"
#             for appt in appointments:
#                 appt_id, date, time_label, doctor_name, therapy_name, status = appt
#                 text += (
#                     f"🆔 ID: {appt_id}\n"
#                     f"📅 Date: {date}\n"
#                     f"⏰ Time: {time_label}\n"
#                     f"👨‍⚕️ Doctor: {doctor_name}\n"
#                     f"💆 Therapy: {therapy_name}\n"
#                     f"📌 Status: {status}\n"
#                     f"\n\n"
#                 )
#             dispatcher.utter_message(text=text)
#         else:
#             dispatcher.utter_message(text="✅ You have no upcoming appointments.")

#         return []


# # -------------------------------------------------------------------
# #  Cancel Appointment
# # -------------------------------------------------------------------
# class ActionCancelAppointment(Action):
#     def name(self) -> Text:
#         return "action_cancel_appointment"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         patient_id = tracker.sender_id
#         conn = get_db_connection()
#         cursor = conn.cursor()

#         cancel_query = """
#         UPDATE appointments
#         SET status = 'Cancelled'
#         WHERE id = (
#             SELECT id FROM (
#                 SELECT id
#                 FROM appointments
#                 WHERE patient_id = %s AND status = 'Scheduled'
#                 ORDER BY date DESC, slot_id DESC
#                 LIMIT 1
#             ) AS subquery
#         )
#         """
#         cursor.execute(cancel_query, (patient_id,))
#         conn.commit()
#         rows_updated = cursor.rowcount
#         cursor.close()
#         conn.close()

#         if rows_updated > 0:
#             dispatcher.utter_message(text="❌ Your latest appointment has been *cancelled*.")
#         else:
#             dispatcher.utter_message(text="ℹ️ You have no scheduled appointments to cancel.")

#         return []


# # -------------------------------------------------------------------
# #  Doctors + Therapies Offered
# # -------------------------------------------------------------------
# class ActionAskDoctors(Action):
#     def name(self):
#         return "action_ask_doctors"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: dict):

#         conn = get_db_connection()
#         cursor = conn.cursor()

#         query = """
#         SELECT d.id, d.name, d.specialization, d.center, d.rating, d.available_days,
#                GROUP_CONCAT(DISTINCT t.name SEPARATOR ', ')
#         FROM doctors d
#         LEFT JOIN doctor_therapies dt ON d.id = dt.doctor_id
#         LEFT JOIN therapies t ON dt.therapy_id = t.id
#         GROUP BY d.id;
#         """
#         cursor.execute(query)
#         rows = cursor.fetchall()

#         if not rows:
#             dispatcher.utter_message("⚠️ No doctors found in the database.")
#         else:
#             response = "👨‍⚕️ **Available Doctors**\n\n"
#             for row in rows:
#                 (doc_id, name, specialization, center, rating, days, therapies) = row
#                 response += (
#                     f"👨‍⚕️ *{name}* ({specialization})\n"
#                     f"   🏥 Center: {center}\n"
#                     f"   ⭐ Rating: {rating}\n"
#                     f"   📅 Available: {days}\n"
#                     f"   💆 Therapies: {therapies if therapies else 'None'}\n"
#                     f"\n\n"
#                 )

#             dispatcher.utter_message(response)

#         cursor.close()
#         conn.close()
#         return []


# # -------------------------------------------------------------------
# #  Therapies + Doctors Offering Them
# # -------------------------------------------------------------------
# class ActionAskTherapies(Action):
#     def name(self):
#         return "action_ask_therapies"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: dict):

#         conn = get_db_connection()
#         cursor = conn.cursor()

#         query = """
#         SELECT t.id, t.name, t.description, t.duration_minutes, t.cost,
#                t.precautions_pre, t.precautions_post,
#                GROUP_CONCAT(DISTINCT d.name SEPARATOR ', ')
#         FROM therapies t
#         LEFT JOIN doctor_therapies dt ON t.id = dt.therapy_id
#         LEFT JOIN doctors d ON dt.doctor_id = d.id
#         GROUP BY t.id;
#         """
#         cursor.execute(query)
#         rows = cursor.fetchall()

#         if not rows:
#             dispatcher.utter_message("⚠️ No therapies found in the database.")
#         else:
#             response = "💆 **Available Therapies**\n\n"
#             for row in rows:
#                 (tid, name, desc, duration, cost, pre, post, doctors) = row
#                 response += (
#                     f"💆 *{name}*\n"
#                     f"   📝 {desc}\n"
#                     f"   ⏱ Duration: {duration} mins\n"
#                     f"   💰 Cost: ₹{cost}\n"
#                     f"   ⚠️ Pre-care: {pre}\n"
#                     f"   ✅ Post-care: {post}\n"
#                     f"   👨‍⚕️ Doctors: {doctors if doctors else 'No doctor assigned'}\n"
#                     f"\n\n"
#                 )

#             dispatcher.utter_message(response)

#         cursor.close()
#         conn.close()
#         return []










# phase 6 a

# actions.py
# from typing import Any, Text, Dict, List
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher

# class ActionTriggerPopup(Action):

#     def name(self) -> Text:
#         return "action_trigger_popup"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         dispatcher.utter_message(text="Sure! Please use the appointment popup to book your slot.")
#         return []

























































# # phase 6b






# from typing import Any, Text, Dict, List
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
# import MySQLdb


# # -------------------------------------------------------------------
# # Helper: Database Connection
# # -------------------------------------------------------------------
# def get_db_connection():
#     return MySQLdb.connect(
#         host="localhost",
#         user="root",
#         passwd="-",
#         db="ayursutra"
#     )


# # -------------------------------------------------------------------
# #  Greeting
# # -------------------------------------------------------------------
# class ActionGreet(Action):
#     def name(self) -> Text:
#         return "action_greet"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         dispatcher.utter_message(
#             text="👋 Hello! Welcome to *Ayursutra*.\n\nHow can I help you today?"
#         )
#         return []


# # -------------------------------------------------------------------
# #  User Info
# # -------------------------------------------------------------------
# class ActionUserInfo(Action):
#     def name(self) -> Text:
#         return "action_user_info"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         patient_id = tracker.sender_id

#         conn = get_db_connection()
#         cursor = conn.cursor()
#         cursor.execute(
#             "SELECT name, email, age, gender, phone FROM patients WHERE id=%s",
#             (patient_id,)
#         )
#         result = cursor.fetchone()
#         cursor.close()
#         conn.close()

#         if result:
#             name, email, age, gender, phone = result
#             response = (
#                 f"🧑 **Your Profile**\n\n"
#                 f"• 🔹 Name: {name}\n"
#                 f"• 📧 Email: {email}\n"
#                 f"• 🎂 Age: {age}\n"
#                 f"•  ⚧ Gender: {gender}\n"
#                 f"• 📱 Phone: {phone}\n"
#             )
#             dispatcher.utter_message(text=response)
#         else:
#             dispatcher.utter_message(text="❌ I could not find your details.")

#         return []


# # -------------------------------------------------------------------
# #  Show Upcoming Appointments
# # -------------------------------------------------------------------
# class ActionShowAppointments(Action):
#     def name(self) -> Text:
#         return "action_show_appointments"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         patient_id = tracker.sender_id
#         conn = get_db_connection()
#         cursor = conn.cursor()

#         query = """
#         SELECT 
#             a.id AS appointment_id,
#             a.date,
#             s.time_label,
#             d.name AS doctor_name,
#             t.name AS therapy_name,
#             a.status
#         FROM appointments a
#         JOIN doctors d ON a.doctor_id = d.id
#         JOIN therapies t ON a.therapy_id = t.id
#         JOIN slots s ON a.slot_id = s.id
#         WHERE a.patient_id = %s
#           AND a.date >= CURDATE()
#           AND a.status = 'Scheduled'
#         ORDER BY a.date, s.time_label;
#         """
#         cursor.execute(query, (patient_id,))
#         appointments = cursor.fetchall()
#         cursor.close()
#         conn.close()

#         if appointments:
#             text = "📅 **Your Upcoming Appointments**\n\n"
#             for appt in appointments:
#                 appt_id, date, time_label, doctor_name, therapy_name, status = appt
#                 text += (
#                     f"🆔 ID: {appt_id}\n"
#                     f"📅 Date: {date}\n"
#                     f"⏰ Time: {time_label}\n"
#                     f"👨‍⚕️ Doctor: {doctor_name}\n"
#                     f"💆 Therapy: {therapy_name}\n"
#                     f"📌 Status: {status}\n"
#                     f"\n\n"
#                 )
#             dispatcher.utter_message(text=text)
#         else:
#             dispatcher.utter_message(text="✅ You have no upcoming appointments.")

#         return []


# # -------------------------------------------------------------------
# #  Cancel Appointment
# # -------------------------------------------------------------------
# class ActionCancelAppointment(Action):
#     def name(self) -> Text:
#         return "action_cancel_appointment"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         patient_id = tracker.sender_id
#         conn = get_db_connection()
#         cursor = conn.cursor()

#         cancel_query = """
#         UPDATE appointments
#         SET status = 'Cancelled'
#         WHERE id = (
#             SELECT id FROM (
#                 SELECT id
#                 FROM appointments
#                 WHERE patient_id = %s AND status = 'Scheduled'
#                 ORDER BY date DESC, slot_id DESC
#                 LIMIT 1
#             ) AS subquery
#         )
#         """
#         cursor.execute(cancel_query, (patient_id,))
#         conn.commit()
#         rows_updated = cursor.rowcount
#         cursor.close()
#         conn.close()

#         if rows_updated > 0:
#             dispatcher.utter_message(text="❌ Your latest appointment has been *cancelled*.")
#         else:
#             dispatcher.utter_message(text="ℹ️ You have no scheduled appointments to cancel.")

#         return []


# # -------------------------------------------------------------------
# #  Doctors + Therapies Offered
# # -------------------------------------------------------------------
# class ActionAskDoctors(Action):
#     def name(self):
#         return "action_ask_doctors"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: dict):

#         conn = get_db_connection()
#         cursor = conn.cursor()

#         query = """
#         SELECT d.id, d.name, d.specialization, d.center, d.rating, d.available_days,
#                GROUP_CONCAT(DISTINCT t.name SEPARATOR ', ')
#         FROM doctors d
#         LEFT JOIN doctor_therapies dt ON d.id = dt.doctor_id
#         LEFT JOIN therapies t ON dt.therapy_id = t.id
#         GROUP BY d.id;
#         """
#         cursor.execute(query)
#         rows = cursor.fetchall()

#         if not rows:
#             dispatcher.utter_message("⚠️ No doctors found in the database.")
#         else:
#             response = "👨‍⚕️ **Available Doctors**\n\n"
#             for row in rows:
#                 (doc_id, name, specialization, center, rating, days, therapies) = row
#                 response += (
#                     f"👨‍⚕️ *{name}* ({specialization})\n"
#                     f"   🏥 Center: {center}\n"
#                     f"   ⭐ Rating: {rating}\n"
#                     f"   📅 Available: {days}\n"
#                     f"   💆 Therapies: {therapies if therapies else 'None'}\n"
#                     f"\n\n"
#                 )

#             dispatcher.utter_message(response)

#         cursor.close()
#         conn.close()
#         return []


# # -------------------------------------------------------------------
# #  Therapies + Doctors Offering Them
# # -------------------------------------------------------------------
# class ActionAskTherapies(Action):
#     def name(self):
#         return "action_ask_therapies"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: dict):

#         conn = get_db_connection()
#         cursor = conn.cursor()

#         query = """
#         SELECT t.id, t.name, t.description, t.duration_minutes, t.cost,
#                t.precautions_pre, t.precautions_post,
#                GROUP_CONCAT(DISTINCT d.name SEPARATOR ', ')
#         FROM therapies t
#         LEFT JOIN doctor_therapies dt ON t.id = dt.therapy_id
#         LEFT JOIN doctors d ON dt.doctor_id = d.id
#         GROUP BY t.id;
#         """
#         cursor.execute(query)
#         rows = cursor.fetchall()

#         if not rows:
#             dispatcher.utter_message("⚠️ No therapies found in the database.")
#         else:
#             response = "💆 **Available Therapies**\n\n"
#             for row in rows:
#                 (tid, name, desc, duration, cost, pre, post, doctors) = row
#                 response += (
#                     f"💆 *{name}*\n"
#                     f"   📝 {desc}\n"
#                     f"   ⏱ Duration: {duration} mins\n"
#                     f"   💰 Cost: ₹{cost}\n"
#                     f"   ⚠️ Pre-care: {pre}\n"
#                     f"   ✅ Post-care: {post}\n"
#                     f"   👨‍⚕️ Doctors: {doctors if doctors else 'No doctor assigned'}\n"
#                     f"\n\n"
#                 )

#             dispatcher.utter_message(response)

#         cursor.close()
#         conn.close()
#         return []



# class ActionTriggerPopup(Action):

#     def name(self) -> Text:
#         return "action_trigger_popup"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         dispatcher.utter_message(text="Sure! Please use the appointment popup to book your slot.")
#         return []























































# # phase 7






# from typing import Any, Text, Dict, List
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
# import MySQLdb


# # -------------------------------------------------------------------
# # Helper: Database Connection
# # -------------------------------------------------------------------
# def get_db_connection():
#     return MySQLdb.connect(
#         host="localhost",
#         user="root",
#         passwd="-",
#         db="ayursutra"
#     )


# # -------------------------------------------------------------------
# #  Greeting
# # -------------------------------------------------------------------
# class ActionGreet(Action):
#     def name(self) -> Text:
#         return "action_greet"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         dispatcher.utter_message(
#             text="👋 Hello! Welcome to *Ayursutra*.\n\nHow can I help you today?"
#         )
#         return []


# # -------------------------------------------------------------------
# #  User Info
# # -------------------------------------------------------------------
# class ActionUserInfo(Action):
#     def name(self) -> Text:
#         return "action_user_info"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         patient_id = tracker.sender_id

#         conn = get_db_connection()
#         cursor = conn.cursor()
#         cursor.execute(
#             "SELECT name, email, age, gender, phone FROM patients WHERE id=%s",
#             (patient_id,)
#         )
#         result = cursor.fetchone()
#         cursor.close()
#         conn.close()

#         if result:
#             name, email, age, gender, phone = result
#             response = (
#                 f"🧑 **Your Profile**\n\n"
#                 f"• 🔹 Name: {name}\n"
#                 f"• 📧 Email: {email}\n"
#                 f"• 🎂 Age: {age}\n"
#                 f"•  ⚧ Gender: {gender}\n"
#                 f"• 📱 Phone: {phone}\n"
#             )
#             dispatcher.utter_message(text=response)
#         else:
#             dispatcher.utter_message(text="❌ I could not find your details.")

#         return []


# # -------------------------------------------------------------------
# #  Show Upcoming Appointments
# # -------------------------------------------------------------------
# class ActionShowAppointments(Action):
#     def name(self) -> Text:
#         return "action_show_appointments"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         patient_id = tracker.sender_id
#         conn = get_db_connection()
#         cursor = conn.cursor()

#         query = """
#         SELECT 
#             a.id AS appointment_id,
#             a.date,
#             s.time_label,
#             d.name AS doctor_name,
#             t.name AS therapy_name,
#             a.status
#         FROM appointments a
#         JOIN doctors d ON a.doctor_id = d.id
#         JOIN therapies t ON a.therapy_id = t.id
#         JOIN slots s ON a.slot_id = s.id
#         WHERE a.patient_id = %s
#           AND a.date >= CURDATE()
#           AND a.status = 'Scheduled'
#         ORDER BY a.date, s.time_label;
#         """
#         cursor.execute(query, (patient_id,))
#         appointments = cursor.fetchall()
#         cursor.close()
#         conn.close()

#         if appointments:
#             text = "📅 **Your Upcoming Appointments**\n\n"
#             for appt in appointments:
#                 appt_id, date, time_label, doctor_name, therapy_name, status = appt
#                 text += (
#                     f"🆔 ID: {appt_id}\n"
#                     f"📅 Date: {date}\n"
#                     f"⏰ Time: {time_label}\n"
#                     f"👨‍⚕️ Doctor: {doctor_name}\n"
#                     f"💆 Therapy: {therapy_name}\n"
#                     f"📌 Status: {status}\n"
#                     f"\n\n"
#                 )
#             dispatcher.utter_message(text=text)
#         else:
#             dispatcher.utter_message(text="✅ You have no upcoming appointments.")

#         return []


# # -------------------------------------------------------------------
# #  Cancel Appointment
# # -------------------------------------------------------------------
# class ActionCancelAppointment(Action):
#     def name(self) -> Text:
#         return "action_cancel_appointment"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         patient_id = tracker.sender_id
#         conn = get_db_connection()
#         cursor = conn.cursor()

#         cancel_query = """
#         UPDATE appointments
#         SET status = 'Cancelled'
#         WHERE id = (
#             SELECT id FROM (
#                 SELECT id
#                 FROM appointments
#                 WHERE patient_id = %s AND status = 'Scheduled'
#                 ORDER BY date DESC, slot_id DESC
#                 LIMIT 1
#             ) AS subquery
#         )
#         """
#         cursor.execute(cancel_query, (patient_id,))
#         conn.commit()
#         rows_updated = cursor.rowcount
#         cursor.close()
#         conn.close()

#         if rows_updated > 0:
#             dispatcher.utter_message(text="❌ Your latest appointment has been *cancelled*.")
#         else:
#             dispatcher.utter_message(text="ℹ️ You have no scheduled appointments to cancel.")

#         return []


# # -------------------------------------------------------------------
# #  Doctors + Therapies Offered
# # -------------------------------------------------------------------
# class ActionAskDoctors(Action):
#     def name(self):
#         return "action_ask_doctors"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: dict):

#         conn = get_db_connection()
#         cursor = conn.cursor()

#         query = """
#         SELECT d.id, d.name, d.specialization, d.center, d.rating, d.available_days,
#                GROUP_CONCAT(DISTINCT t.name SEPARATOR ', ')
#         FROM doctors d
#         LEFT JOIN doctor_therapies dt ON d.id = dt.doctor_id
#         LEFT JOIN therapies t ON dt.therapy_id = t.id
#         GROUP BY d.id;
#         """
#         cursor.execute(query)
#         rows = cursor.fetchall()

#         if not rows:
#             dispatcher.utter_message("⚠️ No doctors found in the database.")
#         else:
#             response = "👨‍⚕️ **Available Doctors**\n\n"
#             for row in rows:
#                 (doc_id, name, specialization, center, rating, days, therapies) = row
#                 response += (
#                     f"👨‍⚕️ *{name}* ({specialization})\n"
#                     f"   🏥 Center: {center}\n"
#                     f"   ⭐ Rating: {rating}\n"
#                     f"   📅 Available: {days}\n"
#                     f"   💆 Therapies: {therapies if therapies else 'None'}\n"
#                     f"\n\n"
#                 )

#             dispatcher.utter_message(response)

#         cursor.close()
#         conn.close()
#         return []


# # -------------------------------------------------------------------
# #  Therapies + Doctors Offering Them
# # -------------------------------------------------------------------
# class ActionAskTherapies(Action):
#     def name(self):
#         return "action_ask_therapies"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: dict):

#         conn = get_db_connection()
#         cursor = conn.cursor()

#         query = """
#         SELECT t.id, t.name, t.description, t.duration_minutes, t.cost,
#                t.precautions_pre, t.precautions_post,
#                GROUP_CONCAT(DISTINCT d.name SEPARATOR ', ')
#         FROM therapies t
#         LEFT JOIN doctor_therapies dt ON t.id = dt.therapy_id
#         LEFT JOIN doctors d ON dt.doctor_id = d.id
#         GROUP BY t.id;
#         """
#         cursor.execute(query)
#         rows = cursor.fetchall()

#         if not rows:
#             dispatcher.utter_message("⚠️ No therapies found in the database.")
#         else:
#             response = "💆 **Available Therapies**\n\n"
#             for row in rows:
#                 (tid, name, desc, duration, cost, pre, post, doctors) = row
#                 response += (
#                     f"💆 *{name}*\n"
#                     f"   📝 {desc}\n"
#                     f"   ⏱ Duration: {duration} mins\n"
#                     f"   💰 Cost: ₹{cost}\n"
#                     f"   ⚠️ Pre-care: {pre}\n"
#                     f"   ✅ Post-care: {post}\n"
#                     f"   👨‍⚕️ Doctors: {doctors if doctors else 'No doctor assigned'}\n"
#                     f"\n\n"
#                 )

#             dispatcher.utter_message(response)

#         cursor.close()
#         conn.close()
#         return []



# # class ActionTriggerPopup(Action):

# #     def name(self) -> Text:
# #         return "action_trigger_popup"

# #     def run(self, dispatcher: CollectingDispatcher,
# #             tracker: Tracker,
# #             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

# #         dispatcher.utter_message(text="Sure! Please use the appointment popup to book your slot.")
# #         return []


# class ActionTriggerPopup(Action):
#     def name(self) -> Text:
#         return "action_trigger_popup"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         dispatcher.utter_message(
#             # text="Sure! Please use the appointment popup to book your slot.",
#             text="📅 Let’s book your appointment! Please fill the details below.",

#             json_message={"open_modal": True}
#         )
#         return []

























# phase 8






from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import MySQLdb


# -------------------------------------------------------------------
# Helper: Database Connection
# -------------------------------------------------------------------
def get_db_connection():
    return MySQLdb.connect(
        host="localhost",
        user="root",
        passwd="-",
        db="ayursutra"
    )


# -------------------------------------------------------------------
#  Greeting
# -------------------------------------------------------------------
class ActionGreet(Action):
    def name(self) -> Text:
        return "action_greet"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(
            text="👋 Hello! Welcome to *Ayursutra*.\n\nHow can I help you today?"
        )
        return []


# -------------------------------------------------------------------
#  User Info
# -------------------------------------------------------------------
class ActionUserInfo(Action):
    def name(self) -> Text:
        return "action_user_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        patient_id = tracker.sender_id

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT name, email, age, gender, phone FROM patients WHERE id=%s",
            (patient_id,)
        )
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        if result:
            name, email, age, gender, phone = result
            response = (
                f"🧑 **Your Profile**\n\n"
                f"• 🔹 Name: {name}\n"
                f"• 📧 Email: {email}\n"
                f"• 🎂 Age: {age}\n"
                f"•  ⚧ Gender: {gender}\n"
                f"• 📱 Phone: {phone}\n"
            )
            dispatcher.utter_message(text=response)
        else:
            dispatcher.utter_message(text="❌ I could not find your details.")

        return []


# -------------------------------------------------------------------
#  Show Upcoming Appointments
# -------------------------------------------------------------------
class ActionShowAppointments(Action):
    def name(self) -> Text:
        return "action_show_appointments"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        patient_id = tracker.sender_id
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
        SELECT 
            a.id AS appointment_id,
            a.date,
            s.time_label,
            d.name AS doctor_name,
            t.name AS therapy_name,
            a.status
        FROM appointments a
        JOIN doctors d ON a.doctor_id = d.id
        JOIN therapies t ON a.therapy_id = t.id
        JOIN slots s ON a.slot_id = s.id
        WHERE a.patient_id = %s
          AND a.date >= CURDATE()
          AND a.status = 'Scheduled'
        ORDER BY a.date, s.time_label;
        """
        cursor.execute(query, (patient_id,))
        appointments = cursor.fetchall()
        cursor.close()
        conn.close()

        if appointments:
            text = "📅 **Your Upcoming Appointments**\n\n"
            for appt in appointments:
                appt_id, date, time_label, doctor_name, therapy_name, status = appt
                text += (
                    f"🆔 ID: {appt_id}\n"
                    f"📅 Date: {date}\n"
                    f"⏰ Time: {time_label}\n"
                    f"👨‍⚕️ Doctor: {doctor_name}\n"
                    f"💆 Therapy: {therapy_name}\n"
                    f"📌 Status: {status}\n"
                    f"\n\n"
                )
            dispatcher.utter_message(text=text)
        else:
            dispatcher.utter_message(text="✅ You have no upcoming appointments.")

        return []


# -------------------------------------------------------------------
#  Cancel Appointment
# -------------------------------------------------------------------
# class ActionCancelAppointment(Action):
#     def name(self) -> Text:
#         return "action_cancel_appointment"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         patient_id = tracker.sender_id
#         conn = get_db_connection()
#         cursor = conn.cursor()

#         cancel_query = """
#         UPDATE appointments
#         SET status = 'Cancelled'
#         WHERE id = (
#             SELECT id FROM (
#                 SELECT id
#                 FROM appointments
#                 WHERE patient_id = %s AND status = 'Scheduled'
#                 ORDER BY date DESC, slot_id DESC
#                 LIMIT 1
#             ) AS subquery
#         )
#         """
#         cursor.execute(cancel_query, (patient_id,))
#         conn.commit()
#         rows_updated = cursor.rowcount
#         cursor.close()
#         conn.close()

#         if rows_updated > 0:
#             dispatcher.utter_message(text="❌ Your latest appointment has been *cancelled*.")
#         else:
#             dispatcher.utter_message(text="ℹ️ You have no scheduled appointments to cancel.")

#         return []





# class ActionCancelAppointment(Action):
#     def name(self) -> Text:
#         return "action_cancel_appointment"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         patient_id = tracker.sender_id
#         conn = get_db_connection()
#         cursor = conn.cursor()

#         # Get latest scheduled appointment
#         cursor.execute("""
#             SELECT id, date, therapy_id 
#             FROM appointments
#             WHERE patient_id=%s AND status='Scheduled'
#             ORDER BY date DESC, slot_id DESC
#             LIMIT 1
#         """, (patient_id,))
#         appt = cursor.fetchone()

#         if not appt:
#             dispatcher.utter_message(text="ℹ️ You have no scheduled appointments to cancel.")
#             cursor.close()
#             conn.close()
#             return []

#         appt_id, date, therapy_id = appt

#         # Cancel the appointment
#         cursor.execute("""
#             UPDATE appointments
#             SET status='Cancelled'
#             WHERE id=%s
#         """, (appt_id,))
#         conn.commit()

#         # Add notification
#         message = f"Your appointment on {date} has been cancelled."
#         cursor.execute("""
#             INSERT INTO notifications (patient_id, appointment_id, type, message, channel)
#             VALUES (%s, %s, %s, %s, %s)
#         """, (patient_id, appt_id, 'Pre-Procedure', message, 'InApp'))
#         conn.commit()

#         cursor.close()
#         conn.close()

#         dispatcher.utter_message(text="❌ Your latest appointment has been *cancelled* and notification sent.")
#         return []


class ActionCancelAppointment(Action):
    def name(self) -> Text:
        return "action_cancel_appointment"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        patient_id = tracker.sender_id
        conn = get_db_connection()
        cursor = conn.cursor()

        # Get latest scheduled appointment
        cursor.execute("""
            SELECT id, date, therapy_id, doctor_id, slot_id
            FROM appointments
            WHERE patient_id=%s AND status='Scheduled'
            ORDER BY date DESC, slot_id DESC
            LIMIT 1
        """, (patient_id,))
        appt = cursor.fetchone()

        if not appt:
            dispatcher.utter_message(text="ℹ️ You have no scheduled appointments to cancel.")
            cursor.close()
            conn.close()
            return []

        appt_id, date, therapy_id, doctor_id, slot_id = appt

        # Get doctor, therapy, and slot details
        cursor.execute("SELECT name FROM doctors WHERE id=%s", (doctor_id,))
        doctor_name = cursor.fetchone()[0]

        cursor.execute("SELECT name FROM therapies WHERE id=%s", (therapy_id,))
        therapy_name = cursor.fetchone()[0]

        cursor.execute("SELECT time_label FROM slots WHERE id=%s", (slot_id,))
        time_label = cursor.fetchone()[0]

        # Cancel the appointment
        cursor.execute("""
            UPDATE appointments
            SET status='Cancelled'
            WHERE id=%s
        """, (appt_id,))
        conn.commit()

        # Add notification with full info
        message = f"Appointment cancelled: {therapy_name} with Dr. {doctor_name} on {date} at {time_label}."
        cursor.execute("""
            INSERT INTO notifications (patient_id, appointment_id, type, message, channel)
            VALUES (%s, %s, %s, %s, %s)
        """, (patient_id, appt_id, 'Pre-Procedure', message, 'InApp'))
        conn.commit()

        cursor.close()
        conn.close()

        dispatcher.utter_message(text="❌ Your latest appointment has been *cancelled* and notification sent.")
        return []

# -------------------------------------------------------------------
#  Doctors + Therapies Offered
# -------------------------------------------------------------------
class ActionAskDoctors(Action):
    def name(self):
        return "action_ask_doctors"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict):

        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
        SELECT d.id, d.name, d.specialization, d.center, d.rating, d.available_days,
               GROUP_CONCAT(DISTINCT t.name SEPARATOR ', ')
        FROM doctors d
        LEFT JOIN doctor_therapies dt ON d.id = dt.doctor_id
        LEFT JOIN therapies t ON dt.therapy_id = t.id
        GROUP BY d.id;
        """
        cursor.execute(query)
        rows = cursor.fetchall()

        if not rows:
            dispatcher.utter_message("⚠️ No doctors found in the database.")
        else:
            response = "👨‍⚕️ **Available Doctors**\n\n"
            for row in rows:
                (doc_id, name, specialization, center, rating, days, therapies) = row
                response += (
                    f"👨‍⚕️ *{name}* ({specialization})\n"
                    f"   🏥 Center: {center}\n"
                    f"   ⭐ Rating: {rating}\n"
                    f"   📅 Available: {days}\n"
                    f"   💆 Therapies: {therapies if therapies else 'None'}\n"
                    f"\n\n"
                )

            dispatcher.utter_message(response)

        cursor.close()
        conn.close()
        return []


# -------------------------------------------------------------------
#  Therapies + Doctors Offering Them
# -------------------------------------------------------------------
class ActionAskTherapies(Action):
    def name(self):
        return "action_ask_therapies"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict):

        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
        SELECT t.id, t.name, t.description, t.duration_minutes, t.cost,
               t.precautions_pre, t.precautions_post,
               GROUP_CONCAT(DISTINCT d.name SEPARATOR ', ')
        FROM therapies t
        LEFT JOIN doctor_therapies dt ON t.id = dt.therapy_id
        LEFT JOIN doctors d ON dt.doctor_id = d.id
        GROUP BY t.id;
        """
        cursor.execute(query)
        rows = cursor.fetchall()

        if not rows:
            dispatcher.utter_message("⚠️ No therapies found in the database.")
        else:
            response = "💆 **Available Therapies**\n\n"
            for row in rows:
                (tid, name, desc, duration, cost, pre, post, doctors) = row
                response += (
                    f"💆 *{name}*\n"
                    f"   📝 {desc}\n"
                    f"   ⏱ Duration: {duration} mins\n"
                    f"   💰 Cost: ₹{cost}\n"
                    f"   ⚠️ Pre-care: {pre}\n"
                    f"   ✅ Post-care: {post}\n"
                    f"   👨‍⚕️ Doctors: {doctors if doctors else 'No doctor assigned'}\n"
                    f"\n\n"
                )

            dispatcher.utter_message(response)

        cursor.close()
        conn.close()
        return []



# class ActionTriggerPopup(Action):

#     def name(self) -> Text:
#         return "action_trigger_popup"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         dispatcher.utter_message(text="Sure! Please use the appointment popup to book your slot.")
#         return []


class ActionTriggerPopup(Action):
    def name(self) -> Text:
        return "action_trigger_popup"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(
            # text="Sure! Please use the appointment popup to book your slot.",
            text="📅 Let’s book your appointment! Please fill the details below.",

            json_message={"open_modal": True}
        )
        return []





