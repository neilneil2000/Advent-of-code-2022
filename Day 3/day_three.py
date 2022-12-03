"""Solution to Advent of Code Day 3"""

from typing import List

from day_three_input import PUZZLE_INPUT

# Generate Scoring dictionary
SCORING = {
    **{chr(ord("a") + n): n + 1 for n in range(26)},
    **{chr(ord("A") + n): n + 27 for n in range(26)},
}


def score(letter: str) -> int:
    """Return Score for given letter"""
    return SCORING[letter]


def get_common_letter(strings: List[str]) -> str:
    """
    Returns single letter that is common to all strings in input list
    WARNING: If more than one letter is common, which common letter returned is undefined
    """
    common_letters = set(strings[0])
    for string in strings[1:]:
        common_letters.intersection_update(string)
    return common_letters.pop()


def bisect_string(string: str) -> List[str]:
    """Splits string into two equal parts"""
    chunk_length = len(string) // 2
    return [string[:chunk_length], string[chunk_length:]]


def get_packing_priority(rucksack: str) -> str:
    """Return priority for a given rucksack by finding incorrectly packed item"""
    return score(get_common_letter(bisect_string(rucksack)))


def get_group_priority(group):
    """Return priority for group by finding commonly packed item"""
    return score(get_common_letter(group))


def elf_groups(elves_per_group=3) -> List[str]:
    """Return List of groups of elves"""
    elves = PUZZLE_INPUT.splitlines()
    return [
        elves[n : n + elves_per_group] for n in range(0, len(elves), elves_per_group)
    ]


def main():  # pylint:disable=missing-function-docstring
    total_priority = 0
    for rucksack in elf_groups(1)[0]:
        total_priority += get_packing_priority(rucksack)
    print(total_priority)

    total_priority = 0
    for group in elf_groups():
        total_priority += get_group_priority(group)
    print(total_priority)


if __name__ == "__main__":
    main()
