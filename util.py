


def format_igt(i):
    parts = []
    while i > 0:
        parts.append(str(i % 60).zfill(2))
        i //= 60
    return ":".join(parts[::-1])
