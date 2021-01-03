class Variable:

    def __init__(self):
        pass

    def __init__(self, pid):
        self.pid = pid
        self.isInitialized = False
        self.memory_location = -1



class VariableArray(Variable):

    def __init__(self, pid, start, end):
        self.pid = pid
        self.start = start
        self.end = end
        self.length = end - start
        self.isInitialized = False
        self.memory_location = -1


class VariableIterator(Variable):

    def __init__(self, name, value, start, end):
        self.name = name
        self.value = value
        self.start = start
        self.end = end
        self.isInitialized = True
        self.memory_location = -1
