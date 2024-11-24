
class Buffer:

    def __init__(self):
        self.buffer = []

    def appendRequest(self, key):
        self.buffer.append(key)

    def isNext(self, key):
        if len(self.buffer) == 0:
            return False
        
        if (self.buffer[0] != key):
            return False
        
        return True
    
    def completeEvent(self):
        self.buffer.pop(0)

