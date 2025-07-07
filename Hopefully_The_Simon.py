# Import libraries
from keras.models import load_model
from PIL import Image, ImageOps  
import pygame
import numpy as np
import random
import time
import cv2
import os

#Loading the machine
np.set_printoptions(suppress=True)
model = load_model("keras_model.h5", compile=False)
class_names = open("labels.txt", "r").readlines()

# Setting up the camera
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

# Game setup
pygame.init()
window_size = (800, 800)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("        Simon Says!")
WHITE = (255,255,255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
text_font = pygame.font.SysFont("Arial", 30)

# functions
def draw_text(text, font, text_col, x, y):
    img = font.render(text.strip(), True, text_col)
    screen.blit(img, (x, y))

def say_cheese():
    photo_path = "captured_photo.jpg"
    ret, frame = cap.read()
    if ret:
        cv2.imwrite(photo_path, frame)
        print("Photo captured")
        return photo_path
    else:
        print("Capture Failed :(")
        return None

def predict_image(image_path):
    image = Image.open(image_path).convert("RGB")
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    data[0] = normalized_image_array
    prediction = model.predict(data)
    index = np.argmax(prediction)
    return index, class_names[index], prediction[0][index]

def simon_says_game():
    playing = True

    while playing:
        screen.fill(WHITE)
        pygame.display.flip()

        random_pose = random.randint(0, len(class_names) - 1)
        simon_said = class_names[random_pose]
        
        draw_text(f"Simon says: {simon_said}", text_font, (0, 0, 0), 200, 300)
        pygame.display.flip()
        pygame.time.delay(1500)

        # Countdown
        for count in [ "2", "1"]:
            screen.fill(WHITE)
            draw_text(count, text_font, (0, 0, 0), 400, 400)
            pygame.display.flip()
            pygame.time.delay(1000)

        # Take photo and predict
        photo_path = say_cheese()
        if photo_path:
            index, user_pose, confidence = predict_image(photo_path)
            print("User Pose:", user_pose.strip(), "| Confidence:", confidence)
            print("Expected Pose Index:", random_pose)
            print("User Pose Index:", index)

            if index == random_pose:
                screen.fill(GREEN)
                draw_text("Correct!", text_font, (0, 0, 0), 330, 300)
                pygame.display.flip()
                pygame.time.delay(1500)
            else:
                screen.fill(RED)
                draw_text("Wrong pose", text_font, (0, 0, 0), 300, 300)
                pygame.display.flip()
                pygame.time.delay(1000)

                screen.fill(WHITE)
                draw_text("Press SPACE to try again", text_font, (0, 0, 0), 200, 300)
                pygame.display.flip()

                # Pause here until SPACE is pressed again
                waiting = True
                while waiting:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            cap.release()
                            exit()
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                waiting = False

# Main game loop
running = True
start_game = False
game_started = False
while running:
    screen.fill(WHITE)
    draw_text("Press SPACE to start Simon Says", text_font, (0, 0, 0), 100, 300)
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_started:
                game_started = True
                simon_says_game()

cap.release()
pygame.quit()