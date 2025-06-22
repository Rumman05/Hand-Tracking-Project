# Hand Tracker

A real-time hand tracking application using OpenCV and MediaPipe that detects hand gestures and counts fingers.

## Features

- Real-time hand detection and tracking
- Finger counting (0-5 fingers)
- Thumbs up gesture recognition
- Visual hand landmark overlay

## Requirements

```
opencv-python
mediapipe
```

## Installation

```bash
pip install opencv-python mediapipe
```

## Usage

Run the script:

```bash
python Hand_Tracker.py
```

- Hold your hand in front of the camera
- The app will display the number of extended fingers
- Make a thumbs up gesture for detection
- Press 'q' to quit

## How it Works

The application uses MediaPipe's hand landmark detection to:
1. Identify 21 key points on each hand
2. Calculate angles between finger joints to determine if fingers are extended
3. Detect specific gestures based on finger positions and angles

## Controls

- **q** - Quit the application

## Notes

- Works with up to 2 hands simultaneously
- Requires decent lighting for best results
- Adjust detection confidence in the code if needed
