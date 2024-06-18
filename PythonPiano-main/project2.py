import pygame
import piano_lists as pl
from pygame import mixer
import mediapipe as mp
import numpy as np
import cv2

pygame.init()
pygame.mixer.set_num_channels(50)

font = pygame.font.Font('assets/Terserah.ttf', 48)
medium_font = pygame.font.Font('assets/Terserah.ttf', 28)
small_font = pygame.font.Font('assets/Terserah.ttf', 16)
real_small_font = pygame.font.Font('assets/Terserah.ttf', 10)
fps = 60
timer = pygame.time.Clock()
WIDTH = 52 * 35
HEIGHT = 400
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('My Python Piano')

active_whites = []
active_blacks = []
white_sounds = []
black_sounds = []

left_hand = pl.left_hand
right_hand = pl.right_hand
piano_notes = pl.piano_notes
white_notes = pl.white_notes
black_notes = pl.black_notes
black_labels = pl.black_labels

for i in range(len(white_notes)):
    white_sounds.append(mixer.Sound(f'assets\\notes\\{white_notes[i]}.wav'))

for i in range(len(black_notes)):
    black_sounds.append(mixer.Sound(f'assets\\notes\\{black_notes[i]}.wav'))


def draw_piano(whites, blacks):
    white_rects = []
    for i in range(52):
        rect = pygame.draw.rect(screen, 'white', [i * 35, HEIGHT - 300, 35, 300], 0, 2)
        white_rects.append(rect)
        pygame.draw.rect(screen, 'black', [i * 35, HEIGHT - 300, 35, 300], 2, 2)
        key_label = small_font.render(white_notes[i], True, 'black')
        screen.blit(key_label, (i * 35 + 3, HEIGHT - 20))
    skip_count = 0
    last_skip = 2
    skip_track = 2
    black_rects = []
    for i in range(36):
        rect = pygame.draw.rect(screen, 'black', [23 + (i * 35) + (skip_count * 35), HEIGHT - 300, 24, 200], 0, 2)
        for q in range(len(blacks)):
            if blacks[q][0] == i:
                if blacks[q][1] > 0:
                    pygame.draw.rect(screen, 'green', [23 + (i * 35) + (skip_count * 35), HEIGHT - 300, 24, 200], 2, 2)
                    blacks[q][1] -= 1

        key_label = real_small_font.render(black_labels[i], True, 'white')
        screen.blit(key_label, (25 + (i * 35) + (skip_count * 35), HEIGHT - 120))
        black_rects.append(rect)
        skip_track += 1
        if last_skip == 2 and skip_track == 3:
            last_skip = 3
            skip_track = 0
            skip_count += 1
        elif last_skip == 3 and skip_track == 2:
            last_skip = 2
            skip_track = 0
            skip_count += 1

    for i in range(len(whites)):
        if whites[i][1] > 0:
            j = whites[i][0]
            pygame.draw.rect(screen, 'green', [j * 35, HEIGHT - 100, 35, 100], 2, 2)
            whites[i][1] -= 1

    return white_rects, black_rects, whites, blacks



#opencv logic




cap = cv2.VideoCapture(0)


desired_width = 1600
desired_height = 800

# Set the width and height for the captured frame
cap.set(cv2.CAP_PROP_FRAME_WIDTH, desired_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, desired_height)

# Initialize MediaPipe Hands
hands = mp.solutions.hands
hands_mesh = hands.Hands(static_image_mode=False, min_detection_confidence=0.7)
draw = mp.solutions.drawing_utils


# Define the dimensions of the piano
piano_width = 35 * 52
piano_height = 400

# Define colors
PURPLE = (128, 0, 128)  # Purple color for the keys
GREEN = (0, 255, 0)  # Green color for the outline

