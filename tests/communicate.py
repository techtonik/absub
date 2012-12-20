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
The test should not deadlock.

The tricky part for Popen.communicate() here
is to close stdin pipe. If it is left open, the
.readline() in called script will hang waiting
for input.
""")


longscript = """\
import os
import sys

sys.stdout.write('stdout stuff\\n')
sys.stderr.write('stderr stuff\\n')
sys.stdout.flush()
sys.stderr.flush()

line = sys.stdin.readline()
print(repr(line))
"""
(fd, abspath) = tempfile.mkstemp('.async.py')
os.write(fd, longscript)
os.close(fd)

python = sys.executable
cmd = [python, abspath]


# Popen returns immediately leaving child process
# executed in background
if 0:
    from subprocess import Popen, PIPE
    p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
else:
    from async_subprocess import AsyncPopen, PIPE
    p = AsyncPopen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)

stdout, stderr = p.communicate()
assert p.returncode != None

#print repr(stdout), repr(stderr)
# split helps avoid line end differences when comparing
print repr(stdout.split()), repr(stderr)
assert stdout.split() == ['stdout', 'stuff', "''"]
assert stderr.split() == ['stderr', 'stuff']


# there is no cleanup, because os.remove() fires up
# faster than Python from Popen() gets to the script
# file
os.remove(abspath)


# Missing tests:
# [ ] p = AsyncPopen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
#   [ ] stdout lineends on different platforms after communicate
#     [x] always \r\n on Windows for the script above
#   [ ] stdout return type on Python 3
