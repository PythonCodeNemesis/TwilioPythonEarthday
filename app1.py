from flask import Flask, request
from flask_cors import CORS, cross_origin
import vonage
from flask_apscheduler import APScheduler

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
scheduler = APScheduler()

# Your Twilio account sid and auth token
client = Client("SID", "TOKEN")


# A list to store phone numbers and frequency of reminders
subscribers = []

def send_reminders(phone_number):
  
  responseData = sms.send_message(
  {
      "from": "Vonage APIs",
      "to": phone_number,
      "text": "Drink a glass of water now!",
  }
  )


  if responseData["messages"][0]["status"] == "0":
      print("Message sent successfully.")
  else:
      print(f"Message failed with error: {responseData['messages'][0]['error-text']}")

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
  print(message["messages"])
  print(message["messages"][0])

  if message["messages"][0]["status"] == "0":
      print("Message sent successfully.")
  else:
      print(f"Message failed with error: {message['messages'][0]['error-text']}")

  scheduler.add_job(id = 'Scheduled Task', func=send_reminders, args = [phone_number], trigger="interval", minutes=int(frequency))
  print("send messge to",phone_number,"with frequency",frequency)


  return "{\"status\" : \"ok\"}", 200

if __name__ == "__main__":
  # Schedule the send_reminders function to run at the frequency specified by the user

  
  scheduler.start()
  app.run(debug=True)


