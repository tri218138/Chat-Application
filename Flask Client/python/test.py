from thread_module import *
class Test:
    def __init__(self):
        self.arr = []
        print(1)
        thread = ThreadWithReturnValue(target=self.fakeVal)
        thread.start()
    def fakeVal(self):
        self.arr = [2,3,4]
        thread = ThreadWithReturnValue(target=self.thr)
        thread.start()
        thread.join()
        print(2)
    def thr(self):
        print('<',self.arr,'>')

test = Test()