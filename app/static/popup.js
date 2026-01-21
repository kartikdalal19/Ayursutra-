// const API_BASE = "http://127.0.0.1:5000"; // Flask appointment_api

// function openModal() {
//   document.getElementById("bookingModal").style.display = "block";
//   loadTherapies();
// }
// function closeModal() {
//   document.getElementById("bookingModal").style.display = "none";
// }

// async function loadTherapies() {
//   const res = await fetch(`${API_BASE}/therapies`);
//   const therapies = await res.json();
//   const select = document.getElementById("therapySelect");
//   select.innerHTML = "<option value=''>Select Therapy</option>";
//   therapies.forEach(t => {
//     select.innerHTML += `<option value="${t.id}">${t.name}</option>`;
//   });
//   select.onchange = () => loadDoctors(select.value);
// }

// async function loadDoctors(therapyId) {
//   const res = await fetch(`${API_BASE}/doctors/${therapyId}`);
//   const doctors = await res.json();
//   const select = document.getElementById("doctorSelect");
//   select.innerHTML = "<option value=''>Select Doctor</option>";
//   doctors.forEach(d => {
//     select.innerHTML += `<option value="${d.id}">${d.name} (${d.specialization})</option>`;
//   });

//   select.onchange = () => {
//     const dateInput = document.getElementById("dateInput");
//     dateInput.onchange = () => loadSlots(select.value, dateInput.value);
//   };
// }

// async function loadSlots(doctorId, date) {
//   const res = await fetch(`${API_BASE}/slots/${doctorId}/${date}`);
//   const slots = await res.json();
//   const select = document.getElementById("slotSelect");
//   select.innerHTML = "<option value=''>Select Slot</option>";
//   slots.forEach(s => {
//     select.innerHTML += `<option value="${s.id}">${s.time_label}</option>`;
//   });
// }

// async function bookAppointment() {
//   const therapyId = document.getElementById("therapySelect").value;
//   const doctorId = document.getElementById("doctorSelect").value;
//   const date = document.getElementById("dateInput").value;
//   const slotId = document.getElementById("slotSelect").value;

//   if (!therapyId || !doctorId || !date || !slotId) {
//     document.getElementById("message").innerText = "Please fill all fields.";
//     return;
//   }

//   const res = await fetch(`${API_BASE}/book`, {
//     method: "POST",
//     headers: { "Content-Type": "application/json" },
//     body: JSON.stringify({
//       doctor_id: doctorId,
//       therapy_id: therapyId,
//       slot_id: slotId,
//       date: date
//     })
//   });

//   const data = await res.json();
//   document.getElementById("message").innerText = data.message;
// }









































// const API_BASE = "http://127.0.0.1:5000"; // Flask backend

// function openModal() {
//   document.getElementById("bookingModal").style.display = "block";
//   loadTherapies();
// }

// function closeModal() {
//   document.getElementById("bookingModal").style.display = "none";
// }

// // ---------------- Load Dropdowns ----------------
// async function loadTherapies() {
//   const res = await fetch(`${API_BASE}/therapies`);
//   const therapies = await res.json();
//   const select = document.getElementById("therapySelect");
//   select.innerHTML = "<option value=''>Select Therapy</option>";
//   therapies.forEach(t => {
//     select.innerHTML += `<option value="${t.id}">${t.name}</option>`;
//   });
//   select.onchange = () => loadDoctors(select.value);
// }

// async function loadDoctors(therapyId) {
//   const res = await fetch(`${API_BASE}/doctors/${therapyId}`);
//   const doctors = await res.json();
//   const select = document.getElementById("doctorSelect");
//   select.innerHTML = "<option value=''>Select Doctor</option>";
//   doctors.forEach(d => {
//     select.innerHTML += `<option value="${d.id}">${d.name} (${d.specialization})</option>`;
//   });

//   select.onchange = () => {
//     const dateInput = document.getElementById("dateInput");
//     dateInput.onchange = () => loadSlots(select.value, dateInput.value);
//   };
// }

// async function loadSlots(doctorId, date) {
//   const res = await fetch(`${API_BASE}/slots/${doctorId}/${date}`);
//   const slots = await res.json();
//   const select = document.getElementById("slotSelect");
//   select.innerHTML = "<option value=''>Select Slot</option>";
//   slots.forEach(s => {
//     select.innerHTML += `<option value="${s.id}">${s.time_label}</option>`;
//   });
// }

// // ---------------- Book Appointment ----------------
// async function bookAppointment() {
//   const therapyId = document.getElementById("therapySelect").value;
//   const doctorId = document.getElementById("doctorSelect").value;
//   const date = document.getElementById("dateInput").value;
//   const slotId = document.getElementById("slotSelect").value;

//   if (!therapyId || !doctorId || !date || !slotId) {
//     document.getElementById("message").innerText = "Please fill all fields.";
//     return;
//   }

