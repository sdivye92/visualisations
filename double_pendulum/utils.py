import numpy as np

g = 9.8

def update_energies(b1,b2):
    """
    Calculate the kinetic and potential energies of each pendulum.
    """
    b1_2, b2_2 = update_positions(b1,b2)
    x1,y1,x2,y2 = b1_2.x, b1_2.y, b2_2.x, b2_2.y

    vx1 = -y1*b1.v
    vy1 = x1*b1.v
    vx2 = vx1 + (y1-y2)*b2.v
    vy2 = vy1 + (x2-x1)*b2.v

    b1.ke = .5*b1.m*(vx1**2 + vy1**2)
    b1.pe = b1.m*g*y1
    b1.energy = b1.ke + b1.pe
    b2.ke = .5*b2.m*(vx2**2 + vy2**2)
    b2.pe = b2.m*g*y2
    b2.energy = b2.ke + b2.pe
    return b1,b2

def update_positions(b1,b2):
    """
    Calculate the x,y positions of each pendulum.
    """
    l1 = b1.l
    t1 = b1.theta

    l2 = b2.l
    t2 = b2.theta

    x1 = l1*np.sin(t1)
    y1 = -l1*np.cos(t1)

    x2 = x1 + l2*np.sin(t2)
    y2 = y1 - l2*np.cos(t2)

    b1.x = x1
    b1.y = y1
    b2.x = x2
    b2.y = y2

    return b1,b2

def get_acceleration(b1,b2):
    """
    Calculates the acceleration on each pendulum.
    """
    m1 = b1.m
    l1 = b1.l
    v1 = b1.v
    v12 = v1*v1
    t1 = b1.theta

    m2 = b2.m
    l2 = b2.l
    v2 = b2.v
    v22 = v2*v2
    t2 = b2.theta

    c = np.cos(t1-t2)
    c1 = np.cos(t1)
    c2 = np.cos(t2)
    s = np.sin(t1-t2)
    s1 = np.sin(t1)
    s2 = np.sin(t2)
    ss = s*s

    norm = (m1 +m2*ss)

    a1 = -.5*m2*np.sin(2*(t1-t2))*v12/norm - l2*m2*s*v22/(l1*norm)
    a1 += (-.5*g/l1)*((2*m1+m2)*s1 + m2*np.sin(t1-2*t2))/norm

    a2 = l1*(m1+m2)*v12*s/(l2*norm) + m2*np.sin(2*(t1-t2))*v22/(2*norm)
    a2 += (g/l2)*(m1+m2)*c1*s/norm

    return a1,a2
