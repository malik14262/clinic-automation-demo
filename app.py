from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

sessions = {}

HTML = """
<!doctype html>
<html>
<head>
<title>Clinic Automation Demo</title>
</head>
<body style="font-family:Arial;background:#f5f5f5">
<h2>🩺 GreenCare Private Clinic – Live Demo</h2>

<div id="chat" style="background:#fff;border:1px solid #ccc;
padding:10px;height:320px;overflow:auto"></div>

<input id="msg" placeholder="Type 'hi' to start"
style="width:75%;padding:8px">
<button onclick="send()" style="padding:8px">Send</button>

<script>
function send(){
  let m = document.getElementById("msg").value;
  document.getElementById("msg").value="";
  document.getElementById("chat").innerHTML += "<b>You:</b> "+m+"<br>";

  fetch("/bot",{
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body:JSON.stringify({message:m})
  })
  .then(r=>r.json())
  .then(d=>{
    document.getElementById("chat").innerHTML +=
    "<b>Bot:</b> "+d.reply+"<br><br>";
  });
}
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/bot", methods=["POST"])
def bot():
    msg = request.json["message"].lower()
    user = "demo"

    if user not in sessions:
        sessions[user] = {"step": None}

    s = sessions[user]

    if msg in ["hi", "hello", "start"]:
        s["step"] = None
        reply = (
            "Hello 👋 Welcome to GreenCare Private Clinic<br>"
            "Please choose:<br>"
            "1️⃣ Book Appointment<br>"
            "2️⃣ Doctor Timings<br>"
            "3️⃣ Consultation Fees<br>"
            "4️⃣ Location<br>"
            "5️⃣ Services<br>"
            "6️⃣ Reset"
        )

    elif msg == "1":
        s["step"] = "name"
        reply = "Please enter patient full name:"

    elif s["step"] == "name":
        s["name"] = msg
        s["step"] = "phone"
        reply = "Please enter contact number:"

    elif s["step"] == "phone":
        s["phone"] = msg
        s["step"] = "date"
        reply = "Preferred appointment date (DD/MM):"

    elif s["step"] == "date":
        s["date"] = msg
        s["step"] = None
        reply = (
            "✅ Appointment request received!<br>"
            f"Name: {s['name']}<br>"
            f"Date: {s['date']}<br>"
            "Our team will confirm shortly."
        )

    elif msg == "2":
        reply = "🕒 Mon–Fri: 9AM–6PM<br>Sat: 10AM–2PM"

    elif msg == "3":
        reply = "💷 Consultation Fee<br>General: £60"

    elif msg == "4":
        reply = "📍 London, United Kingdom (Demo Clinic)"

    elif msg == "5":
        reply = (
            "🩺 Services:<br>"
            "• GP Consultation<br>"
            "• Blood Tests<br>"
            "• Health Checkups"
        )

    elif msg == "6":
        sessions[user] = {"step": None}
        reply = "🔄 Chat reset. Type 'hi' to start again."

    else:
        reply = "Please type 'hi' to see options."

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run()
