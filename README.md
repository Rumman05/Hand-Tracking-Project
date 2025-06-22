# Hand Gesture Mouse Controller

A Python application that uses computer vision and hand tracking to control your mouse cursor and create drawings using hand gestures captured through your webcam.

## Features

- **Mouse Control Mode**: Control your mouse cursor using hand movements
  - Move cursor by pointing with your index finger
  - Left click by extending only your index finger
  - Right click by extending only your middle finger
  - Smooth cursor movement with adjustable sensitivity
  - Stability frames to prevent accidental clicks

- **Draw Mode**: Create digital artwork using hand gestures
  - Draw by extending your index finger
  - Full-screen canvas for drawing
  - Continuous brush strokes
  - Clear canvas with 'C' key
  - Visual cursor indicator

## Requirements

```
opencv-python
mediapipe
pyautogui
tkinter (usually included with Python)
numpy
```

## Installation

1. Clone or download this repository
2. Install the required dependencies:

```bash
pip install opencv-python mediapipe pyautogui numpy
```

## Usage

1. Run the application:
```bash
python Hand_Tracker.py
```

2. A GUI menu will appear with three options:
   - **Mouse Control**: Enables hand gesture mouse control
   - **Draw Mode**: Opens a full-screen drawing canvas
   - **Exit**: Closes the application

3. **For Mouse Control:**
   - Point your index finger to move the cursor
   - Extend only your index finger to left-click
   - Extend only your middle finger to right-click
   - Press 'Q' to quit

4. **For Draw Mode:**
   - Extend your index finger to draw
   - Press 'C' to clear the canvas
   - Press 'Q' to quit

## Controls

### Mouse Control Mode
- **Cursor Movement**: Point with index finger
- **Left Click**: Extend index finger only (middle finger down)
- **Right Click**: Extend middle finger only (index finger down)
- **Quit**: Press 'Q'

### Draw Mode
- **Draw**: Extend index finger
- **Clear Canvas**: Press 'C'
- **Quit**: Press 'Q'

## Technical Details

The application uses:
- **MediaPipe** for hand landmark detection
- **OpenCV** for camera capture and image processing
- **PyAutoGUI** for mouse control
- **Threading** for asynchronous frame capture to improve performance

### Key Parameters
- Camera resolution: 320x240 (for processing)
- Display resolution: 640x480
- Sensitivity: Adjustable cursor movement sensitivity
- Stability frames: Prevents accidental clicks (default: 3 frames)
- Smoothing: Alpha blending for smooth cursor movement

## Troubleshooting

1. **Camera not opening**: Make sure your webcam is connected and not being used by another application
2. **Poor hand detection**: Ensure good lighting and position your hand clearly in front of the camera
3. **Cursor too sensitive**: The sensitivity can be adjusted in the HandMouseController initialization
4. **Application crashes**: Make sure all dependencies are properly installed

## Configuration

You can modify the following parameters in the `HandMouseController` class:
- `sensitivity`: Controls cursor movement sensitivity (default: 0.5)
- `stability_frames`: Number of consecutive frames needed for click detection (default: 3)
- `smoothing_alpha`: Controls cursor smoothing (default: 0.2)
- `cam_width/cam_height`: Camera resolution for processing

## System Requirements

- Python 3.6+
- Webcam
- Windows/macOS/Linux

## Notes

- The application disables PyAutoGUI's fail-safe feature for smooth operation
- Hand tracking works best with good lighting conditions
- Only one hand is tracked at a time
- The application uses model complexity 0 for better performance

## License

This project is open source and available under the MIT License.
