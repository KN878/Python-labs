# Python 3.7.4
import time
import sys

src_files = sys.argv[1:]
files_runtime = {}
for src_file in src_files:
    if not str(src_file).endswith('.py'):
        sys.exit("Ti che pes, {} eto ne piton file".format(src_file))
    else:
        start = time.time()
        exec(open(src_file).read())
        files_runtime[src_file] = time.time() - start

sorted_files = sorted(files_runtime.items(), key=lambda item: item[1])
print("{:<10}|{:<5}|{:<15}".format('PROGRAM', 'RANK', 'TIME ELAPSED'))
rank = 1
for elem in sorted_files:
    print("{:<10} {:<5} {:<15}".format(elem[0], rank, elem[1]))
    rank += 1
