#!/usr/bin/python3.7

import random

class Incrementer:
    def __init__(self, low_value, high_value, increment_value):
        self.current_value = low_value
        self.low_value = low_value
        self.high_value = high_value
        self.increment_value = increment_value

    def get_value(self):
        ret_val = self.current_value
        self.current_value += self.increment_value
        if self.current_value > self.high_value:
            self.current_value = self.low_value
        return ret_val


class uniquleNumber:
    def __init__(self):
        self.value = 0

    def outPut(self,number):
        r =random.sample(range(number), 1)
        self.value = ''.join(map(str, r))
        return self.value
     

class alpha():
    def __init__(self):
        self.alpha = 0

    def random_alpha(self):
        self.alpha = ''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUV') for i in range(1))
        return  self.alpha

def printOutTableOne():
    test = uniquleNumber()
    two = Incrementer(0, 1, 1)
    four = Incrementer(0,3,1)
    ten = Incrementer(0,9,1)
    twenty = Incrementer(0,19,1)
    hundred = Incrementer(0,99,1)
    thousand =Incrementer(0,999,1)
    twothous = Incrementer(0,1999,1)
    fivethous = Incrementer(0,4999,1)
    tenthous =Incrementer(0,9999,1)
    oddonehund = Incrementer(1,99,2)
    evenonehund = Incrementer(2,100,2)
    stringu1 = alpha()
    
    for i in range(0, 10):
        un = test.outPut(100)
        print(f"{un},{i},{two.get_value()},{four.get_value()},{ten.get_value()},{twenty.get_value()},{hundred.get_value()},{thousand.get_value()},{twothous.get_value()},{fivethous.get_value()},{tenthous.get_value()},{oddonehund.get_value()},{evenonehund.get_value()},{stringu1.random_alpha()}xxxxxxxxxxxxxxxxxxxxxxxxx{stringu1.random_alpha()}xxxxxxxxxxxxxxxxxxxxxxxxx{stringu1.random_alpha()}\n")
        #print(f'{stringu1.random_alpha()}xxxxxxxxxxxxxxxxxxxxxxxxx{stringu1.random_alpha()}xxxxxxxxxxxxxxxxxxxxxxxxx{stringu1.random_alpha()}')
printOutTableOne()