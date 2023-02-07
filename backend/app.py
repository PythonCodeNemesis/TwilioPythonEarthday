from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from twilio.rest import Client
import schedule
import time

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Your Twilio account sid and auth token
client = Client("SID", "TOKEN")

# A list to store phone numbers and frequency of reminders
subscribers = []

def send_reminders():
  for subscriber in subscribers:
    phone_number = subscriber["phone_number"]
    message = client.messages.create(
      to=phone_number,
      from_="YOUR TWILIO NUMBER",
      body="Don't forget to practice eco-friendly habits like turning off lights when leaving a room or using reusable bags!"
    )

@app.route("/sign-up", methods=["POST"])
@cross_origin()
def sign_up():
  data = request.get_json()
  phone_number = data["phoneNumber"]
  frequency = data["frequency"]
  print(phone_number)

  # Add the phone number and frequency to the subscribers list
  subscribers.append({"phone_number": phone_number, "frequency": frequency})

  # Send a confirmation message to the user
  message = client.messages.create(
    to=phone_number,
    from_="YOUR TWILIO NUMBER",
    body="Successfully signed up for eco-friendly reminders!"
  )

  return "{\"status\" : \"ok\"}", 200

if __name__ == "__main__":
  # Schedule the send_reminders function to run at the frequency specified by the user
  schedule.every(1).minutes.do(send_reminders)

  while True:
    schedule.run_pending()
    #time.sleep(1)

    app.run(debug=True)
