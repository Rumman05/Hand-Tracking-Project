import cv2
import mediapipe as mp
import math

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False,
                       max_num_hands=2,
                       min_detection_confidence=0.5,
                       min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Initialize Video Capture
cap = cv2.VideoCapture(0)

def calculate_distance(landmark1, landmark2):
    """Calculates the 3D Euclidean distance between two landmarks."""
    x1, y1, z1 = landmark1.x, landmark1.y, landmark1.z
    x2, y2, z2 = landmark2.x, landmark2.y, landmark2.z
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)


def calculate_angle(a, b, c):
    """Calculates the angle between three points (in degrees)."""
    ba_x = a.x - b.x
    ba_y = a.y - b.y
    ba_z = a.z - b.z

    bc_x = c.x - b.x
    bc_y = c.y - b.y
    bc_z = c.z - b.z

    dot_product = ba_x * bc_x + ba_y * bc_y + ba_z * bc_z

    magnitude_ba = math.sqrt(ba_x**2 + ba_y**2 + ba_z**2)
    magnitude_bc = math.sqrt(bc_x**2 + bc_y**2 + bc_z**2)

    if magnitude_ba * magnitude_bc == 0:
        return 0.0

    angle_radians = math.acos(dot_product / (magnitude_ba * magnitude_bc))
    return math.degrees(angle_radians)


def count_fingers_held_up(hand_landmarks):
    """Counts the number of fingers held up (extended from a closed fist)."""
    finger_tips = [8, 12, 16, 20]
    knuckles = [6, 10, 14, 18]
    finger_bases = [5, 9, 13, 17]
    extended_fingers = 0

    for i in range(4):
      tip_landmark = hand_landmarks.landmark[finger_tips[i]]
      knuckle_landmark = hand_landmarks.landmark[knuckles[i]]
      base_landmark = hand_landmarks.landmark[finger_bases[i]]

      angle = calculate_angle(tip_landmark, knuckle_landmark, base_landmark)
      if angle > 150:
        extended_fingers += 1

    thumb_tip = hand_landmarks.landmark[4]
    thumb_base = hand_landmarks.landmark[2]
    wrist = hand_landmarks.landmark[0]
    angle = calculate_angle(thumb_tip, thumb_base, wrist)

    if angle > 120:
       extended_fingers += 1

    return extended_fingers

def detect_hand_symbols(hand_landmarks):
    """Detects 'Okay' and 'Thumbs Up' hand symbols."""
    num_fingers = count_fingers_held_up(hand_landmarks)
    thumb_tip = hand_landmarks.landmark[4]
    index_tip = hand_landmarks.landmark[8]
    wrist = hand_landmarks.landmark[0]
    thumb_base = hand_landmarks.landmark[2]

    # Check if the thumb is pointing upwards
    # The angle between the wrist, thumb base, and thumb tip should be close to 180 degrees for a "Thumbs Up"
    thumb_angle = calculate_angle(wrist, thumb_base, thumb_tip)
    
    if thumb_angle > 160:  # This range can be adjusted to detect upward-pointing thumbs
        if num_fingers == 1:
            return "Thumbs Up"


    return None


while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue
    image = cv2.flip(image, 1)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            # Detect and display hand symbols
            symbol = detect_hand_symbols(hand_landmarks)
            if symbol:
              cv2.putText(image, symbol, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            else:
              num_fingers = count_fingers_held_up(hand_landmarks)
              if num_fingers > 0:
                cv2.putText(image, f"Fingers: {num_fingers}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)


    cv2.imshow('Hand Tracking', image)

    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()