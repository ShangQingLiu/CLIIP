from fractions import Fraction
import math

start_day = 20
start_hour = "00"
hours = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17",
         "18", "19", "20", "21", "22", "23"]
days = [i for i in range(20, 29)]
time_stamps = [i for i in range(1, 399)]
SEIR_simulation_result_statistic = '../simu/model.mat'
id_list_path = '../id_list.pkl'
people_interactive_graph_path = f"../stop_data/day{start_day}_0"
graph_path_root = "../stop_data/day"
model_graph_path_root = "../model_G/"
wearing_mask_path = {
    "ALL_NOT_WEAR_MASK": "both_infected_and_susceptible_people_not_have_wore_mask",
    "OTHER_WEAR_MASK": "only_susceptible_people_wore_mask",
    "INFECTED_WEAR_MASK": "only_infected_wore_mask",
    "ALL_WEAR_MASK": "both_infected_and_susceptible_people_have_wore_mask",
}
wearing_mask_probability = {
    "ALL_NOT_WEAR_MASK": Fraction(1, 1),  # run in
    "OTHER_WEAR_MASK": Fraction(1, 3),  # run in
    "INFECTED_WEAR_MASK": Fraction(1, 14),  # run in
    "ALL_WEAR_MASK": Fraction(1, 60),  # run in 4
}
current_status = "ALL_NOT_WEAR_MASK"
training_data_save_path_root = f"./train_data/{wearing_mask_path[current_status]}/day"

incubation_probability = {
    "incubation_day_1": 0.08,
    "incubation_day_2": 0.16,
    "incubation_day_3": 0.18,
    "incubation_day_4": 0.15,
    "incubation_day_5": 0.11,
    "incubation_day_6": 0.08,
    "incubation_day_7": 0.06,
    "incubation_day_8": 0.04,
    "incubation_day_9": 0.03,
    "incubation_day_10": 0.03,
    "incubation_day_11": 0.02,
    "incubation_day_12": 0.02,
    "incubation_day_13": 0.01,
    "incubation_day_14": 0.01,
    "incubation_day_15": 0.01,
    "incubation_day_16": 0.01,
}
incubation_probability_list = [1] *(int)( incubation_probability["incubation_day_1"] *100)+ \
                              [2] *(int)( incubation_probability["incubation_day_2"] *100)+ \
                              [3] *(int)( incubation_probability["incubation_day_3"] *100)+ \
                              [4] *(int)( incubation_probability["incubation_day_4"] *100)+ \
                              [5] *(int)( incubation_probability["incubation_day_5"] *100)+ \
                              [6] *(int)( incubation_probability["incubation_day_6"] *100)+ \
                              [7] *(int)( incubation_probability["incubation_day_7"] *100)+ \
                              [8] *(int)( incubation_probability["incubation_day_8"] *100)+ \
                              [9] *(int)( incubation_probability["incubation_day_9"] *100)+ \
                              [10] *(int)( incubation_probability["incubation_day_10"] *100)+ \
                              [11] *(int)( incubation_probability["incubation_day_11"] *100)+ \
                              [12] *(int)( incubation_probability["incubation_day_12"] *100)+ \
                              [13] *(int)( incubation_probability["incubation_day_13"] *100)+ \
                              [14] *(int)( incubation_probability["incubation_day_14"] *100)+ \
                              [15] *(int)( incubation_probability["incubation_day_15"] *100)+ \
                              [16] *(int)( incubation_probability["incubation_day_16"] *100)

# ensemble learning constant
wrong_sample1 = [0, 0, 0, 0, 0, 0, 0, 0]

# training_X = [deltaT,deltaD_reverse,I1,I2,I3,E1,E2,E3]
deltaT_index = 0
deltaD_reverse_index = 1
layer_one_I_index = 2
layer_two_I_index = 3
layer_three_I_index = 4
layer_one_E_index = 5
layer_two_E_index = 6
layer_three_E_index = 7

# light gbm parameter
light_gbm_params = {
    'learning_rate': 0.001,
    'boosting_type': 'dart',
    'objective': 'binary',
    'metric': 'binary_logloss',
    'sub_feature': 0.5,
    'num_leaves': 100,
    'min_data': 100,
    'max_depth': 50,
    'max_bin': 100
}

train_test_split_parameter = {
    'test_size': 0.5,
    'random_state': 0
}


def gen_X_Y_ID_path(day, hour):
    x_path = training_data_save_path_root + str(day) + '_' + hour + '_' + 'X'
    y_path = training_data_save_path_root + str(day) + '_' + hour + '_' + 'Y'
    id_path = training_data_save_path_root + str(day) + '_' + hour + '_' + 'ID'
    return x_path, y_path, id_path


def gen_graph_path_graph_tool(search_day, search_hour):
    '''
    get the path of graph tool graph, which finish connecting by interactive data

    :param search_day: int
    :param search_hour: str
    :return:  path: str
    '''
    graph_path = "graph_tool_G/" + str(search_day) + "_" + str(int(search_hour)) + ".xml.gz"
    return graph_path


def gen_graph_path_network_x(search_day, search_hour):
    '''
    get the path of network_x graph, which finish connecting by interactive data

    :param search_day: str
    :param search_hour: str
    :return: path: str
    '''
    graph_path = model_graph_path_root + str(search_day) + "_" + str(search_hour)
    return graph_path
