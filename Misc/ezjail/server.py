import string
import sys
import time
import random
import copy as cp

timestamp = int(time.time() * 1000)
random.seed(timestamp)


class helloOutput:

    def __init__(self, original_stdout):
        self.original_stdout = original_stdout

    def write(self, text):
        self.original_stdout.write("ni hao")

    def flush(self):
        self.original_stdout.write("ni hao")


def check(input):
    if any(i not in string.printable for i in input):
        print("only ascii!!!")
        exit()


def makerandom(text):
    text = list(text)
    random.shuffle(text)
    return text


def check2(ori, new):
    time1 = time.time()
    diff = 0
    for i in range(len(ori)):
        if (ori[i] != new[i]):
            diff += 1
            for _ in range(10000):  # Just for a most strict randommaker checker :p
                if (new[i] not in ori):
                    print("error in randommaker!!!")
                    exit()
    timeuse = time.time() - time1
    print(
        f"After {timeuse} of inspection, there were no issues with the randommaker")


original_stdout = sys.stdout
original_stderr = sys.stderr

while True:
    yourinput = input(">>> ")
    orinput = cp.deepcopy(yourinput)
    check(yourinput)
    yourinput = "".join(makerandom(yourinput))
    hello_output = helloOutput(original_stdout)
    check2(orinput, yourinput)
    sys.stdout = hello_output
    sys.stderr = hello_output
    exec(yourinput)
    sys.stdout = original_stdout
    sys.stderr = original_stderr
