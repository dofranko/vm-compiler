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

    def __init__(self, array, index):
        self.array = array
        self.index = index


class ArrayOfVariables(Variable):

    def __init__(self, pid, memory_location, start, end):
        if start > end:
            raise IncorrectIndexRangeError
        self.pid = pid
        self.start = start
        self.end = end
        self.length = end - start + 1
        self.is_initialized = True
        self.memory_location = memory_location
        self.variables = dict()

    def at_index(self, index: int):
        if not self.start <= index <= self.end:
            raise IndexError
        my_index = index-self.start
        if my_index not in self.variables:
            self.variables[my_index] = Variable(self.pid+"[" + str(my_index) + "]", self.memory_location+my_index)
            self.variables[my_index].is_initialized = True
        return self.variables[my_index]


class VariableIterator(Variable):

    def __init__(self, pid, memory_location, start, end):
        self.pid = pid
        self.start = start
        self.end = end
        self.is_initialized = True
        self.memory_location = memory_location
        self.is_in_register = False
        self.register_location = None

class IncorrectIndexRangeError(Exception):
    pass