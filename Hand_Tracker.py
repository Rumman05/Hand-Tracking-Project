import math
import cv2
import mediapipe as mp
import pyautogui
import tkinter as tk
from tkinter import messagebox
import numpy as np
import threading

# Disable corner fail-safe
pyautogui.FAILSAFE = False


def start_capture_thread(cap, frame_dict, lock):
    """Continuously read frames from cap into frame_dict['frame']"""
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        with lock:
            frame_dict['frame'] = frame
    cap.release()


class HandMouseController:
    """
    Hand-driven mouse control:
      - Reduced model complexity
      - Async frame capture
      - Adjustable sensitivity and smoothing
      - Processing every frame
    """
    TIP_IDS = [4, 8, 12, 16, 20]
    PIP_IDS = [3, 6, 10, 14, 18]

    def __init__(
        self,
        cam_width: int = 320,
        cam_height: int = 240,
        sensitivity: float = 0.5,
        stability_frames: int = 3,
        smoothing_alpha: float = 0.2,
        min_detection_confidence: float = 0.5,
        min_tracking_confidence: float = 0.5
    ):
        self.cam_w = cam_width
        self.cam_h = cam_height
        self.sensitivity = sensitivity
        self.hands = mp.solutions.hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            model_complexity=0,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
        self.screen_w, self.screen_h = pyautogui.size()
        self.left_counter = 0
        self.right_counter = 0
        self.stability_frames = stability_frames
        self.left_down = False
        self.right_down = False
        self.alpha = smoothing_alpha
        self.smooth_x = self.screen_w // 2
        self.smooth_y = self.screen_h // 2
        self.last_lm = None

    def _is_extended(self, lm, tip_id: int, pip_id: int) -> bool:
        return lm[tip_id].y < lm[pip_id].y

    def _move_cursor(self, lm) -> None:
        x_cam = lm.x * self.cam_w
        y_cam = lm.y * self.cam_h
        dx = (x_cam - self.cam_w/2) * (self.screen_w/self.cam_w) * self.sensitivity
        dy = (y_cam - self.cam_h/2) * (self.screen_h/self.cam_h) * self.sensitivity
        target_x = int(self.screen_w/2 + dx)
        target_y = int(self.screen_h/2 + dy)
        self.smooth_x = int(self.alpha * target_x + (1 - self.alpha) * self.smooth_x)
        self.smooth_y = int(self.alpha * target_y + (1 - self.alpha) * self.smooth_y)
        try:
            pyautogui.moveTo(self.smooth_x, self.smooth_y, duration=0)
        except pyautogui.FailSafeException:
            pass

    def _handle_clicks(self, lm) -> None:
        index_ext = self._is_extended(lm, self.TIP_IDS[1], self.PIP_IDS[1])
        middle_ext = self._is_extended(lm, self.TIP_IDS[2], self.PIP_IDS[2])
        if index_ext and not middle_ext:
            self.left_counter += 1
            if self.left_counter >= self.stability_frames and not self.left_down:
                pyautogui.click()
                self.left_down = True
        else:
            self.left_counter = 0
            self.left_down = False
        if middle_ext and not index_ext:
            self.right_counter += 1
            if self.right_counter >= self.stability_frames and not self.right_down:
                pyautogui.rightClick()
                self.right_down = True
        else:
            self.right_counter = 0
            self.right_down = False

    def run(self, camera_index: int = 0) -> None:
        cap = cv2.VideoCapture(camera_index)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.cam_w)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.cam_h)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        if not cap.isOpened():
            messagebox.showerror("Error", "Cannot open camera")
            return
        frame_dict = {'frame': None}
        lock = threading.Lock()
        threading.Thread(
            target=start_capture_thread,
            args=(cap, frame_dict, lock),
            daemon=True
        ).start()
        try:
            while True:
                with lock:
                    f = frame_dict['frame']
                    frame = None if f is None else f.copy()
                if frame is None:
                    continue
                frame = cv2.flip(frame, 1)
                frame = cv2.resize(frame, (self.cam_w, self.cam_h))
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = self.hands.process(rgb)
                if results.multi_hand_landmarks:
                    self.last_lm = results.multi_hand_landmarks[0].landmark
                    self._handle_clicks(self.last_lm)
                if self.last_lm:
                    self._move_cursor(self.last_lm[self.TIP_IDS[1]])
                disp = cv2.resize(frame, (640, 480))
                cv2.imshow("Hand-Mouse Control", disp)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        finally:
            cv2.destroyAllWindows()


class HandDrawController(HandMouseController):
    """Full-screen draw with continuous brush stroke."""
    def run(self, camera_index: int = 0) -> None:
        canvas = np.ones((self.screen_h, self.screen_w, 3), dtype=np.uint8) * 255
        cv2.namedWindow("Draw Mode", cv2.WINDOW_NORMAL)
        cv2.setWindowProperty(
            "Draw Mode",
            cv2.WND_PROP_FULLSCREEN,
            cv2.WINDOW_FULLSCREEN
        )
        cap = cv2.VideoCapture(camera_index)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.cam_w)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.cam_h)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        if not cap.isOpened():
            messagebox.showerror("Error", "Cannot open camera")
            return
        frame_dict = {'frame': None}
        lock = threading.Lock()
        threading.Thread(
            target=start_capture_thread,
            args=(cap, frame_dict, lock),
            daemon=True
        ).start()
        prev_x, prev_y = None, None
        try:
            while True:
                with lock:
                    f = frame_dict['frame']
                    frame = None if f is None else f.copy()
                if frame is None:
                    continue
                frame = cv2.flip(frame, 1)
                frame = cv2.resize(frame, (self.cam_w, self.cam_h))
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = self.hands.process(rgb)
                if results.multi_hand_landmarks:
                    lm = results.multi_hand_landmarks[0].landmark
                    self.last_lm = lm
                if self.last_lm and self._is_extended(
                    self.last_lm, self.TIP_IDS[1], self.PIP_IDS[1]
                ):
                    # continuous stroke: draw line from prev to current
                    curr_x, curr_y = self.smooth_x, self.smooth_y
                    if prev_x is not None and prev_y is not None:
                        cv2.line(canvas, (prev_x, prev_y), (curr_x, curr_y), (0,0,0), 5)
                    prev_x, prev_y = curr_x, curr_y
                else:
                    prev_x, prev_y = None, None
                if self.last_lm:
                    self._move_cursor(self.last_lm[self.TIP_IDS[1]])
                disp = canvas.copy()
                cv2.circle(disp, (self.smooth_x, self.smooth_y), 10, (100,100,100), 2)
                cv2.imshow("Draw Mode", disp)
                key = cv2.waitKey(1) & 0xFF
                if key == ord('c'):
                    canvas[:] = 255
                if key == ord('q'):
                    break
        finally:
            cv2.destroyAllWindows()


# GUI menu using Tkinter

def start_mouse_control() -> None:
    root.destroy()
    HandMouseController().run()

def start_draw_mode() -> None:
    root.destroy()
    HandDrawController().run()

def main() -> None:
    global root
    root = tk.Tk()
    root.title("Hand Gesture App")
    root.geometry("300x200")
    tk.Label(root, text="Select Mode:", font=(None, 14)).pack(pady=10)
    tk.Button(root, text="Mouse Control", width=20, command=start_mouse_control).pack(pady=5)
    tk.Button(root, text="Draw Mode", width=20, command=start_draw_mode).pack(pady=5)
    tk.Button(root, text="Exit", width=20, command=root.destroy).pack(pady=5)
    root.mainloop()


if __name__ == "__main__":
    main()