# Function to draw the piano outline
def draw_piano_outline():
    piano_outline = np.zeros((piano_height, piano_width, 3), dtype=np.uint8)  # Use 3 channels for RGB color

    # Draw white keys
    for i in range(52):
        cv2.rectangle(piano_outline, (i * 35, 100), ((i + 1) * 35, 300), PURPLE, 2, cv2.LINE_AA)
        cv2.rectangle(piano_outline, (i * 35, 100), ((i + 1) * 35, 300), GREEN, 2, cv2.LINE_AA)


    #black key logic
    cv2.rectangle(piano_outline, ((0 * 35) + 23, 100), (((0 + 1) * 35) + 23,  200), PURPLE, -1, cv2.LINE_AA)
    cv2.rectangle(piano_outline, ((0 * 35) + 23, 100), (((0 + 1) * 35) + 23,  200), GREEN, 2, cv2.LINE_AA)

    cv2.rectangle(piano_outline, ((2 * 35) + 23, 100), (((2 + 1) * 35) + 23,  200), PURPLE, -1, cv2.LINE_AA)
    cv2.rectangle(piano_outline, ((2 * 35) + 23, 100), (((2 + 1) * 35) + 23,  200), GREEN, 2, cv2.LINE_AA)

    cv2.rectangle(piano_outline, ((3 * 35) + 23, 100), (((3 + 1) * 35) + 23,  200), PURPLE, -1, cv2.LINE_AA)
    cv2.rectangle(piano_outline, ((3 * 35) + 23, 100), (((3 + 1) * 35) + 23,  200), GREEN, 2, cv2.LINE_AA)
    for i in range(5,50):
        if i % 7 != 1 and i % 7 != 4:
            cv2.rectangle(piano_outline, ((i * 35) + 23, 100), (((i + 1) * 35) + 23,  200), PURPLE, -1, cv2.LINE_AA)
            cv2.rectangle(piano_outline, ((i * 35) + 23, 100), (((i + 1) * 35) + 23,  200), GREEN, 2, cv2.LINE_AA)
    
    
   



    return piano_outline

# Main loop
run = True



while run:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the BGR image to RGB
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame with MediaPipe Hands
    results = hands_mesh.process(rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Get the index finger landmark
            index_finger_landmark = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP]
            thumb_finger_landmark = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.THUMB_TIP]
            middle_finger_landmark = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.MIDDLE_FINGER_TIP]
            ring_finger_landmark = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.RING_FINGER_TIP]
            pinky_finger_landmark = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.PINKY_TIP]
            

            # Convert normalized landmark coordinates to pixel coordinates
            image_height, image_width, _ = frame.shape
            x = int(index_finger_landmark.x * image_width)
            y = int(index_finger_landmark.y * image_height)
            x1 = int(thumb_finger_landmark.x * image_width)
            y1 = int(thumb_finger_landmark.y * image_height)
            x2 = int(middle_finger_landmark.x * image_width)
            y2 = int(middle_finger_landmark.y * image_height)
            x3 = int(ring_finger_landmark.x * image_width)
            y3 = int(ring_finger_landmark.y * image_height)
            x4 = int(pinky_finger_landmark.x * image_width)
            y4 = int(pinky_finger_landmark.y * image_height)




            # Draw a circle at the index finger position (cursor)
            cv2.circle(frame, (x, y), 10, (0, 255, 0), -1)
            cv2.circle(frame, (x1, y1), 10, (0, 255, 0), -1)
            cv2.circle(frame, (x2, y2), 10, (0, 255, 0), -1)
            cv2.circle(frame, (x3, y3), 10, (0, 255, 0), -1)
            cv2.circle(frame, (x4, y4), 10, (0, 255, 0), -1)

            # Perform actions based on the cursor position (you can add your logic here)

    # Display the frame
    frame_resized = cv2.resize(frame, (desired_width, desired_height))
    frame_flipped = cv2.flip(frame_resized, 1)

    piano_outline = draw_piano_outline()

    # Resize the piano outline to match the height of the video frame
    piano_outline_resized = cv2.resize(piano_outline, (frame_flipped.shape[1], frame_flipped.shape[0]))

    # Create an alpha channel with full transparency
    alpha_channel = np.full((frame_flipped.shape[0], frame_flipped.shape[1], 1), 255, dtype=np.uint8)

    # Combine the video frame and the piano outline with transparency
    combined_frame = cv2.addWeighted(frame_flipped, 0.7, piano_outline_resized, 0.3, 0)

    # Display the combined frame
    cv2.imshow('Video Capture with Piano Outline', combined_frame)
    #cv2.imshow("Hand Tracking", combined_frame)

    # Exit when 'q' is pressed
    if cv2.waitKey(1) == ord('q'):
        break

# Release video capture and close all windows
    #cap.release()
    #cv2.destroyAllWindows()
    
    timer.tick(fps)
    screen.fill('gray')
    white_keys, black_keys, active_whites, active_blacks = draw_piano(active_whites, active_blacks)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            black_key = False
            for i in range(len(black_keys)):
                if black_keys[i].collidepoint(event.pos):
                    black_sounds[i].play(0, 1000)
                    black_key = True
                    active_blacks.append([i, 30])
            for i in range(len(white_keys)):
                if white_keys[i].collidepoint(event.pos) and not black_key:
                    white_sounds[i].play(0, 1000)
                    active_whites.append([i, 30])

    pygame.display.flip()
pygame.quit()