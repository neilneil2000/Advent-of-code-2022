from day_eleven_input import EXAMPLE_INPUT, PUZZLE_INPUT

class InputProcessor:
    """Class to process Monkey description files"""

    items = None
    operation = None
    test = None
    true_monkey=None
    false_monkey=None

    @classmethod
    def process(cls,monkey_details:str):
        """
        Process Multiline string representing one monkey into tuple for later processing
        
        EXAMPLE
        =======
        Monkey 0:
          Starting items: 79, 98
          Operation: new = old * 19
          Test: divisible by 23
            If true: throw to monkey 2
            If false: throw to monkey 3
        """
        _,cls.items,cls.operation,cls.test,cls.true_monkey,cls.false_monkey = monkey_details.splitlines()
        
        cls.process_items()
        cls.process_operation()
        cls.process_test()
        cls.process_true_monkey()
        cls.process_false_monkey()
        return(cls.items, cls.operation, cls.test, cls.true_monkey, cls.false_monkey)

    @classmethod
    def process_items(cls):
        items = cls.items.split(':')[1]
        cls.items = list(map(int, items.split(', ')))

    @classmethod
    def process_operation(cls):
        operation = cls.operation.split(':')[1]
        _,_,_,operation, operand = operation.split()
        cls.operation = (operation, operand)

    @classmethod
    def process_test(cls):
        cls.test = int(cls.test.split()[-1])

    @classmethod
    def process_true_monkey(cls):
        cls.true_monkey = int(cls.true_monkey.split()[-1])

    @classmethod
    def process_false_monkey(cls):
        cls.false_monkey = int(cls.false_monkey.split()[-1])




class Monkey:
    """Representation of Monkey with items from backpack"""

    def __init__(
        self,
        starting_items: list,
        operation: list,
        test_divisor: int,
        true_monkey: int,
        false_monkey: int,
    ):
        self.items = starting_items
        self.inspection_operation = operation
        self.test_divisor = test_divisor
        self.true_monkey = true_monkey
        self.false_monkey = false_monkey
        self.items_inspected = 0

    def inspect(self):
        """Monkey inspects object and applies inspection operation"""
        self.items_inspected+=1
        operation, operand = self.inspection_operation
        if operand == "old":
            operand = self.items[0]
        match operation:
            case '*':
                self.items[0] *= int(operand)
            case '+':
                self.items[0] += int(operand)


    def bored(self):
        """Monkey gets bored of object and reduce object worry level"""
        self.items[0] = self.items[0] //3

    def next_monkey(self) -> int:
        """Returns number of monkey to pass to"""
        if self.items[0] % self.test_divisor:
            return self.false_monkey
        return self.true_monkey

    def process_items(self) -> list:
        """Process all items currently in possession of monkey"""
        items_to_throw = []
        for _ in self.items.copy():
            self.inspect()
            self.bored()
            next_monkey = self.next_monkey()
            items_to_throw.append((self.items.pop(0), next_monkey))

        return items_to_throw

    def receive_item(self, item:int):
        """Receive and item and add to item list"""
        self.items.append(item)



class CleverMonkey(Monkey):
    """Monkey that has a clever way of tracking large numbers"""

    def __init__(
        self,
        starting_items: list,
        operation: list,
        test_divisor: int,
        true_monkey: int,
        false_monkey: int,
    ):
        super().__init__(starting_items,
        operation,
        test_divisor,
        true_monkey,
        false_monkey)
        for index,item in enumerate(self.items.copy()):
            self.items[index]= self.convert_item_to_distances(item)

    def convert_item_to_distances(self, item):
        """For each object calculate the additional number before it becomes divisible"""
        return_dict = {}
        monkey_divisors = [13,19,11,17,3,7,5,2]
        #monkey_divisors = [23,19,13,17]
        for divisor in monkey_divisors:
            return_dict[divisor] = divisor -(item % divisor)
        return return_dict

    def next_monkey(self) -> int:
        """Returns number of monkey to pass to"""
        if self.items[0][self.test_divisor] % self.test_divisor:
            return self.false_monkey
        return self.true_monkey

    def bored(self):
        pass

    def inspect(self):
        """Monkey inspects object and applies inspection operation"""
        self.items_inspected+=1
        operation, operand = self.inspection_operation
        if operand == "old":
            for divisor in self.items[0]:
                squared = (divisor-self.items[0][divisor])**2
                self.items[0][divisor]=divisor-(squared % divisor)
            return
            
        match operation:
            case '*':
                for divisor in self.items[0]:
                    self.items[0][divisor]=(self.items[0][divisor]*int(operand))%divisor
                    
            case '+':
                for divisor in self.items[0]:
                    self.items[0][divisor] = self.items[0][divisor]-int(operand)



class MonkeyBusiness:
    """Class to handle overall monkey behaviour and transfer of items between monkeys"""

    def __init__(self):
        self.__monkeys = []

    def add_monkey(self, monkey: Monkey):
        """Add a monkey"""
        self.__monkeys.append(monkey)

    def play_round(self):
        """Execute a single round of passing"""
        for monkey in self.__monkeys:
            items_to_assign = monkey.process_items()
            self.reassign_items(items_to_assign)

    def reassign_items(self,items_to_assign:list):
        """Assign items to new monkeys"""
        for value, monkey_id in items_to_assign:
            self.__monkeys[monkey_id].receive_item(value)

    @property
    def monkey_business_level(self):
        """Calculate level of monkey business"""
        monkey_levels = [monkey.items_inspected for monkey in self.__monkeys]
        monkey_levels.sort()
        return monkey_levels[-1]*monkey_levels[-2]


def main():  # pylint:disable=missing-function-docstring
    NUMBER_OF_ROUNDS_PART1 = 20
    NUMBER_OF_ROUNDS_PART2 = 10_000

    puzzle_input = PUZZLE_INPUT.split("\n\n")
    

    monkey_puzzle = MonkeyBusiness()
    # Build Monkeys and add them to monkey_puzzle
    for monkey in puzzle_input:
        monkey_puzzle.add_monkey(Monkey(*InputProcessor.process(monkey)))

    for _ in range(NUMBER_OF_ROUNDS_PART1):
        monkey_puzzle.play_round()

    print(monkey_puzzle.monkey_business_level)

    monkey_puzzle = MonkeyBusiness()
    for monkey in puzzle_input:
        monkey_puzzle.add_monkey(CleverMonkey(*InputProcessor.process(monkey)))

    for _ in range(NUMBER_OF_ROUNDS_PART2):
        monkey_puzzle.play_round()

    print(monkey_puzzle.monkey_business_level)


if __name__ == "__main__":
    main()
