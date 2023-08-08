from copy import copy

from games_examples.super_mario.entities.EntityBase import EntityBase
from games_examples.super_mario.entities.Item import Item


class CoinBrick(EntityBase):
    def __init__(self, screen, spriteCollection, x, y, dashboard, gravity=0):
        super(CoinBrick, self).__init__(x, y, gravity)
        self.screen = screen
        self.spriteCollection = spriteCollection
        self.image = self.spriteCollection.get("bricks").image
        self.type = "Block"
        self.triggered = False
        self.dashboard = dashboard
        self.item = Item(spriteCollection, screen, self.rect.x, self.rect.y)

    def update(self, cam, dt):
        self.move_counter += dt
        if self.move_counter >= self.SPPED_ENTITY:
            if not self.alive or self.triggered:
                self.image = self.spriteCollection.get("empty").image
                self.item.spawnCoin(cam, self.dashboard)
            self.screen.blit(
                self.spriteCollection.get("sky").image,
                (self.rect.x + cam.x, self.rect.y + 2),
            )
            self.screen.blit(self.image, (self.rect.x + cam.x, self.rect.y - 1))
            self.move_counter = 0
