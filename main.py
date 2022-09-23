import pygame  # importing modules
from random import randint
from pygame.math import Vector2
import sys
import time


print('Hello, dear Twitterino')

print('I present you with everything...')

time.sleep(3)


class Snake:
    def __init__(self):
        self.body = [  # snake vector body
            Vector2(5, 10),
            Vector2(4, 10),
            Vector2(3, 10),
        ]

        self.direction = Vector2(1, 0)  # snake base direction
        self.new_block = False  # boolean building new block

        self.jesse = pygame.image.load('Graphics/Screenshot_3.png').convert_alpha()  # head
        self.jesse = pygame.transform.scale(self.jesse, (cell_size, cell_size))

        self.jesse_down = self.jesse
        self.jesse_up = pygame.transform.rotate(self.jesse, 180)
        self.jesse_right = pygame.transform.rotate(self.jesse, 90)
        self.jesse_left = pygame.transform.rotate(self.jesse, 270)

        self.jane = pygame.image.load('Graphics/Jane.png').convert_alpha()  # tail
        self.jane = pygame.transform.scale(self.jane, (cell_size, cell_size))

        self.jane_up = self.jane
        self.jane_down = pygame.transform.rotate(self.jane, 180)
        self.jane_right = pygame.transform.rotate(self.jane, 90)
        self.jane_left = pygame.transform.rotate(self.jane, 270)

        self.heart = pygame.image.load('Graphics/heart.png')  # middles
        self.heart = pygame.transform.scale(self.heart, (cell_size, cell_size))

        self.head_up = self.jesse_up
        self.head_down = self.jesse_down
        self.head_right = self.jesse_right
        self.head_left = self.jesse_left

        self.tail_up = self.jane_up
        self.tail_down = self.jane_down
        self.tail_right = self.jane_left
        self.tail_left = self.jane_right

        self.sound = pygame.mixer.Sound(
            'Sound/walter-white-screaming-furiously-at-jesse-pinkman-whilst-aggres-By-Tuna.mp3')

    def draw_snake(self):  # drawing snake
        self.update_head()
        self.update_tail()

        for index, block in enumerate(self.body):  # drawing head, body, tail
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            if index == 0:
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            else:
                screen.blit(self.heart, block_rect)
                self.heart = pygame.transform.rotate(self.heart, 90)

    def update_head(self):  # updating head on change
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1, 0): self.head = self.head_left
        elif head_relation == Vector2(-1, 0): self.head = self.head_right
        elif head_relation == Vector2(0, 1): self.head = self.head_up
        elif head_relation == Vector2(0, -1): self.head = self.head_down

    def update_tail(self):  # updating tail on change
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1, 0): self.tail = self.tail_left
        elif tail_relation == Vector2(-1, 0): self.tail = self.tail_right
        elif tail_relation == Vector2(0, 1): self.tail = self.tail_up
        elif tail_relation == Vector2(0, -1): self.tail = self.tail_down

    def move_snake(self):  # moving snake via beheading and appending
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):  # changing value of adding block
        self.new_block = True

    def play_sound(self):  # playing walter sound
        self.sound.play()


class Walter:
    def __init__(self):  # walter fruits spawn
        self.randomize()  # randomising position from the function below

        self.walt = pygame.image.load('Graphics/abdelrahman-kubisi-front-hat.jpg').convert_alpha()  # loading walt image
        self.walt = pygame.transform.scale(self.walt, (cell_size, cell_size))

    def draw_fruit(self):  # drawing walt
        pos_x = int(self.pos.x * cell_size)
        pos_y = int(self.pos.y * cell_size)
        fruit_rect = pygame.Rect(pos_x, pos_y, cell_size, cell_size)
        screen.blit(self.walt, fruit_rect)

    def randomize(self):
        self.x = randint(0, cell_number - 1)
        self.y = randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)


