import cv2
import mediapipe as mp
import scratchattach as scratch3
import random
# Inicjalizacja detektora ręki z MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Funkcja do rysowania punktów na obrazie
def draw_landmarks(image, landmarks):
    for landmark in landmarks.landmark:
        height, width, _ = image.shape
        cx, cy = int(landmark.x * width), int(landmark.y * height)
        cv2.circle(image, (cx, cy), 5, (255, 0, 0), cv2.FILLED)

def draw_bounding_box(image, landmarks):
    x_min, y_min = 10000, 10000
    x_max, y_max = 0, 0

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
    roznica = 0
    # Narysuj kropkę na środku kwadratu ręki
    cv2.circle(image, (center_x, center_y), 5, (0, 0, 255), cv2.FILLED)
    if 470 <= center_x <= 510:
        roznica =  center_y - 240
        print(roznica)
    return roznica

# Funkcja główna
def main():
    cap = cv2.VideoCapture(0)  # Inicjalizacja kamery
    session = scratch3.login("kornivs", "Bobo#2017")
    conn = session.connect_cloud(project_id="1029673056")

    while cap.isOpened():
        ret, frame = cap.read()  # Odczytanie ramki z kamery
        frame = cv2.flip(frame, 1)
        if not ret:
            break
        
        # Konwersja koloru obrazu z BGR na RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Detekcja ręki
        results = hands.process(rgb_frame)
        
        if results.multi_hand_landmarks:
            # Rysowanie punktów na obrazie
            for hand_landmarks in results.multi_hand_landmarks:
                draw_landmarks(frame, hand_landmarks)
                roz = draw_bounding_box(frame, hand_landmarks)
                if roz is not None:
                    cv2.rectangle(frame, (470, 220+roz), (510, 260+roz), (255, 255, 0), 2)
                    if roz > 0:
                        conn.set_var("positive_or_negative", 1)  
                        conn.set_var("left_y", roz) 
                    else:
                        conn.set_var("positive_or_negative", 0)
                        conn.set_var("left_y", roz*-1) 

        cv2.line(frame, (0, 240), (640, 240), (0, 255, 0), 2)
        cv2.line(frame, (490, 90), (490, 390), (0, 255, 0), 2)

       
        # Dane logowania do Scratch oraz ID projektu
       
        
        



        # Wyświetlenie ramki z obiektami
        cv2.imshow('Hand Detection', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Zwolnienie zasobów
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
