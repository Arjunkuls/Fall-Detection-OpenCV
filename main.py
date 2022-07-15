import cv2
import mediapipe as mp
import time

# Set up variables
mpDraw = mp.solutions.drawing_utils
mppose = mp.solutions.pose
pose = mppose.Pose()

positions = []
counter = 0
cap = cv2.VideoCapture("yeet.mp4")
ptime = 0
while(True):
      
    # Capture the video frame
    # by frame
    ret, frame = cap.read()

    # Convert frame from BGR to RGB
    frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Search for pose
    results = pose.process(frameRGB)
    if results.pose_landmarks:
        # Draw the lines
        mpDraw.draw_landmarks(frame, results.pose_landmarks, mppose.POSE_CONNECTIONS)

        # Convert results into array
        lms = []
        for id, lm in enumerate(results.pose_landmarks.landmark):
            h, w, c = frame.shape
            cx, cy = int(lm.x*w), int(lm.y * h)
            lms.append((cx, cy))
        positions.append(lms)

        # Write Coordinates of left ear to file
        with open('leftEar.txt', 'a') as f:
            f.write(str(positions[counter][7]))
            f.write("\n")

        # Write Coordinates of right ear to file
        with open('rightEar.txt', 'a') as f:
            f.write(str(positions[counter][8]))
            f.write("\n")

        counter+=1
  
    # Calculate FPS
    ctime = time.time()
    fps = 1/(ctime-ptime)
    ptime = ctime

    # Display FPS
    cv2.putText(frame, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    # Display the resulting frame
    cv2.imshow('frame', frame)
      
    
    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  
# After the loop release the cap object
cap.release()
# Destroy all the windows
cv2.destroyAllWindows()