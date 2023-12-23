import re

words = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9}


def words_replaced(s: str) -> str:
  buffer = ''
  new_s = ''

  for c in s:
    buffer += c

    for w in words.keys():
      if buffer.endswith(w):
        new_s += buffer.replace(w, str(words[w]))
        buffer = c

  new_s += buffer
  return new_s


def calibration_value(s: str) -> int:
  print(f"initial: {s}")
  replaced = words_replaced(s)
  print(f"replaced: {replaced}")
  digits = re.findall("\d", replaced)
  return int(''.join([digits[0], digits[-1]]))


def calibration_value_v2(s: str) -> int:
  pattern = re.compile(r'\d|one|two|three|four|five|six|seven|eight|nine')
  digits = [words[d] if d in words else int(d) for d in re.findall(pattern, s)]
  return int(''.join([str(digits[0]), str(digits[-1])]))


def main():
  lines = [l.strip() for l in open('../input/day_01.txt').readlines()]

  total = 0

  for l in lines:
    v = calibration_value(l)
    total += v

  print(total)

if __name__ == '__main__':
  main()
