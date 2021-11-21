import threading
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s', )

valsMad = [] # Madhava List
valsNil = [] # Nilakantha List

def PrintVals(eNum,eEnd):
    global valsMad
    global valsNil
    
    eNum.wait()
    eNum.clear()

    print("Est PI Madhava Series = ", valsMad[-1])
    print("Est PI Nilakantha Series = ", valsNil[-1])

# compute pi using madhava series
def produceMadhava(eNum1, eNum2, eEnd):
    global valsMad

    result = 0
    for x in range(1000000):
        if x == 0:
            result = (((-1) ** x) * (4 / ((2 * x) + 1)))
            valsMad.append(result)
        else:
            result = result + (((-1) ** x) * (4 / ((2 * x) + 1)))
            valsMad.append(result)
            eNum1.set()
            eNum2.set()
    eEnd.set()

# compute pi using nilakantha series
def produceNilakantha(eNum1, eNum2, eEnd):
    global valsNil
    value_of_pi = 3
    for index in range(2, 1000000, 4):
            denominator1 = index * (index + 1) * (index + 2)
            denominator2 = (index + 2) * (index + 3) * (index + 4)
            entry = 4 / denominator1 - 4 / denominator2
            value_of_pi += entry
            valsNil.append(value_of_pi)
            eNum1.set()
            eNum2.set()
    eEnd.set()


if __name__ == '__main__':
    eMadNum = threading.Event()
    eNilakantNum = threading.Event()
    eEnd = threading.Event()
    t1 = threading.Thread(name='non-blocking',
                          target=produceMadhava,
                          args=(eMadNum, eNilakantNum, eEnd,))
    t1.start()

    t2 = threading.Thread(name='blocking',
                          target=produceNilakantha,
                          args=(eMadNum, eNilakantNum, eEnd,))
    t2.start()

    t3 = threading.Thread(name='blocking',
                          target=PrintVals,
                          args=(eNilakantNum, eEnd,))
    t3.start()

    t1.join()
    t2.join()
    t3.join()


