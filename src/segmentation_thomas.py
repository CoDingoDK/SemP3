import cv2 as cv
import numpy as np
import math
import classification as cf

def segmentation(image, frame_name):
    hull = []
    res = image
    res = cv.flip(res, 1)
    res = cv.cvtColor(res, cv.COLOR_BGR2GRAY)
    ret, thresh = cv.threshold(res, 0, 255, cv.THRESH_BINARY)

    num_labels, labels_im = cv.connectedComponents(thresh)
    label_hue = np.uint8(255 * labels_im / np.max(labels_im))
    blank_ch = 255 * np.ones_like(label_hue)
    labels_img = cv.merge([blank_ch, blank_ch, blank_ch])
    labels_img[label_hue == 0] = 0

    contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    if len(contours) != 1:
        cv.drawContours(labels_img, contours, -1, (255, 0, 0), 1)
    if contours:
        c = max(contours, key=cv.contourArea)
    else:
        c = None
    if c is not None and len(c) > 4:
        M = cv.moments(c)
        x, y, w, h = cv.boundingRect(c)
        rect = cv.fitEllipse(c)
    else:
        rect = None
    if c is not None:
        left = tuple(c[c[:, :, 0].argmin()][0])
        right = tuple(c[c[:, :, 0].argmax()][0])
        top = tuple(c[c[:, :, 1].argmin()][0])
        bottom = tuple(c[c[:, :, 1].argmax()][0])

        cv.circle(labels_img, left, 8, (0, 50, 255), -1)
        cv.circle(labels_img, right, 8, (0, 255, 255), -1)
        cv.circle(labels_img, top, 8, (255, 50, 0), -1)
        cv.circle(labels_img, bottom, 8, (255, 255, 0), -1)

    # calculate points for each contour
    for i in range(len(contours)):
        # creating convex hull object for each contour
        hull.append(cv.convexHull(contours[i], False, ))
        new_c = max(hull, key=cv.contourArea)
        Minor = cv.moments(new_c)
    for i in range(len(contours)):
        color_contours = (0, 255, 0)
        color = (0, 0, 255)
        cv.drawContours(labels_img, contours, i, color_contours, 1, 8, hierarchy)
        cv.drawContours(labels_img, hull, i, color, 1, 8)
    if rect is not None:
        (xc, yc), (d1, d2), angle = rect
        major = max(d1, d2) / 2
        if angle > 90:
            angle = angle - 90
        else:
            angle = angle + 90

        xtop = xc + math.cos(math.radians(angle)) * major
        ytop = yc + math.sin(math.radians(angle)) * major
        xbot = xc + math.cos(math.radians(angle + 180)) * major
        ybot = yc + math.sin(math.radians(angle + 180)) * major

        cv.line(labels_img, (int(xtop), int(ytop)), (int(xbot), int(ybot)), (0, 0, 255), 3)
        if rect is not None:
            (xc2, yc2), (d12, d22), angle2 = rect
            minor = min(d12, d22) / 2
            if angle > 90:
                angle2 = angle2 - 180
            else:
                angle2 = angle2 + 180
            xtop2 = xc2 + math.cos(math.radians(angle2)) * minor
            ytop2 = yc2 + math.sin(math.radians(angle2)) * minor
            xbot2 = xc2 + math.cos(math.radians(angle2 + 180)) * minor
            ybot2 = yc2 + math.sin(math.radians(angle2 + 180)) * minor
            cv.line(labels_img, (int(xtop2), int(ytop2)), (int(xbot2), int(ybot2)), (0, 0, 255), 3)

            diff_x_major = xtop - xbot
            diff_y_major = ytop - ybot

            diff_x_minor = xtop2 - xbot2
            diff_y_minor = ytop2 - ybot2

            euq_major = cv.sqrt(diff_x_major * diff_x_major + diff_y_major * diff_y_major)
            euq_minor = cv.sqrt(diff_x_minor * diff_x_minor + diff_y_minor * diff_y_minor)

            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])

            mass_x = int(Minor["m10"] / Minor["m00"])
            mass_y = int(Minor["m01"] / Minor["m00"])

            # center of mass for contours
            cv.circle(labels_img, (cX, cY), 5, (255, 0, 0), -1)
            # center of mass for convex hull
            cv.circle(labels_img, (mass_x, mass_y), 5, (50, 125, 200), -1)
            cv.circle(labels_img, (cX, cY), 5, (255, 0, 0), -1)
            cv.rectangle(labels_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            kpCnt = len(contours[0])
            x_list = list(point[0][0] for point in c)
            y_list = list(point[0][1] for point in c)

            avg_c_x = int(np.ceil(sum(x_list) / len(x_list)))
            avg_c_y = int(np.ceil(sum(y_list) / len(y_list)))

            center_coord = (int(mass_x), int(mass_y))
            ax_len = (euq_major[0]/2, euq_minor[0]/2)
            start_ang = angle

            # cv.ellipse(labels_img, center_coord, ax_len, start_ang, 0, 360, (255, 0, 0), 5)
            cv.circle(labels_img, (cX, cY), int(ax_len[0]), (0, 0, 255))



            cv.circle(labels_img, (avg_c_x, avg_c_y), 1, (255, 0, 255), 3)
            cv.line(labels_img, (cX, cY), (avg_c_x, avg_c_y), (255, 0, 255))
            cf.point_to_point_angle((cX, cY), (avg_c_x, avg_c_y))

    return labels_img

def delete_if_inside(radius, origin, pixel):
    diff_x = pixel[0] - origin[0]
    diff_y = pixel[1] - origin[1]
    distance_from_origin = cv.sqrt(diff_x**2 + diff_y**2)[0]
    if distance_from_origin <= radius:
        return True
    return False
