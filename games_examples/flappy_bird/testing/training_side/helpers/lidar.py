import math

from games_examples.flappy_bird.testing.training_side.helpers.sight_line import SightLineFirst


class Lidar:

    def __init__(self, pipes, bird):
        self.pipes = pipes
        self.bird = bird
        self.sight_lines = [
            SightLineFirst(self.bird, math.pi / 6),
            SightLineFirst(self.bird, - math.pi / 6),
            SightLineFirst(self.bird, math.pi / 4),
            SightLineFirst(self.bird, - math.pi / 4),
            SightLineFirst(self.bird, math.pi / 12),
            SightLineFirst(self.bird, -math.pi / 12),
            SightLineFirst(self.bird, 0),
        ]

    def vision(self):
        for line in self.sight_lines:
            line.vision(self.pipes)

    def reset(self):
        for line in self.sight_lines:
            line.reset()
