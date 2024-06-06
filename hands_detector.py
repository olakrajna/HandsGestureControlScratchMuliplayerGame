import cv2
import mediapipe as mp
import scratchattach as scratch3
from dotenv import load_dotenv
import os


load_dotenv('venv/.env')
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)
username: str = os.getenv('SCRATCH_USERNAME')
password: str = os.getenv('SCRATCH_PASSWORD')
project_id: str = os.getenv('PROJECT_ID')
cam_index: int = 0

def draw_landmarks(image, landmarks):
    for landmark in landmarks.landmark:
        height, width, _ = image.shape
        cx, cy = int(landmark.x * width), int(landmark.y * height)
        cv2.circle(image, (cx, cy), 5, (255, 0, 0), cv2.FILLED)

def draw_bounding_box(image, landmarks):
    x_min, y_min = 10000, 10000
    x_max, y_max = 0, 0
    difference: int = 0

    for landmark in landmarks.landmark:
        height, width, _ = image.shape
        x, y = int(landmark.x * width), int(landmark.y * height)
        if x < x_min:
            x_min = x
        if x > x_max:
            x_max = x
        if y < y_min:
            y_min = y
        if y > y_max:
            y_max = y
    
    cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

    center_x = (x_min + x_max) // 2
    center_y = (y_min + y_max) // 2

    cv2.circle(image, (center_x, center_y), 5, (0, 0, 255), cv2.FILLED)

    if 390 <= center_x <= 590:
        difference = center_y - 240

    return difference
def connect_to_scratch(scratch_username: str, scratch_password: str, id_project: str):
    session = scratch3.login(scratch_username, scratch_password)
    conn = session.connect_cloud(id_project)
    return conn

def hand_detector():

    cap = cv2.VideoCapture(cam_index)
    conn = connect_to_scratch(username, password, project_id)

    if not cap.isOpened():
        print("Unable to open camera")
        exit()

    while cap.isOpened():
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        if not ret:
            break
        
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        results = hands.process(rgb_frame)
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                draw_landmarks(frame, hand_landmarks)
                diff = draw_bounding_box(frame, hand_landmarks)
                if diff is not None:
                    cv2.rectangle(frame, (390, 220 + diff), (590, 260 + diff), (255, 255, 0), 2)
                    if diff > 0:
                        conn.set_var("positive_or_negative", 1)  
                        conn.set_var("left_y", diff)
                    else:
                        conn.set_var("positive_or_negative", 0)
                        conn.set_var("left_y", diff*-1)

        cv2.line(frame, (0, 240), (640, 240), (0, 255, 0), 2)
        cv2.line(frame, (490, 90), (490, 390), (0, 255, 0), 2)
        cv2.imshow('Hand Detection', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()


