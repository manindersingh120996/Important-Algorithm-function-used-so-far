"""
In this Code, user can give input video file,
the file size(length) will be reduced by removing the duplicate
frames from the video on the basis of comparison of frame and it's next frame based on
MSE of average of pixels in two frames.

It is as effective as reducing video time from 8 minutes to 50 seconds
and not loosing important information
"""

import cv2
import numpy as np

# Function to calculate Mean Squared Error (MSE) between two frames
def calculate_frame_difference(frame1, frame2):
    mse = np.sum((frame1.astype("float") - frame2.astype("float")) ** 2) / float(frame1.size)
    return mse

# Function to remove duplicate frames from a video
def remove_duplicate_frames(video_path, output_path, mse_threshold=1000, display_duration=1):
    # Open the video file for reading
    cap = cv2.VideoCapture(video_path)
    # Check if the video file is opened successfully
    if not cap.isOpened():
        print("Error: Could not open video.")
        return
    # List to store unique frames
    frames = []
    # Read the first frame
    ret, frame = cap.read()
    frames.append(frame)
    # Loop through the video frames
    while ret:
        # Read the next frame
        ret, frame = cap.read()
        # Check if the frame was read successfully
        if ret:
            # Calculate the Mean Squared Error (MSE) between the current and last frame
            mse = calculate_frame_difference(frames[-1], frame)
            # Append the frame to the list if the MSE is above the threshold
            if mse > mse_threshold:
                frames.append(frame)

    # Release the video capture object
    cap.release()

    # Write unique frames to a new video file
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, 30.0, (frames[0].shape[1], frames[0].shape[0]))

    for frame in frames:
        # Repeat each unique frame for display_duration seconds
        for _ in range(int(30 * display_duration)):
            out.write(frame)

    # Release the video writer object
    out.release()

# Example usage
remove_duplicate_frames('input_video.mp4', 'output_video2.mp4', mse_threshold=1000, display_duration=1)
