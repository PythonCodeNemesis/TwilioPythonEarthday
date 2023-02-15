from flask import Flask, request
from flask_cors import CORS, cross_origin
import vonage
from flask_apscheduler import APScheduler
import random

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
scheduler = APScheduler()

# Your Twilio account sid and auth token
client = Client("SID", "TOKEN")


# A list to store phone numbers and frequency of reminders
subscribers = []

# list of strings
eco_reminders = [
    "Compost food scraps and yard waste to reduce landfill waste",
    "Use reusable water bottles and coffee cups",
    "Switch to LED light bulbs to save energy",
    "Buy local and in-season produce to reduce carbon emissions from transportation",
    "Take public transportation or walk instead of driving whenever possible",
    "Fix leaky faucets to conserve water",
    "Donate or repurpose unwanted items instead of throwing them away",
    "Choose environmentally-friendly cleaning products",
    "Reduce meat consumption to reduce the environmental impact of livestock farming",
    "Use a clothesline to dry clothes instead of a dryer",
    "Take steps to reduce energy consumption in your home, such as adding insulation",
    "Avoid single-use plastics such as straws, utensils, and packaging",
    "Plant a vegetable garden to grow your own food",
    "Shop at secondhand stores to reduce the environmental impact of fast fashion",
    "Turn off the tap while brushing your teeth to conserve water",
    "Use a reusable razor or electric shaver instead of disposable razors",
    "Choose to walk or bike for short trips instead of using a car",
    "Use natural lighting whenever possible instead of turning on lights",
    "Buy products with minimal packaging to reduce waste",
    "Take public transportation, carpool, or work from home to reduce your carbon footprint"
]


def send_reminders(phone_number):
  
  message = client.messages.create(
    to=phone_number,
    from_="YOUR TWILIO NUMBER",
    body=random.choice(eco_reminders)
  )
  print(message["messages"])
  print(message["messages"][0])

  if message["messages"][0]["status"] == "0":
      print("Message sent successfully.")
  else:
      print(f"Message failed with error: {message['messages'][0]['error-text']}")

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


