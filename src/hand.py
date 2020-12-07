LEFT = 1
RIGHT = 2
UP = 3
DOWN = 4
PLAY_PAUSE = 5

VALID_THUMB_DIST = 0


class Hand:
    def __init__(self, com_coord):
        self.CoM_coord = com_coord  # Center of mass coordinates for the hand
        self.angle = None
        self.fingers = []
        self.thumb = None
        self.wrist = None
        self.sign = None

    def get_sign(self):
        return self.sign

    def calc_sign(self):
        if self.thumb is not None and self.thumb.is_valid_dist:
            if abs(self.thumb.angle_from_hand_com) <= 45:
                self.sign = RIGHT
            if abs(self.thumb.angle_from_hand_com) >= 135:
                self.sign = LEFT
            if 45 < self.thumb.angle_from_hand_com < 135:
                self.sign = UP
            if -45 > self.thumb.angle_from_hand_com > -135:
                self.sign = UP

    def __eq__(self, other):
        if isinstance(other, Hand):
            return self.sign == other.sign
        return False


class Extremity:
    def __init__(self, com_coord, angle_from_hand_com, dist_from_hand_com, extended):
        self.CoM_coord = com_coord  # Center of mass coordinates for this extremity
        self.angle_from_hand_com = angle_from_hand_com
        self.dist_from_hand_com = dist_from_hand_com
        self.extended = extended
        self.is_valid_dist = False
