dx = 0
ddx = 5
MAP = []
for i in range(100):
    MAP.append((0, dx))
    dx += ddx
    ddx += 0.01
