import pygame
import random
import mediapipe as mp
import cv2

class Game:
# Initialize Pygame
    def start(self):
        pygame.init()

        # Set up the game window
        window_width = 900
        window_height = 600
        window = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption('Hen and the Egg')

        # Set up the colors
        black = pygame.Color(0, 0, 0)
        red = pygame.Color(255, 0, 0)

        # Load the background image
        background_img = pygame.image.load('hen background.png')
        background_img = pygame.transform.scale(background_img, (window_width, window_height))

        # Load the basket image
        basket_img = pygame.image.load('basket.png')
        basket_img = pygame.transform.scale(basket_img, (90, 90))

        # Load the egg image
        egg_img = pygame.image.load('egg.png')
        egg_img = pygame.transform.scale(egg_img, (40, 40))

        # Load the hen image
        hen_img = pygame.image.load('hen.png')
        hen_img = pygame.transform.scale(hen_img, (70, 70))

        # Set up the game clock
        clock = pygame.time.Clock()

        # Set up the basket size and position
        basket_width = 90
        basket_height = 90
        basket_x = (window_width - basket_width) // 2
        basket_y = window_height - basket_height

        # Set up the hen size and position
        hen_width = 70
        hen_height = 70
        num_hens = 1
        hen_spacing = window_width // (num_hens + 4 )
        hens = [{'x': (i + 1) * hen_spacing - hen_width // 2, 'y': 0, 'laying': False, 'laying_timer': 0} for i in range(num_hens)]
        current_hen_index = 0

        # Set up the egg size and position
        egg_width = 40
        egg_height = 40

        # Set up the eggs
        eggs = []

        # Set up the score
        score = 0
        font = pygame.font.Font('freesansbold.ttf', 24)

        # Set up the game over flag
        game_over = False

        # Initialize MediaPipe Hands module
        mp_hands = mp.solutions.hands
        hands = mp_hands.Hands()

        # Set up the webcam
        cap = cv2.VideoCapture(0)

        # Set up smoothing parameters
        smoothing_factor = 0.5
        hand_x_smoothed = basket_x  # Initialize with the current basket position

        # Main game loop
        while not game_over:
            # Clear the game window
            window.blit(background_img, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True

            # Get hand landmarks using MediaPipe
            ret, frame = cap.read()
            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb_frame)

            # Move the basket based on hand gesture (closed fist)
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Calculate the distance between index finger and thumb landmarks
                    index_finger = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                    thumb = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                    distance = abs(index_finger.x - thumb.x)

                    # Smooth the hand position
                    hand_x_smoothed = (hand_x_smoothed * smoothing_factor) + (int(index_finger.x * window_width) - basket_width // 2) * (1 - smoothing_factor)

                    # If the distance is below a threshold, consider it as a closed fist
                    if distance < 0.1:  # Adjust this threshold according to your preference
                        basket_x = max(0, min(window_width - basket_width, int(hand_x_smoothed)))

            # Generate new eggs continuously and alternatively
            current_hen = hens[current_hen_index]
            if not current_hen['laying']:
                current_hen['laying'] = True
                current_hen['laying_timer'] = random.randint(500, 1500)  # Random laying timer between 0.5s and 1.5s
            else:
                current_hen['laying_timer'] -= clock.get_time()  # Decrease the laying timer

                if current_hen['laying_timer'] <= 0:
                    hen_x = current_hen['x']
                    hen_y = current_hen['y']
                    egg_x = hen_x + hen_width // 2 - egg_width // 2
                    egg_y = hen_y + hen_height
                    egg_speed = random.randint(2, 4)
                    eggs.append({'x': egg_x, 'y': egg_y, 'speed': egg_speed})
                    current_hen['laying_timer'] = random.randint(1000, 2000)  # Reset the laying timer

            current_hen_index = (current_hen_index + 1) % num_hens



            # Update the eggs
            for egg in eggs:
                egg['y'] += egg['speed']

                # Check if the egg is caught by the basket
                if (egg['y'] + egg_height > basket_y and egg['y'] < basket_y + basket_height and
                        egg['x'] + egg_width > basket_x and egg['x'] < basket_x + basket_width):
                    # Increase the score
                    score += 1

                    # Remove the egg from the list
                    eggs.remove(egg)
                if score >= num_hens * 10:
                    num_hens += 1
                    hens = [{'x': (i + 1) * hen_spacing - hen_width // 2, 'y': 0, 'laying': False, 'laying_timer': 0} for i in range(num_hens)]
                    hen_spacing = window_width // (num_hens + 1)
                    eggs.clear()



                # Check if the egg reaches the bottom
                if egg['y'] > window_height:
                    game_over = True
                    break

            # Draw the basket
            window.blit(basket_img, (basket_x, basket_y))

            # Draw the hens
            for hen in hens:
                window.blit(hen_img, (hen['x'], hen['y']))

            # Draw the eggs
            for egg in eggs:
                window.blit(egg_img, (egg['x'], egg['y']))

            # Draw the score
            score_text = font.render(f'Score: {score}', True, black)
            window.blit(score_text, (10, 70))
            score_text = font.render(f'Level: {num_hens}', True, black)
            window.blit(score_text, (10, 95))

            # Update the game display
            pygame.display.flip()

            # Set the game speed
            clock.tick(60)

        # Release the webcam
        cap.release()

        # Game over message
        game_over_text = font.render('Game Over', True, red)
        window.blit(game_over_text, (window_width // 2 - 50, window_height // 2 - 12))

        # Final score
        final_score_text = font.render(f'Final Score: {score}', True, black)
        window.blit(final_score_text, (window_width // 2 - 70, window_height // 2 + 30))

        # Update the game display
        pygame.display.flip()

        # Wait for a few seconds before quitting the game
        pygame.time.wait(4000)

        # Quit the game
        pygame.quit()