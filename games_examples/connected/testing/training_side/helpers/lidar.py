
import math

from games_examples.connected.testing.training_side.helpers.sight_line import SightLineFirst


class Lidar:

    def __init__(self, pipes, ball):
        self.pipes = pipes
        self.ball = ball
        self.sight_lines = [
            SightLineFirst(self.ball, math.pi / 6),
            SightLineFirst(self.ball, - math.pi / 6),
            SightLineFirst(self.ball, math.pi / 4),
            SightLineFirst(self.ball, - math.pi / 4),
            SightLineFirst(self.ball, math.pi / 12),
            SightLineFirst(self.ball, -math.pi / 12),
            SightLineFirst(self.ball, 0),
        ]

    def vision(self):
        for line in self.sight_lines:
            line.vision(self.pipes)

    def reset(self):
        for line in self.sight_lines:
            line.reset()

