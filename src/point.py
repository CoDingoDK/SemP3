class Point:
    def __init__(self, coord, center_of_mass_angle, center_of_mass_dist):
        self.coord = coord
        self.center_of_mass_angle = center_of_mass_angle
        self.center_of_mass_dist = center_of_mass_dist

    def __eq__(self, other):
        if isinstance(other, Point):
            return self.center_of_mass_dist == other.center_of_mass_dist and \
                   self.center_of_mass_angle == other.center_of_mass_angle
        else:
            return False