//   const res = await fetch(`${API_BASE}/book`, {
//     method: "POST",
//     headers: { "Content-Type": "application/json" },
//     body: JSON.stringify({
//       doctor_id: doctorId,
//       therapy_id: therapyId,
//       slot_id: slotId,
//       date: date
//     })
//   });

//   const data = await res.json();
//   document.getElementById("message").innerText = data.message;
// }

// // ---------------- Chat Integration ----------------
// const chatbox = document.getElementById("chatbox");
// const input = document.getElementById("userInput");
// document.getElementById("sendBtn").onclick = sendMessage;

// async function sendMessage() {
//   const text = input.value;
//   if (!text) return;

//   chatbox.innerHTML += `<p class="userMsg">You: ${text}</p>`;
//   input.value = "";

//   const res = await fetch("/send_message", {
//     method: "POST",
//     headers: { "Content-Type": "application/json" },
//     body: JSON.stringify({ message: text })
//   });

//   const data = await res.json();

//   if (data.length > 0) {
//     data.forEach(msg => {
//       chatbox.innerHTML += `<p class="botMsg">Bot: ${msg.text}</p>`;

//       // Trigger popup automatically if Rasa suggests booking
//       if (msg.text.toLowerCase().includes("appointment")) {
//         openModal();
//       }
//     });
//   }
//   chatbox.scrollTop = chatbox.scrollHeight;
// }



































// -----------------------------------------------------------------------------------------------------------
// popup.js


// const API_BASE = "http://127.0.0.1:5000"; // Flask backend

// // ---------------- Modal Controls ----------------
// function openModal() {
//   document.getElementById("bookingModal").style.display = "block";
//   loadTherapies();
// }

// function closeModal() {
//   document.getElementById("bookingModal").style.display = "none";
// }

// // ---------------- Load Dropdowns ----------------
// async function loadTherapies() {
//   const res = await fetch(`${API_BASE}/therapies`);
//   const therapies = await res.json();
//   const select = document.getElementById("therapySelect");
//   select.innerHTML = "<option value=''>Select Therapy</option>";
//   therapies.forEach(t => {
//     select.innerHTML += `<option value="${t.id}">${t.name}</option>`;
//   });
//   select.onchange = () => loadDoctors(select.value);
// }

// async function loadDoctors(therapyId) {
//   const res = await fetch(`${API_BASE}/doctors/${therapyId}`);
//   const doctors = await res.json();
//   const select = document.getElementById("doctorSelect");
//   select.innerHTML = "<option value=''>Select Doctor</option>";
//   doctors.forEach(d => {
//     select.innerHTML += `<option value="${d.id}">${d.name} (${d.specialization})</option>`;
//   });

//   select.onchange = () => {
//     const dateInput = document.getElementById("dateInput");
//     dateInput.onchange = () => loadSlots(select.value, dateInput.value);
//   };
// }

// async function loadSlots(doctorId, date) {
//   const res = await fetch(`${API_BASE}/slots/${doctorId}/${date}`);
//   const slots = await res.json();
//   const select = document.getElementById("slotSelect");
//   select.innerHTML = "<option value=''>Select Slot</option>";
//   slots.forEach(s => {
//     select.innerHTML += `<option value="${s.id}">${s.time_label}</option>`;
//   });
// }

// // ---------------- Book Appointment ----------------
// async function bookAppointment() {
//   const therapyId = document.getElementById("therapySelect").value;
//   const doctorId = document.getElementById("doctorSelect").value;
//   const date = document.getElementById("dateInput").value;
//   const slotId = document.getElementById("slotSelect").value;

//   if (!therapyId || !doctorId || !date || !slotId) {
//     document.getElementById("message").innerText = "⚠️ Please fill all fields.";
//     return;
//   }

//   const res = await fetch(`${API_BASE}/book`, {
//     method: "POST",
//     headers: { "Content-Type": "application/json" },
//     body: JSON.stringify({
//       doctor_id: doctorId,
//       therapy_id: therapyId,
//       slot_id: slotId,
//       date: date
//     })
//   });

//   const data = await res.json();
//   document.getElementById("message").innerText = data.message;
// }

// // ---------------- Chat Integration ----------------
// const chatbox = document.getElementById("chatbox");
// const input = document.getElementById("userInput");
// document.getElementById("sendBtn").onclick = sendMessage;

// async function sendMessage() {
//   const text = input.value;
//   if (!text) return;

//   // User bubble
//   const userMsg = document.createElement("div");
//   userMsg.className = "msg-card userMsg";
//   userMsg.textContent = text;
//   chatbox.appendChild(userMsg);

//   input.value = "";

//   const res = await fetch("/send_message", {
//     method: "POST",
//     headers: { "Content-Type": "application/json" },
//     body: JSON.stringify({ message: text })
//   });

//   const data = await res.json();

