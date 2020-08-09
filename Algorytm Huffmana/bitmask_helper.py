from bitarray import bitarray


def from_bitmask_to_number(mask):
    result = 0
    for bit in mask:
        result *= 2
        if bit:
            result += 1
    return result


def from_number_to_bitmask(number, shift = None):
    result = bitarray()
    while number > 0:
        result.insert(0, number % 2 == 1)
        number = number // 2
    if shift is not None:
        while len(result) < shift:
            result.insert(0, False)
    return result

