import pygame
import piano_lists as pl
from pygame import mixer
import cv2
import mediapipe as mp
import numpy as np

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







run = True
while run:
    #opencv part here
  

    cap = cv2.VideoCapture(0)

# Initialize MediaPipe Hands
    hands = mp.solutions.hands
    hands_mesh = hands.Hands(static_image_mode=False, min_detection_confidence=0.7)
    draw = mp.solutions.drawing_utils

# Main loop
    while True:
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
        cv2.imshow("Hand Tracking", frame)

    # Exit when 'q' is pressed
        if cv2.waitKey(1) == ord('q'):
            break

# Release video capture and close all windows
    cap.release()
    cv2.destroyAllWindows()
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