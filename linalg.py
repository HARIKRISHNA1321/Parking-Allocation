import math

# relative vector: S-V=(x_s-x_v,y_s-y_v)
def subtract(s,v):
    return (s[0]-v[0],s[1]-v[1])

# L1 norm (Manhattan distance): ||d||_1=|d_x|+|d_y|
def l1_norm(d):
    return abs(d[0])+abs(d[1])

# L2 norm (Euclidean distance): ||d||_2=sqrt(d_x^2+d_y^2)
def l2_norm(d):
    return math.sqrt(d[0]**2+d[1]**2)

# argmin: index of the smallest value (first one wins an exact tie)
def argmin(values):
    best=0
    for i in range(1,len(values)):
        if values[i]<values[best]:
            best=i
    return best
