# Example using untrusted.string and static type checking

# > mypy unsafe-made-safe.py
# unsafe-made-safe.py:10: error: Argument 1 to "write" of "IO" has incompatible type "String"; expected "str"

# > python3 unsafe-made-safe.py
# Enter any string?
# <script>alert("hack");</script>
# Traceback (most recent call last):
#   File "unsafe-made-safe.py", line 10, in <module>
#     sys.stdout.write("You wrote: <b>"+s+"</b>\n") # <- possibility of HTML injection
# TypeError: must be str, not String



import html
import untrusted
import sys

sys.stdout.write('Enter any string?\n')
s = untrusted.string(sys.stdin.readline().strip())
sys.stdout.write("You wrote: <b>"+s+"</b>\n") # <- possibility of HTML injection


# print(s) would raise a Runtime error,
# but is not detected statically by mypy.
# Thus, we use the typed sys.stdout.write(str).


