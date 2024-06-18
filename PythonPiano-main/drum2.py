import cv2
import mediapipe as mp
import pygame
import numpy as np

# Initialize Pygame
pygame.init()

# Define screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Define drum colors
DRUM_COLORS = [(255, 0, 0), (0, 0, 255)]  # Red, Green, Blue

# Initialize Pygame screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Virtual Drum")

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2)

# Drum positions
drum_positions = [(150, 150),  (450, 150)]
drum_radius = 120

# Load drum sounds
drum_sounds = [pygame.mixer.Sound('snare_drum.mp3'), pygame.mixer.Sound('drum3.mp3')]
drum_active = [False] * len(drum_positions)
# Initialize video capture device
cap = cv2.VideoCapture(0)  # 0 for the default camera, you can specify a file path for a video file

# Main loop
running = True
while running:
    # Capture video frame
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame horizontally for a later selfie-view display
    frame = cv2.flip(frame, 1)

    # Convert the BGR image to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame with MediaPipe Hands
    results = hands.process(rgb_frame)

    # Draw drums on OpenCV capture window
    for i, pos in enumerate(drum_positions):
        cv2.circle(frame, pos, drum_radius, DRUM_COLORS[i], thickness=2)

    # Check for hand landmarks
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Check if the hand is left or right
            hand_side = "Left" if results.multi_handedness[0].classification[0].label == "Left" else "Right"

            # Process only the index finger landmarks
            index_finger_landmark = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP]

            # Get landmark positions for index finger
            xpos = index_finger_landmark.x
            ypos = index_finger_landmark.y

            # Calculate positions for index finger
            height, width, _ = frame.shape
            cx, cy = int(xpos * width), int(ypos * height)
            cv2.circle(frame, (cx, cy), 10, (0, 255, 0), -1)

            # Check if hand landmark is within drum region
            for i, (drum_x, drum_y) in enumerate(drum_positions):
                dist = np.sqrt((cx - drum_x) ** 2 + (cy - drum_y) ** 2)


                # Check if the hand landmark is within drum region and corresponds to the correct hand
                if dist < drum_radius and ((i == 0 ) or (i == 1 ) ):
                    # If the drum is not active, play the sound and set it as active
                    if not drum_active[i]:
                        drum_sounds[i].play()
                        drum_active[i] = True
                elif(i == 2 and dist < drum_radius):
                    if not drum_active[i]:
                        drum_sounds[i].play()
                        drum_active[i] = True

                else:
                    drum_active[i] = False

    # Display the frame with drum outlines
    cv2.imshow("Drums", frame)

    # Check for quit events
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

# Clean up
pygame.quit()
cv2.destroyAllWindows()
cap.release()


