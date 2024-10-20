def descending_order(num):
    sorted_digits = sorted(str(num), reverse=True)
    return int(''.join(sorted_digits))
