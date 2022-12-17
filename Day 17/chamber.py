from rocks import RockFactory, Rock


class Chamber:
    """Representation of a narrow chamber with rocks falling"""

    new_spawn_height = 3

    def __init__(self, factory: RockFactory, width: int, jets: str):
        self.factory = factory
        self.width = width
        self.jets = jets
        self.jet_pointer = 0
        self.current_block: Rock = None
        self.landed = False
        self.floor = [1 for _ in range(width)]
        self.blocked_spaces = {(x, 0) for x in range(width)}

    @property
    def landing_zone(self):
        """Defines the landing zone for the rocks"""
        return set((x, y) for x, y in enumerate(self.floor))

    @property
    def floor_height(self):
        """Returns height of first clear row"""
        return max(self.floor)

    def next_jet(self):
        """Next jet in sequence"""
        jet = self.jets[self.jet_pointer]
        self.jet_pointer = (self.jet_pointer + 1) % len(self.jets)
        return jet

    def apply_jet(self):
        """Applies Impact of Jet to Block"""
        match self.next_jet():
            case "<":
                self.move_left()
            case ">":
                self.move_right()
            case _:
                raise ValueError("Invalid Jet")

    def move_left(self):
        """Attempt to move block left"""
        if self.current_block.left_edge == 0:
            return
        if self.is_blocked_left():
            return
        self.current_block.move_left()

    def move_right(self):
        """Attempt to move block right"""
        if self.current_block.right_edge == self.width - 1:
            return
        if self.is_blocked_right():
            return
        self.current_block.move_right()

    def is_blocked_left(self):
        new_position = set((x - 1, y) for x, y in self.current_block.full_position)
        for block_part in new_position:
            if block_part in self.blocked_spaces:
                return True
        return False

    def is_blocked_right(self):
        new_position = set((x + 1, y) for x, y in self.current_block.full_position)
        for block_part in new_position:
            if block_part in self.blocked_spaces:
                return True
        return False

    def is_blocked_down(self):
        new_position = set((x, y - 1) for x, y in self.current_block.full_position)
        for block_part in new_position:
            if block_part in self.blocked_spaces:
                return True
        return False

    def is_blocked_down_old(self):
        """Returns True if path down is blocked"""
        for block_part in self.current_block.full_position:
            if block_part in self.landing_zone:
                return True
        return False

    def move_down(self):
        """Attempt to move block down"""
        if self.is_blocked_down():
            self.landed = True
            self.update_landing_zone()
            return
        self.current_block.move_down()

    def update_landing_zone(self):
        """Update floor with landed block"""
        self.blocked_spaces.update(self.current_block.full_position)
        for x, y in self.current_block.full_position:
            if y >= self.floor[x]:
                self.floor[x] = y + 1
        pass

    def spawn_block(self):
        """Spawn a new block"""
        self.current_block = self.factory.get_next_rock(
            self.floor_height + self.new_spawn_height
        )
        self.landed = False

    def do_block_cycle(self):
        self.spawn_block()
        while not self.landed:
            self.apply_jet()
            self.move_down()
