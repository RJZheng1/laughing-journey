from display import *
from matrix import *
import math

MAX_STEPS = 100

def add_polygon( points, x0, y0, z0, x1, y1, z1, x2, y2, z2 ):
    add_point(points, x0, y0, z0)
    add_point(points, x1, y1, z1)
    add_point(points, x2, y2, z2)

def draw_polygons( points, screen, color ):
    x = 0
    while x < len(points):
        if cull(points[x], points[x+1], points[x+2], [0, 0, -1]):
            draw_line(screen, points[x][0], points[x][1], points[x+1][0], points[x+1][1], color)
            draw_line(screen, points[x+1][0], points[x+1][1], points[x+2][0], points[x+2][1], color)
            draw_line(screen, points[x][0], points[x][1], points[x+2][0], points[x+2][1], color)
        x += 3

def cull(p0, p1, p2, v):
    a = [p1[0]-p0[0], p1[1]-p0[1], p1[2]-p0[2]]
    b = [p2[0]-p0[0], p2[1]-p0[1], p2[2]-p0[2]]
    
    n = [a[1]*b[2] - a[2]*b[1],
         a[2]*b[0] - a[0]*b[2],
         a[0]*b[1] - a[1]*b[0]]
    return n[0] * v[0] + n[1] * v[1] + n[2] * v[2] < 0

def add_box( points, x, y, z, width, height, depth ):
    x1 = x + width
    y1 = y - height
    z1 = z - depth
# front 012,230
    add_polygon(points, x, y, z, x, y1, z, x1, y1, z)
    add_polygon(points, x1, y1, z, x1, y, z, x, y, z)
# top 403,374
    add_polygon(points, x, y, z1, x, y, z, x1, y, z)
    add_polygon(points, x1, y, z, x1, y, z1, x, y, z1)
# bottom 621,156
    add_polygon(points, x1, y1, z1, x1, y1, z, x, y1, z)
    add_polygon(points, x, y1, z, x, y1, z1, x1, y1, z1)
# back 765,547
    add_polygon(points, x1, y, z1, x1, y1, z1, x, y1, z1)
    add_polygon(points, x, y1, z1, x, y, z1, x1, y, z1)
# left 451,104
    add_polygon(points, x, y, z1, x, y1, z1, x, y1, z)
    add_polygon(points, x, y1, z, x, y, z, x, y, z1)
# right 326,673
    add_polygon(points, x1, y, z, x1, y1, z, x1, y1, z1)
    add_polygon(points, x1, y1, z1, x1, y, z1, x1, y, z)

def add_sphere( points, cx, cy, cz, r, step ):
    
    temp = []

    generate_sphere( temp, cx, cy, cz, r, float(step) )

    i = 0
    
    while i < len(temp):
        add_polygon(points, temp[i][0], temp[i][1], temp[i][2], temp[i+1][0], temp[i+1][1], temp[i+1][2], temp[i+2][0], temp[i+2][1], temp[i+2][2])
        i += 3

def generate_sphere( points, cx, cy, cz, r, step ):

    rotation = 0
    rot_stop = MAX_STEPS
    circle = 0
    circ_stop = MAX_STEPS/2
    
    x = lambda circ, rot: r * math.cos( 2 * math.pi * circ ) + cx
    y = lambda circ, rot: r * math.sin( 2 * math.pi * circ ) * math.cos( 2 * math.pi * rot ) + cy
    z = lambda circ, rot: r * math.sin( 2 * math.pi * circ ) * math.sin( 2 * math.pi * rot ) + cz

    while rotation < rot_stop:
        circle = 0
        rot = float(rotation) / MAX_STEPS
        while circle < circ_stop:
            
            circ = float(circle) / MAX_STEPS
            
            point_i = [(x(circ, rot)), (y(circ, rot)), (z(circ, rot))]
            point_i1 = [(x(circ+step/MAX_STEPS, rot)), (y(circ+step/MAX_STEPS, rot)), (z(circ+step/MAX_STEPS, rot))]
            point_in = [(x(circ, rot+step/MAX_STEPS)), (y(circ, rot+step/MAX_STEPS)), (z(circ, rot+step/MAX_STEPS))]
            point_in1 = [(x(circ+step/MAX_STEPS, rot+step/MAX_STEPS)), (y(circ+step/MAX_STEPS, rot+step/MAX_STEPS)), (z(circ+step/MAX_STEPS, rot+step/MAX_STEPS))]

            add_polygon(points, point_i[0], point_i[1], point_i[2], point_i1[0], point_i1[1], point_i1[2], point_in1[0], point_in1[1], point_in1[2])
            add_polygon(points, point_in1[0], point_in1[1], point_in1[2], point_in[0], point_in[1], point_in[2], point_i[0], point_i[1], point_i[2])
            circle+= step

        rotation+= step

def add_torus( points, cx, cy, cz, r0, r1, step ):
    
    temp = []

    generate_torus( temp, cx, cy, cz, r0, r1, float(step) )

    i = 0
    
    while i < len(temp):
        add_polygon(points, temp[i][0], temp[i][1], temp[i][2], temp[i+1][0], temp[i+1][1], temp[i+1][2], temp[i+2][0], temp[i+2][1], temp[i+2][2])
        i += 3