//   if (data.length > 0) {
//     data.forEach(msg => {
//       const botMsg = document.createElement("div");
//       botMsg.className = "msg-card botMsg";

//       if (msg.cards) {
//         const cardList = document.createElement("div");
//         cardList.className = "card-list";
//         msg.cards.forEach(c => {
//           const card = document.createElement("div");
//           card.className = "info-card";
//           card.innerHTML = `<h4>${c.title}</h4><p>${c.desc}</p>`;
//           cardList.appendChild(card);
//         });
//         botMsg.appendChild(cardList);
//       } else {
//         botMsg.textContent = msg.text;
//       }

//       chatbox.appendChild(botMsg);

//       // Auto trigger popup if appointment is mentioned
//       if (msg.text && msg.text.toLowerCase().includes("appointment")) {
//         openModal();
//       }
//     });
//   }
//   chatbox.scrollTop = chatbox.scrollHeight;
// }























// popup.js

const API_BASE = "http://127.0.0.1:5000"; // Flask backend

// ---------------- Modal Controls ----------------
function openModal() {
  document.getElementById("bookingModal").style.display = "block";
  loadTherapies();
}

function closeModal() {
  document.getElementById("bookingModal").style.display = "none";
}

// ---------------- Load Dropdowns ----------------
async function loadTherapies() {
  const res = await fetch(`${API_BASE}/therapies`);
  const therapies = await res.json();
  const select = document.getElementById("therapySelect");
  select.innerHTML = "<option value=''>Select Therapy</option>";
  therapies.forEach(t => {
    select.innerHTML += `<option value="${t.id}">${t.name}</option>`;
  });
  select.onchange = () => loadDoctors(select.value);
}

async function loadDoctors(therapyId) {
  const res = await fetch(`${API_BASE}/doctors/${therapyId}`);
  const doctors = await res.json();
  const select = document.getElementById("doctorSelect");
  select.innerHTML = "<option value=''>Select Doctor</option>";
  doctors.forEach(d => {
    select.innerHTML += `<option value="${d.id}">${d.name} (${d.specialization})</option>`;
  });

  select.onchange = () => {
    const dateInput = document.getElementById("dateInput");
    dateInput.onchange = () => loadSlots(select.value, dateInput.value);
  };
}

async function loadSlots(doctorId, date) {
  const res = await fetch(`${API_BASE}/slots/${doctorId}/${date}`);
  const slots = await res.json();
  const select = document.getElementById("slotSelect");
  select.innerHTML = "<option value=''>Select Slot</option>";
  slots.forEach(s => {
    select.innerHTML += `<option value="${s.id}">${s.time_label}</option>`;
  });
}

// ---------------- Book Appointment ----------------
async function bookAppointment() {
  const therapyId = document.getElementById("therapySelect").value;
  const doctorId = document.getElementById("doctorSelect").value;
  const date = document.getElementById("dateInput").value;
  const slotId = document.getElementById("slotSelect").value;

  if (!therapyId || !doctorId || !date || !slotId) {
    document.getElementById("message").innerText = "⚠️ Please fill all fields.";
    return;
  }

  const res = await fetch(`${API_BASE}/book`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      doctor_id: doctorId,
      therapy_id: therapyId,
      slot_id: slotId,
      date: date
    })
  });

  const data = await res.json();
  document.getElementById("message").innerText = data.message;
}

// ---------------- Chat Integration ----------------
const chatbox = document.getElementById("chatbox");
const input = document.getElementById("userInput");
document.getElementById("sendBtn").onclick = sendMessage;

async function sendMessage() {
  const text = input.value;
  if (!text) return;

  // User bubble
  const userMsg = document.createElement("div");
  userMsg.className = "msg-card userMsg";
  userMsg.textContent = text;
  chatbox.appendChild(userMsg);

  input.value = "";

  const res = await fetch("/send_message", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: text })
  });

  const data = await res.json();

  if (data.length > 0) {
    data.forEach(msg => {
      const botMsg = document.createElement("div");
      botMsg.className = "msg-card botMsg";

      if (msg.cards) {
        const cardList = document.createElement("div");
        cardList.className = "card-list";
        msg.cards.forEach(c => {
          const card = document.createElement("div");
          card.className = "info-card";
          card.innerHTML = `<h4>${c.title}</h4><p>${c.desc}</p>`;
          cardList.appendChild(card);
        });
        botMsg.appendChild(cardList);
      } else {
        botMsg.textContent = msg.text;
      }

      chatbox.appendChild(botMsg);

      // ✅ Only open when bot explicitly sends open_modal flag
      // if (msg.open_modal === true) {
      //   openModal();
      // }
      // ✅ Only open when bot explicitly sends open_modal flag
      if (msg.custom && msg.custom.open_modal === true) {
        openModal();
      }

    });
  }
  chatbox.scrollTop = chatbox.scrollHeight;
}
