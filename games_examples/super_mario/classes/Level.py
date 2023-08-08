import json
import os

import pygame

from games_examples.super_mario.classes.Sprites import Sprites
from games_examples.super_mario.classes.Tile import Tile
from games_examples.super_mario.entities.Coin import Coin
from games_examples.super_mario.entities.CoinBrick import CoinBrick
from games_examples.super_mario.entities.Goomba import Goomba
from games_examples.super_mario.entities.Mushroom import RedMushroom
from games_examples.super_mario.entities.Koopa import Koopa
from games_examples.super_mario.entities.CoinBox import CoinBox
from games_examples.super_mario.entities.RandomBox import RandomBox

current_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
level_path = os.path.join(current_directory, 'levels')

nb_entites = 0

class Level:
    def __init__(self, screen, dashboard, levelname, feature):
        self.sprites = Sprites()
        self.feature = feature
        self.dashboard = dashboard
        self.screen = screen
        self.level = None
        self.levelLength = 0
        self.entityList = []
        self.nb_entities = 0
        self.loadLevel(levelname, self.feature)


    def loadLevel(self, levelname, feature):
        file = os.path.join(level_path, '{}.json')
        with open(file.format(levelname)) as jsonData:
            data = json.load(jsonData)
            self.loadLayers(data)
            self.loadObjects(data)
            self.loadEntities(data)
            self.levelLength = data["length"]
            self.nb_entites = len(self.entityList)



    def loadEntities(self, data):
        try:
            [self.addCoinBox(x, y) for x, y in data["level"]["entities"]["CoinBox"]]
            if self.feature is not None:
                if self.feature[0] == "ennemies" or self.feature[0] == "balance":
                    if len(data["level"]["entities"][self.feature[1]]["Koopa"]) == 0:
                        [self.addGoomba(x, y) for x, y in data["level"]["entities"][self.feature[1]]["Goomba"]]
                    elif len(data["level"]["entities"][self.feature[1]]["Goomba"]) == 0:
                        [self.addKoopa(x, y) for x, y in data["level"]["entities"][self.feature[1]]["Koopa"]]
                    elif len(data["level"]["entities"][self.feature[1]]["Goomba"]) != 0 and len(data["level"]["entities"][self.feature[1]]["Koopa"]) != 0 :
                        [self.addGoomba(x, y) for x, y in data["level"]["entities"][self.feature[1]]["Goomba"]]
                        [self.addKoopa(x, y) for x, y in data["level"]["entities"][self.feature[1]]["Koopa"]]
            else:
                #print("$$$$$$$$$$$$$$$$$$$$$$$ Je passe pas par feature $$$$$$$$$$$$$$$$$$$$$$$")
                [self.addGoomba(x, y) for x, y in data["level"]["entities"]["Goomba"]]
                [self.addKoopa(x, y) for x, y in data["level"]["entities"]["Koopa"]]
            [self.addCoin(x, y) for x, y in data["level"]["entities"]["coin"]]
            [self.addCoinBrick(x, y) for x, y in data["level"]["entities"]["coinBrick"]]
            [self.addRandomBox(x, y, item) for x, y, item in data["level"]["entities"]["RandomBox"]]
        except:
            # if no entities in Level
            pass

    def loadLayers(self, data):
        layers = []
        for x in range(*data["level"]["layers"]["sky"]["x"]):
            layers.append(
                (
                        [
                            Tile(self.sprites.spriteCollection.get("sky"), None)
                            for y in range(*data["level"]["layers"]["sky"]["y"])
                        ]
                        + [
                            Tile(
                                self.sprites.spriteCollection.get("ground"),
                                pygame.Rect(x * 32, (y - 1) * 32, 32, 32),
                            )
                            for y in range(*data["level"]["layers"]["ground"]["y"])
                        ]
                )
            )
        self.level = list(map(list, zip(*layers)))

    def loadObjects(self, data):
        for x, y in data["level"]["objects"]["bush"]:
            self.addBushSprite(x, y)
        for x, y in data["level"]["objects"]["cloud"]:
            self.addCloudSprite(x, y)
        if self.feature is not None and (self.feature[0] == "jump" or self.feature[0] == "balance"):
            for x, y, z in data["level"]["objects"]["pipe"][self.feature[1]]:
                self.addPipeSprite(x, y, z)
        elif len(data["level"]["objects"]["pipe"]) != 0:
            for x, y, z in data["level"]["objects"]["pipe"]:
                self.addPipeSprite(x, y, z)
        if self.feature is not None and self.feature[0] == "balance":
            for x, y in data["level"]["objects"]["sky"][self.feature[1]]:
                self.level[y][x] = Tile(self.sprites.spriteCollection.get("sky"), None)
        else:
            for x, y in data["level"]["objects"]["sky"]:
                self.level[y][x] = Tile(self.sprites.spriteCollection.get("sky"), None)
        for x, y in data["level"]["objects"]["ground"]:
            self.level[y][x] = Tile(
                self.sprites.spriteCollection.get("ground"),
                pygame.Rect(x * 32, y * 32, 32, 32),
            )

    def updateEntities(self, cam, dt):
        for entity in self.entityList:
            entity.update(cam, dt)
            if entity.alive is None:
                self.entityList.remove(entity)
                self.nb_entites = len(self.entityList)

    def drawLevel(self, camera, dt):
        try:
            for y in range(0, 15):
                for x in range(0 - int(camera.pos.x + 1), 20 - int(camera.pos.x - 1)):
                    if self.level[y][x].sprite is not None:
                        if self.level[y][x].sprite.redrawBackground:
                            self.screen.blit(
                                self.sprites.spriteCollection.get("sky").image,
                                ((x + camera.pos.x) * 32, y * 32),
                            )
                        self.level[y][x].sprite.drawSprite(
                            x + camera.pos.x, y, self.screen
                        )
            self.updateEntities(camera, dt)
        except IndexError:
            return

    def addCloudSprite(self, x, y):
        try:
            for yOff in range(0, 2):
                for xOff in range(0, 3):
                    self.level[y + yOff][x + xOff] = Tile(
                        self.sprites.spriteCollection.get("cloud{}_{}".format(yOff + 1, xOff + 1)), None, )
        except IndexError:
            return

    def addPipeSprite(self, x, y, length=8):
        try:
            # add pipe head
            self.level[y][x] = Tile(
                self.sprites.spriteCollection.get("pipeL"),
                pygame.Rect(x * 32, y * 32, 32, 32),
            )
            self.level[y][x + 1] = Tile(
                self.sprites.spriteCollection.get("pipeR"),
                pygame.Rect((x + 1) * 32, y * 32, 32, 32),
            )
            # add pipe body
            for i in range(1, length + 20):
                self.level[y + i][x] = Tile(
                    self.sprites.spriteCollection.get("pipe2L"),
                    pygame.Rect(x * 32, (y + i) * 32, 32, 32),
                )
                self.level[y + i][x + 1] = Tile(
                    self.sprites.spriteCollection.get("pipe2R"),
                    pygame.Rect((x + 1) * 32, (y + i) * 32, 32, 32),
                )
        except IndexError:
            return

    def addBushSprite(self, x, y):
        try:
            self.level[y][x] = Tile(self.sprites.spriteCollection.get("bush_1"), None)
            self.level[y][x + 1] = Tile(
                self.sprites.spriteCollection.get("bush_2"), None
            )
            self.level[y][x + 2] = Tile(
                self.sprites.spriteCollection.get("bush_3"), None
            )
        except IndexError:
            return

    def addCoinBox(self, x, y):
        self.level[y][x] = Tile(None, pygame.Rect(x * 32, y * 32 - 1, 32, 32))
        self.entityList.append(
            CoinBox(
                self.screen,
                self.sprites.spriteCollection,
                x,
                y,
                self.dashboard,
            )
        )

    def addRandomBox(self, x, y, item):
        self.level[y][x] = Tile(None, pygame.Rect(x * 32, y * 32 - 1, 32, 32))
        self.entityList.append(
            RandomBox(
                self.screen,
                self.sprites.spriteCollection,
                x,
                y,
                item,
                self.dashboard,
                self
            )
        )

    def addCoin(self, x, y):
        self.entityList.append(Coin(self.screen, self.sprites.spriteCollection, x, y))

    def addCoinBrick(self, x, y):
        self.level[y][x] = Tile(None, pygame.Rect(x * 32, y * 32 - 1, 32, 32))
        self.entityList.append(
            CoinBrick(
                self.screen,
                self.sprites.spriteCollection,
                x,
                y,
                self.dashboard
            )
        )

    def addGoomba(self, x, y):
        self.entityList.append(
            Goomba(self.screen, self.sprites.spriteCollection, x, y, self)
        )

    def addKoopa(self, x, y):
        self.entityList.append(
            Koopa(self.screen, self.sprites.spriteCollection, x, y, self)
        )

    def addRedMushroom(self, x, y):
        self.entityList.append(
            RedMushroom(self.screen, self.sprites.spriteCollection, x, y, self)
        )
