from clipio.eca.comparator_action import ComparatorAction

class NotEqual(ComparatorAction):
    def __string_switch(self, input_var, condition_const):
        if str(input_var) != str(condition_const):
            self.__trigger_action()

    def __number_switch(self, input_var, condition_const):
        if float(input_var) != float(condition_const):
            self.__trigger_action()

    def __integer_switch(self, input_var, condition_const):
        if int(input_var) != int(condition_const):
            self.__trigger_action()

    def __boolean_switch(self, input_var, condition_const):
        """ if input_var == "True" or input_var == "true":
           input_var = 1
        if input_var == "False" or input_var == "false":
           input_var = 0

        if condition_const == "True" or condition_const == "true":
           condition_const = 1
        if condition_const == "False" or condition_const == "false":
           condition_const = 0 """

        if int(input_var) != int(condition_const):
            self.__trigger_action()