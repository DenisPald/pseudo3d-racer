import random

TOTAL_SEGMENTS = 500
MAP = []

STEP = 100
N_OF_STEPS = TOTAL_SEGMENTS // STEP

dx = [0, ]
dy = [0, ]
for i in range(1, N_OF_STEPS - 1):
    cur_dy = random.randint(0, 0)
    cur_dx = random.randint(-0, 0)

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

for i in range(N_OF_STEPS):
    for j in range(STEP):
        MAP.append((dx[i], dy[i]))
