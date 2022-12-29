import math

c1 = 1.70158
c2 = c1 * 1.525
c3 = c1 + 1
c4 = (2*math.pi)/3
c5 = (2*math.pi)/4.5
n1 = 7.5625
d1 = 2.75

def linear(x):
    return x
def ease_out(x):
    return x
def ease_in(x):
    return x
def quad_in(x):
    return x*x #dumbs
def quad_out(x):
    return 1 - (1-x) * (1-x)
def quad_in_out(x):
    return 1 - (1-x) * (1-x)
def cubic_in(x):
    return x * x * x
def cubic_out(x):
    return 1 - math.pow(1 - x, 3)
def cubic_in_out(x):
    return (4 * x * x * x) if  (x < 0.5) else (1 - math.pow(-2 * x + 2, 3) / 2)
def quart_in(x):
    return x * x * x * x
def quart_out(x):
    return 1 - math.pow(1 - x, 4)
def quart_in_out(x):
    return (8 * x * x * x * x ) if x < 0.5 else ( 1 - math.pow(-2 * x + 2, 4) / 2)
def quint_in(x):
    return x * x * x * x * x
def quint_out(x):
    return 1 - math.pow(1 - x, 5)
def quint_in_out(x):
    return 16 * x * x * x * x * x if (x<0.5) else (1 - math.pow(-2 * x + 2, 5) / 2)
def sine_in(x):
    return 1 - math.cos((x * math.pi) / 2)
def sine_out(x):
    return math.sin((x * math.pi) / 2)
def sine_in_out(x):
    return -(math.cos(math.pi * x) - 1) / 2
def expo_in(x):
    return 0 if (x==0) else math.pow(2, 10*x-10)
def expo_out(x):
    return 1 if x == 1 else 1-math.pow(2,-10*x)
def expo_in_out(x):
    return 0 if x==0 \
        else (1 if x==1 \
        else (math.pow(2,20*x-10)/2 if x < 0.5\
        else(2-math.pow(2,-20*x+10))/2))
def circ_in(x):
    return 1 - math.sqrt(1 - math.pow(x, 2))
def circ_out(x):
    return math.sqrt(1 - math.pow(x - 1, 2))
def circ_in_out(x):
    if x<0.5:
        return (1 - math.sqrt(1 - math.pow(2 * x, 2))) / 2
    else:
        return (math.sqrt(1 - math.pow(-2 * x + 2, 2)) + 1) / 2
def elastic_in(x):
    if x == 0:
        return 0
    else:
        if x == 1:
            return 1
        else:
            return -math.pow(2, 10 * x - 10) * math.sin((x * 10 - 10.75) * c4)
def elastic_out(x):
    if x == 0:
        return 0
    else:
        if x == 1:
            return 1
        else:
            return math.pow(2, -10 * x) * math.sin((x * 10 - 0.75) * c4) + 1
def elastic_half_out(x):
    return x# ?
def elastic_quarter_out(x):
    return x# ?
def elastic_in_out(x):
    if (x==0):
        return 0
    elif x == 1:
        return 1
    elif x < 0.5:
        return -(math.pow(2, 20 * x - 10) * math.sin((20 * x - 11.125) * c5)) / 2
    else:
        return (math.pow(2, -20 * x + 10) * math.sin((20 * x - 11.125) * c5)) / 2 + 1
def back_in(x):
    return c3 * x * x * x - c1 * x * x
def back_out(x):
    return 1 + c3 * math.pow(x - 1, 3) + c1 * math.pow(x - 1, 2)
def back_in_out(x):
    if x < 0.5:
        return (math.pow(2 * x, 2) * ((c2 + 1) * 2 * x - c2)) / 2
    else:
        return (math.pow(2 * x - 2, 2) * ((c2 + 1) * (x * 2 - 2) + c2) + 2) / 2
def bounce_in(x):
    return 1 - bounce_in(1 - x)
def bounce_out(x):
    if (x < 1 / d1):
        return n1 * x * x
    elif (x < 2 / d1):
        x -= 1.5
        return n1 * (x / d1) * x + 0.75
    elif (x < 2.5 / d1):
        x -= 2.25
        return n1 * (x / d1) * x + 0.9375
    else:
        x -= 2.625
        return n1 * (x / d1) * x + 0.984375
def bounce_in_out(x):
    if x < 0.5:
        (1 - bounce_out(1 - 2 * x)) / 2
    else:
        return (1 + bounce_out(2 * x - 1)) / 2
    

easings = [
    linear,             # 0
    ease_out,           # 1
    ease_in,            # 2
    quad_in,            # 3
    quad_out,           # 4
    quad_in_out,        # 5
    cubic_in,           # 6
    cubic_out,          # 7
    cubic_in_out,       # 8
    quart_in,           # 9
    quart_out,          # 10
    quart_in_out,       # 11
    quint_in,           # 12
    quint_out,          # 13
    quint_in_out,       # 14
    sine_in,            # 15
    sine_out,           # 16
    sine_in_out,        # 17
    expo_in,            # 18
    expo_out,           # 19
    expo_in_out,        # 20
    circ_in,            # 21
    circ_out,           # 22
    circ_in_out,        # 23
    elastic_in,         # 24
    elastic_out,        # 25
    elastic_half_out,   # 26
    elastic_quarter_out,# 27
    elastic_in_out,     # 28
    back_in,            # 29
    back_out,           # 30
    back_in_out,        # 31
    bounce_in,          # 32
    bounce_out,         # 33
    bounce_in_out       # 34

]