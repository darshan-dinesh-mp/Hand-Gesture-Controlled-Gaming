import cv2
import face_recognition
import numpy as np
import os
import time

class SignIn:
    def __init__(self, faces_folder="faces", camera_index=0):
        self.known_face_encodings, self.known_face_names = self.load_known_face_encodings(faces_folder)
        self.cap = cv2.VideoCapture(camera_index)

    def load_known_face_encodings(self, folder_path):
        known_face_encodings = []
        known_face_names = []

        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)

            try:
                with open(file_path, "r") as f:
                    face_encoding = [float(line.strip()) for line in f]
                    known_face_encodings.append(face_encoding)
                    known_face_names.append(os.path.splitext(file_name)[0])
            except Exception as e:
                print(f"Error loading face encoding from {file_path}: {e}")

        return np.array(known_face_encodings), known_face_names

    def _capture_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            print("Error: Couldn't capture frame.")
            return None
        return frame

    def _convert_to_rgb(self, frame):
        return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    def _compare_face_encoding(self, face_encoding):
        if len(self.known_face_encodings) > 0:
            results = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            name = "Unknown"
            if any(results):
                name = self.known_face_names[results.index(True)]
            return name
        return "Unknown"

    def sign_in(self):
        while True:
            frame = self._capture_frame()
            if frame is None:
                break

            rgb_frame = self._convert_to_rgb(frame)
            face_locations = face_recognition.face_locations(rgb_frame)
            time.sleep(1)
            for face_location in face_locations:
                top, right, bottom, left = face_location
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

                face_encoding = face_recognition.face_encodings(rgb_frame, [face_location])[0]

                name = self._compare_face_encoding(face_encoding)
                cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

                print(f"Detected: {name}")
                self.cap.release()
                cv2.destroyAllWindows()
                return name

            cv2.imshow('Video', frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()
        

if __name__ == "__main__":
    sign_in_instance = SignIn()
    sign_in_instance.sign_in()