class Main:  # a class for everything
    def __init__(self):
        self.snake = Snake()  # jesse
        self.walter = Walter()  # walter

        self.call_you = pygame.mixer.Sound('Sound/CALL YOU A BITCH - AUDIO FROM JAYUZUMI.COM.mp3')  # end-phrase 1
        self.bitch = pygame.mixer.Sound('Sound/BITCH - AUDIO FROM JAYUZUMI.COM.mp3')  # end-phrase 2
        self.jesus = pygame.mixer.Sound('Sound/JESUS - AUDIO FROM JAYUZUMI.COM.mp3')  # fail phrase

        self.count = 0  # counter

        self.twenty_five = pygame.mixer.Sound('Sound/25.mp3')  # counters
        self.fifty = pygame.mixer.Sound('Sound/50.mp3')
        self.seventy_five = pygame.mixer.Sound('Sound/75.mp3')
        self.hundred = pygame.mixer.Sound('Sound/100.mp3')

    def update(self):  # updating everything
        self.snake.move_snake()
        self.collision()
        self.check_fail()

    def draw_elements(self):  # drawing everything
        self.draw_walter()
        self.draw_score()
        self.walter.draw_fruit()
        self.snake.draw_snake()

    def collision(self):  # checking for collisions with walter

        if self.walter.pos == self.snake.body[0]:
            self.count += 1
            self.walter.randomize()
            self.snake.add_block()
            if self.count == 25:  # ifs on sounds
                self.twenty_five.play()
            elif self.count == 50:
                self.fifty.play()
            elif self.count == 75:
                self.seventy_five.play()
            elif self.count == 100:
                self.hundred.play()
                time.sleep(5)
                pygame.quit()
                sys.exit()
            else:
                self.snake.play_sound()

        for block in self.snake.body[1:]:
            if block == self.walter.pos:
                self.walter.randomize()

    def check_fail(self):  # checking if failed (reason: hit wall)
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.jesus.play()
            self.game_over()

        for block in self.snake.body[1:]: # checking if failed (reason: hit yourself)
            if block == self.snake.body[0]:
                self.jesus.play()
                self.game_over()

    def game_over(self):  # resetting the game
        self.reset()

    def draw_walter(self):  # drawing bg image

        bg = pygame.image.load('Graphics/Без названия (1).jpg')
        bg = pygame.transform.scale(bg, (cell_pos, cell_pos))
        screen.blit(bg, (0, 0))

    def draw_score(self):  # drawing score
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text, True, pygame.Color('white'))
        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center = (score_x, score_y))

        screen.blit(score_surface, score_rect)

    def reset(self):  # respawning the snake
        self.snake.body = [
            Vector2(5, 10),
            Vector2(4, 10),
            Vector2(3, 10),
        ]

        self.snake.direction = Vector2(1, 0)  # necessary for proper motion right

        self.snake.move_snake()  # moving once so it doesn't get stuck

    def bitching(self):  # ending phrase
        self.call_you.play()
        time.sleep(4)
        self.bitch.play()
        time.sleep(1)


pygame.init()  # initialising pygame


cell_size = 40  # playground parameters
cell_number = 20
cell_pos = cell_size * cell_number


pygame.mixer.music.load('Sound/breaking_bad_01 - Breaking Bad - Main Title Theme (Extended).mp3')  # bg music
pygame.mixer.music.set_volume(0.07)
pygame.mixer.music.play(-1)


SCREEN_UPDATE = pygame.USEREVENT  # Screen updater - higher is slower
pygame.time.set_timer(SCREEN_UPDATE, 90)


game_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 25)  # Font for counter


screen = pygame.display.set_mode((cell_pos, cell_pos))  # setting display resolution, title, icon and framerate counter
pygame.display.set_icon(pygame.image.load('Graphics/Hank.png'))
pygame.display.set_caption('JESSE VS WALTER')
clock = pygame.time.Clock()


main = Main()  # loading everything to an object


while True:
    for event in pygame.event.get():  # event updater

        if event.type == pygame.QUIT:  # quit button
            main.bitching()
            pygame.quit()
            sys.exit()

        if event.type == SCREEN_UPDATE:  # updater for snake
            main.update()

        if event.type == pygame.KEYDOWN:  # snake moving
            if event.key == pygame.K_UP:
                if main.snake.direction.y != 1:
                    main.snake.direction = Vector2(0, -1)  # up
            if event.key == pygame.K_DOWN:
                if main.snake.direction.y != -1:
                    main.snake.direction = Vector2(0, 1)  # down
            if event.key == pygame.K_RIGHT:
                if main.snake.direction.x != -1:
                    main.snake.direction = Vector2(1, 0)  # right
            if event.key == pygame.K_LEFT:
                if main.snake.direction.x != 1:
                    main.snake.direction = Vector2(-1, 0)  # left

    main.draw_elements()  # drawing everything
    pygame.display.update()  # updating screen

    clock.tick(60)  # limiting fps to 60