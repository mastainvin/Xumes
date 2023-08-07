import pygame
from pygame.locals import *
import sys


class Input:
    def __init__(self, entity):
        self.mouseX = 0
        self.mouseY = 0
        self.entity = entity

    def checkForInput(self):
        events = pygame.event.get()
        self.checkForKeyboardInput(events)
        self.checkForMouseInput(events)
        self.checkForQuitAndRestartInputEvents(events)

    def checkForKeyboardInput(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT or event.key == pygame.K_h and not event.key == pygame.K_RIGHT:
                    self.entity.traits["goTrait"].direction = -1
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_l and not event.key == pygame.K_LEFT:
                    self.entity.traits["goTrait"].direction = 1
                else:
                    self.entity.traits['goTrait'].direction = 0

                isJumping = event.key == pygame.K_SPACE or event.key == pygame.K_k or event.key == pygame.K_UP
                self.entity.traits['jumpTrait'].jump(isJumping)

                self.entity.traits['goTrait'].boost = pygame.K_LSHIFT

    def checkForMouseInput(self, events):
        mouseX, mouseY = pygame.mouse.get_pos()
        if self.isRightMouseButtonPressed(events):
            self.entity.levelObj.addKoopa(
                mouseY / 32, mouseX / 32 - self.entity.camera.pos.x
            )
            self.entity.levelObj.addGoomba(
                mouseY / 32, mouseX / 32 - self.entity.camera.pos.x
            )
            self.entity.levelObj.addRedMushroom(
                mouseY / 32, mouseX / 32 - self.entity.camera.pos.x
            )
        if self.isLeftMouseButtonPressed(events):
            self.entity.levelObj.addCoin(
                mouseX / 32 - self.entity.camera.pos.x, mouseY / 32
            )

    def checkForQuitAndRestartInputEvents(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and \
                (event.key == pygame.K_ESCAPE or event.key == pygame.K_F5):
                self.entity.pause = True
                self.entity.pauseObj.createBackgroundBlur()

    def isLeftMouseButtonPressed(self, events):
        return self.checkMouse(events, 1)

    def isRightMouseButtonPressed(self, events):
        return self.checkMouse(events, 3)

    def checkMouse(self, events, button):
        for e in events:
            if e.type == pygame.MOUSEBUTTONUP and e.button == button:
                return True
        return False
