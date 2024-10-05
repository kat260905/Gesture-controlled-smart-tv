# Gesture-controlled-smart-tv



---

# Hand Gesture Control System Using OpenCV and MediaPipe

This project implements a **gesture-based control system** that allows users to control their computer's mouse, volume, and scrolling functionality using hand gestures detected through a webcam. It leverages **OpenCV** for real-time video capture, **MediaPipe** for hand landmark detection, and uses **PyAutoGUI** and **Pycaw** libraries to interface with the operating system's mouse and audio controls.

## Features

- **Mouse Control**: Move the cursor with your index finger.
- **Click Gesture**: Perform a mouse click by pinching your index and middle fingers.
- **Volume Control**: Adjust the system volume by changing the distance between your thumb and index fingers.
- **Scroll Gesture**: Scroll up with an open hand and down with a closed fist.

## Demo

![Demo GIF](link-to-demo-gif-or-image)

## Requirements

Make sure you have Python 3.6+ installed. Install the required Python libraries using:

```bash
pip install opencv-python mediapipe numpy pyautogui pycaw comtypes
```

## Setup and Usage

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/hand-gesture-control.git
    ```
   
2. Navigate to the project directory:
    ```bash
    cd hand-gesture-control
    ```

3. Run the script:
    ```bash
    python airWritten.py
    ```

4. Once the program starts, you can control the mouse, volume, and scroll using the following gestures:

   - **Mouse Movement**: Move the cursor with your index finger.
   - **Click Gesture**: Simulate a mouse click by pinching the index and middle fingers.
   - **Volume Control**: Adjust volume by changing the distance between your thumb and index fingers.
   - **Scroll Gesture**: Open hand for scrolling up, closed fist for scrolling down.

Press 'q' to exit the application.

## Hand Gestures

| Gesture        | Action                |
|----------------|-----------------------|
| Index finger up| Move the mouse cursor  |
| Pinch (index + middle finger) | Left-click |
| Thumb and index distance | Volume control |
| Open hand      | Scroll up             |
| Closed fist    | Scroll down           |

## How It Works

- **Hand Detection**: Uses MediaPipe to detect hand landmarks in real-time from the webcam feed.
- **Mouse Control**: Moves the mouse cursor based on the index finger's position on the screen.
- **Volume Control**: Adjusts the system volume by measuring the distance between the thumb and index fingers.
- **Scroll Control**: Scrolls up or down using the open-hand or closed-fist gestures, respectively.

## Code Overview

- `fingers_closed(landmarks)`: Function to detect if the hand is in a closed fist position.
- `find_distance(lmList, p1, p2)`: Computes the Euclidean distance between two points on the hand (e.g., thumb and index finger) for controlling the volume.
- **Main Loop**:
  - Captures frames from the webcam.
  - Detects hand landmarks using MediaPipe.
  - Executes the respective action (mouse control, volume control, or scrolling) based on the hand gestures detected.

## Troubleshooting

- **Hand Detection Not Working**: Ensure your hand is fully visible and well-lit for accurate detection. Adjust the `min_detection_confidence` and `min_tracking_confidence` values for better performance.
- **Lagging/Low Performance**: Lower the resolution of the webcam feed by changing the parameters in `cap.set()` to improve performance on lower-end systems.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

## Acknowledgements

This project uses:
- [MediaPipe](https://mediapipe.dev/) for hand landmark detection.
- [OpenCV](https://opencv.org/) for video capture and frame processing.
- [PyAutoGUI](https://pyautogui.readthedocs.io/) for mouse control.
- [PyCaw](https://github.com/AndreMiras/pycaw) for audio volume control.

---

