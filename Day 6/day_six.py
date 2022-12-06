"""Advent of Code 2022 Day 6"""

from day_six_input import PUZZLE_INPUT


def find_start(buffer: str):
    start = 0
    length = 14
    while len(set(buffer[start : start + length])) != length:
        start += 1
    return start + length


def find_start_2(buffer: str, length: int):
    for start in range(len(buffer) - length):
        if len(set(buffer[start : start + length])) == length:
            break
    return start + length


def find_start_3(buffer: str, length: int):
    for end in range(length, len(buffer)):
        if len(set(buffer[end - length : end])) == length:
            break
    return end


def is_unique(buffer: str, end: int, length: int) -> bool:
    return len(set(buffer[end - length : end])) == length


def find_start_4(buffer: str, length: int):
    for end in range(length, len(buffer)):
        if is_unique(buffer, end, length):
            break
    return end


print(find_start(PUZZLE_INPUT))
print(find_start_3(PUZZLE_INPUT, 4))
print(find_start_3(PUZZLE_INPUT, 14))
