# std library
import pickle
import random
import numpy as np
import lightgbm as lgb
from os.path import isfile
from sklearn.preprocessing import normalize
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score
from statistics import median

# custom module
from CLIIP_module.constant import days, hours, training_data_save_path_root, incubation_probability_list, wrong_sample1, \
    deltaT_index, deltaD_reverse_index, train_test_split_parameter, light_gbm_params,total_people,debug_flag


def transfer_predict(Y_judge_line, Y_prediction):
    result_list = []
    for item in Y_prediction:
        if item > Y_judge_line:
            result_list.append(1)
            continue
        result_list.append(0)
    return result_list


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
        # print(f"input_X: {input_X}")
        # print(f"input_Y: {input_Y}")
        random_state = train_test_split_parameter['random_state']
        test_size = train_test_split_parameter['test_size']
        X_train, X_test, Y_train, Y_test = train_test_split(np.array(input_X), np.array(input_Y),
                                                            test_size=test_size,
                                                            random_state=random_state)
        data_train = lgb.Dataset(X_train, label=Y_train)
        clf = lgb.train(light_gbm_params, data_train, num_boost_round=100)
        Y_prediction = clf.predict(X_test)
        Y_judge_line = 0.6

        sorted_X_test = [x for _, x in sorted(zip(Y_prediction,X_test),key=lambda x:x[0])]
        sorted_Y_result = [x for _, x in sorted(zip(Y_prediction,Y_test),key=lambda x:x[0],reverse=True)]
        sorted_Y_test = Y_prediction.sort()
        plot_x = []
        plot_y = []
        origin_x = []
        origin_y = []
        sum = 0
        for item in sorted_Y_result:
           sum +=item
        current_sum = 0
        for index,item in enumerate(sorted_Y_result):
            current_sum+=item
            plot_x.append((index+1)/len(sorted_Y_result))
            plot_y.append(current_sum/sum)
        current_sum = 0
        for index,item in enumerate(Y_test):
            current_sum+=item
            origin_x.append((index+1)/len(Y_test))
            origin_y.append(current_sum/sum)


        import matplotlib.pyplot as plt
        plt.style.use('seaborn-whitegrid')
        fig = plt.figure()
        ax = plt.axes()
        ax.plot(plot_x,plot_y,label= "model")
        ax.plot(origin_x,origin_y,label= "origin")
        plt.legend(loc="upper left")
        plt.xlabel('people scale', fontsize=10)
        plt.ylabel('coverage', fontsize=10)
        plt.savefig('test.pdf')

        result_prediction = transfer_predict(Y_judge_line,Y_prediction)
        cm = confusion_matrix(Y_test, result_prediction)
        accuracy = accuracy_score(result_prediction, Y_test)
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
        x_list_queue = self.merge_all_dict(self.varX)
        y_list_queue = self.merge_all_dict(self.varY)
        # debug
        if debug_flag:
            self.x_list_queue = x_list_queue
            self.y_list_queue = y_list_queue
            return

        incubation_day = random.choice(incubation_probability_list)
        x_list_queue_len = len(x_list_queue)

        if x_list_queue_len > 1:
            start_infection_day = self.find_start_infection_day(x_list_queue_len, incubation_day)
            last_updated_group_index = x_list_queue_len - 1
            last_second_updated_group_index = x_list_queue_len - 2
            print(f"last_second_updated_group_index: {last_second_updated_group_index}")
            print(f"last_updated_group_index: {last_updated_group_index}")
            last_updated_group_index_id = list(y_list_queue.keys())[int(last_updated_group_index)]
            last_second_updated_group_index_id =list(y_list_queue.keys())[last_second_updated_group_index]
            influence_id_list = self.find_influence_ids(y_list_queue[last_second_updated_group_index_id],
                                                        y_list_queue[last_updated_group_index_id])

            for i in range(start_infection_day, last_updated_group_index):
                for id in influence_id_list:
                    # make it affected
                    x_list_queue[i][id] = 1
        # no need to update
        else:
            pass
        self.x_list_queue = x_list_queue

    def pre_processing(self):
        x_list_queue = self.x_list_queue
        y_list_queue = self.y_list_queue
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
            deltaD_reverse_list.append(x_list_queue[id][deltaD_reverse_index])

        deltaT_list_normalize = [float(i)/sum(deltaT_list) for i in deltaT_list]
        deltaD_reverse_list_normalize = [float(i)/sum(deltaD_reverse_list) for i in deltaD_reverse_list]

        wrong_sample_id_list = []
        index = 0
        for id in list(x_list_queue.keys()):
            # no possible people around
            if x_list_queue[id][:6] == wrong_sample1[:6]:
                x_list_queue.pop(id, None)
                y_list_queue.pop(id, None)
                wrong_sample_id_list.append(id)
                continue

            # substitute normalize number
            x_list_queue[id][deltaT_index] = deltaT_list_normalize[index]
            x_list_queue[id][deltaD_reverse_index] = deltaD_reverse_list_normalize[index]
            index = index + 1

        # print(f"wrong_sample_id_list: {wrong_sample_id_list}")
        print(f"wrong_sample_id_list_len: {len(wrong_sample_id_list)}")
        print(f"wrong_sample_id_list_rate: {len(wrong_sample_id_list)/total_people}")

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
        print(f"original_group: {original_group}")
        print(f"changed_group: {changed_group}")
        not_shared_items = []
        for k in original_group:
            if k in changed_group:
                if original_group[k] != changed_group[k] and changed_group[k] == 1:
                    not_shared_items.append(k)
        print(f"length of not_shared_items:{len(not_shared_items)}")
        return not_shared_items

    @staticmethod
    def merge_all_dict(list_of_dict_element: list) -> dict:
        merge_dict = {}
        for dict_element in list_of_dict_element:
            merge_dict = {**merge_dict, **dict_element}
        return merge_dict
