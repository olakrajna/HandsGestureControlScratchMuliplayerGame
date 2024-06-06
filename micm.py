# import scratchattach as scratch3

# events = scratch3.CloudEvents("1029673056")

# @events.event
# def on_set(event): #Called when a cloud var is set
#     print(f"{event.user} set the variable {event.var} to the valuee {event.value} at {event.timestamp}")

# @events.event
# def on_del(event):
#     print(f"{event.user} deleted variable {event.var}")

# @events.event
# def on_create(event):
#     print(f"{event.user} created variable {event.var}")

# @events.event #Called when the event listener is ready
# def on_ready():
#    print("Event listener ready!")

# events.start() #Make sure this is ALWAYS at the bottom of your Python file!

import scratchattach as scratch3
import random
from dotenv import load_dotenv
import os

load_dotenv('venv/.env')

username: str = os.getenv('SCRATCH_USERNAME')
password: str = os.getenv('SCRATCH_PASSWORD')
project_id: str = os.getenv('PROJECT_ID')

session = scratch3.login(username, password)

for i in range(0,100):
    random_number = random.randint(-150, 150)
    print(random_number)
    conn = session.connect_cloud(project_id=project_id)
    if random_number < 0:
        conn.set_var("positive_or_negative", 1)
        conn.set_var("left_y", random_number*-1)
    else:
        conn.set_var("positive_or_negative", 0)
        conn.set_var("left_y", random_number)

