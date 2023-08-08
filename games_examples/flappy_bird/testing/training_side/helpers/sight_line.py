import math
from abc import abstractmethod, ABC

from games_examples.flappy_bird.params import HEIGHT, WIDTH


def line_rect_intersection(line_start, line_end, rect):

    # Find the four corners of the rectangle
    corners = [(rect[0], rect[1]), (rect[2], rect[1]),
               (rect[2], rect[3]), (rect[0], rect[3])]

    intersections = []
    for i in range(4):
        # Find the intersection point of the line and the current edge of the rectangle
        x1, y1 = corners[i]
        x2, y2 = corners[(i + 1) % 4]
        x3, y3 = line_start
        x4, y4 = line_end

        if x2 - x1 == 0:  # Edge is vertical
            x_intersect = x1
            m = (y4 - y3) / (x4 - x3)
            b = y3 - m * x3
            y_intersect = m * x_intersect + b
        elif y2 - y1 == 0:  # Edge is horizontal
            y_intersect = y1
            m = (y4 - y3) / (x4 - x3)
            b = y3 - m * x3
            if m != 0:
                x_intersect = (y_intersect - b) / m
            else:
                x_intersect = float('inf')
        else:
            m1 = (y2 - y1) / (x2 - x1)
            b1 = y1 - m1 * x1
            m2 = (y4 - y3) / (x4 - x3)
            b2 = y3 - m2 * x3
            x_intersect = (b2 - b1) / (m1 - m2)
            y_intersect = m1 * x_intersect + b1

        # Check if the intersection point is on the line segment and within the rectangle
        if (min(x1, x2) <= x_intersect <= max(x1, x2) and
                min(y1, y2) <= y_intersect <= max(y1, y2) and
                min(x3, x4) <= x_intersect <= max(x3, x4) and
                min(y3, y4) <= y_intersect <= max(y3, y4)):
            intersections.append((x_intersect, y_intersect))

    return intersections


class SightLine:

    @abstractmethod
    def color(self):
        pass

    def __init__(self, bird, angle):
        self.bird = bird
        self.angle = angle
        self.max_length = 2000
        self.distance = 2000

    # Use to compute the new intersection
    def end_virtual_position(self):
        x, y = self.bird.center
        end_x = x + self.max_length * math.cos(self.angle)
        end_y = y + self.max_length * math.sin(self.angle)
        return end_x, end_y

    # Use to get the actual distance
    def end_position(self):
        x, y = self.bird.center
        end_x = x + self.distance * math.cos(self.angle)
        end_y = y + self.distance * math.sin(self.angle)
        return end_x, end_y

    def check_collision_pipe(self, pipe):

        intersections = []
        intersections.extend(line_rect_intersection(self.bird.center, self.end_virtual_position(), tuple(pipe.rect1)))
        intersections.extend(line_rect_intersection(self.bird.center, self.end_virtual_position(), tuple(pipe.rect2)))

        x_player, y_player = self.bird.center

        distance = 2000  # TODO remove magic number
        if intersections is not None:
            # For every intersections we keep the min distance
            for (x, y) in intersections:
                d = math.sqrt((x_player - x) ** 2 + (y_player - y) ** 2)
                if d < distance:
                    distance = d

        return distance

    @abstractmethod
    def vision(self, pipes):
        pass

    def check_collision_ground(self):
        x_player, y_player = self.bird.center

        intersections = line_rect_intersection(self.bird.center, self.end_virtual_position(), (0, HEIGHT, WIDTH, 10))

        distance = 2000  # TODO remove magic number
        if intersections is not None:
            # For every intersections we keep the min distance
            for (x, y) in intersections:
                d = math.sqrt((x_player - x) ** 2 + (y_player - y) ** 2)
                if d < distance:
                    distance = d

        return distance

    def check_collision_sky(self):
        x_player, y_player = self.bird.center

        intersections = line_rect_intersection(self.bird.center, self.end_virtual_position(), (0, -10, WIDTH, 10))

        distance = 2000  # TODO remove magic number
        if intersections is not None:
            # For every intersections we keep the min distance
            for (x, y) in intersections:
                d = math.sqrt((x_player - x) ** 2 + (y_player - y) ** 2)
                if d < distance:
                    distance = d

        return distance

    def reset(self):
        self.max_length = 2000
        self.distance = 2000


class SightLineFirst(SightLine, ABC):
    def vision(self, pipes):
        distances = []
        # We compute distances between the line and every pipe
        for pipe in pipes.pipes:
            distances.append(self.check_collision_pipe(pipe))
        distances.append(self.check_collision_ground())
        distances.append(self.check_collision_sky())
        # We keep the min
        if distances:
            self.distance = min(distances)

    def color(self):
        return "red"

