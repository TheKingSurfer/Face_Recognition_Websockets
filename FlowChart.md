# Server-Client Communication and Face Recognition Flowchart

## Server Side

1. **Start Server:**
   - Initialize face recognition module (`SimpleFacerec`).
   - Load encoding images using `load_encoding_images`.

2. **Initialize WebSocket Server:**
   - Use `websockets.serve` to start the server.

3. **Video Stream Loop:**
   - Open the camera using OpenCV (`cv2.VideoCapture`).
   - Capture frames and analyze them using `analyze_frame`.
   - Combine frame and analysis result.
   - Send the data to the client using WebSocket.

## Client Side

1. **Connect to Server:**
   - Use `websockets.connect` to establish a WebSocket connection.

2. **Receive Video Stream:**
   - Use `receive_video` to continuously receive data from the server.
   - Parse the JSON data to extract frame and analysis result.

3. **Display Live Stream:**
   - Decode the frame using `decode_frame`.
   - Display the live stream using OpenCV (`cv2.imshow`).

4. **Process Analysis Result:**
   - Print detected faces and face locations.

## Face Recognition Module (facerec_module.py)

1. **Initialize `SimpleFacerec`:**
   - Initialize lists for known face encodings and names.

2. **Load Encoding Images:**
   - Load images from the specified path.
   - Extract names without extensions.
   - Check validity of face names using `is_valid_face_name`.
   - Skip invalid names and load face encodings.

3. **Recognize Faces:**
   - Resize the frame for faster processing.
   - Detect face locations using `face_recognition`.
   - Compare face encodings to known faces.
   - Return recognized face names and locations.

4. **Encode and Decode Frames:**
   - Use base64 to encode and decode frames for WebSocket transmission.

## WebSocket Communication:

1. **Server Sends:**
   - Server sends a JSON object containing frame and analysis result.

2. **Client Receives:**
   - Client receives the JSON object from the server.

3. **Analysis Result Processing:**
   - Extract information from the JSON object.
   - Decode the frame for display.

4. **Display and Analysis:**
   - Display the live stream.
   - Process the analysis result (e.g., print detected faces and locations).

## End Communication:

1. **Close Connection:**
   - When the user exits, close the WebSocket connection and release resources.

