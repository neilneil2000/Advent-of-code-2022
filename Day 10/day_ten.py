"""Advent of Code 2022"""
from day_ten_input import PUZZLE_INPUT

class CRT:
    """
    Representation of a CRT Monitor
    6 lines high
    40 pixels wide
    """

    CRT_HEIGHT = 6
    CRT_WIDTH = 40
    SPRITE_WIDTH = 3

    PIXEL_ON = '#'
    PIXEL_OFF = ' '

    def __init__(self):
        self.pixels=[] #Model pixels as 1D array

    def draw_from_history(self,register_history:list)-> None:
        """Draw screen output from CPU register history"""
        for index, value in enumerate(register_history):
            if self.is_sprite_visible_here(index, value):
                self.pixels.append(self.PIXEL_ON)
            else:
                self.pixels.append(self.PIXEL_OFF)

    def is_sprite_visible_here(self, pixel_index:int, sprite_centre:int)-> bool:
        """Return True if sprite visible at this location"""
        pixel_row_index = pixel_index % self.CRT_WIDTH
        return pixel_row_index-1 <= sprite_centre <= pixel_row_index+1

    def display_screen(self)-> None:
        """Print display to screen"""
        for index, pixel in enumerate(self.pixels):
            if index >= self.CRT_HEIGHT*self.CRT_WIDTH:
                break
            if index>0 and index % self.CRT_WIDTH==0:
                print()
            print(pixel,end="")


class CPU:
    """Representation of a device with a CPU"""
    def __init__(self):
        self.clock_cycles = 0
        self.register_history = [1]

    @property
    def register_value(self):
        """Current value in register"""
        return self.register_history[-1]

    def add_to_register(self, new_register_value:int=0)-> None:
        """Add value to register"""
        self.clock_cycles+=1
        self.register_history.append(new_register_value+self.register_value)

    def do_noop(self)-> None:
        """Execute noop operation"""
        self.add_to_register()

    def do_addx(self,V:int)-> None:
        """Execute addx operation"""
        self.do_noop()
        self.add_to_register(V)

    def run_command(self, command: str)-> None:
        """Run a command"""
        command_name,*command_args = command.split()
        match command_name:
            case 'noop':
                self.do_noop()
            case 'addx':
                self.do_addx(int(command_args[0]))

    @property
    def signal_strength(self) -> int:
        """Calculate Signal strength"""
        return sum(index*self.register_history[index-1] for index in range(20,221,40))


def main(): #pylint:disable=missing-function-docstring
    device = CPU()
    for command in PUZZLE_INPUT.splitlines():
        device.run_command(command)
    print(device.signal_strength)

    screen = CRT()
    screen.draw_from_history(device.register_history)
    screen.display_screen()


if __name__ == "__main__":
    main()
