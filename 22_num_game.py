import pygame
import math
import numpy as np
import time

screen_width = 500

# Set up the drawing window


# Run until the user asks to quit
Green = (204, 204, 204)
Red = (243, 243, 243)
running = True
success = False
success_time = 0

state = np.arange(25)
state[-1] = state[-2] = 0
id1 = np.array([1, 3, 5, 6, 8, 10, 12, 14, 16, 18, 21])
id2 = np.array([2, 4, 7, 9, 11, 13, 15, 17, 19, 20, 22])
state[id1] = np.random.permutation(state[id1])
state[id2] = np.random.permutation(state[id2])
# state = np.array([ 0, 0, 13, 21, 11, 6, 14, 0, 10, 17, 5, 4, 1, 7, 8, 15, 16, 22, 12, 2, 20, 3, 9, 18, 19])

def area(x1, y1, x2, y2, x3, y3):
    return abs((x1 * (y2 - y3) + x2 * (y3 - y1) 
                + x3 * (y1 - y2)) / 2.0)

def isInside(x1, y1, x2, y2, x3, y3, x, y):
    A = area(x1, y1, x2, y2, x3, y3)
    A1 = area(x, y, x2, y2, x3, y3)
    A2 = area(x1, y1, x, y, x3, y3)
    A3 = area(x1, y1, x2, y2, x, y)
    if(abs(A - A1 - A2 - A3) < 0.001):
        return True
    else:
        return False

def point_to_loc(n):
    s = math.sqrt(3)
    points = np.array([[-2, -2*s], [0, -2*s], [2, -2*s], [-3, -s], [-1, -s], [1, -s], [3, -s], [-4, 0], [-2, 0], [0, 0], 
              [2, 0], [4, 0], [-3, s], [-1, s], [1, s], [3, s], [-2, 2*s], [0, 2*s], [2, 2*s]])
    return points[n-1] * 40 + screen_width // 2

def get_loc(n):
    tri = np.array([[1, 4, 5], [1, 5, 2], [2, 5, 6], [2, 3, 6], [3, 6, 7],
           [4, 8, 9], [4, 5, 9], [5, 9, 10], [5, 6, 10], [6, 10, 11], [6, 7, 11], [7, 11, 12],
           [8, 9, 13], [9, 13, 14], [9, 10, 14], [10, 14, 15], [10, 11, 15], [11, 15, 16], [11, 12, 16],
           [13, 14, 17], [14, 17, 18], [14, 15, 18], [15, 18, 19], [15, 16, 19]])
    a, b, c = tri[n-1]
    return np.array([point_to_loc(a), point_to_loc(b), point_to_loc(c)])

def dis(i, j):
    pi, pj = get_loc(i), get_loc(j)
    ci, cj = (pi[0]+pi[1]+pi[2])/3, (pj[0]+pj[1]+pj[2])/3
    d = np.linalg.norm(ci - cj)
    return d

def move(n, init = False):
    global success, success_time
    if n == 0:
        n = 24
    for i in range(1, 25):
        for j in range(1, 25):
            if abs(dis(j, n) - 46.188) < 0.01 and state[j] == 0 and abs(dis(i, j) - 46.188) < 0.01 and state[i] == 0 and i != n:
                tmp = state[n]
                state[n] = state[i]
                state[i] = tmp
                break

    if init == False:
        success_state = np.arange(25)
        success_state[-1] = success_state[-2] = 0
        if (state == success_state).all():
            success = True
            success_time = int(time.time() - start_time)

def draw(screen, p, id):
    p1, p2, p3 = p
    pygame.draw.polygon(screen, Red, p)
    c = (p1 + p2 + p3) / 3
    p1, p2, p3 = c + (p1 - c) * 0.9, c + (p2 - c) * 0.9, c + (p3 - c) * 0.9
    pygame.draw.polygon(screen, Green, [p1, p2, p3])
    if state[id] > 0:
        text = font.render(str(state[id]), True, (50, 50, 50))
        screen.blit(text, (c[0] - text.get_width() // 2, c[1] - text.get_height() // 2))

def draw_time(screen, t):
    t = int(t)
    sec = str(t % 60)
    if len(sec) == 1:
        sec = '0' + sec
    text = font.render(str(t // 60) + ':' + sec, True, (50, 50, 50))
    screen.blit(text, (screen_width // 2 - text.get_width() // 2, 50 - text.get_height() // 2))

def draw_success(screen):
    t = success_time
    sec = str(t % 60)
    if len(sec) == 1:
        sec = '0' + sec
    text = font.render('You Win, time = ' + str(t // 60) + ':' + sec, True, (60, 195, 60))
    screen.blit(text, (screen_width // 2 - text.get_width() // 2, 50 - text.get_height() // 2))

# for i in range(30):
#     print(i)
#     _ = np.random.randint(24)
#     move(_, init = True)
# print(state)

pygame.init()
screen = pygame.display.set_mode([screen_width, screen_width])
font = pygame.font.SysFont("Arial", 36)

start_time = time.time()

while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
 
        elif event.type == pygame.MOUSEBUTTONDOWN:  # 鼠标按下
            if success == False:
                mx, my = pygame.mouse.get_pos()
                for i in range(24):
                    p1, p2, p3 = get_loc(i)
                    if isInside(p1[0], p1[1], p2[0], p2[1], p3[0], p3[1], mx, my):
                        move(i)
                        break


    # Fill the background with white
    screen.fill(Green)

    # Draw a solid blue circle in the center
    for i in range(1, 25):
        draw(screen, get_loc(i), i)
    current_time = time.time()
    if success == False:
        draw_time(screen, current_time - start_time)
    else:
        draw_success(screen)

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()