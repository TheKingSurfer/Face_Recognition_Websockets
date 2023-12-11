import asyncio
import websockets
import cv2
import json
from Logics.facerec_module import decode_frame

async def receive_video(websocket):
    while True:
        data_str = await websocket.recv()

        # Parse the received JSON data
        data = json.loads(data_str)

        # Extract frame and analysis result
        img_str = data["frame"]
        analysis_result = data["analysis"]

        # Decode the frame
        frame = decode_frame(img_str)

        # Display the live stream
        cv2.imshow('Live Stream', frame)

        # Process the analysis result (in this case, print detected faces)
        detected_faces = analysis_result.get("faces", [])
        if detected_faces:
            print("Detected Faces:", detected_faces)

            # Extract face locations and print them
            for face_loc in detected_faces:
                print("Face Location:", face_loc)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

uri = "ws://localhost:8865"
asyncio.get_event_loop().run_until_complete(websockets.connect(uri, ping_timeout=None))

websocket = asyncio.get_event_loop().run_until_complete(websockets.connect(uri))
asyncio.get_event_loop().run_until_complete(receive_video(websocket))
