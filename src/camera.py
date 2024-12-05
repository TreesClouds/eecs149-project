import pyrealsense2.pyrealsense2 as rs
import numpy as np
import cv2

pipe = rs.pipeline()
cfg = rs.config()

cfg.enable_stream(rs.stream.color, 640,480, rs.format.bgr8, 30)

pipe.start(cfg)

arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)
arucoParams = cv2.aruco.DetectorParameters_create()

while True:
    frame = pipe.wait_for_frames() 
    color_frame = frame.get_color_frame()

    color_image = np.asanyarray(color_frame.get_data())

    (corners, ids, rejected) = cv2.aruco.detectMarkers(color_image,
		arucoDict, parameters=arucoParams)

    
    # check if any aruco tags have been detected
    if len(corners) > 0:

        ids = ids.flatten()

        # loop over the detected aruco corners
        for (markerCorner, markerID) in zip(corners, ids):
            # extract the marker corners. Order is: (top-left, top-right, bottom-right, and bottom-left)
            corners = markerCorner.reshape((4, 2))
            (topLeft, topRight, bottomRight, bottomLeft) = corners

            # int conversions
            topRight = (int(topRight[0]), int(topRight[1]))
            bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
            bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
            topLeft = (int(topLeft[0]), int(topLeft[1]))
        
            # draw the bounding boxes for each tag
            cv2.line(color_image, topLeft, topRight, (0, 255, 0), 2)
            cv2.line(color_image, topRight, bottomRight, (0, 255, 0), 2)
            cv2.line(color_image, bottomRight, bottomLeft, (0, 255, 0), 2)
            cv2.line(color_image, bottomLeft, topLeft, (0, 255, 0), 2)

            # compute and draw the center (x, y)-coordinates of the aruco marker
            cX = int((topLeft[0] + bottomRight[0]) / 2.0)
            cY = int((topLeft[1] + bottomRight[1]) / 2.0)
            cv2.circle(color_image, (cX, cY), 4, (0, 0, 255), -1)

            # draw the aruco tag ID
            cv2.putText(color_image, str(markerID), (topLeft[0], topLeft[1] - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
 
    cv2.imshow('rgb', color_image)

    if cv2.waitKey(1) == ord('q'):
        break

pipe.stop()
