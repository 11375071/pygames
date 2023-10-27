import pygame
import math
import numpy as np
import time

screen_width = 1536
screen_height = 700

# Set up the drawing window

colors = np.array([(0, 0, 0), (255, 0, 0), (255, 165, 0), (255, 255, 0), (0, 255, 0), (0, 255, 255), (0, 0, 255), 
          (128, 0, 128), (255, 255, 255)], dtype=int)

q_size = 20

# Run until the user asks to quit
Gray = (204, 204, 204)
running = True
success = False
success_time = 0

selected = -1
selected_loc = (0, 0)
valid = np.ones(12)

def merge(state, merge_size):
    new_state = np.copy(state)
    size = state.shape[0]
    for i in range(size):
        for j in range(size):
            cnt = np.zeros(9)
            for s in range(merge_size):
                for t in range(merge_size):
                    cnt[state[(i+s)%size][(j+t)%size]] += 1
            new_state[i][j] = cnt.argmax()
    return new_state

state = np.random.randint(9, size=(q_size, q_size))
state = merge(state, 6)

def draw_question(screen):
    start_x = 60
    start_y = 240
    width = 12
    for i in range(q_size):
        for j in range(q_size):
            pygame.draw.rect(screen, colors[state[i][j]], (start_x + i * width, start_y + j * width, width, width))



answered_loc = []
for i in range(12):
    answered_loc.append((0, 0))

def draw_board(screen, draw=True):
    start_x = 360
    start_y = 200
    width = 16
    ans_state = np.ones(shape=(q_size, q_size), dtype=int) * -1
    for id in range(12):
        if valid[id] == 0:
            x, y = answered_loc[id]
            for i in range(q_size // 2):
                for j in range(q_size // 2):
                    if ans_state[i+x][j+y] == -1:
                        ans_state[i+x][j+y] = c_state[id][i][j]
                    else:
                        ans_state[i+x][j+y] = (ans_state[i+x][j+y] + c_state[id][i][j]) % 9

    if draw:
        for i in range(q_size):
            for j in range(q_size):
                if ans_state[i][j] == -1:
                    pygame.draw.rect(screen, Gray, (start_x + i * width, start_y + j * width, width, width))
                else:
                    pygame.draw.rect(screen, colors[ans_state[i][j]], (start_x + i * width, start_y + j * width, width, width))

        for i in range(q_size):
            for j in range(q_size):
                pygame.draw.rect(screen, (50, 50, 50), (start_x + i * width, start_y + j * width, width, width), 1)
    else:
        return ans_state

def generate_question():
    total_state = np.copy(state)
    c_state = []
    for _ in range(8):
        x = np.random.choice(np.arange(11), p=np.array([8, 5, 4, 3, 3, 2, 3, 3, 4, 5, 8])/48)
        y = np.random.choice(np.arange(11), p=np.array([8, 5, 4, 3, 3, 2, 3, 3, 4, 5, 8])/48)
        tmp_state = np.random.randint(9, size=(q_size // 2, q_size // 2))
        tmp_state = merge(tmp_state, 6)
        c_state.append(tmp_state)
        for i in range(q_size // 2):
            for j in range(q_size // 2):
                total_state[i+x][j+y] = (total_state[i+x][j+y] - tmp_state[i][j]) % 9

    c_state.append(total_state[:q_size // 2, :q_size // 2])
    c_state.append(total_state[:q_size // 2, q_size // 2:])
    c_state.append(total_state[q_size // 2:, :q_size // 2])
    c_state.append(total_state[q_size // 2:, q_size // 2:])
    return c_state

c_state = generate_question()

def draw_choice(screen):
    for w in range(4):
        for h in range(3):
            if selected == w * 3 + h:
                mx, my = pygame.mouse.get_pos()
                start_x = 740 + w * 200 + mx - selected_loc[0]
                start_y = 100 + h * 200 + my - selected_loc[1]
            else:
                start_x = 740 + w * 200
                start_y = 100 + h * 200
            width = 16
            for i in range(q_size // 2):
                for j in range(q_size // 2):
                    # if c_state[w * 3 + h][i][j] == 0:
                    #     pygame.draw.rect(screen, Gray, (start_x + i * width, start_y + j * width, width, width))
                    # else:
                    #     pygame.draw.rect(screen, colors[c_state[w * 3 + h][i][j]], (start_x + i * width, start_y + j * width, width, width))
                    if valid[w * 3 + h] == 1:
                        pygame.draw.rect(screen, colors[c_state[w * 3 + h][i][j]], (start_x + i * width, start_y + j * width, width, width))
                    else:
                        pygame.draw.rect(screen, (colors[c_state[w * 3 + h][i][j]] * 0.2 + (165, 165, 165)).astype(int), (start_x + i * width, start_y + j * width, width, width))

def place(id, start_x, start_y):
    if start_x > 360 - 8 and start_x < 520 + 8 and start_y > 200 - 8 and start_y < 360 + 8:
        x, y = round((start_x - 360) / 16), round((start_y - 200) / 16)
        answered_loc[id] = (x, y)
        return True
    return False

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

def success_check():
    global success_time
    for i in range(12):
        if valid[i] == 1:
            return False 

    if (draw_board(0, False) == state).all():
        success_time = int(time.time() - start_time)
        return True 
    
    return False

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
                for w in range(4):
                    for h in range(3):
                        start_x = 740 + w * 200
                        start_y = 100 + h * 200
                        if mx > start_x and mx < start_x + 8 * q_size and my > start_y and my < start_y + 8 * q_size:
                            selected = 3 * w + h
                            valid[selected] = 1
                            selected_loc = (mx, my)

        elif event.type == pygame.MOUSEBUTTONUP:
            if success == False:
                if selected != -1:
                    mx, my = pygame.mouse.get_pos()
                    w, h = selected // 3, selected % 3
                    start_x = 740 + w * 200 + mx - selected_loc[0]
                    start_y = 100 + h * 200 + my - selected_loc[1]
                    if place(selected, start_x, start_y):
                        valid[selected] = 0
                        success = success_check()
                selected = -1


    # Fill the background with white
    screen.fill(Gray)

    # Draw a solid blue circle in the center
    draw_question(screen)
    draw_board(screen)
    draw_choice(screen)

    current_time = time.time()
    if success == False:
        draw_time(screen, current_time - start_time)
    else:
        draw_success(screen)

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()