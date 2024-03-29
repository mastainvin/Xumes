# Connected

# Author : Prajjwal Pathak (pyguru)
# Date : Thursday, 8 August, 2021

import random
import pygame
import time
from games_examples.connected_new.objects import Balls, Coins, Tiles, Particle, Message, Button
from games_examples.connected_new.generator import PipeGenerator

# RADIUS = 70

class Game:
	terminated = False

	SCREEN = WIDTH, HEIGHT = 288, 512
	CENTER = WIDTH // 2, HEIGHT // 2
	RADIUS = 70

	RED = (255, 0, 0)
	GREEN = (0, 177, 64)
	BLUE = (30, 144, 255)
	ORANGE = (252, 76, 2)
	YELLOW = (254, 221, 0)
	PURPLE = (155, 38, 182)
	AQUA = (0, 103, 127)
	WHITE = (255, 255, 255)
	BLACK = (0, 0, 0)
	GRAY = (25, 25, 25)



	def __init__(self):
		pygame.init()

		self.info = pygame.display.Info()
		self.width = self.info.current_w
		self.height = self.info.current_h
		self.dt=0
		if self.width >= self.height:
			self.win = pygame.display.set_mode(self.SCREEN, pygame.NOFRAME)
		else:
			self.win = pygame.display.set_mode(self.SCREEN, pygame.NOFRAME | pygame.SCALED | pygame.FULLSCREEN)
		pygame.display.set_caption('Connected')
		self.generator = PipeGenerator(game=self,win = self.win)
		self.clock = pygame.time.Clock()
		self.FPS = 0

	# COLORS **********************************************************************

		self.color_list = [self.PURPLE, self.GREEN, self.BLUE, self.ORANGE, self.YELLOW, self.RED]
		self.color_index = 0
		self.color = self.color_list[self.color_index]

		# VARIABLES *******************************************************************

		self.clicked = False
		self.new_coin = True
		self.num_clicks = 0
		# self.score = 0

		self.player_alive = True
		self.score = 0
		self.highscore = 0
		self.sound_on = True
		self.easy_level = True

		self.home_page = True
		self.game_page = False
		self.score_page = False
		self.running = True
		self.collided_rectangles = False

	# SOUNDS **********************************************************************

		import os

		current_directory = os.path.dirname(__file__)
		sounds_directory = os.path.abspath(os.path.join(current_directory, '..', 'connected/Sounds'))


	# FONTS ***********************************************************************


		fonts_directory = os.path.join(current_directory, 'Fonts')

		self.title_font = os.path.join(fonts_directory, 'Aladin-Regular.ttf')
		self.score_font = os.path.join(fonts_directory, 'DroneflyRegular-K78LA.ttf')
		self.game_over_font = os.path.join(fonts_directory, 'ghostclan.ttf')
		self.final_score_font = os.path.join(fonts_directory, 'DalelandsUncialBold-82zA.ttf')
		self.new_high_font = os.path.join(fonts_directory, 'BubblegumSans-Regular.ttf')

		self.connected = Message(self.WIDTH//2, 120, 55, "ConnecteD", self.title_font, self.WHITE, self.win)
		self.score_msg = Message(self.WIDTH//2, 100, 60, "0", self.score_font, (150, 150, 150), self.win)
		self.game_msg = Message(80, 150, 40, "GAME", self.game_over_font, self.BLACK, self.win)
		self.over_msg = Message(210, 150, 40, "OVER!", self.game_over_font, self.WHITE, self.win)
		self.final_score = Message(self.WIDTH//2, self.HEIGHT//2, 90, "0", self.final_score_font, self.RED, self.win)
		self.new_high_msg = Message(self.WIDTH//2, self.HEIGHT//2+60, 20, "New High", None, self.GREEN, self.win)

	# Button images

		assets_directory = os.path.join(current_directory, 'Assets')

		self.home_img = pygame.image.load(os.path.join(assets_directory, 'homeBtn.png'))
		self.replay_img = pygame.image.load(os.path.join(assets_directory, 'replay.png'))
		self.sound_off_img = pygame.image.load(os.path.join(assets_directory, 'soundOffBtn.png'))
		self.sound_on_img = pygame.image.load(os.path.join(assets_directory, 'soundOnBtn.png'))
		self.easy_img = pygame.image.load(os.path.join(assets_directory, 'easy.jpg'))
		self.hard_img = pygame.image.load(os.path.join(assets_directory, 'hard.jpg'))
	# Buttons

		self.easy_btn = Button(self.easy_img, (70, 24), self.WIDTH//4-10, self.HEIGHT-100)
		self.hard_btn = Button(self.hard_img, (70, 24), self.WIDTH//2 + 10, self.HEIGHT-100)
		self.home_btn = Button(self.home_img, (24, 24), self.WIDTH // 4 - 18, self.HEIGHT//2 + 120)
		self.replay_btn = Button(self.replay_img, (36,36), self.WIDTH // 2  - 18, self.HEIGHT//2 + 115)
		self.sound_btn = Button(self.sound_on_img, (24, 24), self.WIDTH - self.WIDTH // 4 - 18, self.HEIGHT//2 + 120)

	# Groups **********************************************************************

		self.ball_group = pygame.sprite.Group()
		self.coin_group = pygame.sprite.Group()
		self.tile_group = pygame.sprite.Group()
		self.particle_group = pygame.sprite.Group()

		if self.easy_level:

			self.ball = Balls((self.CENTER[0], self.CENTER[1] + self.RADIUS), self.RADIUS, 90, self.win)
			self.ball_group.add(self.ball)
		else:
			self.ball = Balls((self.CENTER[0], self.CENTER[1] + self.RADIUS), self.RADIUS, 90, self.win)
			self.ball_group.add(self.ball)
			self.ball = Balls((self.CENTER[0], self.CENTER[1] - self.RADIUS), self.RADIUS, 270, self.win)
			self.ball_group.add(self.ball)

	# TIME ************************************************************************

		self.start_time = pygame.time.get_ticks()
		self.current_time = 0
		self.coin_delta = 500
		self.tile_delta = 1200


		self.coin = Coins(0, self.win)
		self.tile = Tiles(0, 0, self.win)

	def run(self):

		while self.running:
			self.update_check()
			self.render()
		self.dt = self.clock.tick(60) / 1000

	def update(self):
		# print("update called")
		self.update_main()

		self.ball_group.update(self.color)
		self.coin_group.update(self.color)
		self.tile_group.update()
		self.score_msg.update(self.score)
		self.particle_group.update()
		self.clock.tick(self.FPS)
		pygame.display.update()

	def update_main(self):
		# print(self.ball.rect,self.coin.py.x,self.tile.x,"yesok")
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running = False

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE or \
						event.key == pygame.K_q:
					self.running = False


			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and self.game_page:
				if not self.clicked:
					self.clicked = True
					for self.ball in self.ball_group:
						self.ball.dtheta *= -1
						self.flip_fx.play()

					self.num_clicks += 1
					if self.num_clicks % 5 == 0:
						self.color_index += 1
						if self.color_index > len(self.color_list) - 1:
							self.color_index = 0

						self.color = self.color_list[self.color_index]

			if event.type == pygame.KEYUP and event.key == pygame.K_SPACE and self.game_page:
				self.clicked = False

			# if event.type == pygame.KEYDOWN and event.key == pygame.K_UP and self.game_page:
			# 	if (not self.clicked)  and  self.ball.dtheta<0:
			# 		self.clicked = True
			# 		for self.ball in self.ball_group:
			# 			self.ball.dtheta *= -1
			# 			self.flip_fx.play()
			#
			# 		self.num_clicks += 1
			# 		if self.num_clicks % 5 == 0:
			# 			self.color_index += 1
			# 			if self.color_index > len(self.color_list) - 1:
			# 				self.color_index = 0
			#
			# 			self.color = self.color_list[self.color_index]
			#
			# if event.type == pygame.KEYUP and event.key == pygame.K_UP and self.game_page:
			# 	self.clicked = False
			#
			#
			# elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN and self.game_page:
			# 	if (not self.clicked)  and  self.ball.dtheta>0:
			# 		self.clicked = True
			# 		for self.ball in self.ball_group:
			# 			self.ball.dtheta *= -1
			# 			self.flip_fx.play()
			#
			# 		self.num_clicks += 1
			# 		if self.num_clicks % 5 == 0:
			# 			self.color_index += 1
			# 			if self.color_index > len(self.color_list) - 1:
			# 				self.color_index = 0
			#
			# 			self.color = self.color_list[self.color_index]
			#
			# if event.type == pygame.KEYUP and event.key == pygame.K_DOWN and self.game_page:
			# 	self.clicked = False

		if self.game_page:

			if self.player_alive:

				for self.ball in self.ball_group:
					if pygame.sprite.spritecollide(self.ball, self.coin_group, True):
						self.score_fx.play()

						self.score += 1
						# print(self.score)
						Balls.update_score(self, self.score)

						if self.highscore <= self.score:
							self.highscore = self.score
							#print(self.highscore)
							Balls.update_highscore(self, self.highscore)

						x, self.y = self.ball.rect.center
						for i in range(10):
							particle = Particle(x, self.y, self.color, self.win)
							self.particle_group.add(particle)

					self.collided_rectangles = pygame.sprite.spritecollide(self.ball, self.tile_group, True)
					if self.collided_rectangles:
						# print("collide")
						self.ball_group.remove(self.ball)
						x, y = self.ball.rect.center
						for i in range(30):
							particle = Particle(x, y, self.color, self.win)
							self.particle_group.add(particle)

						self.player_alive = False
						self.end_game()
						print("false")
						self.dead_fx.play()
						#print("score",self.score)
						self.collided_rectangles = False

				self.current_time = pygame.time.get_ticks()
				self.delta = self.current_time - self.start_time

				# self.generator.generator(self.dt)
				# self.generator.move(self.color)
				if self.coin_delta < self.delta < self.coin_delta + 100 and self.new_coin and len(self.coin_group)==0:
					self.y = random.randint(self.CENTER[1] - self.RADIUS, self.CENTER[1] + self.RADIUS)
					self.coin = Coins(self.y, self.win)
					self.coin_group.add(self.coin)
					self.new_coin = False
					# self.end_game()

				if self.current_time - self.start_time >= self.tile_delta and len(self.tile_group)==0:
					self.y = random.choice([self.CENTER[1] - 80, self.CENTER[1], self.CENTER[1] + 80])
					self.type_ = random.randint(1, 3)
					self.tile = Tiles(self.y, self.type_, self.win)
					self.tile_group.add(self.tile)


					self.start_time = self.current_time
					self.new_coin = True



				# if any(tile.x < 32 for tile in self.tile_group):
					# self.end_game()


				tiles_to_remove = [tile for tile in self.tile_group if tile.x < 31]
				for tile in tiles_to_remove:
					self.tile_group.remove(tile)

				coins_to_remove = [coin for coin in self.coin_group if coin.x < 60]
				for coin in coins_to_remove:
					self.coin_group.remove(coin)




		if not self.player_alive and len(self.particle_group) == 0:
			# self.score_page = True
			self.game_page = False
			print("test")
			#self.score_page_fx.play()

			self.ball_group.empty()
			self.tile_group.empty()
			self.coin_group.empty()

			self.end_game()

	def update_check(self):

		self.update_main()
		self.check_end()

	def render(self):

		self.FPS = 240

		self.win.fill(self.GRAY)


		self.game_page = True


		if self.game_page:
			pygame.draw.circle(self.win, self.BLACK, self.CENTER, 80, 20)
			self.ball_group.update(self.color)
			self.coin_group.update(self.color)
			self.tile_group.update()
			self.score_msg.update(self.score)
			self.particle_group.update()

		self.clock.tick(self.FPS)
		pygame.draw.rect(self.win, self.BLUE, (0, 0, self.WIDTH, self.HEIGHT), 5, border_radius=10)
		pygame.display.update()

	def check_end(self):
		if self.terminated:
			# self.reset()
			pass

	def end_game(self):
		# print("true")
		self.terminated = True
		# time.sleep(2)

	def reset(self):
		if self.terminated or self.score>=1:
			print("reset called")
			balls_to_remove = [ball for ball in self.ball_group]
			for ball in balls_to_remove:
				self.ball_group.remove(ball)
			self.ball.reset()
			#simuler le bouton replay
			self.game_page = True
			self.score = 0
			self.score_msg = Message(self.WIDTH//2, 100, 60,       "0"  , self.score_font, (150, 150, 150), self.win)

			if self.easy_level:

				self.ball = Balls((self.CENTER[0], self.CENTER[1] + self.RADIUS), self.RADIUS, 90, self.win)
				self.ball_group.add(self.ball)
			else:
				self.ball = Balls((self.CENTER[0], self.CENTER[1] + self.RADIUS), self.RADIUS, 90, self.win)
				self.ball_group.add(self.ball)
				self.ball = Balls((self.CENTER[0], self.CENTER[1] - self.RADIUS), self.RADIUS, 270, self.win)
				self.ball_group.add(self.ball)

			self.player_alive = True
			self.terminated = False

	def reset2(self):
		# if self.terminated:
		print("reset2 called")
		balls_to_remove = [ball for ball in self.ball_group]
		for ball in balls_to_remove:
			self.ball_group.remove(ball)
		self.ball.reset()
			#simuler le bouton replay
		self.game_page = True
		self.score = 0
		self.score_msg = Message(self.WIDTH//2, 100, 60,       "0"  , self.score_font, (150, 150, 150), self.win)

		if self.easy_level:
			self.ball = Balls((self.CENTER[0], self.CENTER[1] + self.RADIUS), self.RADIUS, 90, self.win)
			self.ball_group.add(self.ball)
		else:
			self.ball = Balls((self.CENTER[0], self.CENTER[1] + self.RADIUS), self.RADIUS, 90, self.win)
			self.ball_group.add(self.ball)
			self.ball = Balls((self.CENTER[0], self.CENTER[1] - self.RADIUS), self.RADIUS, 270, self.win)
			self.ball_group.add(self.ball)

		self.player_alive = True
		self.terminated = False

		tiles_to_remove = [tile for tile in self.tile_group]
		for tile in tiles_to_remove:
			self.tile_group.remove(tile)

		coins_to_remove = [coin for coin in self.coin_group]
		for coin in coins_to_remove:
			self.coin_group.remove(coin)
if __name__ == "__main__":
	game = Game()
	game.run()