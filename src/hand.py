from point import Point

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
        self.fingers: [Extremity] = []
        self.thumb: Extremity = None
        self.wrist: Extremity = None
        self.sign: Extremity = None

    def get_sign(self):
        return self.sign

    def calc_sign(self):
        if self.wrist is not None:
            if self.wrist.angle_from_hand_com <= -50 or self.wrist.angle_from_hand_com >= 120:
                return
            if self.fingers and self.thumb is not None and self.thumb.extended:
                if 135 >= self.wrist.angle_from_hand_com >= 40:
                    self.sign = PLAY_PAUSE
                return
            if self.thumb is not None and self.thumb.extended:
                if abs(self.thumb.angle_from_hand_com) <= 45:
                    self.sign = RIGHT
                if abs(self.thumb.angle_from_hand_com) >= 135:
                    self.sign = LEFT
                if 45 < self.thumb.angle_from_hand_com < 135:
                    self.sign = DOWN
                if -45 > self.thumb.angle_from_hand_com > -135:
                    self.sign = UP

    def __eq__(self, other):
        if isinstance(other, Hand):
            return self.sign == other.sign
        return False

    def __repr__(self):
        string = ""
        if self.sign == 1:
            string = "LEFT"
        elif self.sign == 2:
            string = "RIGHT"
        elif self.sign == 3:
            string = "UP"
        elif self.sign == 4:
            string = "DOWN"
        elif self.sign == 5:
            string = "PLAY"
        if self.thumb is not None:
            string += str(int(self.thumb.angle_from_hand_com))
        return string

class Extremity:
    def __init__(self, point: Point, extended):
        self.CoM_coord = point.coord  # Center of mass coordinates for this extremity
        self.angle_from_hand_com = point.center_of_mass_angle
        self.dist_from_hand_com = point.center_of_mass_dist
        self.extended = extended
        self.is_valid_dist = False
