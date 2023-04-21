import pygame
import random
import os
import time
from abc import ABC, abstractmethod

# Define constants
WIDTH = 600
HEIGHT = 600
FPS = 10

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
SNAKE_COLOR = (81, 47, 95)

class Game(ABC):
    @abstractmethod
    def load_high_score(self):
        pass

    @abstractmethod
    def save_high_score(self):
        pass

    @abstractmethod
    def show_score(self):
        pass

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def logic(self):
        pass

    @abstractmethod
    def event_handler(self):
        pass

    @abstractmethod
    def show_start_button(self):
        pass

    @abstractmethod
    def splash_screen(self):
        pass

    @abstractmethod
    def start_game(self):
        pass

    @abstractmethod
    def mainloop(self):
        pass

    @abstractmethod
    def game_over_screen(self):
        pass

class SnakeGame(Game):
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake Game")
        self.background = pygame.image.load(os.path.join("assets", "background.png"))
        self.splash_background = pygame.image.load(os.path.join("assets", "splash.png"))
        self.game_screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.game_over = False
        self.game_started = False
        self.snake_position = [WIDTH//2, HEIGHT//2]
        self.food_position = [(random.randrange(1, WIDTH//10) * 10),
                              (random.randrange(1, HEIGHT//10) * 10)]
        self.velocity = 10
        self.snake_direction = 'RIGHT'
        self.snake_body = [self.snake_position]
        self.score = 0
        self.high_score = self.load_high_score()

    def load_high_score(self):
        try:
            with open('highScore.txt', 'r') as file:
                return int(file.read())
        except:
            return 0

    def save_high_score(self):
        with open('highScore.txt', 'w') as file:
            file.write(str(self.high_score))

    def show_score(self):
        show_score = pygame.font.SysFont("sans-serif", 25)
        show_score_surface = show_score.render(
            f"Score: {self.score}", True, BLACK)
        score_rect = show_score_surface.get_rect()

        score_rect.topleft = (5, 5)
        self.game_screen.blit(show_score_surface, score_rect)

        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()

        show_high_score = pygame.font.SysFont("sans-serif", 25)
        show_high_score_surface = show_high_score.render(
            f"High Score: {self.high_score}", True, BLACK)
        high_score_rect = show_high_score_surface.get_rect()

        high_score_rect.topright = (WIDTH - 5, 5)
        self.game_screen.blit(show_high_score_surface, high_score_rect)

    def draw(self):
        global snake_rect, food_rect

        image_w, image_h = self.background.get_size()
        image_w -= 33
        image_h -= 33

        # background image repeatedly displayed
        for x in range(0,  WIDTH, image_w):
            for y in range(0, HEIGHT, image_h):
                self.game_screen.blit(self.background, (x, y))

        pygame.draw.rect(self.game_screen, WHITE, [0, 0, WIDTH, HEIGHT], 5)

        snake_rect = pygame.Rect(
            self.snake_position[0], self.snake_position[1], 10, 10)
        pygame.draw.rect(self.game_screen, SNAKE_COLOR, snake_rect)

        food_rect = pygame.Rect(
            self.food_position[0], self.food_position[1], 10, 10)
        pygame.draw.rect(self.game_screen, RED, food_rect)

        for pos in self.snake_body:
            pygame.draw.rect(self.game_screen, SNAKE_COLOR,
                             pygame.Rect(pos[0], pos[1], 10, 10))

        for block in self.snake_body[1:]:
            if block[0] == self.snake_position[0] and block[1] == self.snake_position[1]:
                self.game_over = True

        if self.snake_position[0] <= 0 or self.snake_position[0] >= WIDTH - 5 or self.snake_position[1] <= 0 or self.snake_position[1] >= HEIGHT - 5:
            self.game_over = True

    def logic(self):
        global score

        self.snake_body.insert(0, list(self.snake_position))
        if self.snake_position[0] <= 0 or self.snake_position[0] >= WIDTH - 5 or self.snake_position[1] <= 0 or self.snake_position[1] >= HEIGHT - 5:
            self.game_over = True

        if self.snake_position == self.food_position:
            self.food_position = [(random.randrange(1, WIDTH//10) * 10),
                                (random.randrange(1, HEIGHT//10) * 10)]
            self.score += 10
        else:
            if len(self.snake_body) > 1:
                self.snake_body.pop()

        if self.score > self.high_score:
            self.high_score = self.score

        for block in self.snake_body[1:]:
            if block == self.snake_position:
                self.game_over = True

        if self.snake_direction == 'UP':
            self.snake_position[1] -= self.velocity
        if self.snake_direction == 'DOWN':
            self.snake_position[1] += self.velocity
        if self.snake_direction == 'LEFT':
            self.snake_position[0] -= self.velocity
        if self.snake_direction == 'RIGHT':
            self.snake_position[0] += self.velocity

    def event_handler(self):
        direction_change_to = self.snake_direction

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    direction_change_to = 'UP'
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    direction_change_to = 'DOWN'
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    direction_change_to = 'LEFT'
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    direction_change_to = 'RIGHT'

        if direction_change_to == 'UP' and self.snake_direction != 'DOWN':
            self.snake_direction = 'UP'
        if direction_change_to == 'DOWN' and self.snake_direction != 'UP':
            self.snake_direction = 'DOWN'
        if direction_change_to == 'LEFT' and self.snake_direction != 'RIGHT':
            self.snake_direction = 'LEFT'
        if direction_change_to == 'RIGHT' and self.snake_direction != 'LEFT':
            self.snake_direction = 'RIGHT'

    def show_start_button(self):
        startFont = pygame.font.SysFont("Ubuntu", 20)
        startSurface = startFont.render("Press SPACE to Start", True, WHITE)
        startRect = startSurface.get_rect()

        startRect.midbottom = (WIDTH/2, HEIGHT - 50)
        self.game_screen.blit(startSurface, startRect)

        exitFont = pygame.font.SysFont("sans-serif", 30)
        exitSurface = exitFont.render("For Exit Press Q", True, RED)
        exitRect = exitSurface.get_rect()

        exitRect.bottomright = (WIDTH - 10, HEIGHT - 10)
        self.game_screen.blit(exitSurface, exitRect)

        pygame.display.update()

    def splash_screen(self):
        splash_image = pygame.transform.scale(self.splash_background.convert_alpha(), (WIDTH, HEIGHT))
        self.game_screen.blit(splash_image, (0, 0))
        self.show_start_button()
        pygame.display.update()
        self.game_screen.fill(BLACK)
        self.start_game()

    def start_game(self):
        while not self.game_started:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.game_started = True
                    if event.key == pygame.K_q:
                        pygame.quit()
                        quit()
        self.mainloop()

    def mainloop(self):
        while not self.game_over:
            self.event_handler()
            self.logic()
            self.draw()
            self.show_score()

            self.clock.tick(FPS)
            pygame.display.update()

        self.game_over_screen()

    def game_over_screen(self):
        gameOverFont = pygame.font.SysFont("Ubuntu", 50)
        gameOverSurface = gameOverFont.render("Game Over", True, RED)

        myHighScore = pygame.font.SysFont("Ubuntu", 30)
        highScoreSurface = myHighScore.render(
            f"High Score: {str(self.high_score)}", True, BLUE)

        myScore = pygame.font.SysFont("Ubuntu", 30)
        scoreSurface = myScore.render(
            f"Score: {str(self.score)}", True, BLUE)

        gameOverRect = gameOverSurface.get_rect()
        highScoreRect = highScoreSurface.get_rect()
        scoreRect = scoreSurface.get_rect()

        gameOverRect.midtop = (WIDTH/2, HEIGHT/2 - 50)
        highScoreRect.midtop = (WIDTH/2, HEIGHT - 50)
        scoreRect.midbottom = (WIDTH/2, HEIGHT - 50)

        self.game_screen.blit(gameOverSurface, gameOverRect)
        self.game_screen.blit(highScoreSurface, highScoreRect)
        self.game_screen.blit(scoreSurface, scoreRect)

        pygame.display.update()

        time.sleep(2)

        self.game_started = False
        self.game_over = False
        self.snake_position = [WIDTH//2, HEIGHT//2]
        self.food_position = [(random.randrange(1, WIDTH//10) * 10),
                            (random.randrange(1, HEIGHT//10) * 10)]
        self.velocity = 10
        self.snake_direction = 'RIGHT'
        self.snake_body = [self.snake_position]
        self.score = 0

        self.game_screen.fill(BLACK)
        self.show_start_button()

        self.start_game()

    def run(self):
        self.splash_screen()

if __name__ == "__main__":
    game = SnakeGame()
    game.run()