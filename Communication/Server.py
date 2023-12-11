import os
import asyncio
import websockets
import cv2
import json
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
from Logics.facerec_module import SimpleFacerec, encode_frame
os.chdir(os.path.dirname(os.path.abspath(__file__)))
print("Working Directory:", os.getcwd())
# Configure the main logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s]: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Define the log file path for the current day
current_log_file = f'face_detection_{datetime.now().strftime("%Y-%m-%d")}.log'

# Check if the log file for the current day already exists
if not os.path.exists(current_log_file):
    # If not, create a new log file
    open(current_log_file, 'a').close()

# Create a rotating file handler for daily logs
log_file_handler = RotatingFileHandler(
    filename=current_log_file,
    maxBytes=1e6,  # Set the maximum file size to 1 MB
    backupCount=5  # Keep up to 5 backup files
)
log_file_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s]: %(message)s'))

# Add the rotating file handler to the main logger
logging.getLogger('').addHandler(log_file_handler)

# Initialize face recognition
sfr = SimpleFacerec()
# Construct absolute path relative to the script's location
images_relative_path = "../Images/BillGates/"
images_absolute_path = os.path.abspath(os.path.join(os.path.dirname(__file__), images_relative_path))

# Use the absolute path to load images
sfr.load_encoding_images(images_absolute_path)
async def analyze_frame(frame):
    # Detect faces and return analysis result
    face_locations, face_names = sfr.recognize_faces(frame)

    # Log detected faces to the rotating log file
    for name in face_names:
        if name != 'Unknown':
            log_file_handler.emit(logging.LogRecord(
                name='',
                level=logging.INFO,
                pathname='',
                lineno=0,
                msg=f'Detected face: {name}',
                args=(),
                exc_info=None
            ))

    return {"faces": face_names}

async def video_stream(websocket, path):
    logging.info('Client connected.')


    cap = cv2.VideoCapture(0)  # Use 0 for the default camera

    try:
        while cap.isOpened() and websocket.open:
            ret, frame = cap.read()

            if not ret:
                break

            try:
                # Analyze the frame
                analysis_result = await analyze_frame(frame)

                # Combine the frame and analysis result into a dictionary
                response_data = {"frame": encode_frame(frame), "analysis": analysis_result}

                # Send the data to the client as JSON
                await websocket.send(json.dumps(response_data))

            except Exception as e:
                # Log any exceptions that occur during frame processing
                logging.error(f'Error processing frame: {e}')

    except websockets.exceptions.ConnectionClosed:
        # Log when the client disconnects
        logging.info('Client disconnected.')
    finally:
        cap.release()

# Start the WebSocket server
start_server = websockets.serve(video_stream, "localhost", 8865)

# Log server start
logging.info('Server started.')

# Run the server
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
