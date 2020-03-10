#!/usr/bin/python3
from firebase import firebase
from datetime import datetime
from PIL import ImageFile
import cv2
import numpy as np
import platform
import time
import sys
import pickle
import os.path
import os
import dlib
import PIL.Image

## Firebase comm code
##

db = firebase.FirebaseApplication('LINK_REMOVED_FOR_GITHUB_PUBLIC_VIEWING', None)

def time_stamp():
    dateTimeObj = datetime.now()
    timestampStr = dateTimeObj.strftime('%d-%b-%Y (%I:%M:%S %p)')
    return timestampStr

def send_to_db(name):
    data = {
        'name': name,
        'time': time_stamp()
    }

    result = db.put('/Classroom 1/1st Period/Attended', data['name'], data['time'])
    return result

## Functions
##

def adjust_img_bounds(obj, img_shape):
    return max(obj[0], 0), min(obj[1], img_shape[1]), min(obj[2], img_shape[0]), max(obj[3], 0)

def rect_to_tuple(rect):
    return rect.top(), rect.right(), rect.bottom(), rect.left()

def tuple_to_rect(obj):
    return dlib.rectangle(obj[3], obj[0], obj[1], obj[2])

def face_similarity(face_encodings, compare_face):
    if len(face_encodings) == 0:
        return np.empty((0))
    return np.linalg.norm(face_encodings - compare_face, axis=1)

def face_locations(img):
    return [adjust_img_bounds(rect_to_tuple(face), img.shape) for face in face_detect(img, 1)]

def face_fetaures(face_image, face_locations=None):
    if face_locations == None:
        face_locations = face_detect(face_image, 1)
    else:
        face_locations = [tuple_to_rect(face_location) for face_location in face_locations]

    pose_predictor = model_face_id
    return [pose_predictor(face_image, face_location) for face_location in face_locations]

def face_encodings(face_image, known_face_locations=None):
    features = face_fetaures(face_image, known_face_locations)
    return [np.array(model_face_encoder.compute_face_descriptor(face_image, raw_landmark_set, 1)) for raw_landmark_set in features]

def compare_faces(known_faces, check_face, rigidity=0.6):
    return list(face_similarity(known_faces, check_face) <= rigidity)

## Load Models
##

face_detect=dlib.get_frontal_face_detector()
model_face_id=dlib.shape_predictor('./models/model_face_predict.dat')
model_face_encoder=dlib.face_recognition_model_v1('./models/model_face_encode.dat')

## Face Encoding - optional during run if dataset/name already files exists
##

# define our path and see what files are in directory
face_path = os.getcwd() + '/faces/'#'/home/nano/Desktop/faces/'
try:
    images_face = [f for f in os.listdir(face_path) if os.path.isfile(os.path.join(face_path , f))]
except IOError:
    print('\x1bc')
    print('No \'data_file\' directory was found...\n\n\
Please make a new directory for the \'data_file\' folder at path:')
    print(face_path + 'data_file/')
    sys.exit()

# clear screen
print('\x1bc')

# print images found to console
if len(images_face) == 0:
    print('Total images found:', len(images_face))
else:
    print('Images found:', images_face)
    print('Total images:', len(images_face))

if len(images_face) == 0:
    print('\nNo images found...')
    print('Looking for data file and name list...\n')
    time.sleep(1)
    response = 'n'
else:
    # get user response to build new dataset file
    response = input('\nDo you want to make a new encoding of all images?\n\
---> ALL previous encodings and names will be DELETED!: \'Y\' or \'n\' ? ')

if response == 'Y':

    print('\nCollecting images and encoding...')

    name_list = []
    faces_encoded = []

    for face in images_face:
        name_list.append(face)
        img = PIL.Image.open(face_path + face)
        img = img.convert('RGB')
        img_loaded = np.array(img)
        
        faces_encoded.append(face_encodings(img_loaded)[0])

    # remove old dataset file & name file if present
    try:
        os.remove(face_path + 'data_file/' + 'all_encoded_faces')
        os.remove(face_path + 'data_file/' + 'name_list')
    except OSError:
        pass

    # create new single dataset file of our face encodings
    try:
        with open(face_path + 'data_file/' + 'all_encoded_faces', 'wb') as f:
            pickle.dump(faces_encoded , f)
        f.close()
    except IOError:
        print('No \'data_file\' directory exists...\n\n\
Please make a new directory for the \'data_file\' folder at path:')
        print(face_path + 'data_file/')
        sys.exit()

    # clean names of file extensions
    name_list = [x[:-4] for x in name_list]

    try:
        # create new name list for dataset file of our face encodings
        # we could store as a binary with pickle if desired
        with open(face_path + 'data_file/' + 'name_list', 'w') as f:
            for name in name_list:
                f.write('%s\n' % name)
        f.close()
    except IOError:
        print('No \'data_file\' directory was found...\n\n\
Please make a new directory for the \'data_file\' folder at path:')
        print(face_path + 'data_file/')
        sys.exit()

