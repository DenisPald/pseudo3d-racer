import random

def remake_map(total_segments, step):
    res = []
    n_of_steps = total_segments // step

    dx = [0, ]
    dy = [0, ]
    for i in range(1, n_of_steps - 1):
        cur_dy = random.randint(0, 4)
        cur_dx = random.randint(-50, 50)

        if sum(dy) < 0:
            dy.append(cur_dy)
        else:
            dy.append(-cur_dy)

        if sum(dx) < 150:
            dx.append(cur_dx)
        else:
            dx.append(-cur_dx)

    dx.append(-sum(dx))
    dy.append(-sum(dy))

    for i in range(n_of_steps):
        for j in range(step):
            res.append((dx[i], dy[i]))

    return res
