# Licensed to the public domain
# by anatoly techtonik <techtonik@gmail.com>

import os
import sys
import tempfile
import time

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
# this returns immediately leaving child process
# executed in background
#p = AsyncPopen(cmd)
p = AsyncPopen(cmd, stdout=PIPE)

counter = 0
while p.poll() is None:
  time.sleep(0.001) # sleep to avoid 100% CPU load
  counter += 1
  out, err = p.communicate()
  if out:
    print("Got '%s' on %dth iteration." % (out.strip(), counter))

# there is no cleanup, because os.remove() fires up
# faster than Python from Popen() gets to the script
# file
os.remove(abspath)
