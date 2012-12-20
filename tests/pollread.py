# Licensed to the public domain
# by anatoly techtonik <techtonik@gmail.com>

import os
import sys
import tempfile
import time

# add parent dir to module search path
ABSUB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ABSUB)

print("""\
The test should run for 5 seconds, showing
one line per second. If you see all five
lines at once, that means test fails.
""")


longscript = """\
import time
import sys

for x in range(5):
  print(x)
  time.sleep(1)
  # flush() is important when output is redirected
  # otherwise will be no output until buffer is full
  sys.stdout.flush()
"""
(fd, abspath) = tempfile.mkstemp('.async.py')
os.write(fd, longscript)
os.close(fd)

python = sys.executable
cmd = [python, abspath]



from async_subprocess import AsyncPopen, PIPE
# Popen returns immediately leaving child process
# executed in background
p = AsyncPopen(cmd, stdout=PIPE)

counter = 0
while p.poll() is None:
  time.sleep(0.001) # sleep to avoid 100% CPU load
  counter += 1
  out, err = p.asyncomm()
  if out:
    print("Got '%s' on %dth iteration." % (out.strip(), counter))

# there is no cleanup, because os.remove() fires up
# faster than Python from Popen() gets to the script
# file
os.remove(abspath)


# Missing tests:
# [ ] p = AsyncPopen(cmd)
#   [ ] asyncomm() with dead pipes returns (None, None)
# [ ] p = AsyncPopen(cmd, stdout=PIPE)
#   [ ] asyncomm() with one dead pipe returns str, None
#   [ ] asyncomm() with Python 3 returns ???, None
#   [ ] asyncomm() with empty pipe returns '', None
#   [ ] asyncomm() with closed pipe returns None, None
#     [ ] figure out when asyncomm() can be called wuth closed pipe
# [ ] p = AsyncPopen(cmd, stdin=PIPE)
#   [ ] try to guide some process
# [ ] p = AsyncPopen(cmd, stdout=PIPE, stderr=PIPE)
#
