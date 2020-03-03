import numpy as np
from shapely.geometry import Polygon


def pickTopLeft(poly):
    idx = np.argsort(poly[:, 0])
    if poly[idx[0], 1] < poly[idx[1], 1]:
        s = idx[0]
    else:
        s = idx[1]

    return poly[(s, (s + 1) % 4, (s + 2) % 4, (s + 3) % 4), :]

#过滤掉无意义及宽度过小文本框；图片中对应文本框坐标，按照相同比例缩放，并确定四个点顺序为：以左上为原点，顺时针排列；
def orderConvex(p):
    points = Polygon(p).convex_hull
    points = np.array(points.exterior.coords)[:4] #去所有维度的前四个数字
    points = points[::-1] #切片 -号表示倒序，数字1表示步长，也可以改为其他步长
    points = pickTopLeft(points)
    points = np.array(points).reshape([4, 2])
    return points

#根据文本框坐标点，回归文本框上下两条直线，然后将文本框，以步长为16切分为小框；并按照小框的最大最小横纵坐标，返回每个小框的左上、右下坐标
def shrink_poly(poly, r=16):
    # y = kx + b
    x_min = int(np.min(poly[:, 0]))
    x_max = int(np.max(poly[:, 0]))

    k1 = (poly[1][1] - poly[0][1]) / (poly[1][0] - poly[0][0])
    b1 = poly[0][1] - k1 * poly[0][0]

    k2 = (poly[2][1] - poly[3][1]) / (poly[2][0] - poly[3][0])
    b2 = poly[3][1] - k2 * poly[3][0]

    res = []

    start = int((x_min // 16 + 1) * 16)
    end = int((x_max // 16) * 16)

    p = x_min
    res.append([p, int(k1 * p + b1),
                start - 1, int(k1 * (p + 15) + b1),
                start - 1, int(k2 * (p + 15) + b2),
                p, int(k2 * p + b2)])

    for p in range(start, end + 1, r):
        res.append([p, int(k1 * p + b1),
                    (p + 15), int(k1 * (p + 15) + b1),
                    (p + 15), int(k2 * (p + 15) + b2),
                    p, int(k2 * p + b2)])
    return np.array(res, dtype=np.int).reshape([-1, 8])

if __name__ == '__main__':
    poly = np.array([0,1,1,1,1,0,0,0]).reshape(4,2)
    print(poly)
    poly = orderConvex(poly)
    print(poly)
