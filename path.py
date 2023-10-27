import pygame
import math
import numpy as np
import time

screen_width = 1000
screen_height = 700

# Set up the drawing window

# Run until the user asks to quit
Gray = (204, 204, 204)
running = True
success = False
success_time = 0
score = 0
op = -1
selected = -1
selected_loc = (0, 0)
edges = set()
link = -1

p1 = pygame.image.load("p10.png")
# p1 = pygame.transform.scale(p1, (25, 25))
p2 = pygame.image.load("p20.png")
# p2 = pygame.transform.scale(p2, (25, 25))
p3 = pygame.image.load("p30.png")
# p3 = pygame.transform.scale(p3, (25, 25))
p = ['null', p1, p2, p3]

state = np.array([[3, 3, 1, 2, 3, 1, 1, 1, 3, 2, 2, 3, 3, 1, 3, 2], [3, 1, 1, 1, 2, 3, 3, 3, 2, 2, 2, 3, 2, 2, 2, 3], 
                 [3, 1, 3, 3, 3, 1, 1, 1, 2, 3, 3, 3, 2, 2, 3, 3], [1, 3, 2, 2, 3, 3, 3, 3, 3, 2, 3, 3, 1, 3, 2, 2], 
                 [1, 1, 1, 1, 3, 1, 3, 1, 2, 1, 3, 1, 3, 1, 1, 1], [3, 2, 2, 2, 1, 3, 2, 2, 1, 1, 3, 3, 3, 1, 1, 1],
                 [1, 1, 3, 2, 1, 1, 3, 2, 1, 1, 3, 2, 3, 1, 1, 3], [1, 3, 1, 3, 1, 2, 3, 3, 1, 3, 2, 1, 1, 3, 2, 1],
                 [3, 3, 1, 1, 2, 2, 3, 3, 3, 3, 2, 2, 1, 1, 2, 2], [3, 1, 1, 1, 2, 1, 3, 3, 3, 3, 1, 1, 3, 3, 1, 1],
                 [2, 3, 1, 1, 2, 3, 3, 3, 2, 2, 2, 3, 2, 2, 3, 1], [3, 2, 2, 1, 3, 2, 3, 3, 1, 3, 1, 2, 1, 1, 3, 2],
                 [3, 3, 1, 1, 1, 3, 3, 1, 1, 1, 3, 3, 1, 1, 3, 2], [1, 3, 2, 2, 1, 3, 2, 2, 3, 2, 2, 2, 3, 3, 3, 3],
                 [2, 3, 1, 1, 2, 3, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1], [1, 3, 2, 2, 3, 2, 2, 2, 3, 3, 3, 2, 1, 1, 1, 3], 
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])

for _ in range(100):
    i = np.random.randint(16)
    j = np.random.randint(16)
    state[16] = state[i]
    state[i] = state[j]
    state[j] = state[16]

def inside(x, y, r1, r2, r3, r4):
    if x < r1 or x > r1 + r3:
        return False
    if y < r2 or y > r2 + r4:
        return False
    return True

