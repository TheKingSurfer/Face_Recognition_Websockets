import cv2
import face_recognition
import os
import glob
import numpy as np
import base64

class SimpleFacerec:
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []
        self.frame_resizing = 0.25

    def load_encoding_images(self, abs_images_path):
        images_path = glob.glob(os.path.join(abs_images_path, "*.*"))

        print("{} encoding images found.".format(len(images_path)))

        for img_path in images_path:
            img = cv2.imread(img_path)
            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            basename = os.path.basename(img_path)
            (filename, ext) = os.path.splitext(basename)
            # Use the name without the extension
            filename = os.path.splitext(filename)[0]

            # Skip if the name is a folder or doesn't meet certain criteria
            if not self.is_valid_face_name(filename):
                print(f"Skipping invalid face name: {filename}")
                continue

            img_encodings = face_recognition.face_encodings(rgb_img)

            # Check if at least one face encoding is found
            if img_encodings:
                img_encoding = img_encodings[0]
                self.known_face_encodings.append(img_encoding)
                self.known_face_names.append(filename)
                print(f"Face encoding loaded for {filename}")
            else:
                print(f"No face encoding found for {filename}. Skipping.")

        print("Encoding images loaded")

    def is_valid_face_name(self, name):
        # Add your criteria for valid face names
        # For example, you might want to skip names that are folder names
        return not os.path.isdir(name)
    def recognize_faces(self, frame):
        small_frame = cv2.resize(frame, (0, 0), fx=self.frame_resizing, fy=self.frame_resizing)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            name = "Unknown"

            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = self.known_face_names[best_match_index]
            face_names.append(name)

        face_locations = np.array(face_locations)
        face_locations = face_locations / self.frame_resizing
        return face_locations.astype(int), face_names

def encode_frame(frame):
    _, buffer = cv2.imencode('.jpg', frame)
    img_str = base64.b64encode(buffer).decode('utf-8')
    return img_str

def decode_frame(img_str):
    img_data = base64.b64decode(img_str)
    nparr = np.frombuffer(img_data, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return frame
