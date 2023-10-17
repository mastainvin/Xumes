"""
Snake Eater
Made with PyGame
"""

import pygame, sys, time, random

# 难度设置
# Difficulty settings
class Settings:
    def __init__(self):
        # 难度设置，值越大越难
        # Difficulty setting, the larger the value, the more difficult
        self.difficulty = 25

        # 窗口大小设置
        # Window size settings
        self.frame_size_x = 720
        self.frame_size_y = 480

        # 颜色设置 (R, G, B)
        # Color settings (R, G, B)
        self.black = pygame.Color(0, 0, 0)
        self.white = pygame.Color(255, 255, 255)
        self.red = pygame.Color(255, 0, 0)
        self.green = pygame.Color(0, 255, 0)
        self.blue = pygame.Color(0, 0, 255)


class Game:
    def __init__(self, settings):
        self.settings = settings
        self.score = 0
        self.snake_pos = [100, 50]
        self.snake_body = [[100, 50], [100-10, 50], [100-(2*10), 50]]
        self.food_pos = [random.randrange(1, (self.settings.frame_size_x//10)) * 10, random.randrange(1, (self.settings.frame_size_y//10)) * 10]
        self.food_spawn = True
        self.direction = 'RIGHT'
        self.change_to = self.direction
        self.fps_controller = pygame.time.Clock()

        # 检查是否有错误
        # Check for errors
        check_errors = pygame.init()
        if check_errors[1] > 0:
            print(f'[!] Had {check_errors[1]} errors when initialising game, exiting...')
            sys.exit(-1)
        else:
            print('[+] Game successfully initialised')

        # 初始化游戏窗口
        # Initialise game window
        pygame.display.set_caption('Snake Eater')
        self.game_window = pygame.display.set_mode((self.settings.frame_size_x, self.settings.frame_size_y))

    # 游戏结束
    # Game Over
    def game_over(self):
        my_font = pygame.font.SysFont('times new roman', 90)
        game_over_surface = my_font.render('YOU DIED', True, self.settings.red)
        game_over_rect = game_over_surface.get_rect()
        game_over_rect.midtop = (self.settings.frame_size_x/2, self.settings.frame_size_y/4)
        self.game_window.fill(self.settings.black)
        self.game_window.blit(game_over_surface, game_over_rect)
        self.show_score(0, self.settings.red, 'times', 20)
        pygame.display.flip()
        time.sleep(3)
        pygame.quit()
        sys.exit()

    # 显示分数
    # Display score
    def show_score(self, choice, color, font, size):
        score_font = pygame.font.SysFont(font, size)
        score_surface = score_font.render('Score : ' + str(self.score), True, color)
        score_rect = score_surface.get_rect()
        if choice == 1:
            score_rect.midtop = (self.settings.frame_size_x/10, 15)
        else:
            score_rect.midtop = (self.settings.frame_size_x/2, self.settings.frame_size_y/1.25)
        self.game_window.blit(score_surface, score_rect)

    # 主要的游戏逻辑
    # Main game logic
    def run_game(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # 每当有键被按下
                # Whenever a key is pressed down
                elif event.type == pygame.KEYDOWN:
                    # W -> 上; S -> 下; A -> 左; D -> 右
                    # W -> Up; S -> Down; A -> Left; D -> Right
                    if event.key == pygame.K_UP or event.key == ord('w'):
                        self.change_to = 'UP'
                    if event.key == pygame.K_DOWN or event.key == ord('s'):
                        self.change_to = 'DOWN'
                    if event.key == pygame.K_LEFT or event.key == ord('a'):
                        self.change_to = 'LEFT'
                    if event.key == pygame.K_RIGHT or event.key == ord('d'):
                        self.change_to = 'RIGHT'
                    # Esc -> 创建退出游戏的事件
                    # Esc -> Create event to quit the game
                    if event.key == pygame.K_ESCAPE:
                        pygame.event.post(pygame.event.Event(pygame.QUIT))

            # 确保蛇不能瞬间移动到相反的方向
            # Making sure the snake cannot move in the opposite direction instantaneously
            if self.change_to == 'UP' and self.direction != 'DOWN':
                self.direction = 'UP'
            if self.change_to == 'DOWN' and self.direction != 'UP':
                self.direction = 'DOWN'
            if self.change_to == 'LEFT' and self.direction != 'RIGHT':
                self.direction = 'LEFT'
            if self.change_to == 'RIGHT' and self.direction != 'LEFT':
                self.direction = 'RIGHT'

            # 移动蛇
            # Moving the snake
            if self.direction == 'UP':
                self.snake_pos[1] -= 10
            if self.direction == 'DOWN':
                self.snake_pos[1] += 10
            if self.direction == 'LEFT':
                self.snake_pos[0] -= 10
            if self.direction == 'RIGHT':
                self.snake_pos[0] += 10

            # 蛇身体的增长机制
            # Snake body growing mechanism
            self.snake_body.insert(0, list(self.snake_pos))
            if self.snake_pos[0] == self.food_pos[0] and self.snake_pos[1] == self.food_pos[1]:
                self.score += 1
                self.food_spawn = False
            else:
                self.snake_body.pop()

            # 在屏幕上产生食物
            # Spawning food on the screen
            if not self.food_spawn:
                self.food_pos = [random.randrange(1, (self.settings.frame_size_x//10)) * 10, random.randrange(1, (self.settings.frame_size_y//10)) * 10]
            self.food_spawn = True

            # 图形界面
            # GFX
            self.game_window.fill(self.settings.black)
            for pos in self.snake_body:
                # 蛇的身体
                # Snake body
                pygame.draw.rect(self.game_window, self.settings.green, pygame.Rect(pos[0], pos[1], 10, 10))

            # 蛇的食物
            # Snake food
            pygame.draw.rect(self.game_window, self.settings.white, pygame.Rect(self.food_pos[0], self.food_pos[1], 10, 10))

            # 游戏结束的条件
            # Game Over conditions
            if self.snake_pos[0] < 0 or self.snake_pos[0] > self.settings.frame_size_x-10:
                self.game_over()
            if self.snake_pos[1] < 0 or self.snake_pos[1] > self.settings.frame_size_y-10:
                self.game_over()
            for block in self.snake_body[1:]:
                if self.snake_pos[0] == block[0] and self.snake_pos[1] == block[1]:
                    self.game_over()

            self.show_score(1, self.settings.white, 'consolas', 20)
            pygame.display.update()
            self.fps_controller.tick(self.settings.difficulty)


# 运行游戏
# Running the game
if __name__ == '__main__':
    settings = Settings()
    game = Game(settings)
    game.run_game()
