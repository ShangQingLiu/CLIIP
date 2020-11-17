# std library
import pickle
import random
import numpy as nd
import lightgbm as lgb
from os.path import isfile
from sklearn.preprocessing import normalize
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score

# custom module
from CLIIP_module.constant import days, hours, training_data_save_path_root, incubation_probability_list, wrong_sample1, \
    deltaT_index, deltaD_reverse_index, train_test_split_parameter, light_gbm_params


class Ensemble_model:
    '''
    STEP
    1. import data
    2. pre-processing
    3. reinforcement_learning
    4. ensemble_learning
    '''

    def __init__(self):
        self.firstIndex = 0
        self.varX = []
        self.varY = []
        self.x_list_queue = {}
        self.y_list_queue = {}

    def ensemble_lightGBM(self):
        input_X = list(self.x_list_queue.values())
        input_Y = list(self.y_list_queue.values())
        print(f"input_X: {input_X}")
        print(f"input_Y: {input_Y}")
        random_state = train_test_split_parameter['random_state']
        test_size = train_test_split_parameter['test_size']
        X_train, X_test, Y_train, Y_test = train_test_split(nd.array(input_X), nd.array(input_Y),
                                                            test_size=test_size,
                                                            random_state=random_state)
        data_train = lgb.Dataset(X_train, label=Y_train)
        clf = lgb.train(light_gbm_params, data_train, num_boost_round=100)
        Y_prediction = clf.predict(X_test)

        cm = confusion_matrix(Y_test, Y_prediction)
        accuracy = accuracy_score(Y_prediction, Y_test)
        print(f"accuracy: {accuracy}")
        feature_importance = clf.feature_importance()
        print(f"feature_importance: {feature_importance}")

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

    def incubation_update(self):
        x_list_queue = self.x_list_queue
        y_list_queue = self.y_list_queue
        incubation_day = random.choice(incubation_probability_list)
        x_list_queue_len = len(x_list_queue)
        if x_list_queue_len > 1:
            start_infection_day = self.find_start_infection_day(x_list_queue_len, incubation_day)
            last_updated_group_index = x_list_queue_len - 1
            last_seconde_updated_group_index = x_list_queue_len - 2
            influence_id_list = self.find_influence_ids(y_list_queue[last_seconde_updated_group_index],
                                                        y_list_queue[last_updated_group_index])
            for i in range(start_infection_day, last_updated_group_index):
                for id in influence_id_list:
                    # make it affected
                    x_list_queue[i][id] = 1
        # no need to update
        else:
            pass
        self.x_list_queue = x_list_queue

    def pre_processing(self, x_list_queue: dict, y_list_queue: dict):
        deltaT_list = []
        deltaD_reverse_list = []
        for id in list(x_list_queue.keys()):
            # shorten the number digit
            deltaT = x_list_queue[id][deltaT_index]
            deltaD_reverse = x_list_queue[id][deltaD_reverse_index]
            if deltaT < 0:
                x_list_queue[deltaT_index] = abs(deltaT)
            if deltaD_reverse < 0:
                x_list_queue[deltaD_reverse_index] = abs(deltaD_reverse)

            deltaT_list.append(x_list_queue[id][deltaT_index])
            deltaD_reverse_index.append(x_list_queue[id][deltaD_reverse_index])

        deltaT_list_normalize = normalize(deltaT_list)
        deltaD_reverse_list_normalize = normalize(deltaD_reverse_list)

        wrong_sample_id_list = []
        index = 0
        for id in list(x_list_queue.keys()):
            # no possible people around
            if x_list_queue[id][:6] == wrong_sample1[:6]:
                x_list_queue.pop(id, None)
                y_list_queue.pop(id, None)
                wrong_sample_id_list.append(id)

            # substitute normalize number
            x_list_queue[id][deltaT_index] = deltaT_list_normalize[index]
            x_list_queue[id][deltaD_reverse_index] = deltaD_reverse_list_normalize[index]
            index = index + 1

        print(f"wrong_sample_id_list: {wrong_sample_id_list}")

        self.x_list_queue = x_list_queue
        self.y_list_queue = y_list_queue

    @staticmethod
    def find_start_infection_day(x_list_queue_len, incubation_day):
        if (x_list_queue_len - incubation_day) < 0:
            return 0
        else:
            return x_list_queue_len - incubation_day

    @staticmethod
    def find_influence_ids(original_group: dict, changed_group: dict) -> list:
        # focus on the changed group members who become infected
        not_shared_items = {k: original_group[k] for k in original_group if
                            k in changed_group and original_group[k] != changed_group[k] and changed_group[k] == 1}
        print(f"length of not_shared_items:{len(not_shared_items)}")
        return list(not_shared_items.keys())
