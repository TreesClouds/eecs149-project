import pyrealsense2.pyrealsense2 as rs
import numpy as np
import cv2


class Camera:
  def __init__(self):
    self.pipe = rs.pipeline()
    cfg = rs.config()

    cfg.enable_stream(rs.stream.color, 640,480, rs.format.bgr8, 30)

    self.pipe.start(cfg)

    self.arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)
    self.arucoParams = cv2.aruco.DetectorParameters_create()

  def get_coordinates(self):
    frame = self.pipe.wait_for_frames() 
    color_frame = frame.get_color_frame()

    color_image = np.asanyarray(color_frame.get_data())

    (corners, ids, rejected) = cv2.aruco.detectMarkers(color_image,
		self.arucoDict, parameters=self.arucoParams)

    pacmanX = -1
    pacmanY = -1

    ghostX = -1
    ghostY = -1

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

            # compute and draw the center (x, y)-coordinates of the aruco marker
            cX = int((topLeft[0] + bottomRight[0]) / 2.0)
            cY = int((topLeft[1] + bottomRight[1]) / 2.0)

            if markerID == 2:
              pacmanX = cX
              pacmanY = cY
            elif markerID == 3:
              ghostX = cX
              ghostY = cY
    
    return pacmanX, pacmanY, ghostX, ghostY
