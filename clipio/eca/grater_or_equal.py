from clipio.eca.comparator_action import ComparatorAction

class GreaterOrEqual(ComparatorAction):
    def __string_switch(self, input_var, condition_const):
        if str(input_var) >= str(condition_const):
            self.__trigger_action()

    def __number_switch(self, input_var, condition_const):
        if float(input_var) >= float(condition_const):
            self.__trigger_action()

    def __integer_switch(self, input_var, condition_const):
        if int(input_var) >= int(condition_const):
            self.__trigger_action()

    def __boolean_switch(self, input_var, condition_const):
        pass