import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import socket
import struct
import time


UDP_IP = "127.0.0.1"
UDP_PORT = 5005
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3, 640)  # Width
cap.set(4, 480)  # Height


detector = HandDetector(maxHands=1, detectionCon=0.8, minTrackCon=0.8)

# State variables
final_x, final_y = 0.5, 0.5
fps = 0
frame_count = 0
prev_time = time.time()

print("Palm Center Tracking Started! Press ESC to exit.")

while True:
    success, img = cap.read()
    if not success:
        continue

    # Flip horizontally for mirror view
    img = cv2.flip(img, 1)

    # Find hands
    hands, img = detector.findHands(img, draw=False, flipType=False)

    if hands:
        hand = hands[0]
        lmList = hand["lmList"]

        # Get palm landmarks for center calculation
        # Using wrist (0), index finger MCP (5), and pinky MCP (17)
        if len(lmList) >= 18:  # Ensure we have enough landmarks
            wrist = lmList[0]  # Landmark 0: Wrist
            index_mcp = lmList[5]  # Landmark 5: Index finger MCP
            pinky_mcp = lmList[17]  # Landmark 17: Pinky MCP

            # Calculate center of palm (average of wrist, index MCP, and pinky MCP)
            palm_center_x = (wrist[0] + index_mcp[0] + pinky_mcp[0]) / 3
            palm_center_y = (wrist[1] + index_mcp[1] + pinky_mcp[1]) / 3

            # Alternative: Using only wrist and middle finger MCP (9) for simpler calculation
            # middle_mcp = lmList[9]
            # palm_center_x = (wrist[0] + middle_mcp[0]) / 2
            # palm_center_y = (wrist[1] + middle_mcp[1]) / 2

            # Convert to normalized coordinates (0-1)
            h, w, _ = img.shape
            final_x = palm_center_x / w
            final_y = palm_center_y / h

            # Send via UDP
            data = struct.pack("ff", final_x, final_y)
            sock.sendto(data, (UDP_IP, UDP_PORT))

            # Draw palm center
            cv2.circle(img, (int(palm_center_x), int(palm_center_y)), 15, (0, 255, 0),
                       cv2.FILLED)  # Green filled circle
            cv2.circle(img, (int(palm_center_x), int(palm_center_y)), 18, (255, 0, 0), 2)  # Blue outline

            # Draw connecting lines to show the triangle used for calculation
            cv2.line(img, (int(wrist[0]), int(wrist[1])),
                     (int(index_mcp[0]), int(index_mcp[1])), (255, 255, 0), 2)
            cv2.line(img, (int(index_mcp[0]), int(index_mcp[1])),
                     (int(pinky_mcp[0]), int(pinky_mcp[1])), (255, 255, 0), 2)
            cv2.line(img, (int(pinky_mcp[0]), int(pinky_mcp[1])),
                     (int(wrist[0]), int(wrist[1])), (255, 255, 0), 2)


            cv2.circle(img, (int(wrist[0]), int(wrist[1])), 8, (0, 0, 255), cv2.FILLED)  # Red: Wrist
            cv2.circle(img, (int(index_mcp[0]), int(index_mcp[1])), 8, (0, 255, 255), cv2.FILLED)  # Yellow: Index MCP
            cv2.circle(img, (int(pinky_mcp[0]), int(pinky_mcp[1])), 8, (255, 0, 255), cv2.FILLED)  # Purple: Pinky MCP



    # FPS calculation
    frame_count += 1
    current_time = time.time()
    if current_time - prev_time >= 1.0:
        fps = frame_count
        frame_count = 0
        prev_time = current_time

    # Display info
    cv2.putText(img, f"FPS: {fps}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.putText(img, f"Palm Center: ({final_x:.2f}, {final_y:.2f})", (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # Display hand detected status
    status_text = "Hand: Detected" if hands else "Hand: Not Detected"
    status_color = (0, 255, 0) if hands else (0, 0, 255)
    cv2.putText(img, status_text, (10, 90),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, status_color, 2)

    # Show which points are used for calculation (legend)
    if hands:
        cv2.putText(img, "Red: Wrist (0)", (10, 120),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(img, "Yellow: Index MCP (5)", (10, 140),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
        cv2.putText(img, "Purple: Pinky MCP (17)", (10, 160),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)

    # Show the image
    cv2.imshow("Hand Tracking", img)

    # Exit on ESC
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
print("Palm Center Tracking Stopped")