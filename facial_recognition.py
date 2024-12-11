import face_recognition
import cv2
import numpy as np

# Initialize the webcam
video_capture = cv2.VideoCapture(0)

# Load a sample picture and  to recognize it
try:
    cristiano_image = face_recognition.load_image_file("C:/Users/Shamanth. V/Desktop/Face_recognition/Cristiano/cristiano.jpeg")
    cristiano_face_encoding = face_recognition.face_encodings(cristiano_image)[0]
    shamanth_image = face_recognition.load_image_file("C:/Users/Shamanth. V/Desktop/Face_recognition/Shamanth/shamanth.jpg")
    shamanth_face_encoding = face_recognition.face_encodings(shamanth_image)[0]
    #aishwarya_image = face_recognition.load_image_file("C:/Users/Shamanth. V/Desktop/Face_recognition/Cristiano/cristiano.jpeg")
    #aishwarya_face_encoding = face_recognition.face_encodings(aishwarya_image)[0]
except IndexError:
    print("Error: No face found in the Cristiano image.")
    exit()

# Known face encodings and their names
known_face_encodings = [cristiano_face_encoding,shamanth_face_encoding]
known_face_names = ["Cristiano","Shamanth"]
#known_face_encodings = [shamanth_face_encoding]
#known_face_names = ["Shamanth"]
#known_face_encodings = [aishwarya_face_encoding]
#known_face_names = ["Aishwarya"]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR (OpenCV format) to RGB (face_recognition format)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame for efficiency
    if process_this_frame:
        # Find all the face locations and encodings in the current frame
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        # Initialize an empty list for names
        face_names = []
        for face_encoding in face_encodings:
            # Check if the face matches any known face
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # Use the face with the smallest distance if there's a match
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)

    # Toggle processing for every other frame
    process_this_frame = not process_this_frame

    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale face locations back up to match the original frame size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with the name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
video_capture.release()
cv2.destroyAllWindows()
