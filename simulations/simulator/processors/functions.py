import numpy as np

LOOK_AROUND = [(x, y) for x in range(-5, 6) for y in range(-5, 6)]
LOOK_AROUND = sorted(LOOK_AROUND, key=lambda x: max(x))
LOOK_AROUND.remove((0, 0))


def clamp(value, lower, upper) -> int:
    return lower if value < lower else value if value < upper else upper


def crop_area(area, field_size):
    return [x for x in area if 0 <= x[0] < field_size and 0 <= x[1] < field_size]


def get_circle(vector):
    return max(abs(int(vector[0])), abs(int(vector[1])))


def lerp(v1, v2, time):
    return v1 * (1 - time) + v2 * time


def vector_sum(first, second):
    return first[0] + second[0], first[1] + second[1]


def vector_diff(first, second):
    return first[0] - second[0], first[1] - second[1]


def get_vision_field(location, look_around):
    return [vector_sum(x, location) for x in look_around]


def get_vector(goal, circle):
    if circle == 0:
        return 0, 0
    time = 0.2
    while True:
        result = lerp(np.array((0, 0)), np.array(goal), time)
        if get_circle(result) == circle:
            return int(result[0]), int(result[1])
        time += 0.2


def clamp_2d(goal, speed):
    if get_circle(goal) - speed <= 0:
        return goal
    return get_vector(goal, speed)