## Face detection system prep
##

# nano compatability
platform.machine() == "aarch64"

# Load our face encodings dataset file
try:
    with open(face_path + 'data_file/all_encoded_faces', 'rb') as f:
        faces_encoded = pickle.load(f)
except IOError:
    print('Encoded dataset file not found at path:')
    print(face_path + 'data_file/')
    time.sleep(1)
    print('\nShutting down...')
    time.sleep(1)
    sys.exit()

# load our face encodings name list
try:
    with open(face_path + 'data_file/name_list', 'r') as f:
        name_list = f.read().splitlines()
except IOError:
    print('Name list not found at path')
    print(face_path + 'data_file/')
    time.sleep(1)
    print('\nShutting down...')
    time.sleep(1)
    sys.exit()

print('\nLoading image dataset...')
time.sleep(1)

# openCV/nano compatability for camera (nvidia required format)
def get_jetson_gstreamer_source(capture_width=640, capture_height=480, display_width=640, display_height=480, framerate=90, flip_method=0):

    return (
            f'nvarguscamerasrc ! video/x-raw(memory:NVMM), ' +
            f'width=(int){capture_width}, height=(int){capture_height}, ' +
            f'format=(string)NV12, framerate=(fraction){framerate}/1 ! ' +
            f'nvvidconv flip-method={flip_method} ! ' +
            f'video/x-raw, width=(int){display_width}, height=(int){display_height}, format=(string)BGRx ! ' +
            'videoconvert ! video/x-raw, format=(string)BGR ! appsink'
            )

face_names = []
face_locs = []
face_encodes = []
face_names_all = []
names_attended = []

# Create reference for webcam
video_capture = cv2.VideoCapture(get_jetson_gstreamer_source(), cv2.CAP_GSTREAMER)

print('\nSystem ready...')

## Face detection start
##

while True:
    # Grab a video frame
    ret, frame = video_capture.read()

    # Resize frame to speed up processing & convert to RGB
    frame_sized = (cv2.resize(frame, (0, 0), fx=0.25, fy=0.25))[:, :, ::-1]

    # Find all faces and face encodings from the now downsized frame of video
    face_locs = face_locations(frame_sized)
    face_encodes = face_encodings(frame_sized, face_locs)

    face_names = []
    for face_encoding in face_encodes:
        # See if the face in frame is a match among our face encodings
        matches = compare_faces(faces_encoded, face_encoding,
        rigidity=0.6)
        name = "Unregistered"

        # Match with face that has smallest distance among all faces
        face_dist = face_similarity(faces_encoded, face_encoding)
        best_match_index = np.argmin(face_dist)
        if matches[best_match_index]:
            name = name_list[best_match_index]

        face_names.append(name)
        # mark only detected and registered faces as attended
        if name not in names_attended and name != 'Unregistered'\
and name in face_names:
            print('\nAttendance Recorded: ', name)
            names_attended.append(name)
            send_to_db(name)
    
    for (top, right, bottom, left), name in zip(face_locs, face_names):
        # upsize image to original after downsizing before
        top, bottom, left, right = top*4, bottom*4, left*4, right*4

        # Make box around face - for identified/attended
        if name in names_attended:
            cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 2)

        # Label of box - for attended
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (255, 0, 0), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Make box around face - for unregistered/unidentified
        else:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Label of box - for unregistered
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_COMPLEX
            cv2.putText(frame, name, (left + 7, bottom - 7), font, 1.0, (255, 255, 255), 1)

    # Write to screen
    cv2.imshow('Video', frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        
    # Press 'p' to take new pic
    if cv2.waitKey(1) & 0xFF == ord('p'):
        shot = input('Enter \'p\' to take a picture')
        if shot == 'p':
            ret, pic = video_capture.read()
            cv2.imshow('Picture', pic)
            yname = input('Enter your name: ')
            vidObj = cv2.VideoCapture(face_path + yname + '.jpg')
            success, image = video_capture.read()
            img = cv2.imread(face_path + yname + '.jpg')
            cv2.imwrite(face_path + yname + '.jpg', \
0, image) #[cv2.IMWRITE_JPEG_QUALITY,100])
            #time.sleep(1)
            video_capture.release()
        else:
            continue

        
# Release and close window
video_capture.release()
cv2.destroyAllWindows()

sys.exit()
