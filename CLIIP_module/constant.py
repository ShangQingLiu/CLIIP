from fractions import Fraction

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
incubation_probability_list = [1] * incubation_probability["incubation_day_1"] + \
                              [2] * incubation_probability["incubation_day_2"] + \
                              [3] * incubation_probability["incubation_day_3"] + \
                              [4] * incubation_probability["incubation_day_4"] + \
                              [5] * incubation_probability["incubation_day_5"] + \
                              [6] * incubation_probability["incubation_day_6"] + \
                              [7] * incubation_probability["incubation_day_7"] + \
                              [8] * incubation_probability["incubation_day_8"] + \
                              [9] * incubation_probability["incubation_day_9"] + \
                              [10] * incubation_probability["incubation_day_10"] + \
                              [11] * incubation_probability["incubation_day_11"] + \
                              [12] * incubation_probability["incubation_day_12"] + \
                              [13] * incubation_probability["incubation_day_13"] + \
                              [14] * incubation_probability["incubation_day_14"] + \
                              [15] * incubation_probability["incubation_day_15"] + \
                              [15] * incubation_probability["incubation_day_15"]


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
