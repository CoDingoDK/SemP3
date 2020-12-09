import cv2 as cv
import numpy as np
import math
from hand import *
from point import Point


def segmentation(image, frame_name, min_size):
    hand = None
    res = cv.flip(image, 1)
    ret, thresh = cv.threshold(res, 0, 255, cv.THRESH_BINARY)
    return_image = thresh
    num_labels, component_image = cv.connectedComponents(thresh)
    if np.max(component_image) > 0:
        label_hue = np.uint8(255 * component_image / np.max(component_image))
    else:
        label_hue = np.uint8(255 * component_image / np.max(1))
    blank_ch = 255 * np.ones_like(label_hue)
    component_overlay_image = cv.merge([blank_ch])
    component_overlay_image[label_hue == 0] = 0
    contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    if len(contours) != 1:
        None
        cv.drawContours(component_overlay_image, contours, -1, (255), 1)
        cv.imshow("contour", component_overlay_image)
    if contours:
        largest_countour = max(contours, key=cv.contourArea)
    else:
        largest_countour = None
    if largest_countour is not None and len(largest_countour) > 4:
        largest_countour_moment = cv.moments(largest_countour)
        bounding_rect = cv.fitEllipse(largest_countour)
    else:
        bounding_rect = None
    if bounding_rect is not None:
        (xc, yc), (d1, d2), angle = bounding_rect
        major = max(d1, d2) / 2
        if angle > 90:
            angle = angle - 90
        else:
            angle = angle + 90
        major_lower_coord = xc + math.cos(math.radians(angle + 180)) * major, yc + math.sin(math.radians(angle + 180)) * major
        major_upper_coord = xc + math.cos(math.radians(angle)) * major, yc + math.sin(math.radians(angle)) * major

        if bounding_rect is not None:
            (xc2, yc2), (d12, d22), angle2 = bounding_rect
            minor = min(d12, d22) / 2
            if angle > 90:
                angle2 = angle2 - 180
            else:
                angle2 = angle2 + 180
            minor_upper_coord = xc2 + math.cos(math.radians(angle2)) * minor, yc2 + math.sin(math.radians(angle2)) * minor
            minor_lower_coord = xc2 + math.cos(math.radians(angle2 + 180)) * minor, yc2 + math.sin(math.radians(angle2 + 180)) * minor

            diff_major = major_upper_coord[0] - major_lower_coord[0], major_upper_coord[1] - major_lower_coord[1]
            diff_minor = minor_upper_coord[0] - minor_lower_coord[0], minor_upper_coord[1] - minor_lower_coord[1]

            euq_major = cv.sqrt(diff_major[0]**2 + diff_major[1]**2)
            euq_minor = cv.sqrt(diff_minor[0]**2 + diff_minor[1]**2)

            major_axis_len = (euq_major[0]/2, euq_minor[0]/2)
            hand_mass_center_coord = int(largest_countour_moment["m10"] / largest_countour_moment["m00"]), int(largest_countour_moment["m01"] / largest_countour_moment["m00"])

            extremities = np.zeros(component_overlay_image.shape,dtype=np.uint8)
            extremities = extremities.astype(np.uint8)
            cv.circle(extremities, hand_mass_center_coord, int(major_axis_len[0]*0.75), 255, -1)
            extremities = component_overlay_image - extremities
            extremities[extremities < 255] = 0
            _, extremity_labels, stats, centroids = cv.connectedComponentsWithStats(extremities, 8, cv.CV_32S)
            cv.imshow("labels", extremities)
            points = np.zeros_like(extremities)
            point_list: [Point] = []
            for i, (centroid, stat) in enumerate(zip(centroids, stats)):
                if i == 0:
                    continue
                if stat[4] > min_size:
                    center_of_mass_angle = point_to_point_angle(hand_mass_center_coord, (centroid[0], centroid[1]))
                    if center_of_mass_angle is None:
                        continue
                    center_of_mass_dist = euclidean_dist(hand_mass_center_coord, (centroid[0], centroid[1]))
                    p = Point((int(centroid[0]), int(centroid[1])), center_of_mass_angle, center_of_mass_dist)
                    point_list.append(p)
                    cv.circle(points, p.coord, 2, 255)
                    cv.line(points, hand_mass_center_coord, p.coord, 255)
            if len(point_list) < 3:
                return None, hand
            cv.circle(points, hand_mass_center_coord, 5, 255)
            wrist_assumption_point: Point = largest_angle(point_list, points)
            if wrist_assumption_point is not None:
                point_list.remove(wrist_assumption_point)
            else:
                return None, hand
            thumb_assumption_point = max(point_list, key=lambda p: p.center_of_mass_dist, default=None)
            cv.circle(points, thumb_assumption_point.coord, 50, 255)
            hand = Hand(hand_mass_center_coord)
            if wrist_assumption_point is not None and 125 > wrist_assumption_point.center_of_mass_angle > -40:
                text_coord = wrist_assumption_point.coord[0], wrist_assumption_point.coord[1]+20
                cv.putText(points, str("wrist"), text_coord, cv.FONT_HERSHEY_SIMPLEX, 0.5, 255, 1, cv.LINE_AA)
                hand.angle = wrist_assumption_point.center_of_mass_angle
                text_coord = thumb_assumption_point.coord[0], thumb_assumption_point.coord[1] + 20
                longest_extremity_relative_to_hand_com = world_to_hand_orientation(thumb_assumption_point, wrist_assumption_point)
                if abs(longest_extremity_relative_to_hand_com) > 135:
                    if 2 <= len(point_list) <= 3:
                        fingers_only = [Extremity(f, True) for f in point_list if abs(world_to_hand_orientation(f, wrist_assumption_point)) > 135]
                        hand.fingers = fingers_only
                        fingers_removed = [f for f in point_list if 90 <= world_to_hand_orientation(f, wrist_assumption_point) <= 135]
                        if fingers_removed:
                            thumb = fingers_removed[0]
                            if 135 >= abs(world_to_hand_orientation(thumb, wrist_assumption_point)) >= 75:
                                hand.thumb = Extremity(thumb, True)
                                hand.wrist = Extremity(wrist_assumption_point, True)
                elif 135 >= abs(longest_extremity_relative_to_hand_com) > 75:
                    # Assume thumb
                    hand.thumb = Extremity(thumb_assumption_point, True)
                    hand.wrist = Extremity(wrist_assumption_point, True)
            else:
                return None, None
            cv.imshow("fingers", points)
    return component_overlay_image, hand


