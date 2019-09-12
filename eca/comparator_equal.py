from comparator import Comparator

class Equal(Comparator):
    def string_switch(self, input_var, condition_const):
        if str(input_var) == str(condition_const):
            self.trigger_action()

    def number_switch(self, input_var, condition_const):
        if float(input_var) == float(condition_const):
            self.trigger_action()

    def integer_switch(self, input_var, condition_const):
        if int(input_var) == int(condition_const):
            self.trigger_action()

    def boolean_switch(self, input_var, condition_const):
        if input_var == "True" or input_var == "true":
           input_var = 1
        if input_var == "False" or input_var == "false":
           input_var = 0

        if condition_const == "True" or condition_const == "true":
           condition_const = 1
        if condition_const == "False" or condition_const == "false":
           condition_const = 0

        if int(input_var) == int(condition_const):
            self.trigger_action()