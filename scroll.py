import cv2
import mediapipe as mp
import pyautogui

# Initialize MediaPipe Hand model
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)

# Video capture from the webcam
cap = cv2.VideoCapture(0)

def fingers_closed(landmarks):
    # Thumb: compare tip (landmark 4) with the MCP joint (landmark 2)
    if landmarks[4].x < landmarks[3].x:  # Thumb comparison (based on direction)
        return False

    # For other fingers: compare the tip with the lower joint (tip should be below)
    for tip_idx, joint_idx in [(8, 6), (12, 10), (16, 14), (20, 18)]:
        if landmarks[tip_idx].y > landmarks[joint_idx].y:
            return False
    return True

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to RGB (MediaPipe needs RGB)
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False

    # Process the image to detect hands
    result = hands.process(image)

    # Draw the hand annotations on the original frame
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            # Draw hand landmarks
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Check if all fingers are closed
            if fingers_closed(hand_landmarks.landmark):
                print("Scroll Down Gesture - Fist Detected")
                pyautogui.scroll(-500)  # Scroll down
            else:
                print("Scroll Up Gesture - Open Hand Detected")
                pyautogui.scroll(500)  # Scroll up

    # Show the image with landmarks
    cv2.imshow('Hand Gesture Control', image)

    # Exit the loop when 'q' is pressed
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
