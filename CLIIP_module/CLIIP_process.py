# import library
from os.path import isfile

import CLIIP_module.model_util as model_util
# import custom library
from CLIIP_module.SEIR import SEIR
from CLIIP_module.constant import days, hours, start_day, start_hour, \
    time_stamps, gen_X_Y_ID_path, current_status
from CLIIP_module.utils import save_pickle

Data = {'S': [],
        'E': [],
        'I': [],
        'R': [],
        'Mask_I': [],
        'time_stamp': [i for i in range(1, 399)]
        }
# prepare the rate of mask infected
'''
both infected and susceptible people not have wore mask: 1
only susceptible people have wore mask: 1/3
only infected have wore mask:1/14
both infected and susceptible people have wore mask :1/60
'''


# finding what would be the result of having wear the mask
# if __name__ == '__main__':
def CLIIP_process():
    seir_modle = SEIR()
    print(f"current status: {current_status}")
    model_maintainer = seir_modle.model_init(start_day, start_hour)

    update_iterate_time = 0
    for day in days:
        for hour in hours:
            X_path, Y_path, ID_path = gen_X_Y_ID_path(day, hour)
            if isfile(X_path) or isfile(Y_path):
                update_iterate_time = update_iterate_time + 1
                continue
            if update_iterate_time >= len(time_stamps):
                break
            model_maintainer, update_flag = seir_modle.model_update(day, hour, model_maintainer,
                                                                    time_stamps[update_iterate_time])
            print("%%%%%%%%%%%%%%%%%%%%%%")
            print("S_number", len(model_maintainer["S"][1]))
            print("E_number", len(model_maintainer["E"][1]))
            print("I_number", len(model_maintainer["I"][1]))
            print("R_number", len(model_maintainer["R"][1]))
            print("Sq_number", len(model_maintainer["Sq"][1]))
            print("Eq_number", len(model_maintainer["Eq"][1]))
            print("H_number", len(model_maintainer["H"][1]))
            print("%%%%%%%%%%%%%%%%%%%%%%")
            update_iterate_time = update_iterate_time + 1

            Data['S'].append(model_maintainer["S"][0])
            Data['E'].append(model_maintainer["E"][0])
            Data['I'].append(model_maintainer["I"][0])
            Data['R'].append(model_maintainer["R"][0])
            # Data['Mask_I'].append(model_maintainer["Mask_I"][0])

            # generate X and Y
            no_infect_combine = []
            infect_combine = []
            X_group = []
            Y_group = []
            record_id_list = []

            no_infect_combine.extend(model_maintainer['S'][1] +
                                     model_maintainer['Sq'][1] +
                                     model_maintainer['E'][1] +
                                     model_maintainer['Eq'][1] +
                                     model_maintainer['R'][1])

            infect_combine.extend(model_maintainer['I'][1])
            # infect_combine.extend(model_maintainer['Mask_I'][1])
            num_infected = len(infect_combine)

            # running the same amount as infected for balancing the non-infected data
            for not_infected_person in no_infect_combine:
                num_infected = num_infected - 1

                if num_infected < 0:
                    break
                model_util_obj = model_util.model_util(day, int(hour))
                train_data_X = model_util_obj.get_train_data_X(model_maintainer, not_infected_person)
                X_element = {str(not_infected_person): train_data_X}
                X_group.append(X_element)
                Y_element = {str(not_infected_person): 0}
                Y_group.append(Y_element)

                del model_util_obj
                record_id_list.append(not_infected_person)
            print("finish finding false infected")

            for infected in infect_combine:
                model_util_obj = model_util.model_util(day, int(hour))
                train_data_X = model_util_obj.get_train_data_X(model_maintainer, infected)
                X_element = {str(infected): train_data_X}
                X_group.append(X_element)
                Y_element = {str(infected): 1}
                Y_group.append(Y_element)
                del model_util_obj
                record_id_list.append(infected)
            print("finish finding true infected")

            save_pickle(X_path, X_group)
            save_pickle(Y_path, Y_group)
            save_pickle(ID_path, record_id_list)
            print("finish saving data")
            print("\n\n")

            # draw the line for test
            # draw_SEIR_process(Data)

            # start training the model

            # start using the model to predict
