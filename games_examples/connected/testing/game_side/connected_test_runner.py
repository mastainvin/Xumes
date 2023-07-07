import random
import sys
import logging

import pygame
from xumes.game_module import TestRunner, GameService, PygameEventFactory, CommunicationServiceGameMq, State

from games_examples.connected.main import Game
from games_examples.connected.objects import Balls, Coins, Tiles, Particle, CENTER


class ConnectedTestRunner(TestRunner):

    def __init__(self):
        super().__init__()
        self.game = Game()
        self.game = self.bind(self.game, "game", state=State("terminated", methods_to_observe=["end_game", "reset"]))

        def get_pos(pos_list):
            pos_dct = []
            for pos in pos_list:
                pos_dict = {
                    "x": pos[0],
                    "y": pos[1]
                }
                pos_dct.append(pos_dict)
            return pos_dct

        self.game.Balls = self.bind(Balls(pos=(CENTER[0], CENTER[1] + self.game.RADIUS), radius=self.game.RADIUS, angle = 90, win=self.game.win), name="balls", state=[
            State("pos_list",func=get_pos, methods_to_observe="update"),
            State("score", methods_to_observe="update_score"),
            State("highscore", methods_to_observe="update_highscore")
        ])

        self.game.Coins = self.bind(Coins(y=random.randint(CENTER[1]-self.game.RADIUS, CENTER[1] + self.game.RADIUS), win = self.game.win), name="coins", state=[
            State("x", methods_to_observe="update"),
            State("y", methods_to_observe="__init__"),
        ])

        self.game.Tiles = self.bind(Tiles(y = random.choice([CENTER[1]-80, CENTER[1], CENTER[1]+80]) ,type_= random.randint(1,3), win=self.game.win), name="tiles", state=[
            State("x", methods_to_observe="update"),
            State("y", methods_to_observe="__init__"),
            State("type", methods_to_observe="__init__"),
        ])

        self.game.Particle = self.bind(Particle(x=self.game.ball.rect.center,y=self.game.ball.rect.center,color=self.game.color_list[self.game.color_index],win=self.game.win), name="particle", state=[
            State("x", methods_to_observe="update"),
            State("y", methods_to_observe="update")
        ])

        self.game.all_sprites = pygame.sprite.Group()
        self.game.all_sprites.add(self.game.Balls)
        self.game.all_sprites.add(self.game.Tiles)
        self.game.all_sprites.add(self.game.Coins)
        self.game.all_sprites.add(self.game.Particle)

    def run_test(self) -> None:

        while self.game.running:

            self.test_client.wait()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or \
                            event.key == pygame.K_q:
                        self.game.running = False

                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and self.game.game_page:
                    if not self.game.clicked:
                        self.game.clicked = True
                        for self.game.ball in self.game.ball_group:
                            self.game.ball.dtheta *= -1
                            self.game.flip_fx.play()

                        self.game.num_clicks += 1
                        if self.game.num_clicks % 5 == 0:
                            self.game.color_index += 1
                            if self.game.color_index > len(self.game.color_list) - 1:
                                self.game.color_index = 0

                            self.game.color = self.game.color_list[self.game.color_index]

                if event.type == pygame.KEYUP and event.key == pygame.K_SPACE and self.game.game_page:
                    self.game.clicked = False

            if self.game.game_page:

                if self.game.player_alive:

                    for self.game.ball in self.game.ball_group:
                        if pygame.sprite.spritecollide(self.ball, self.game.coin_group, True):
                            self.game.score_fx.play()
                            self.game.score += 1
                            Balls.update_score(self, self.game.score)
                            if self.game.highscore <= self.game.score:
                                self.game.highscore = self.game.score
                                Balls.update_highscore(self, self.game.highscore)

                            x, self.game.y = self.game.ball.rect.center
                            for i in range(10):
                                particle = Particle(x, self.game.y, self.game.color, self.game.win)
                                self.game.particle_group.add(particle)

                        if pygame.sprite.spritecollide(self.game.ball, self.game.tile_group, True):
                            x, y = self.game.ball.rect.center
                            for i in range(30):
                                particle = Particle(x, y, self.game.color, self.game.win)
                                self.game.particle_group.add(particle)

                            self.game.player_alive = False
                            self.game.dead_fx.play()

                    self.game.current_time = pygame.time.get_ticks()
                    self.game.delta = self.game.current_time - self.game.start_time
                    if self.game.coin_delta < self.game.delta < self.game.coin_delta + 100 and self.game.new_coin:
                        self.game.y = random.randint(self.game.CENTER[1] - self.game.RADIUS,
                                                     self.game.CENTER[1] + self.game.RADIUS)
                        self.game.coin = Coins(self.game.y, self.game.win)
                        self.game.coin_group.add(self.game.coin)
                        self.game.new_coin = False

                    if self.game.current_time - self.game.start_time >= self.game.tile_delta:
                        self.game.y = random.choice(
                            [self.game.CENTER[1] - 80, self.game.CENTER[1], self.game.CENTER[1] + 80])
                        self.game.type_ = random.randint(1, 3)
                        self.game.t = Tiles(self.game.y, self.game.type_, self.game.win)
                        self.game.tile_group.add(self.game.t)

                        self.game.start_time = self.game.current_time
                        self.game.new_coin = True

            if not self.game.player_alive and len(self.game.particle_group) == 0:
                # self.score_page = True
                self.game.game_page = False

                self.game.score_page_fx.play()

                self.game.ball_group.empty()
                self.game.tile_group.empty()
                self.game.coin_group.empty()

                self.game.end_game()

            #self.game.check_end()

    def run_test_render(self) -> None:

        while self.game.running:

            self.test_client.wait()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or \
                            event.key == pygame.K_q:
                        self.game.running = False

                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and self.game.game_page:
                    if not self.game.clicked:
                        self.game.clicked = True
                        for self.game.ball in self.game.ball_group:
                            self.game.ball.dtheta *= -1
                            self.game.flip_fx.play()

                        self.game.num_clicks += 1
                        if self.game.num_clicks % 5 == 0:
                            self.game.color_index += 1
                            if self.game.color_index > len(self.game.color_list) - 1:
                                self.game.color_index = 0

                            self.game.color = self.game.color_list[self.game.color_index]

                if event.type == pygame.KEYUP and event.key == pygame.K_SPACE and self.game.game_page:
                    self.game.clicked = False


            if self.game.game_page:

                if self.game.player_alive:

                    for self.game.ball in self.game.ball_group:
                        if pygame.sprite.spritecollide(self.ball, self.game.coin_group, True):
                            self.game.score_fx.play()
                            self.game.score += 1
                            Balls.update_score(self, self.game.score)
                            if self.game.highscore <= self.game.score:
                                self.game.highscore = self.game.score
                                Balls.update_highscore(self, self.game.highscore)

                            x, self.game.y = self.game.ball.rect.center
                            for i in range(10):
                                particle = Particle(x, self.game.y, self.game.color, self.game.win)
                                self.game.particle_group.add(particle)

                        if pygame.sprite.spritecollide(self.game.ball, self.game.tile_group, True):
                            x, y = self.game.ball.rect.center
                            for i in range(30):
                                particle = Particle(x, y, self.game.color, self.game.win)
                                self.game.particle_group.add(particle)

                            self.game.player_alive = False
                            self.game.dead_fx.play()

                    self.game.current_time = pygame.time.get_ticks()
                    self.game.delta = self.game.current_time - self.game.start_time
                    if self.game.coin_delta < self.game.delta < self.game.coin_delta + 100 and self.game.new_coin:
                        self.game.y = random.randint(self.game.CENTER[1] - self.game.RADIUS, self.game.CENTER[1] + self.game.RADIUS)
                        self.game.coin = Coins(self.game.y, self.game.win)
                        self.game.coin_group.add(self.game.coin)
                        self.game.new_coin = False

                    if self.game.current_time - self.game.start_time >= self.game.tile_delta:
                        self.game.y = random.choice([self.game.CENTER[1] - 80, self.game.CENTER[1], self.game.CENTER[1] + 80])
                        self.game.type_ = random.randint(1, 3)
                        self.game.t = Tiles(self.game.y, self.game.type_, self.game.win)
                        self.game.tile_group.add(self.game.t)

                        self.game.start_time = self.game.current_time
                        self.game.new_coin = True

            if not self.game.player_alive and len(self.game.particle_group) == 0:
                # self.score_page = True
                self.game.game_page = False

                self.game.score_page_fx.play()

                self.game.ball_group.empty()
                self.game.tile_group.empty()
                self.game.coin_group.empty()

                self.game.end_game()

            self.game.render()

    def reset(self) -> None:
        self.game.reset()

    def random_reset(self) -> None:
        self.reset()

    def delete_screen(self) -> None:
        pass


if __name__ == "__main__":

    if len(sys.argv) > 1:
        if sys.argv[1] == "-test":
            logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
        if sys.argv[1] == "-render":
            logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

        game_service = GameService(test_runner=ConnectedTestRunner(),
                                   event_factory=PygameEventFactory(),
                                   communication_service=CommunicationServiceGameMq(ip="localhost"))
        if sys.argv[1] == "-test":
            game_service.run()
        if sys.argv[1] == "-render":
            game_service.run_render()

    else:
        game = Game()
        game.run()

