import pygame

from demo.flappy_bird.params import PIPE_WIDTH, PIPE_SPACE, HEIGHT, PIPE_SPEED, LEFT_POSITION, BIRD_HEIGHT, \
    BIRD_WIDTH


class Pipe:
    player_passed = False

    def __init__(self, player=None, generator=None, space_length=PIPE_SPACE, height=100, position=0):
        self.space_length = space_length
        self.width = PIPE_WIDTH
        self.position = position
        self.height = height
        self.player = player
        self.generator = generator
        self.rect1 = pygame.Rect(self.position, 0, self.width, height)
        self.image1 = pygame.image.load("/home/vincent/Documents/Xumes/demo/flappy_bird/assets/pipe_top.png")
        self.image1 = pygame.transform.scale(self.image1, (self.width, self.height))
        self.rect2 = pygame.Rect(self.position, self.space_length + self.height, self.width, HEIGHT - self.height)
        self.image2 = pygame.image.load("/home/vincent/Documents/Xumes/demo/flappy_bird/assets/pipe_bottom.png")
        self.image2 = pygame.transform.scale(self.image2, (self.width, HEIGHT - self.height))

    def draw(self, canvas):
        canvas.blit(self.image1, self.rect1)
        canvas.blit(self.image2, self.rect2)

    def move(self, dt):
        # Go to left
        self.position -= dt * PIPE_SPEED
        # Move rectangles
        self.rect1 = pygame.Rect(self.position, 0, self.width, self.height)
        self.rect2 = pygame.Rect(self.position, self.space_length + self.height, self.width,
                                 HEIGHT - self.height - self.space_length)

        # Check if collides with player
        if not self.collision():
            # Check if player passed the pipe (win one point)
            self.is_player_passed()

    def collision(self):
        # if the pipe collides we stop the game
        if (
                # player's x coordinate is between the width of the pipe
                self.position <= BIRD_WIDTH + LEFT_POSITION <= self.position + PIPE_WIDTH) and (
                # player's y coordinate touches one edge of the pipe
                self.player.position <= self.height or self.player.position + BIRD_HEIGHT >= self.space_length + self.height):
            self.generator.end()
            return True
        return False

    def is_player_passed(self):
        # if the mid point of the pipe passes the x coordinate of the player
        if self.position + PIPE_WIDTH / 2 <= BIRD_WIDTH + LEFT_POSITION \
                and not self.player_passed:
            self.player_passed = True
            self.player.gain_point()
