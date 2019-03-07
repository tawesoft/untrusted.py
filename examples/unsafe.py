# Example without using untrusted.string and static type checking

# > mypy unsafe-example`
# (no output)

# > python3 unsafe.py
# Enter any string?
# <script>alert("hack");</script>
# You wrote: <b><script>alert("hack");</script></b>

import sys

print('Enter any string?')
s = sys.stdin.readline().strip()
print("You wrote: <b>" + s + "</b>") # <- possibility of HTML injection



