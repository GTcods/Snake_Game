import numpy as np
import pygame
import random
import sys
from pygame import Vector2
import time
import plotly.io as pio
import plotly.express as px
from Buttons import Button, RectButton, CircleButton

pygame.init()

# pygame.mixer.pre_init(44100, -16, 2, 512)
# pygame.mixer.init()


class Main:
    def __init__(self):
        self.stats = Stats()
        self.game = Game()

    def start_game(self):
        self.stats = Stats()
        self.game = Game(border=main.game.border, speed=main.game.speed)
        menu_loop()

    def back_to_menu(self):
        self.game = Game(border=main.game.border, speed=main.game.speed)
        self.stats = Stats()
        menu_loop()

    def restart_game(self):
        self.game = Game(border=main.game.border, speed=main.game.speed)
        self.stats = Stats()
        game_loop()

    @staticmethod
    def game_over():
        main.stats.final_stats()
        game_over_loop()

    @staticmethod
    def quit_game():
        pygame.quit()
        sys.exit()


class Game:
    def __init__(self, border=False, speed=150):
        self.border = border
        if self.border:
            self.create_border()
        else:
            self.surface = pygame.Surface((block_size * screen_x, block_size * screen_y))

        # self.surface_color = (54, 117, 136)
        self.surface_color = (53, 140, 159)
        self.surface_x, self.surface_y = self.surface.get_size()

        self.frame = pygame.transform.scale(frame, ((screen_x + 0.7) * block_size, (screen_y + 0.7) * block_size))

        # self.grass_color = (52, 142, 148)
        self.grass_color = (53, 130, 148)
        self.score = 0
        self.speed = speed

        self.snake = Snake()
        self.apple = Apple()

    def draw_elements(self):
        self.surface.fill(self.surface_color)
        self.draw_grass()
        self.apple.draw_apple()
        self.snake.draw_snake()
        self.draw_score()
        if self.border:
            self.draw_border()
        else:
            screen.blit(self.surface, (0, 0))

    def create_border(self):
        self.surface = pygame.Surface(((screen_x - 2) * block_size, (screen_y - 2) * block_size))
        self.surface_x, self.surface_y = self.surface.get_size()

    def draw_border(self):
        screen.blit(self.frame, (-block_size / 2.5, -block_size / 2.5))
        screen.blit(self.surface, (block_size, block_size))

    def draw_grass(self):
        for j in range(self.surface_y // block_size):
            for i in range(j % 2, self.surface_x // block_size, 2):
                grass = pygame.Surface((block_size, block_size))
                grass.fill(self.grass_color)
                self.surface.blit(grass, (i * block_size, j * block_size))

    def draw_score(self):
        pygame.font.init()
        font = pygame.font.Font(None, 50)
        score_surface = font.render(str(self.score), True, "black")
        score_rect = score_surface.get_rect()
        score_rect.center = block_size * (screen_x - 3 / 2), block_size * (3 / 2)
        self.surface.blit(score_surface, score_rect)


class Stats:
    def __init__(self):
        self.pause_timer = 0
        self.image = pygame.Surface((screen_x / 2 * block_size, screen_y / 2 * block_size))

    def final_stats(self):
        main.game.apple.durations.append(time.time() - main.game.apple.duration)
        self.create_stats()

    def quick_stats(self):
        main.game.apple.durations.append(main.stats.pause_timer - main.game.apple.duration)

        self.create_stats()

        main.game.apple.durations.remove(main.game.apple.durations[-1])

    def create_stats(self):
        np_data = np.zeros([screen_x, screen_y])
        for x, y, t in zip(main.game.apple.x_coordinates, main.game.apple.y_coordinates, main.game.apple.durations):
            np_data[y][x] = t

        heatmap = px.imshow(np_data, color_continuous_scale='aggrnyl')

        heatmap.update_layout(plot_bgcolor='black', paper_bgcolor='rgb(24,56,72)',
                              xaxis={
                                  'tickfont': {'family': 'Arial', 'size': 20, 'color': 'white'}},
                              yaxis={
                                  'tickfont': {'family': 'Arial', 'size': 20, 'color': 'white'}},
                              coloraxis_colorbar={
                                  'tickfont': {'family': 'Arial', 'size': 20, 'color': 'white'}})

        pio.write_image(heatmap, "Graphics/stats.png")

        self.image = pygame.image.load("Graphics/stats.png")
        cropped_rect = pygame.Rect(140, 30, 560, 420)
        self.image = self.image.subsurface(cropped_rect)
        self.image = pygame.transform.scale(self.image, (screen_x * block_size / 1.5, screen_y * block_size / 2.2))

    def draw_stats(self):
        self.final_stats()
        game_over_loop()


class Snake:
    def __init__(self):
        self.head = Vector2(screen_x // 3, screen_y / 2)
        self.blocks = [self.head, self.head - Vector2(1, 0), self.head - Vector2(2, 0)]
        self.direction = Vector2(1, 0)
        self.length = len(self.blocks)
        # self.color = (209, 90, 135)
        self.color = (232, 115, 107)

    def draw_snake(self):
        head_rect = pygame.Rect(self.head.x * block_size, self.head.y * block_size, block_size, block_size)
        pygame.draw.rect(main.game.surface, self.color, head_rect)
        # head_surf = pygame.Surface((block_size, block_size))
        # head_surf.fill(snake_color)
        # main_surface.blit(head_surf, (self.head.x * block_size, self.head.y * block_size))
        for v in self.blocks[1:-1]:
            body_rect = pygame.Rect(v.x * block_size, v.y * block_size, block_size, block_size)
            pygame.draw.rect(main.game.surface, self.color, body_rect)
            # body_surf = pygame.Surface((block_size, block_size))
            # body_surf.fill(snake_color)
            # main_surface.blit(body_surf, (v.x * block_size, v.y * block_size))

        tail_rect = pygame.Rect(self.blocks[-1].x * block_size, self.blocks[-1].y * block_size, block_size, block_size)
        pygame.draw.rect(main.game.surface, self.color, tail_rect)
        # tail_surf = pygame.Surface((block_size, block_size))
        # tail_surf.fill(snake_color)
        # main_surface.blit(tail_surf, (self.blocks[-1].x * block_size, self.blocks[-1].y * block_size))

    def move_snake(self):
        self.head = Vector2(self.blocks[0].x, self.blocks[0].y) + self.direction

        if not main.game.border:
            if self.head.x < 0 or self.head.x >= screen_x:
                self.head.x = screen_x - abs(self.head.x)
            if self.head.y < 0 or self.head.y >= screen_y:
                self.head.y = screen_y - abs(self.head.y)

        if not self.eaten_apple():
            self.blocks.remove(self.blocks[-1])

        self.check_collision()

        self.blocks.insert(0, self.head)

    def eaten_apple(self):
        if self.head == main.game.apple.block:
            # eating_sfx.play()
            main.game.score += 1
            main.game.apple.randomize()
            return True

    def change_direction(self, direction):
        if direction != -self.direction:
            self.direction = direction
            return True
        else:
            return False

    def check_collision(self):
        if self.head in self.blocks:
            main.stats.draw_stats()
        elif main.game.border:
            if not 0 <= self.head.x < screen_x - 2 or not 0 <= self.head.y < screen_y - 2:
                main.stats.draw_stats()


class Apple:
    def __init__(self):
        # self.x, self.y, self.block = self.randomize()
        self.x = random.randint(0, screen_x - 3)
        self.x = random.randint(1, screen_x - 3)
        self.y = random.randint(1, screen_y - 3)
        self.block = Vector2(self.x, self.y)
        self.color = (201, 0, 0)
        self.leaf_color = (0, 200, 0)
        self.duration = time.time()

        self.x_coordinates = [self.x]
        self.y_coordinates = [self.y]
        self.durations = []

    def randomize(self):
        self.x = random.randint(1, screen_x - 3)
        self.y = random.randint(1, screen_y - 3)
        self.block = Vector2(self.x, self.y)

        while self.block in main.game.snake.blocks:
            self.randomize()

        self.durations.append(time.time() - self.duration)
        self.duration = time.time()

        self.x_coordinates.append(self.x)
        self.y_coordinates.append(self.y)

        # return self.x, self.y, self.block

    def draw_apple(self):
        apple_x = self.x * block_size + block_size / 2
        apple_y = self.y * block_size + block_size / 1.5
        leaf_x = apple_x
        leaf_y = apple_y - block_size / 1.7
        leaf_size = block_size / 4
        pygame.draw.circle(main.game.surface, self.color, (apple_x, apple_y), block_size / 3)
        pygame.draw.rect(main.game.surface, self.leaf_color, (leaf_x, leaf_y, leaf_size, leaf_size),
                         border_top_left_radius=int(0.2 * block_size), border_bottom_right_radius=int(0.2 * block_size))


block_size = 30
screen_x, screen_y = 20, 20

frame = pygame.image.load('Graphics/square-frame.jpeg')

# eating_sfx = pygame.mixer.Sound('Game/Sounds/eating-sound.wav')

screen = pygame.display.set_mode((block_size * screen_x, block_size * screen_y))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()


def menu_loop():
    menu_surface = pygame.Surface((screen_x * block_size, screen_y * block_size))
    menu_surface_color = (24, 56, 72)

    my_font = pygame.font.SysFont("Impact", 80)
    snake_text_surface = my_font.render('SNAKE!', True, "white")
    snake_text_rect = snake_text_surface.get_rect()
    snake_text_rect.center = (block_size * screen_x / 2, block_size * screen_y / 6)

    if main.game.speed == 150:
        difficulty_color = (53, 222, 139)
        easy_color = (53, 222, 139)
        medium_color = (24, 40, 60)
        hard_color = (24, 40, 60)
    elif main.game.speed == 100:
        difficulty_color = "orange"
        easy_color = (24, 40, 60)
        medium_color = "orange"
        hard_color = (24, 40, 60)
    else:
        difficulty_color = "red"
        easy_color = (24, 40, 60)
        medium_color = (24, 40, 60)
        hard_color = "red"

    if main.game.border:
        border_text = "Border"
        border_color = "orange"
        no_color = (24, 40, 60)
        yes_color = "orange"
    else:
        border_text = "!Border"
        border_color = (53, 222, 139)
        no_color = (53, 222, 139)
        yes_color = (24, 40, 60)

    play_button = RectButton(block_size * (screen_x // 2 - 1.5), block_size * (screen_y / 2 + 2), block_size * 3,
                             block_size,(24, 40, 60), "Play", "Impact", "white",
                             15, 1, "white", "grey")

    border_button = RectButton(block_size * (screen_x / 2 - 6), block_size * screen_y / 2, block_size * 3, block_size,
                               (24, 40, 60), border_text, "Impact", "white",
                               15, 1, "white", border_color)

    without_button = RectButton(screen_x * block_size / 8, block_size * (screen_y / 2 - 2), block_size * 3, block_size,
                                no_color, "Without", "Impact", "white",
                                13, 1, "white", (53, 222, 139))

    with_button = RectButton(screen_x * block_size / 3.7, block_size * (screen_y / 2 - 2), block_size * 3, block_size,
                             yes_color, "With", "Impact", "white",
                             13, 1, "white", "orange")

    difficulty_button = RectButton(block_size * (screen_x / 2 + 3), block_size * screen_y / 2, block_size * 3,
                                   block_size,
                                   (24, 40, 60), "Difficulty", "Impact", "white",
                                   15, 1, "white", difficulty_color)

    easy_button = RectButton(block_size * (screen_x / 2), block_size * (screen_y / 2 - 2), block_size * 3, block_size,
                             easy_color, "Easy", "Impact", "white",
                             13, 1, "white", (53, 222, 139))

    medium_button = RectButton(block_size * (screen_x / 2 + 3), block_size * (screen_y / 2 - 2), block_size * 3,
                               block_size, medium_color, "Medium", "Impact", "white",
                               13, 1, "white", "orange")

    hard_button = RectButton(screen_x * 0.8 * block_size, block_size * (screen_y / 2 - 2), block_size * 3, block_size,
                             hard_color, "Hard", "Impact", "white",
                             13, 1, "white", "red")

    border_pressed = False
    difficulty_pressed = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main.quit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    game_loop()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if difficulty_pressed:
                    if easy_button.check_if_clicked(mouse_pos):
                        main.game.speed = 150
                        difficulty_button.hover_color = (53, 222, 139)
                        easy_button.color = (53, 222, 139)
                        medium_button.color = (24, 40, 60)
                        hard_button.color = (24, 40, 60)
                        difficulty_pressed = False
                    if medium_button.check_if_clicked(mouse_pos):
                        main.game.speed = 100
                        difficulty_button.hover_color = "orange"
                        easy_button.color = (24, 40, 60)
                        medium_button.color = "orange"
                        hard_button.color = (24, 40, 60)
                        difficulty_pressed = False
                    if hard_button.check_if_clicked(mouse_pos):
                        main.game.speed = 80
                        difficulty_button.hover_color = "red"
                        easy_button.color = (24, 40, 60)
                        medium_button.color = (24, 40, 60)
                        hard_button.color = "red"
                        difficulty_pressed = False
                if border_pressed:
                    if without_button.check_if_clicked(mouse_pos):
                        main.game.border = False
                        border_pressed = False
                        border_button.hover_color = (53, 222, 139)
                        border_button.change_text("!Border")
                        without_button.color = (53, 222, 139)
                        with_button.color = (24, 40, 60)
                        main.game.surface = pygame.Surface((screen_x * block_size, screen_y * block_size))
                        main.game.surface_x, main.game.surface_y = main.game.surface.get_size()
                    if with_button.check_if_clicked(mouse_pos):
                        main.game.border = True
                        border_pressed = False
                        border_button.hover_color = "orange"
                        border_button.change_text("Border")
                        with_button.color = "orange"
                        without_button.color = (24, 40, 60)
                        main.game.create_border()
                if border_button.check_if_clicked(mouse_pos):
                    if border_pressed:
                        border_pressed = False
                    else:
                        border_pressed = True
                if difficulty_button.check_if_clicked(mouse_pos):
                    if difficulty_pressed:
                        difficulty_pressed = False
                    else:
                        difficulty_pressed = True
                if play_button.check_if_clicked(mouse_pos):
                    game_loop()

        menu_surface.fill(menu_surface_color)

        Button.draw_buttons(play_button, border_button, difficulty_button, screen=menu_surface)
        if border_pressed:
            Button.draw_buttons(with_button, without_button, screen=menu_surface)
        if difficulty_pressed:
            Button.draw_buttons(easy_button, medium_button, hard_button, screen=menu_surface)

        menu_surface.blit(snake_text_surface, snake_text_rect)
        screen.blit(menu_surface, (0, 0))
        pygame.display.update()
        clock.tick(60)


def game_loop():
    screen_update = pygame.USEREVENT
    pygame.time.set_timer(screen_update, main.game.speed)
    pressed = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main.quit_game()
            if event.type == screen_update:
                main.game.snake.move_snake()
                pressed = False
            if not pressed:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pause_loop()
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        pressed = main.game.snake.change_direction(Vector2(0, -1))
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        pressed = main.game.snake.change_direction(Vector2(0, 1))
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        pressed = main.game.snake.change_direction(Vector2(-1, 0))
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        pressed = main.game.snake.change_direction(Vector2(1, 0))

        main.game.draw_elements()
        # screen.blit(main.game.surface, (0, 0))
        pygame.display.update()
        clock.tick(30)


def pause_loop():
    pause_surface = pygame.Surface((block_size * (screen_x / 4), block_size * screen_y), pygame.SRCALPHA)
    pause_surface.fill((24, 56, 72, 200))

    resume_button = RectButton(block_size, block_size * 2, block_size * 3, block_size,
                               (24, 40, 60), "Resume", "Impact", "white",
                               15, 1, "white", "grey")

    menu_button = RectButton(block_size, block_size * 4, block_size * 3, block_size,
                             (24, 40, 60), "Menu", "Impact", "white",
                             15, 1, "white", "grey")

    stats_button = RectButton(block_size, block_size * 6, block_size * 3, block_size,
                              (24, 40, 60), "Stats", "Impact", "white",
                              15, 1, "white", "grey")

    quit_button = RectButton(block_size, block_size * 8, block_size * 3, block_size,
                             (24, 40, 60), "Quit", "Impact", "white",
                             15, 1, "white", "grey")

    main.stats.pause_timer = time.time()

    while True:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main.quit_game()
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_SPACE):
                    main.game.apple.duration += time.time() - main.stats.pause_timer
                    return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if resume_button.check_if_clicked(mouse_pos):
                    main.game.apple.duration += time.time() - main.stats.pause_timer
                    return None
                if menu_button.check_if_clicked(mouse_pos):
                    main.start_game()
                if stats_button.check_if_clicked(mouse_pos):
                    stats_loop()
                if quit_button.check_if_clicked(mouse_pos):
                    main.quit_game()

        main.game.apple.draw_apple()
        main.game.snake.draw_snake()

        if main.game.border:
            screen.blit(main.game.surface, (block_size, block_size))
            main.game.draw_border()
        else:
            screen.blit(main.game.surface, (0, 0))

        screen.blit(pause_surface, (0, 0))
        Button.draw_buttons(resume_button, menu_button, stats_button, quit_button, screen=screen)
        pygame.display.update()
        clock.tick(30)


def stats_loop():
    stats_surface = pygame.Surface((block_size * screen_x, block_size * screen_y))
    stats_surface_color = (24, 56, 72)
    main.stats.quick_stats()

    my_font = pygame.font.SysFont("Impact", 80)
    text_surface = my_font.render("STATS!", True, "white")
    text_rect = text_surface.get_rect()
    text_rect.center = (block_size * screen_x / 2, block_size * screen_y / 8)

    back_button = RectButton(block_size / 2, block_size / 2, block_size * 3, block_size,
                             (24, 40, 60), "Back", "Impact", "white",
                             15, 1, "white", "grey")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main.quit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                pass
                if back_button.check_if_clicked(mouse_pos):
                    return None

        stats_surface.fill(stats_surface_color)
        stats_surface.blit(main.stats.image, (screen_x * block_size / 5, screen_y * block_size / 4))
        screen.blit(stats_surface, (0, 0))
        screen.blit(text_surface, text_rect)
        back_button.draw_button(screen)
        pygame.display.update()
        clock.tick(30)


def game_over_loop():
    game_over_surface = pygame.Surface((block_size * screen_x, block_size * screen_y))
    game_over_surface_color = (24, 56, 72)

    my_font1 = pygame.font.SysFont("Impact", 80)
    text_surface = my_font1.render("GAME OVER!", True, "White")
    text_rect = text_surface.get_rect(center=(screen_x * block_size // 2, screen_y * block_size // 8))

    menu_button = RectButton(block_size / 2, block_size / 2, block_size * 2, block_size,
                             (24, 40, 60), "Menu", "Impact", "white",
                             15, 1, "white", "grey")

    restart_button = CircleButton(block_size * screen_x / 2, (screen_y - 4) * block_size, block_size * 2, (24, 56, 72),
                                  "Restart", "Impact", "white", 20,
                                  1, "black", (24, 76, 102))
    restart_pressed = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main.quit_game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if menu_button.check_if_clicked(event.pos):
                    main.back_to_menu()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main.back_to_menu()
                if event.key == pygame.K_RETURN:
                    restart_pressed = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN:
                    restart_pressed = False

        mouse_pressed = pygame.mouse.get_pressed()
        if mouse_pressed:
            mouse_pos = pygame.mouse.get_pos()
            if restart_button.check_if_clicked(mouse_pos):
                if mouse_pressed[0]:
                    if restart_button.update_arc(0):
                        main.restart_game()
                if mouse_pressed[2]:
                    restart_button.update_arc(2)

        if restart_pressed:
            if restart_button.update_arc(0):
                main.restart_game()

        game_over_surface.fill(game_over_surface_color)

        game_over_surface.blit(main.stats.image, (screen_x * block_size / 4, screen_y * block_size / 5))
        game_over_surface.blit(text_surface, text_rect)

        Button.draw_buttons(restart_button, menu_button, screen=game_over_surface)

        screen.blit(game_over_surface, (0, 0))
        pygame.display.update()
        clock.tick(30)


main = Main()
main.start_game()
