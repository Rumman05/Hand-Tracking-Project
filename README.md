# Hand Tracker

A real-time hand tracking application using OpenCV and MediaPipe that detects finger counting and hand gestures.

## Features

- **Real-time hand detection** - Tracks up to 2 hands simultaneously
- **Finger counting** - Counts and displays the number of extended fingers (0-5)
- **Gesture recognition** - Detects "Thumbs Up" gesture
- **Live video feed** - Uses your webcam for real-time tracking

## Requirements

```
opencv-python
mediapipe
```

## Installation

1. Install the required packages:
```bash
pip install opencv-python mediapipe
```

2. Run the application:
```bash
python Hand_Tracker.py
```

## Usage

- Point your hand(s) toward the camera
- The application will display:
  - Hand landmarks and connections
  - Number of extended fingers
  - "Thumbs Up" when detected
- Press 'q' to quit

## How it Works

The application uses MediaPipe's hand tracking solution to:
1. Detect hand landmarks in real-time
2. Calculate angles between finger joints to determine if fingers are extended
3. Count extended fingers based on joint angles
4. Recognize specific gestures like "Thumbs Up" based on thumb positioning

## Controls

- **Q** - Quit the application

---

*Note: Make sure you have a working webcam connected to your system.*
