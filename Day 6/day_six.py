"""Advent of Code 2022 Day 6"""

from time import perf_counter

from day_six_input import PUZZLE_INPUT


def find_start(buffer: str, length: int):
    start = 0
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


def is_substring_unique(buffer: str, start: int, end: int) -> bool:
    """Return True if substring buffer[start:end] containst unique characters"""
    return len(set(buffer[start:end])) == end - start


def find_start_4(buffer: str, length: int):
    for end in range(length, len(buffer)):
        if is_substring_unique(buffer, end - length, end):
            break
    return end


def next_unique_start_point(buffer: str):
    """Returns pointer to location from which all characters are unique"""
    for pointer in reversed(range(len(buffer))):
        if not is_substring_unique(buffer, pointer, len(buffer)):
            break
    return pointer + 1


def find_start_scalable(buffer: str, length: int):
    """Scablable start finding for use with very large input buffer streams"""
    pointer = length
    while not is_substring_unique(buffer, pointer - length, pointer):
        pointer += next_unique_start_point(buffer[pointer - length : pointer])
    return pointer


print(find_start_scalable(PUZZLE_INPUT, 20))
print(find_start_scalable(PUZZLE_INPUT, 14))

lots_of_as = "".join("aaaaaaaaaaa" for i in range(10_000_000))

start = perf_counter()
print(find_start_scalable(lots_of_as + PUZZLE_INPUT, 20))
end = perf_counter()
print(f"Solution found in {end-start} seconds")

start = perf_counter()
print(find_start(lots_of_as + PUZZLE_INPUT, 20))
end = perf_counter()
print(f"Solution found in {end-start} seconds")
