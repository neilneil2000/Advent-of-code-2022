import json

from day_thirteen_input import EXAMPLE_INPUT, PUZZLE_INPUT


def are_both_ints(item_1, item_2):
    """Returns True if both items are integers"""
    return isinstance(item_1, int) and isinstance(item_2, int)


def handle_ints(item_1, item_2):
    """Returns True if ints are in the right order"""
    if item_1 < item_2:
        return True
    if item_1 > item_2:
        return False
    return None


def are_both_lists(item_1, item_2):
    """Returns True if both items are lists"""
    return isinstance(item_1, list) and isinstance(item_2, list)


def handle_lists(item_1, item_2):
    """Returns True if ints are in the right order"""
    for sub_item_1, sub_item_2 in zip(item_1, item_2):
        result = compare_items(sub_item_1, sub_item_2)
        if result is not None:
            return result
    if len(item_1) < len(item_2):
        return True
    if len(item_1) > len(item_2):
        return False
    return None


def compare_items(item_1, item_2):
    """Return True if items are in the correct order"""
    if are_both_ints(item_1, item_2):
        return handle_ints(item_1, item_2)

    if are_both_lists(item_1, item_2):
        return handle_lists(item_1, item_2)

    if isinstance(item_1, int):
        item_1 = [item_1]
    else:
        item_2 = [item_2]
    return handle_lists(item_1, item_2)


def get_correct_position(item, sorted_list) -> int:
    """Returns index of position in sorted_list that item should be inserted"""
    for index, _ in enumerate(sorted_list):
        if compare_items(item, sorted_list[index]):
            return index

    return len(sorted_list)


def place_item_in_list(item, sorted_list: list):
    """Places item in correct position in list"""
    sorted_list.insert(get_correct_position(item, sorted_list), item)
    return sorted_list


def sort_list(items: list):
    sorted_list = [items.pop(0)]
    while len(items) > 0:
        sorted_list = place_item_in_list(items.pop(0), sorted_list)
    return sorted_list


def main():  # pylint:disable=missing-function-docstring
    pairs = EXAMPLE_INPUT.split("\n\n")
    results = []
    for pair in pairs:
        left, right = pair.splitlines()
        left = json.loads(left)
        right = json.loads(right)
        outcome = compare_items(left, right)
        print(f"{left} vs {right} : {outcome}")
        results.append(outcome)
    total = 0
    for index, result in enumerate(results):
        if result:
            total += index + 1
    print(total)

    packets = []
    for line in PUZZLE_INPUT.splitlines():
        if line:
            packets.append(json.loads(line))
    DIVIDER_1 = [[2]]
    DIVIDER_2 = [[6]]
    packets.append(DIVIDER_1)
    packets.append(DIVIDER_2)
    sorted_list = sort_list(packets)
    answer = (sorted_list.index(DIVIDER_1) + 1) * (sorted_list.index(DIVIDER_2) + 1)
    print(answer)


if __name__ == "__main__":
    main()
