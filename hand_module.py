import cv2
import mediapipe as mp

class HandRecognition:
    def __init__(self, webcam_index=0):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands()

        self.mp_drawing = mp.solutions.drawing_utils

        self.cap = cv2.VideoCapture(webcam_index)

    def process_frame(self):
        ret, frame = self.cap.read()

        frame = cv2.flip(frame, 1)

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = self.hands.process(rgb_frame)
        flag = False
        if results.multi_hand_landmarks:
            flag = True
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

        if flag:
            message = "Hand Detected,Press S to continue"
            cv2.putText(frame, message, (10, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        cv2.imshow('Hand Recognition', frame)

    def run(self):
        while True:
            self.process_frame()

            if cv2.waitKey(1) & 0xFF == ord('s'):
                self.cap.release()
                cv2.destroyAllWindows()
                return True

        


# if __name__ == "__main__":
#     hand_recognition = HandRecognition(webcam_index=2)
#     hand_recognition.run()
