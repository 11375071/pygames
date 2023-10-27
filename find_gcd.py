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
score = 0

rank = np.array([0, 50, 19, 24, 12, 15, 16, 13, 9, 8, 3, 7, 6, 5, 5, 4, 4, 4, 4, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2]) * 6
choice = []
for i in range(1, 100):
    if i < 30:
        for _ in range(rank[i]):
            choice.append(i)
    else:
        choice.append(i)

def get_question():
    gcd = np.random.choice(choice)
    while(1):
        i = np.random.randint(1, 200 // gcd + 1)
        j = np.random.randint(1, 200 // gcd + 1)
        if math.gcd(i, j) == 1:
            return [i*gcd, j*gcd]

question = get_question()

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
    return points[n-1] * 40 + screen_width // 2 + np.array([0, 50])

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

def draw(screen, p, id):
    p1, p2, p3 = p
    pygame.draw.polygon(screen, Red, p)
    c = (p1 + p2 + p3) / 3
    p1, p2, p3 = c + (p1 - c) * 0.9, c + (p2 - c) * 0.9, c + (p3 - c) * 0.9
    pygame.draw.polygon(screen, Green, [p1, p2, p3])
    if i == 24:
        text = font.render('>23', True, (50, 50, 50))
    else:
        text = font.render(str(id), True, (50, 50, 50))
    screen.blit(text, (c[0] - text.get_width() // 2, c[1] - text.get_height() // 2))

def draw_time_score(screen, t):
    global success
    t = int(t)
    if t <= 60:
        t = 60 - t
    else:
        t = 0
        success = True
    sec = str(t % 60)
    if len(sec) == 1:
        sec = '0' + sec
    t = str(t // 60) + ':' + sec 
    text = 'Time: ' + t + ', Score: ' + str(score)
    if success == False:
        text = font.render(text, True, (50, 50, 50))
    else:
        text = font.render(text, True, (60, 195, 60))
    screen.blit(text, (screen_width // 2 - text.get_width() // 2, 50 - text.get_height() // 2))

def draw_question(screen, question):
    question_str = 'click on the gcd of ' + str(question[0]) + ' and ' + str(question[1])
    text = font.render(question_str, True, (60, 195, 60))
    screen.blit(text, (screen_width // 2 - text.get_width() // 2, 100 - text.get_height() // 2))

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
                        if (i == math.gcd(question[0], question[1])) or (i == 0 and math.gcd(question[0], question[1]) > 23):
                            score += 1 
                        else:
                            score -= 4
                        question = get_question()
                        break


    # Fill the background with white
    screen.fill(Green)

    # Draw a solid blue circle in the center
    for i in range(1, 25):
        draw(screen, get_loc(i), i)
    current_time = time.time()
    if success == False:
        draw_question(screen, question)
    draw_time_score(screen, current_time - start_time)

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()