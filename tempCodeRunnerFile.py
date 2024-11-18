import cv2 as cv
import mediapipe as mp
import utility  # Assumes a custom module for additional calculations
import pyautogui as py

# Screen dimensions
screen_width, screen_height = py.size()

# Mediapipe hands setup
mphand = mp.solutions.hands
hands = mphand.Hands(
    static_image_mode=False,  # Fixed parameter name
    model_complexity=1,       # Fixed parameter name
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
    max_num_hands=1           # Detect only one hand
)

# Function to find the index fingertip
def find_finger(process):
    if process.multi_hand_landmarks:
        hand_landmark = process.multi_hand_landmarks[0]
        return hand_landmark.landmark[mphand.HandLandmark.INDEX_FINGER_TIP]
    return None

# Gesture detection function
def detect_gesture(frame, landmark_list, process):
    if len(landmark_list) >= 21:
        index_FingureTip = find_finger(process)
        # Detect gesture based on landmarks and distances
        thumb_fingure_distance = utility.get_distance((landmark_list[4], landmark_list[5])) 
        if thumb_fingure_distance < 50 and utility.get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) > 90:
            mouse_move(index_FingureTip)

# Mouse movement function
def mouse_move(index_FingureTip):
    if index_FingureTip is not None:
        x = int(index_FingureTip.x * screen_width)
        y = int(index_FingureTip.y * screen_height)
        if x:  # Ensure x is valid
            print("Moving mouse to:", x, y)
            py.moveTo(x, y)

# Main function
def main():
    capture = cv.VideoCapture(0)  # Open the webcam
    draw = mp.solutions.drawing_utils  # For drawing hand landmarks

    try: 
        while capture.isOpened():
            ret, frame = capture.read()
            if not ret:
                break
            frame = cv.flip(frame, 1)  # Flip the frame horizontally
            frameRGB = cv.cvtColor(frame, cv.COLOR_BGR2RGB)  # Convert frame to RGB

            # Process hand detection
            process = hands.process(frameRGB) 
            landmark_list = []

            if process.multi_hand_landmarks:
                hand_landmark = process.multi_hand_landmarks[0]
                draw.draw_landmarks(frame, hand_landmark, mphand.HAND_CONNECTIONS)
                for lm in hand_landmark.landmark:
                    landmark_list.append((lm.x, lm.y))  # Store normalized coordinates

            # Detect gestures based on landmarks
            detect_gesture(frame, landmark_list, process)

            # Show the video feed
            cv.imshow("Frame", frame)

            # Exit if 'q' is pressed
            if cv.waitKey(1) & 0xff == ord("q"):
                break

    finally:
        capture.release()  # Release the webcam
        cv.destroyAllWindows()  # Close all OpenCV windows

# Entry point
if __name__ == "__main__":
    main()
