from comparator import Comparator

class Greater(Comparator):
    def string_switch(self, input_var, condition_const):
        if str(input_var) > str(condition_const):
            self.trigger_action()

    def number_switch(self, input_var, condition_const):
        if float(input_var) > float(condition_const):
            self.trigger_action()

    def integer_switch(self, input_var, condition_const):
        if int(input_var) > int(condition_const):
            self.trigger_action()

    def boolean_switch(self, input_var, condition_const):
        pass