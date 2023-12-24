import re


def hash_step(c: str, current: int) -> int:
    current += ord(c)
    current *= 17
    return current % 256


def hash(s: str) -> int:
    current = 0
    for c in s:
        current = hash_step(c, current)
    return current


def main():
    with open('input/day_15.txt') as f:
        steps = f.read().strip().split(',')

    step_pattern = re.compile(r'^([a-z]+)(-|=(\d+)?)$')

    boxes = []
    for _ in range(256):
        boxes.append([])

    # run operations
    for step in steps:
        match = step_pattern.match(step)
        step_label = match.group(1)
        box_index = hash(step_label)

        if match.group(2) == '-':
            boxes[box_index] = [(label, focus) for (label, focus) in boxes[box_index] if label != step_label]
        else:
            focus = int(match.group(3))
            label_index = next((i for i, v in enumerate(boxes[box_index]) if v[0] == step_label), None)
            if label_index is not None:
                boxes[box_index][label_index] = (step_label, focus)
            else:
                boxes[box_index].append((step_label, focus))

    # compute focus power
    total = 0
    for box_number, box in enumerate(boxes):
        for lens_index, (_label, focus) in enumerate(box):
            total += (box_number + 1) * (lens_index + 1) * focus

    print("Day 15 part 2:", total)


if __name__ == '__main__':
    main()
