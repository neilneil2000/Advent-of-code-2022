from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Rock(ABC):
    """
    Representation of a rock
    Co-ordinates of rock pieces use (0,0) as bottom-left most piece
    """

    position: tuple

    @property
    def full_position(self):
        return set((x + self.x_position, y + self.y_position) for x, y in self.shape)

    @property
    def x_position(self):
        return self.position[0]

    @property
    def y_position(self):
        return self.position[1]

    @property
    @abstractmethod
    def shape(self):
        pass

    @property
    def right_edge(self) -> int:
        """Return the furthest right point on the shape"""
        return max(part[0] for part in self.full_position)

    @property
    def left_edge(self) -> int:
        """Return the furthest left point on the shape"""
        return min(part[0] for part in self.full_position)

    @property
    def bottoms(self) -> set:
        """Return set of lowest locations"""
        pos_dict = {}
        for part in self.full_position:
            x, y = part
            if pos_dict.get(x) is None:
                pos_dict[x] = []
            pos_dict[x].append(y)

        return set((key, max(value)) for key, value in pos_dict.items())

    def move_down(self):
        """Moves rock down one position"""
        self.position = (self.x_position, self.y_position - 1)

    def move_left(self):
        """Moves rock left one position if possible"""
        self.position = (self.x_position - 1, self.y_position)

    def move_right(self):
        """Moves rock left one position if possible"""
        self.position = (self.x_position + 1, self.y_position)


@dataclass
class Hero(Rock):
    """
    ####
    """

    name = "Hero"
    shape = {(0, 0), (1, 0), (2, 0), (3, 0)}
    width = 4


@dataclass
class CrossMan(Rock):
    """
    .#.
    ###
    .#.
    """

    name = "CrossMan"
    shape = {(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)}
    width = 3


class BigEll(Rock):
    """
    ..#
    ..#
    ###
    """

    name = "BigEll"
    shape = {(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)}
    width = 3


class TallPaul(Rock):
    """
    #
    #
    #
    #
    """

    name = "TallPaul"
    shape = {(0, 0), (0, 1), (0, 2), (0, 3)}
    width = 1


class Smashboy(Rock):
    """
    ##
    ##
    """

    name = "SmashBoy"
    shape = {(0, 0), (0, 1), (1, 0), (1, 1)}
    width = 2


class RockFactory:

    rocks = [Hero, CrossMan, BigEll, TallPaul, Smashboy]
    pointer = 0

    @classmethod
    def get_next_rock(cls, height: int):
        """Returns next rock in sequence at specfied height"""
        next_rock = cls.rocks[cls.pointer]
        cls.pointer = (cls.pointer + 1) % len(cls.rocks)
        return next_rock((2, height))
