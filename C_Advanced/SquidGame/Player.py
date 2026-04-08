import cv2
from cvzone.PoseModule import PoseDetector



class Player:
    """Class to manage individual player data"""

    def __init__(self, player_id, cam_id=0):
        self.id = player_id
        self.cam_id = cam_id
        self.cap = cv2.VideoCapture(cam_id, cv2.CAP_DSHOW)
        self.detector = PoseDetector()
        self.subtractor = cv2.createBackgroundSubtractorMOG2(3)

        # Player state
        self.gameStart = False
        self.gameOver = False
        self.gameWon = False
        self.greenLight = True
        self.greenFirstFrame = True
        self.countRed = 0
        self.randomDelay = 0
        self.timeStart = 0
        self.timeStartGreen = 0
        self.bbox = None
        self.detected = False

    def update_camera(self, width, height):

        self.cap.set(3, width)
        self.cap.set(4, height)

    def read_frame(self):

        return self.cap.read()

    def release(self):

        self.cap.release()