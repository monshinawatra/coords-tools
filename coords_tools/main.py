import cv2
import numpy as np

# 100 colors for 100 points
POINT_COLORS = np.random.randint(0, 255, (100, 3)).tolist()
global is_button_down

def CallBackFunc(event, x, y, flags, param):
    corner_points_list = param
    global is_button_down
    # If left button is clicked, add point to list
    if event == cv2.EVENT_LBUTTONDOWN and not is_button_down:
        is_button_down = True
        corner_points_list.append([x, y])
    # If mouse is moving and left button is down, update last point in list
    # (is dragging)
    elif event == cv2.EVENT_MOUSEMOVE and is_button_down:
        corner_points_list[-1] = [x, y]

    # Reset is_button_down flag when left button is released
    elif event == cv2.EVENT_LBUTTONUP and is_button_down:
        is_button_down = False


def get_area_coords(frame: np.ndarray, length:int) -> np.ndarray:
    global is_button_down
    # Initialize global variables
    is_button_down, corner_points_list = False, []

    try:
        # Initialize window
        windowName = "MouseCallback"
        cv2.namedWindow(windowName)
        cv2.setMouseCallback(windowName, CallBackFunc, (corner_points_list))

        # Main loop
        while cv2.getWindowProperty(windowName, 0) >= 0:
            im0s = frame.copy()
            image = cv2.resize(im0s, (960, 540))
            # Draw points (Real-time)
            for i, point in enumerate(corner_points_list):
                cv2.circle(image, point, 7, (255, 255, 255), -1)
                cv2.circle(image, point, 5, POINT_COLORS[i], -1)

            # Draw lines connecting between points (Real-time)
            for i in range(len(corner_points_list)):
                if i == len(corner_points_list) - 1:
                    if (len(corner_points_list) > 2):
                        cv2.line(
                            image,
                            corner_points_list[i],
                            corner_points_list[0],
                            (0, 255, 0),
                            1,
                        )
                    continue

                cv2.line(
                    image,
                    corner_points_list[i],
                    corner_points_list[i+1],
                    (0, 255, 0),
                    1,
                )

            # Show image
            cv2.imshow(windowName, image)
            # Exit if already have 4 points
            # if cv2.waitKey(1) and (len(corner_points_list) >= length and not is_button_down):
            if cv2.waitKey(1) & 0xFF == ord('q'):
                corner_points_list = np.array(corner_points_list, dtype=np.float32)
                # Normalize points
                corner_points_list /= np.array([960, 540], dtype=np.float32)
                # Multiply by image size
                corner_points_list *= np.array([frame.shape[1], frame.shape[0]], dtype=np.float32)
                break
    except Exception as e:
        print(e)
    
    finally:
        # Destroy all cv2 windows
        cv2.destroyAllWindows()
    return corner_points_list

if __name__ == "__main__":
    frame = np.zeros((540, 960, 3), dtype=np.uint8)
    print(get_area_coords(frame, 5))
