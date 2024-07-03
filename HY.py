import math
def polygon_area(points):
    n = len(points)
    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        area += points[i][0] * points[j][1]
        area -= points[j][0] * points[i][1]
    area = abs(area) / 2.0
    return area
def polygon_perimeter(points):
    n = len(points)
    perimeter = 0.0
    for i in range(n):
        j = (i + 1) % n
        dist = ((points[j][0] - points[i][0]) ** 2 + (points[j][1] - points[i][1]) ** 2) ** 0.5
        perimeter += dist
    return perimeter
def width():
    S =area1-area2
    R=perimeter1/(2*math.pi)
    r=perimeter2/(2*math.pi)
    d=S/((R+r)*math.pi)
    return d

# points1=[(171,65),(142,116),(223,170),(277,161),(381,109),(293,61),(252,41)]
# points2=[(190,87),(179,195),(273,204),(327,147),(308,78),(237,70),(200,132)]
if __name__ == '__main__':
    points1 = [(0,0),(0,6),(6,6),(6,0)]
    points2 = [(2,2),(2,4),(4,4),(4,2)]

    area1= polygon_area(points1)
    perimeter1= polygon_perimeter(points1)
    area2 =polygon_area(points2)
    perimeter2= polygon_perimeter(points2)
    d=width()
    print('血管壁平均厚度为{:.2f}'.format(d))



