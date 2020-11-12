# std library
import pickle
from os.path import isfile

# custom module
from CLIIP_module.constant import days, hours, training_data_save_path_root


class Ensemble_model:
    def __init__(self):
        self.firstIndex = 0
        self.varX = []
        self.varY = []

    def ensemble_lightGBM(self):
        # import data

        # pre-processing
        # reinforcement_learning
        # ensemble_learning
        pass

    def import_data(self):
        index = 0
        for day in days:
            for hour in hours:
                Xpath = training_data_save_path_root + str(day) + '_' + hour + '_' + 'X'
                Ypath = training_data_save_path_root + str(day) + '_' + hour + '_' + 'Y'

                if not isfile(Xpath) or not isfile(Ypath):
                    continue
                else:
                    with open(Xpath, "rb") as inputX_f:
                        input_X = pickle.load(inputX_f)
                    with open(Ypath, "rb") as inputY_f:
                        input_Y = pickle.load(inputY_f)

                if index == self.firstIndex:
                    self.varX = input_X
                    self.varY = input_Y
                else:
                    self.varX.extend(input_X)
                    self.varY.extend(input_Y)
            index = index + 1

        def incubation_update(self, x_list_queue, y_list_queue):

            pass

        def pre_processing(self):
            pass
