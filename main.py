import sys

print("my name is {}".format(sys.argv[0]))
if len(sys.argv) == 3:
    print(int(sys.argv[1]) + int(sys.argv[2]))
else:
    print(0)