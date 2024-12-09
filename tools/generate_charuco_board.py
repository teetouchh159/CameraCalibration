import cv2
import numpy as np

# Parameters for Charuco board
squares_x = 5  # Number of squares along the x-axis
squares_y = 7  # Number of squares along the y-axis
square_length = 0.04  # Square size in meters
marker_length = 0.02  # ArUco marker size in meters

# Dictionary for ArUco markers
aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)
charuco_board = cv2.aruco.CharucoBoard_create(
    squares_x, squares_y, square_length, marker_length, aruco_dict
)

# Save the board image
board_image = charuco_board.draw((600, 800))  # Adjust resolution
cv2.imwrite("charuco_board.png", board_image)

