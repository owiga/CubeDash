def ch_angle(angle):
    if angle <= 0:
        if -70 >= angle >= -90:
            if angle <= -180:
                if angle <= -270:
                    if angle <= -360:
                        return -360
                    return -270
                return -180
            return -90
        return 0

print(ch_angle(-70))