def generate_torus( points, cx, cy, cz, r0, r1, step ):

    rotation = 0
    rot_stop = MAX_STEPS
    circle = 0
    circ_stop = MAX_STEPS
    
    x = lambda circ, rot: math.cos( 2 * math.pi * rot ) * (r0 * math.cos( 2 * math.pi * circ) + r1 ) + cx
    y = lambda circ, rot: r0 * math.sin(2 * math.pi * circ) + cy
    z = lambda circ, rot: math.sin( 2 * math.pi * rot ) * (r0 * math.cos(2 * math.pi * circ) + r1) + cz

    while rotation < rot_stop:
        circle = 0
        rot = float(rotation) / MAX_STEPS
        while circle < circ_stop:
            
            circ = float(circle) / MAX_STEPS

# Original point
            point_i = [(x(circ, rot)), (y(circ, rot)), (z(circ, rot))]
# Next point down on same circle 
            point_i1 = [(x(circ+step/MAX_STEPS, rot)), (y(circ+step/MAX_STEPS, rot)), (z(circ+step/MAX_STEPS, rot))]
# Original point rotated
            point_in = [(x(circ, rot+step/MAX_STEPS)), (y(circ, rot+step/MAX_STEPS)), (z(circ, rot+step/MAX_STEPS))]
# Next point rotated
            point_in1 = [(x(circ+step/MAX_STEPS, rot+step/MAX_STEPS)), (y(circ+step/MAX_STEPS, rot+step/MAX_STEPS)), (z(circ+step/MAX_STEPS, rot+step/MAX_STEPS))]

            add_polygon(points, point_in[0], point_in[1], point_in[2], point_in1[0], point_in1[1], point_in1[2], point_i1[0], point_i1[1], point_i1[2])
            add_polygon(points, point_i1[0], point_i1[1], point_i1[2], point_i[0], point_i[1], point_i[2], point_in[0], point_in[1], point_in[2])

            circle+= step

        rotation+= step

def add_circle( points, cx, cy, cz, r, step ):
    x0 = r + cx
    y0 = cy

    t = step
    while t<= 1:
        
        x = r * math.cos( 2 * math.pi * t ) + cx
        y = r * math.sin( 2 * math.pi * t ) + cy

        add_edge( points, x0, y0, cz, x, y, cz )
        x0 = x
        y0 = y
        t+= step
        add_edge( points, x0, y0, cz, cx + r, cy, cz )

def add_curve( points, x0, y0, x1, y1, x2, y2, x3, y3, step, curve_type ):
    xcoefs = generate_curve_coefs( x0, x1, x2, x3, curve_type )
    ycoefs = generate_curve_coefs( y0, y1, y2, y3, curve_type )
    
    t =  step
    while t <= 1:
        
        x = xcoefs[0][0] * t * t * t + xcoefs[0][1] * t * t + xcoefs[0][2] * t + xcoefs[0][3]
        y = ycoefs[0][0] * t * t * t + ycoefs[0][1] * t * t + ycoefs[0][2] * t + ycoefs[0][3]

        add_edge( points, x0, y0, 0, x, y, 0 )
        x0 = x
        y0 = y
        t+= step

def draw_lines( matrix, screen, color ):
    if len( matrix ) < 2:
        print "Need at least 2 points to draw a line"
        
    p = 0
    while p < len( matrix ) - 1:
        draw_line( screen, matrix[p][0], matrix[p][1],
                   matrix[p+1][0], matrix[p+1][1], color )
        p+= 2

def add_edge( matrix, x0, y0, z0, x1, y1, z1 ):
    add_point( matrix, x0, y0, z0 )
    add_point( matrix, x1, y1, z1 )

def add_point( matrix, x, y, z=0 ):
    matrix.append( [x, y, z, 1] )


def draw_line( screen, x0, y0, x1, y1, color ):
    dx = x1 - x0
    dy = y1 - y0
    if dx + dy < 0:
        dx = 0 - dx
        dy = 0 - dy
        tmp = x0
        x0 = x1
        x1 = tmp
        tmp = y0
        y0 = y1
        y1 = tmp
        
    if dx == 0:
        y = y0
        while y <= y1:
            plot(screen, color,  x0, y)
            y = y + 1
    elif dy == 0:
        x = x0
        while x <= x1:
            plot(screen, color, x, y0)
            x = x + 1
    elif dy < 0:
        d = 0
        x = x0
        y = y0
        while x <= x1:
            plot(screen, color, x, y)
            if d > 0:
                y = y - 1
                d = d - dx
            x = x + 1
            d = d - dy
    elif dx < 0:
        d = 0
        x = x0
        y = y0
        while y <= y1:
            plot(screen, color, x, y)
            if d > 0:
                x = x - 1
                d = d - dy
            y = y + 1
            d = d - dx
    elif dx > dy:
        d = 0
        x = x0
        y = y0
        while x <= x1:
            plot(screen, color, x, y)
            if d > 0:
                y = y + 1
                d = d - dx
            x = x + 1
            d = d + dy
    else:
        d = 0
        x = x0
        y = y0
        while y <= y1:
            plot(screen, color, x, y)
            if d > 0:
                x = x + 1
                d = d - dy
            y = y + 1
            d = d + dx

