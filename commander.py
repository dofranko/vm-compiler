from variables import *
from expressioner import *
from conditioner import *
from helping_functions import *


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
                print("\n".join(i.code))


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


class AssignCommand(Command):

    def __init__(self, variable, expression: Expression):
        self.variable = variable
        self.expression = expression
        self.code = []

    def generate_code(self, register="b"):
        self.code = self.expression.generate_code("b")
        self.code.extend(load_value_to_register(
            self.variable.memory_location, "a"))
        self.code.append("STORE " + register + " a")


class IfCommand(Command):

    def __init__(self, condition: Condition, commands: list):
        self.condition = condition
        self.commands = commands
        self.code = []

    def generate_code(self, register="a"):
        commands_code = []
        code = []
        for command in self.commands:
            command.generate_code()
            commands_code.extend(command.code)
        code = self.condition.generate_code(len(commands_code)+1)
        code.extend(commands_code)


class IfElseCommand(Command):

    def __init__(self, condition: Condition, commands_if: list, commands_else: list):
        self.condition = condition
        self.commands_if = commands_if
        self.commands_else = commands_else
        self.code = []

    def generate_code(self, register="a"):
        commands_if_code = []
        commands_else_code = []
        for command in self.commands_if:
            command.generate_code()
            commands_if_code.extend(command.code)

        for command in self.commands_else:
            command.generate_code()
            commands_else_code.extend(command.code)

        self.code = self.condition.generate_code(len(commands_if_code)+1)
        self.code.extend(commands_if_code)
        self.code.extend(commands_else_code)


class WhileCommand(Command):

    def __init__(self, condition: Condition, commands: list):
        self.condition = condition
        self.commands = commands
        self.code = []

    def generate_code(self, register="a"):
        commands_code = []
        for command in self.commands:
            command.generate_code()
            commands_code.extend(command.code)

        self.code = self.condition.generate_code(len(commands_code)+2)
        self.code.extend(commands_code)
        self.code.append("JUMP " + str(-len(self.code)))


class RepeatCommand(Command):

    def __init__(self, condition: Condition, commands: list):
        self.condition = condition
        self.commands = commands
        self.code = []

    def generate_code(self, register="a"):
        commands_code = []
        for command in self.commands:
            command.generate_code()
            commands_code.extend(command.code)

        self.code = commands_code
        self.code.extend(self.condition.generate_code(-len(self.code)))
