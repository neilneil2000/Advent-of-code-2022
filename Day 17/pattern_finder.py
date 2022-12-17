def is_increment_consistent(step, offset, values):
    """Returns True if 3 steps in a row have the same increment"""
    increments = set()

    prev = values[offset]
    for index in range(offset + step, len(values), step):
        increments.add(prev - values[index])
        prev = values[index]

    if len(increments) == 1:
        return increments
    return 0


def find_pattern(values, target=1_000_000_000_000):
    for step in range(5, len(values) // 4):
        for offset in range(step):
            increment = is_increment_consistent(step, offset, values)
            if increment:

                # len(values)-1-offset is the completed block number that has the pattern in it
                block_number = len(values) - 1 - offset
                if (target - block_number) % step == 0:
                    print(f"Useable Pattern found for step:{step} at offset:{offset}")
                    print(
                        f"Additional {(target-block_number)//step} iterations required"
                    )
                    print(f"Increment is {increment}")