def interpolate(origin, destination, norm_percentage=1.0):
    diff_x = destination[0] - origin[0]
    diff_y = destination[1] - origin[1]
    return int(origin[0]+diff_x*norm_percentage), int(origin[1] + diff_y*norm_percentage)


def point_to_point_angle(origin, destination):
    if (any(origin) and any(destination)) and destination[0]-origin[0] != 0:
        return int(math.degrees(math.atan2((destination[1] - origin[1]),(destination[0] - origin[0]))))
    return None

def largest_angle(points: [Point], img):
    res = sorted(points, key=lambda p: p.center_of_mass_angle, reverse=False)
    resstring = []
    for i, p in enumerate(res):
        resstring.append(p.center_of_mass_angle)
        cv.putText(img, str(p.center_of_mass_angle), p.coord, cv.FONT_HERSHEY_SIMPLEX,0.4, 255, 1, cv.LINE_AA)
        cv.putText(img, str(int(p.center_of_mass_dist)), (p.coord[0], p.coord[1]+10),cv.FONT_HERSHEY_SIMPLEX,0.4, 255, 1, cv.LINE_AA)
    largest_angle_diff_index = -1
    largest_angle_diff = 0
    for i, p in enumerate(res):
        if i != 0:
            left = i-1
        else:
            left = len(res)-1
        if i != len(res)-1:
            right = i+1
        else:
            right = 0
        curr_diff = abs_angle_diff(res[left].center_of_mass_angle, res[i].center_of_mass_angle) + \
                    abs_angle_diff(res[i].center_of_mass_angle, res[right].center_of_mass_angle)
        if curr_diff > largest_angle_diff:
            largest_angle_diff_index = i
            largest_angle_diff = curr_diff
    if largest_angle_diff_index == -1:
        return None
    else:
        return res[largest_angle_diff_index]



def abs_angle_diff(origin_angle, dest_angle):
    phi = abs(origin_angle - dest_angle) % 360
    if phi > 180:
        return 360-phi
    else:
        return phi

def world_to_hand_orientation(point, hand_point):
    hand_relative_orientation_offset = (point.center_of_mass_angle - hand_point.center_of_mass_angle) % 360
    if hand_relative_orientation_offset > 180:
        return -(360 - hand_relative_orientation_offset)
    elif hand_relative_orientation_offset < -180:
        return 360 - abs(hand_relative_orientation_offset)
    else:
        return hand_relative_orientation_offset


def euclidean_dist(origin, destination):
    diff_x, diff_y = origin[0] - destination[0], origin[1] - destination[1]
    return math.sqrt(diff_x**2 + diff_y**2)

#
# def find_thumb(point_list, wrist):
#     closest_accurate_angle = 360
#     thumb_index = None
#     left_bounds = 70, 135
#     left_middle = sum(left_bounds)/len(left_bounds)
#     right_bounds = -70, -125
#     right_middle = sum(right_bounds)/len(left_bounds)
#     for i, p in enumerate(point_list):
#         p_angle_relative = world_to_hand_orientation(p, wrist)
#
#         if left_bounds[0] <= p_angle_relative <= left_bounds[1]:
#             point_diff_from_expected_thumb = abs_angle_diff(p_angle_relative, left_middle)
#             if point_diff_from_expected_thumb < closest_accurate_angle:
#                 closest_accurate_angle = point_diff_from_expected_thumb
#                 thumb_index = i
#         elif right_bounds[0] >= p_angle_relative >= right_bounds[1]:
#             point_diff_from_expected_thumb = abs_angle_diff(p_angle_relative, right_middle)
#             if point_diff_from_expected_thumb < closest_accurate_angle:
#                 closest_accurate_angle = point_diff_from_expected_thumb
#                 thumb_index = i
#     if thumb_index is not None:
#         return point_list[thumb_index]
#     else:
#         return None
