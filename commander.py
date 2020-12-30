from variables import *


class Program:

    def __init__(self):
        self.commands = []

    def __init__(self, commands: list):
        self.commands = commands

    def add_command(self, command):
        self.commands.append(command)

    def execute_commands(self):
        for i in self.commands:
            if isinstance(i, Command):
                i.generate_code()
                print(i.code)


class Command:

    def __init__(self):
        pass

    def generate_code(self):
        pass


class WriteCommand(Command):

    def __init__(self, variable):
        self.variable = variable
        self.code = []

    def generate_code(self):
        if type(self.variable) == int:
            pass
        elif isinstance(self.variable, Variable):
            self.code = load_value_to_register(
                self.variable.memory_location, "a")
            self.code.append("PUT " + "a")


class ReadCommand(Command):

    def __init__(self, variable):
        self.variable = variable
        self.code = []

    def generate_code(self):
        self.code = load_value_to_register(
            self.variable.memory_location, "a")
        self.code.append("GET " + "a")


def load_value_to_register(value: int, register):
    code = []
    code.append("RESET " + register)
    code.extend(generate_number(value, register))
    return code


def generate_number(value: int, register):
    if value == 0:
        return
    elif value == 1:
        return ["INC " + register]
    else:
        code = []
        value_in_binary = str(bin(value)[2:])
        for i in range(length(value_in_binary)):
            if value_in_binary[i] == "1":
                code.append("INC " + register)
            if i < length(value_in_binary - 1):
                code.append("ADD " + register + " " + register)
    return code
