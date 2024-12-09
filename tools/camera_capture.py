import gi
import os
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib
import cv2
import numpy as np
import threading

bgr_image = None
path_name = "Captured_images"
os.makedirs(path_name, exist_ok=True)
count = 0

def on_keyboard_event():
    """
    Capture a frame when the user presses Enter and save it as a .png file.
    """
    global bgr_image, count
    if bgr_image is not None:
        print("Capturing frame...")
        filename = f"{path_name}/captured_frame_{count}.png"
        cv2.imwrite(filename, bgr_image)
        count += 1
        print(f"Frame saved as {filename}.")
    else:
        print("No frame available to capture.")



def capture_frames():
    global bgr_image
    Gst.init(None)

    # Define the GStreamer pipeline with appsink for capturing frames
    pipeline_str = (
        "v4l2src device=/dev/video0 ! "
        "video/x-raw,format=UYVY,width=1920,height=1080,framerate=30/1 ! "
        "appsink name=appsink sync=false emit-signals=true max-buffers=1 drop=true"
    )

    pipeline = Gst.parse_launch(pipeline_str)
    pipeline.set_state(Gst.State.PLAYING)  

    try:
        appsink = pipeline.get_by_name("appsink")
        while True:
            sample = appsink.emit("pull-sample")
            
            if sample:
                buffer = sample.get_buffer()
                caps = sample.get_caps()
                width = caps.get_structure(0).get_value("width")
                height = caps.get_structure(0).get_value("height")

                # Convert the GStreamer buffer to a NumPy array
                success, mapinfo = buffer.map(Gst.MapFlags.READ)
                if not success:
                    print("Failed to map buffer.")
                    continue
                try:
                    data = np.frombuffer(mapinfo.data, dtype=np.uint8)
                    data = data.reshape((height, width, 2))  # UYVY is 2 bytes per pixel

                    # Convert UYVY to BGR using OpenCV
                    bgr_image = cv2.cvtColor(data, cv2.COLOR_YUV2BGR_UYVY)

                    cv2.imshow("Capture Frame", bgr_image)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                finally:
                    buffer.unmap(mapinfo)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        cv2.destroyAllWindows()
        pipeline.set_state(Gst.State.NULL)
        
def CheckKeyboardEvent():
    try:
        while True:
            input("Press Enter to capture a frame...")
            on_keyboard_event()
    except KeyboardInterrupt:
        print("Exiting...")

if __name__ == "__main__":
    thread1 = threading.Thread(target=capture_frames, daemon=True)
    thread1.start()

    CheckKeyboardEvent()
