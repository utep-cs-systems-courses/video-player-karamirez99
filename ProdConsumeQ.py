from threading import Semaphore, Lock

class ProdConsumeQ:
    def __init__(self, capacity):
        self.full =  Semaphore(0)
        self.empty = Semaphore(capacity)
        self.buffer = list()
        self.bufferLock = Lock()

    def get(self):
        self.full.acquire()
        self.bufferLock.acquire()
        returnItem = self.buffer.pop(0)
        self.bufferLock.release()
        self.empty.release()
        return returnItem

    def put(self, val):
        self.empty.acquire()
        self.bufferLock.acquire()
        self.buffer.append(val)
        self.bufferLock.release()
        self.full.release()



