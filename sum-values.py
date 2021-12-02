# Compute sum of all values through using threads with locks

from concurrent.futures import ThreadPoolExecutor
import threading
import time
import os
import random

e = threading.Event()
LockFile = threading.Lock()
sum = 0.0
maxValue = 0
fin = 0
count = 0


# producer thread
def generateRandom():
    global e
    global maxValue
    global count
    val = random.randint(0, 100000)
    appendVal(val)
    count += 1
    if count == maxValue:
        e.set()
    return val


# clear the file
def clearFile():
    fin = open("data.txt", "w")
    fin.close()


# write values in the file
def appendVal(val):
    global LockFile
    LockFile.acquire()
    fin = open("data.txt", "at")
    fin.write('\n' + str(val) + '\n');
    fin.close()
    LockFile.release()


# read the values on the file
def readVals():
    global LockFile
    global e
    global sum
    while not e.isSet():
        if (os.path.getsize("data.txt") != 0):
            LockFile.acquire()
            fin = open("data.txt", "r")
            while True:
                # read next line
                SeqNo = fin.readline()
                # if line is blank, then you struck the EOF
                if not SeqNo:
                    break;
                else:
                    # read value
                    val = fin.readline()
                    sum += int(val)
                    print(f"The current sum of the values is {sum}")
                    # time.sleep(2)
            fin.close()
            clearFile()
            LockFile.release()


def main():
    global maxValue
    clearFile()
    t0 = time.time()

    maxValue = 500000

    t1 = time.time()

    with ThreadPoolExecutor(max_workers=10) as executor:
        # consumer thread
        results = executor.submit(readVals)
        # producer
        for i in range(1, maxValue):
            results = executor.submit(generateRandom)

    # print("Total Execution Time {}".format(t1 - t0))


main()
