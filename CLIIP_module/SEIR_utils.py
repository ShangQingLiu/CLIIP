from math import radians, cos, sin, sqrt, atan2, floor
from .constant import group_size_factor

class SEIR_utils:
    @staticmethod
    def distance(lon1, lat1, lon2, lat2):
        R = 6373.0

        lat1 = radians(lat1)
        lon1 = radians(lon1)
        lat2 = radians(lat2)
        lon2 = radians(lon2)

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        if a < 0:
            a = abs(a)
        if a == 0 or a >= 1:
            return 0

        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = R * c
        return distance

    @staticmethod
    def split_number(number):
        if number % 2 != 0:  # odd
            split_1 = int((number - 1) / 2 + 1)
            split_2 = int((number - 1) / 2)
        else:  # even
            split_1 = int((number - 1) / 2)
            split_2 = split_1
        return split_1, split_2

    @staticmethod
    def init_model_maintainer(model, time_step, probability) -> dict and dict:
        model_maintainer = {}
        S_number = int(model[time_step][0] //group_size_factor )
        E_number = floor(int(model[time_step][1]) * probability//group_size_factor)
        I_number = floor(int(model[time_step][2]) * probability//group_size_factor)
        Sq_number = floor(int(model[time_step][3]//group_size_factor))
        Eq_number = floor(int(model[time_step][4]//group_size_factor))
        H_number = floor(int(model[time_step][5]//group_size_factor))
        R_number = floor(int(model[time_step][6]) * (model[time_step][5] + model[time_step][2] * probability) / (
                model[time_step][5] + model[time_step][2]))//group_size_factor
        print("expect S_number ", S_number)
        print("expect E_number ", E_number)
        print("expect I_number ", I_number)
        print("expect R_number ", R_number)
        print("expect Sq_number ", Sq_number)
        print("expect Eq_number ", Eq_number)
        print("expect H_number ", H_number)

        model_maintainer.update({"S": [S_number, []],
                                 "E": [E_number, []],
                                 "I": [I_number, []],
                                 "Sq": [Sq_number, []],
                                 "Eq": [Eq_number, []],
                                 "H": [H_number, []],
                                 "R": [R_number, []]})
        model_number_dict = {}
        model_number_dict.update(
            {"S_number": S_number, "E_number": E_number, "I_number": I_number, "Sq_number": Sq_number,
             "Eq_number": Eq_number, "H_number": H_number, "R_number": R_number})
        return model_maintainer, model_number_dict