def update_edges(x, y):
    global edges
    new_edges = set()
    for e in edges:
        u, v = e
        u1, u2 = u // 16, u % 16
        u1, u2 = u1 // 4, u2 // 4
        u = u1 * 4 + u2
        v1, v2 = v // 16, v % 16
        v1, v2 = v1 // 4, v2 // 4
        v = v1 * 4 + v2
        if u == x and v == x:
            new_edges.add((e[0] + (y // 4 - x // 4) * 64 + (y % 4 - x % 4) * 4, e[1] + (y // 4 - x // 4) * 64 + (y % 4 - x % 4) * 4))
        elif u == x:
            pass
        elif v == x:
            pass
        elif u == y and v == y:
            new_edges.add((e[0] + (x // 4 - y // 4) * 64 + (x % 4 - y % 4) * 4, e[1] + (x // 4 - y // 4) * 64 + (x % 4 - y % 4) * 4))
        elif u == y:
            pass
        elif v == y:
            pass
        else:
            new_edges.add(e)
    edges = new_edges

def place(start_x, start_y):
    if start_x > 300 - 40 and start_x < 600 + 40 and start_y > 150 - 40 and start_y < 450 + 40:
        x, y = round((start_x - 300) / 100), round((start_y - 150) / 100)
        loc = 4 * y + x
        state[16] = state[loc]
        state[loc] = state[selected]
        state[selected] = state[16]
        update_edges(loc, selected)
        return True
    return False

def success_check():
    global success_time, edges, score
    cnt = np.zeros(256)
    dot = np.ones(256)
    for e in edges:
        x, y = e
        cnt[x] += 1
        dot[x] *= y
        cnt[y] += 1
        dot[y] *= x
    score = 1
    valid = 0
    for i in range(256):
        if cnt[i] > 2:
            return False
        if cnt[i] == 2:
            score += 1
            if state[(i // 64) * 4 + (i % 16) // 4][((i // 16) % 4) * 4 + (i % 4)] == 1:
                if round(dot[i] - i**2) != -1:
                    return False
            if state[(i // 64) * 4 + (i % 16) // 4][((i // 16) % 4) * 4 + (i % 4)] == 2:
                if round(dot[i] - i**2) != -256:
                    return False
            if state[(i // 64) * 4 + (i % 16) // 4][((i // 16) % 4) * 4 + (i % 4)] == 3:
                if round(dot[i] - i**2) == -1 or round(dot[i] - i**2) == -256:
                    return False
        if cnt[i] == 1:
            valid += 1
            if state[(i // 64) * 4 + (i % 16) // 4][((i // 16) % 4) * 4 + (i % 4)] == 1:
                if abs(dot[i] - i) != 1:
                    return False
            if state[(i // 64) * 4 + (i % 16) // 4][((i // 16) % 4) * 4 + (i % 4)] == 2:
                if abs(dot[i] - i) != 16:
                    return False
    if valid != 2:
        return False

    success_time = int(time.time() - start_time)
    return True 
    

def draw_board(screen):
    width = 25
    start_x = 300
    start_y = 150
    size = 16

    for i in range(size):
        for j in range(size):
            id = i // 4 * 4 + j // 4
            screen.blit(p[state[id][i % 4 * 4 + j % 4]], (start_x + j * width, start_y + i * width))

    for i in range(4):
        for j in range(4):
            pygame.draw.rect(screen, (0, 255, 0), (start_x + i * 100, start_y + j * 100, 100, 100), 1)

    for edge in edges:
        x, y = edge
        start_pos = (312 + 25 * (x % 16), 162 + 25 * (x // 16))
        end_pos = (312 + 25 * (y % 16), 162 + 25 * (y // 16))
        pygame.draw.line(screen, (255, 0, 0), start_pos, end_pos, 2)

def draw_tools(screen):
    if op == 1:
        text = font.render("move", True, (255, 0, 0)) # 72, 42
    else:
        text = font.render("move", True, (50, 50, 50)) # 72, 42
    screen.blit(text, (800, 400))

    if op == 2:
        text = font.render("link", True, (255, 0, 0)) # 45, 42
    else:
        text = font.render("link", True, (50, 50, 50)) # 45, 42
    screen.blit(text, (800, 460))

    text = font.render("submit", True, (50, 50, 50)) # 88, 42
    screen.blit(text, (800, 520))

    text = font.render("clear", True, (50, 50, 50)) # 65, 42
    screen.blit(text, (800, 580))

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
    text = font.render('You Win, time = ' + str(t // 60) + ':' + sec + ', score = ' + str(score), True, (60, 195, 60))
    screen.blit(text, (screen_width // 2 - text.get_width() // 2, 50 - text.get_height() // 2))

pygame.init()
screen = pygame.display.set_mode([screen_width, screen_height])
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
                if inside(mx, my, 800, 400, 72, 42):
                    op = 1
                if inside(mx, my, 800, 460, 45, 42):
                    op = 2
                if inside(mx, my, 800, 520, 88, 42):
                    if success_check():
                        success = True
                if inside(mx, my, 800, 580, 65, 42):
                    edges.clear()
                        
                if op == 1:
                    for w in range(4):
                        for h in range(4):
                            start_x = 300 + h * 100
                            start_y = 150 + w * 100
                            if inside(mx, my, start_x, start_y, 100, 100):
                                selected = 4 * w + h
                                selected_loc = (mx, my)
                if op == 2:
                    for w in range(16):
                        for h in range(16):
                            start_x = 300 + h * 25
                            start_y = 150 + w * 25
                            if inside(mx, my, start_x, start_y, 25, 25):
                                click = 16 * w + h
                                if link == -1:
                                    link = click
                                else:
                                    if abs(link - click) == 16 or (abs(link - click) == 1 and ((link + click) % 16 != 15 or (link * click) % 16 != 0)):
                                        if (link, click) in edges:
                                            edges.remove((link, click))
                                        elif (click, link) in edges:
                                            edges.remove((click, link))
                                        else:
                                            edges.add((link, click))
                                        link = -1
                                    else:
                                        link = click

        elif event.type == pygame.MOUSEBUTTONUP:
            if success == False:
                if op == 1:
                    if selected != -1:
                        mx, my = pygame.mouse.get_pos()
                        w, h = selected // 4, selected % 4
                        start_x = 300 + h * 100 + mx - selected_loc[0]
                        start_y = 150 + w * 100 + my - selected_loc[1]
                        place(start_x, start_y)
                    selected = -1

    # Fill the background with white
    screen.fill(Gray)

    # Draw a solid blue circle in the center
    draw_board(screen)
    draw_tools(screen)

    current_time = time.time()
    if success == False:
        draw_time(screen, current_time - start_time)
    else:
        draw_success(screen)

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()