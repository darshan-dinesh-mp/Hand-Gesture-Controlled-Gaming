import cv2
import face_recognition
import numpy as np

class FaceRecognition:
    def __init__(self,id,name,age,problem,score,camera_index=0):
        self.id = id
        self.name = name
        self.age = age
        self.problem = problem
        self.score = score
        self.cap = cv2.VideoCapture(camera_index)

    def _capture_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            print("Error: Couldn't capture frame.")
            return None
        return frame

    def _convert_to_rgb(self, frame):
        return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    def detect_and_save_face_encoding(self):
        while True:
            frame = self._capture_frame()
            if frame is None:
                break

            rgb_frame = self._convert_to_rgb(frame)
            face_locations = face_recognition.face_locations(rgb_frame)

            for face_location in face_locations:
                top, right, bottom, left = face_location
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

            cv2.imshow('Video', frame)

            if face_locations:
                face_encoding = face_recognition.face_encodings(rgb_frame, [face_locations[0]])[0]

                key = cv2.waitKey(1) & 0xFF
                if key == ord('s'):
                    with open(f"faces/{self.id}.txt", "w") as f:
                        for value in face_encoding:
                            f.write(str(value) + "\n")
                    with open(f"details/{self.id}.txt", "w") as f:
                        f.write("User ID: "+str(self.id) + "\n"+
                        str("Name: "+self.name) + "\n"+
                        str("Age: "+str(self.age)) + "\n"+
                        str("Problem: "+self.problem) + "\n"+
                        str("Score: "+str(self.score)) + "\n")
                    print("Face encoding saved!")
                    break

                elif key == ord('q'):
                    break

        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    face_recognizer = FaceRecognition()
    face_recognizer.detect_and_save_face_encoding()
