class Variable:

    def __init__(self):
        pass

    def __init__(self, pid, memory_location):
        self.pid = pid
        self.is_initialized = False
        self.memory_location = memory_location
        self.is_shadowed = False
        self.reference_to_iterator = None


class VariableOfArray(Variable):

    def __init__(self, pid, memory_location_start, index):
        self.pid = pid
        self.memory_location_start = memory_location_start
        self.index = index


class ArrayOfVariables(Variable):

    def __init__(self, pid, memory_location, start, end):
        self.pid = pid
        self.start = start
        self.end = end
        self.length = end - start
        self.isInitialized = False
        self.memory_location = memory_location
        self.variables = [Variable(pid + "[" + str(i+1) + "]", memory_location+i)
                          for i in range(self.length)]

    def at_index(self, index: int):
        return self.variables[index-self.start]


class VariableIterator(Variable):

    def __init__(self, pid, memory_location, start, end):
        self.pid = pid
        self.start = start
        self.end = end
        self.is_initialized = True
        self.memory_location = memory_location
        self.is_in_register = False
        self.register_location = None
