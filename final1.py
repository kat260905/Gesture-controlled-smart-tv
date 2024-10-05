import cv2
import mediapipe as mp
import numpy as np
import time
import math
import pyautogui
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


# Initialize MediaPipe and pycaw
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)

# Audio control setup
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]

# Video capture from webcam
cap = cv2.VideoCapture(0)
wCam, hCam = 640, 480
cap.set(3, wCam)
cap.set(4, hCam)

# Variables
pTime = 0
plocX, plocY = 0, 0
smoothening = 7
wScr, hScr = pyautogui.size()

def fingers_closed(landmarks):
    """Checks if all five fingers are closed by comparing the tip of each finger with the lower joint."""
    if landmarks[4].x < landmarks[3].x:  # Thumb comparison (based on direction)
        return False
    for tip_idx, joint_idx in [(8, 6), (12, 10), (16, 14), (20, 18)]:
        if landmarks[tip_idx].y > landmarks[joint_idx].y:
            return False
    return True

def find_distance(lmList, p1, p2):
    x1, y1 = lmList[p1][1:3]
    x2, y2 = lmList[p2][1:3]
    length = math.hypot(x2 - x1, y2 - y1)
    cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
    return length, (x1, y1, x2, y2, cx, cy)

while True:
    success, frame = cap.read()
    if not success:
        break

    # Convert the frame to RGB (MediaPipe needs RGB)
    imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    imgRGB.flags.writeable = False
    result = hands.process(imgRGB)
    imgRGB.flags.writeable = True
    img = cv2.cvtColor(imgRGB, cv2.COLOR_RGB2BGR)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            # Drawing landmarks
            mp_drawing.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            lmList = [[id, int(lm.x * wCam), int(lm.y * hCam)] for id, lm in enumerate(hand_landmarks.landmark)]
            fingers = [1 if lmList[i][2] < lmList[i - 2][2] else 0 for i in [8, 12, 16, 20]]

            # Volume Control using Thumb and Index distance
            if len(lmList) > 0:
                length, info = find_distance(lmList, 4, 8)
                vol = np.interp(length, [50, 200], [minVol, maxVol])
                volume.SetMasterVolumeLevel(vol, None)

                # Visual feedback for volume control
                cv2.circle(img, (info[4], info[5]), 10, (0, 255, 0), cv2.FILLED)
                cv2.putText(img, f'Vol: {int(np.interp(length, [50, 200], [0, 100]))}%', (40, 450),
                            cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

            # Scroll Control - Closed Fist Scrolls Down, Open Hand Scrolls Up
            elif fingers_closed(hand_landmarks.landmark):
                print("Scroll Down Gesture - Fist Detected")        
                pyautogui.scroll(-500)  # Scroll down
            else:
                print("Scroll Up Gesture - Open Hand Detected")
                pyautogui.scroll(500)  # Scroll up

            # Mouse Control using Index finger
            if fingers[0] == 1 and fingers[1] == 0:  # Only Index finger up
                x1, y1 = lmList[8][1], lmList[8][2]
                x3 = np.interp(x1, (150, wCam - 150), (0, wScr))
                y3 = np.interp(y1, (150, hCam - 150), (0, hScr))
                clocX = plocX + (x3 - plocX) / smoothening
                clocY = plocY + (y3 - plocY) / smoothening
                pyautogui.moveTo(wScr - clocX, clocY)
                cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
                plocX, plocY = clocX, clocY

            # Click action (both index and middle finger up)
            if fingers[0] == 1 and fingers[1] == 1:
                length, info = find_distance(lmList, 8, 12)
                if length < 40:
                    cv2.circle(img, (info[4], info[5]), 15, (0, 255, 0), cv2.FILLED)
                    pyautogui.click()

    # Frame rate calculation
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Show the image with landmarks
    cv2.imshow('Hand Gesture Control', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
