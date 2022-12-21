from day_twenty_one_input import EXAMPLE_INPUT, PUZZLE_INPUT


class Monkeys:
    """Class Representing Shouting Monkeys"""

    def __init__(self, numbers: dict):
        self.numbers = numbers

    @staticmethod
    def do_operation(operand_a, operand_b, operation) -> int:
        """Carry out mathematical operation"""
        if operation == "+":
            return operand_a + operand_b
        if operation == "-":
            return operand_a - operand_b
        if operation == "/":
            return operand_a / operand_b
        if operation == "*":
            return operand_a * operand_b

    @staticmethod
    def do_inverse_operation_a(result, operand, operation) -> int:
        """Carry out mathematical operation"""
        if operation == "+":
            return result - operand
        if operation == "-":
            return result + operand
        if operation == "/":
            return result * operand
        if operation == "*":
            return result / operand

    @staticmethod
    def do_inverse_operation_b(result, operand, operation) -> int:
        """Carry out mathematical operation"""
        if operation == "+":
            return result - operand
        if operation == "-":
            return operand - result
        if operation == "/":
            return operand / result
        if operation == "*":
            return result / operand

    def get_number(self, monkey_name: str):
        """Get number represented by monkey_name"""
        number = self.numbers[monkey_name]
        if isinstance(number, int):
            return number
        operand_a, operation, operand_b = number
        operand_a = self.get_number(operand_a)
        operand_b = self.get_number(operand_b)
        return self.do_operation(operand_a, operand_b, operation)

    def get_number_stack(self, monkey_name: str) -> list:
        """Return the stack of operations between root and human"""
        if monkey_name == "root":
            return []
        for key, value in self.numbers.items():
            if value is None:
                continue
            if isinstance(value, int):
                if key == monkey_name and monkey_name != "humn":
                    print(value)
                    return [monkey_name, value]
                continue
            if value[0] == monkey_name:
                stack = self.get_number_stack(key)
                stack.append([monkey_name, self.numbers[monkey_name]])
                return stack
            elif value[2] == monkey_name:
                stack = self.get_number_stack(key)
                stack.append([monkey_name, self.numbers[monkey_name]])
                return stack

    def get_human_number(self) -> int:
        """Calculate and return number human should shout"""
        stack = self.get_number_stack("humn")
        print(stack)
        root_value = self.numbers["root"]
        root_value = {root_value[0], root_value[2]}
        root_value.remove(stack[0][0])
        print(root_value)
        target_value = self.get_number(list(root_value).pop())
        print(target_value)
        for index, value in enumerate(stack):
            monkey_name, process = value
            if monkey_name == "humn":
                break
            operand_a, operation, operand_b = process
            if operand_a == stack[index + 1][0]:
                number = self.get_number(operand_b)
                target_value = self.do_inverse_operation_a(
                    target_value, number, operation
                )
            else:
                number = self.get_number(operand_a)
                target_value = self.do_inverse_operation_b(
                    target_value, number, operation
                )
        print(target_value)
        return target_value


def parse_input(input_string: str) -> list:
    """Parse input"""
    parsed = {}
    for line in input_string.splitlines():
        line = line.split()
        if len(line) == 2:
            parsed[line[0][:-1]] = int(line[1])
            continue
        parsed[line[0][:-1]] = [line[1], line[2], line[3]]
    return parsed


def main():  # pylint:disable=missing-function-docstring
    numbers = parse_input(PUZZLE_INPUT)
    my_monkeys = Monkeys(numbers)
    print(my_monkeys.get_number("root"))
    my_monkeys.numbers["humn"] = None
    print(my_monkeys.get_human_number())


if __name__ == "__main__":
    main()
