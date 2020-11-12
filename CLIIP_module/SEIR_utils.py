from math import radians, cos, sin, sqrt, atan2, floor


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
        S_number = int(model[time_step][0])
        E_number = floor(int(model[time_step][1]) * probability)
        I_number = floor(int(model[time_step][2]) * probability)
        Sq_number = floor(int(model[time_step][3]) * probability)
        Eq_number = floor(int(model[time_step][4]) * probability)
        H_number = floor(int(model[time_step][5]) * probability)
        R_number = floor(int(model[time_step][6]) * probability)
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
