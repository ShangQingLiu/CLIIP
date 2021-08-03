import pickle
import random

import networkx as nx
import scipy.io as sio

# custom module
from CLIIP_module.SEIR_utils import SEIR_utils
from CLIIP_module.constant import SEIR_simulation_result_statistic, id_list_path, people_interactive_graph_path, \
    model_graph_path_root, graph_path_root, current_status, wearing_mask_probability, tmp_id_list_path,group_size_factor


class SEIR():
    def __init__(self):
        pass

    @staticmethod
    def build_edge(z, day, hour, distance_limit=0.02, delta_limit=30):
        from os.path import isfile
        model_graph_path = model_graph_path_root + str(day) + "_" + str(hour)
        if isfile(model_graph_path):
            try:
                G = nx.read_gpickle(model_graph_path)
                return G
            except EOFError:
                print("load model_G fail")
        else:
            G = nx.DiGraph()
            for key, value in z.items():

                for inside_k, inside_v in z.items():
                    if key == inside_k:
                        continue
                    else:
                        # print(f"value: {value}")
                        # print(f"type: {type(value)}")
                        # print(f"value[0]: {value[0]}")
                        d = SEIR_utils.distance(value[0][0], value[0][1], inside_v[0][0], inside_v[0][1])
                        if d < distance_limit:
                            # value[1] time-stamp
                            delta = value[1] - inside_v[1]
                            if delta < delta_limit:
                                continue
                            if delta >= 0:
                                G.add_edge(key, inside_k, distance=d, delta=delta, start_time=value[1])
                            elif delta < 0:
                                delta = -delta
                                G.add_edge(inside_k, key, distance=d, delta=delta, start_time=value[1])
            nx.write_gpickle(G, model_graph_path)
            return G

    @staticmethod
    def find_id_list() -> list:
        try:
            with open(id_list_path, 'rb') as id_list_input:
                id_list = pickle.load(id_list_input)
                return id_list
        except Exception as e:
            print(e)

    @staticmethod
    def dump_tmp_id_list(tmp_id_list):
        try:
            with open(tmp_id_list_path, 'wb') as file:
                pickle.dump(tmp_id_list, file)
        except Exception as e:
            print(e)

    @staticmethod
    def find_tmp_id_list() -> list:
        try:
            with open(tmp_id_list_path, 'rb') as id_list_input:
                id_list = pickle.load(id_list_input)
                return id_list
        except Exception as e:
            print(e)

    def model_init(self, day, hour, start_time_step=0) -> dict:
        id_list = self.find_id_list()
        matfn = SEIR_simulation_result_statistic
        model = sio.loadmat(matfn)["AA"]
        print("start_time_step", start_time_step)
        # {key:type,value:[chage_number,[id_1,id_2,id_3...]]}
        model_maintainer, model_number_dict = SEIR_utils.init_model_maintainer(model, start_time_step,
                                                                               wearing_mask_probability[current_status])

        # # print(random.sample(id_list,int(S_number)))
        # a = [1,2,3,4,5]
        # b = [1,2]
        # a = [e for e in a if e not in b]

        print("id_list len", len(id_list))
        tmp_list = id_list
        tmp_list = tmp_list[:len(tmp_list) //group_size_factor]
        self.dump_tmp_id_list(tmp_list)
        if model_number_dict['R_number'] > 0:
            model_maintainer["R"][1] = random.sample(tmp_list, int(model_number_dict['R_number']//group_size_factor))
            tmp_list = [e for e in tmp_list if e not in model_maintainer["R"][1]]
        else:
            model_maintainer["R"][1] = []

        if model_number_dict['H_number'] > 0:
            model_maintainer["H"][1] = random.sample(tmp_list, int(model_number_dict['H_number']//group_size_factor))
            tmp_list = [e for e in tmp_list if e not in model_maintainer["H"][1]]
        else:
            model_maintainer["H"][1] = []

        if model_number_dict['Eq_number'] > 0:
            model_maintainer["Eq"][1] = random.sample(tmp_list, int(model_number_dict['Eq_number']//group_size_factor))
            tmp_list = [e for e in tmp_list if e not in model_maintainer["Eq"][1]]
        else:
            model_maintainer["Eq"][1] = []

        if model_number_dict['Sq_number'] > 0:
            model_maintainer["Sq"][1] = random.sample(tmp_list, int(model_number_dict['Sq_number']//group_size_factor))
            tmp_list = [e for e in tmp_list if e not in model_maintainer["Sq"][1]]
        else:
            model_maintainer["Sq"][1] = []

        if model_number_dict['I_number'] > 0:
            model_maintainer["I"][1] = random.sample(tmp_list, int(model_number_dict['I_number']//group_size_factor))
            tmp_list = [e for e in tmp_list if e not in model_maintainer["I"][1]]
        else:
            model_maintainer["I"][1] = []

        # if model_number_dict['I_number'] > 0:
        #     I_number_split_1, I_number_split_2 = SEIR_utils.split_number(model_number_dict['I_number'])
        #     model_maintainer["I"][0] = int(I_number_split_1)
        #     model_maintainer["I"][1] = random.sample(tmp_list, int(I_number_split_1))
        #     tmp_list = [e for e in tmp_list if e not in model_maintainer["I"][1]]
        #     read_path = people_interactive_graph_path
        #
        #     with open(read_path, "rb") as G_input_file:
        #         z = pickle.load(G_input_file)
        #         # print(f"z: {z}")
        #         # print(f"z_type: {type(z)}")
        #         # print(f"read_path: {read_path}")
        #         G = self.build_edge(z, day, hour)
        #     mask_i_possible_list = []
        #
        #     for infect_person in model_maintainer["I"][1]:
        #         if G.has_node(infect_person):
        #             successors_list = G.successors(infect_person)
        #             mask_i_possible_list.extend(successors_list)
        #             for successors in successors_list:
        #                 mask_i_possible_list.extend(G.successors(successors))
        #     mask_i_possible_list = [e for e in mask_i_possible_list if e in tmp_list]
        #     model_maintainer.update({"Mask_I": [I_number_split_2, []]})
        #
        #     if int(I_number_split_2 - 5) < len(mask_i_possible_list) and int(I_number_split_2 - 5) > 0:
        #         print(f"I_number_split_2;{int(I_number_split_2 - 5)}")
        #         print(f"len I;{len(mask_i_possible_list)}")
        #         model_maintainer["Mask_I"][1] = random.sample(mask_i_possible_list, int(I_number_split_2 - 5))
        #         tmp_list = [e for e in tmp_list if e not in model_maintainer["Mask_I"][1]]
        #         other = random.sample(tmp_list, 5)
        #         model_maintainer["Mask_I"][1].extend(other)
        #     else:
        #         model_maintainer["Mask_I"][1] = random.sample(mask_i_possible_list, len(mask_i_possible_list))
        #         tmp_list = [e for e in tmp_list if e not in model_maintainer["Mask_I"][1]]
        #         if I_number_split_2 - len(mask_i_possible_list) >= 0:
        #             other = random.sample(tmp_list, I_number_split_2)
        #             model_maintainer["Mask_I"][1].extend(other)
        #
        #     # add back to I
        #     model_maintainer["I"][0] = model_maintainer["I"][0] + model_maintainer["Mask_I"][0]
        #     model_maintainer["I"][1].extend(model_maintainer["Mask_I"][1])
        # else:
        #     model_maintainer["I"][1] = []

        # if model_number_dict['E_number'] > 0:
        #     mask_i_possible_list = []
        #     combine_I = []
        #     combine_I.extend(model_maintainer["I"][1])
        #     # combine_I.extend(model_maintainer["Mask_I"][1])
        #     for infect_person in combine_I:
        #         if G.has_node(infect_person):
        #             successors_list = G.successors(infect_person)
        #             mask_i_possible_list.extend(successors_list)
        #     mask_i_possible_list = [e for e in mask_i_possible_list if e in tmp_list]
        #     E_number = model_number_dict['E_number'];
        #     if model_number_dict['E_number'] > len(mask_i_possible_list):
        #         E_number = len(mask_i_possible_list)
        #         model_maintainer["E"][0] = E_number
        #         print("E_number change", E_number)
        #     model_maintainer["E"][1] = random.sample(mask_i_possible_list, E_number)
        #     model_maintainer["E"][0] = len(model_maintainer["E"][1])
        #     tmp_list = [e for e in tmp_list if e not in model_maintainer["E"][1]]
        # else:
        #     model_maintainer["E"][1] = []

        # init G
        read_path = people_interactive_graph_path

        with open(read_path, "rb") as G_input_file:
            z = pickle.load(G_input_file)
            # print(f"z: {z}")
            # print(f"z_type: {type(z)}")
            # print(f"read_path: {read_path}")
            G = self.build_edge(z, day, hour)

        if model_number_dict['E_number'] > 0:
            E_possible_list = []

            for infect_person in model_maintainer["I"][1]:
                if G.has_node(infect_person):
                    E_possible_list.extend(list(G.successors(infect_person)))

            num_E_from_possible_list = model_number_dict['E_number']
            num_E_from_S = 0

            if model_number_dict['E_number'] > len(E_possible_list):
                num_E_from_S = model_number_dict['E_number'] - len(E_possible_list)
                num_E_from_possible_list = len(E_possible_list)
            model_maintainer["E"][1] = random.sample(E_possible_list, num_E_from_possible_list)
            model_maintainer["E"][0] = len(model_maintainer["E"][1])

            if num_E_from_S > 0:
                model_maintainer["E"][1].extend(random.sample(tmp_list, num_E_from_S))
                model_maintainer["E"][0] = len(model_maintainer["E"][1])

            tmp_list = [e for e in tmp_list if e not in model_maintainer["E"][1]]
        else:
            model_maintainer["E"][1] = []
            model_maintainer["E"][0] = 0

        if model_number_dict['S_number'] > 0:
            model_maintainer["S"][1] = random.sample(tmp_list, int(model_number_dict['S_number']))
            # tmp_list = [e for e in tmp_list if e not in model_maintainer["S"][1]]
        else:
            model_maintainer["S"][1] = []

        return model_maintainer

    # S-->E-->|I|-->R
    # S-->Sq-->S
    # S-->Eq-->H-->R
    # S-->E-->|I|-->H-->R
    def model_update(self, day, hour, old_model_maintainer, next_time_step):
        matfn = SEIR_simulation_result_statistic
        model = sio.loadmat(matfn)["AA"]
        tmp_id_list = self.find_tmp_id_list()
        # {key:type,value:[chage_number,[id_1,id_2,id_3...]]}
        print("next_time_step", next_time_step)
        new_model_maintainer, model_number_dict = SEIR_utils.init_model_maintainer(model, next_time_step,
                                                                                   wearing_mask_probability[
                                                                                       current_status])

        old_S_number = old_model_maintainer["S"][0]
        old_E_number = old_model_maintainer["E"][0]
        old_I_number = old_model_maintainer["I"][0]
        old_Sq_number = old_model_maintainer["Sq"][0]
        old_Eq_number = old_model_maintainer["Eq"][0]
        old_H_number = old_model_maintainer["H"][0]
        old_R_number = old_model_maintainer["R"][0]

        new_model_maintainer["S"][1] = old_model_maintainer["S"][1]
        new_model_maintainer["E"][1] = old_model_maintainer["E"][1]
        new_model_maintainer["I"][1] = old_model_maintainer["I"][1]
        new_model_maintainer["R"][1] = old_model_maintainer["R"][1]
        new_model_maintainer["Sq"][1] = old_model_maintainer["Sq"][1]
        new_model_maintainer["Eq"][1] = old_model_maintainer["Eq"][1]
        new_model_maintainer["H"][1] = old_model_maintainer["H"][1]

        update_flag = False

        # R update (1) from old I and old H
        R_number = int(model_number_dict['R_number'])
        old_R_number = int(old_model_maintainer["R"][0])

        if R_number >= old_R_number:
            delta_R = R_number - old_R_number

            R_number_from_H = old_model_maintainer["H"][0] if old_model_maintainer["H"][
                                                                  0] < delta_R // 2 else delta_R // 2
            R_number_from_I = old_model_maintainer["I"][0] if old_model_maintainer["I"][0] < (
                    delta_R - R_number_from_H) else (delta_R - R_number_from_H)

            new_model_maintainer["R"][1].extend(random.sample(old_model_maintainer["I"][1], R_number_from_I))
            new_model_maintainer["R"][0] = len(new_model_maintainer["R"][1])
            old_model_maintainer["I"][1] = [e for e in old_model_maintainer["I"][1] if
                                            e not in new_model_maintainer["R"][1]]
            old_model_maintainer["I"][0] = len(old_model_maintainer["I"][1])

            new_model_maintainer["R"][1].extend(random.sample(old_model_maintainer["H"][1], R_number_from_H))
            new_model_maintainer["R"][0] = len(new_model_maintainer["R"][1])
            old_model_maintainer["H"][1] = [e for e in old_model_maintainer["H"][1] if
                                            e not in new_model_maintainer["R"][1]]
            old_model_maintainer["H"][0] = len(old_model_maintainer["H"][1])

            update_flag = True
        else:
            new_model_maintainer["R"][1] = old_model_maintainer["R"][1]
            new_model_maintainer["R"][0] = len(new_model_maintainer["R"][1])

        # H update (5) from old Eq and old I
        H_number = int(model_number_dict['H_number'])
        old_H_number = int(old_model_maintainer["H"][0])

        if H_number >= old_H_number:
            delta_H = H_number - old_H_number
            H_number_from_Eq = old_model_maintainer["Eq"][0] if old_model_maintainer["Eq"][
                                                                    0] < delta_H // 2 else delta_H // 2
            H_number_from_I = old_model_maintainer["I"][0] if old_model_maintainer["I"][0] < (
                    delta_H - H_number_from_Eq) else (delta_H - H_number_from_Eq)

            new_model_maintainer["H"][1].extend(random.sample(old_model_maintainer["I"][1], H_number_from_I))
            new_model_maintainer["H"][0] = len(new_model_maintainer["H"][1])
            old_model_maintainer["I"][1] = [e for e in old_model_maintainer["I"][1] if
                                            e not in new_model_maintainer["H"][1]]
            old_model_maintainer["I"][0] = len(old_model_maintainer["I"][1])

            new_model_maintainer["H"][1].extend(random.sample(old_model_maintainer["Eq"][1], H_number_from_Eq))
            new_model_maintainer["H"][0] = len(new_model_maintainer["H"][1])
            old_model_maintainer["Eq"][1] = [e for e in old_model_maintainer["Eq"][1] if
                                             e not in new_model_maintainer["H"][1]]
            old_model_maintainer["Eq"][0] = len(old_model_maintainer["Eq"][1])

            update_flag = True
        else:
            new_model_maintainer["H"][1] = old_model_maintainer["H"][1]
            new_model_maintainer["H"][0] = len(new_model_maintainer["H"][1])

        # I update (2) from old E
        I_number = int(model_number_dict['I_number'])
        old_I_number = int(old_model_maintainer["I"][0])

        if I_number >= old_I_number:
            delta_I = I_number - old_I_number
            delta_I_from_E = old_model_maintainer["E"][0] if old_model_maintainer["E"][0] < delta_I else delta_I

            new_model_maintainer["I"][1].extend(random.sample(old_model_maintainer["E"][1], delta_I_from_E))
            new_model_maintainer["I"][0] = len(new_model_maintainer["I"][1])
            old_model_maintainer["E"][1] = [e for e in old_model_maintainer["E"][1] if
                                            e not in new_model_maintainer["I"][1]]
            old_model_maintainer["E"][0] = len(old_model_maintainer["E"][1])
            update_flag = True
        else:
            new_model_maintainer["I"][1] = old_model_maintainer["I"][1]
            new_model_maintainer["I"][0] = old_model_maintainer["I"][0]

        # Ready the IDG to decide E from I
        read_path = graph_path_root + str(day) + "_" + str(int(hour))
        with open(read_path, "rb") as graph_input_file:
            z = pickle.load(graph_input_file)
            G = self.build_edge(z, day, hour)
        possible_list = []

        for infect_person in new_model_maintainer["I"][1]:

            if G.has_node(infect_person):
                successors_list = G.successors(infect_person)
                possible_list.extend(successors_list)
        # 避免閉環
        e_possible_list = [e for e in possible_list if e in old_model_maintainer["S"][1]]
        e_possible_list = [e for e in e_possible_list if e in tmp_id_list]
        eq_possible_list = [e for e in possible_list if e in old_model_maintainer["Sq"][1]]
        eq_possible_list = [e for e in eq_possible_list if e in tmp_id_list]

        # E update (3) from old S affected by old I
        E_number = int(model_number_dict['E_number'])
        old_E_number = int(old_E_number)

        if E_number >= old_E_number:
            delta_E = E_number - old_E_number
            len_new_S = len(old_model_maintainer["S"][1])

            if len_new_S < delta_E:
                delta_E = len_new_S

            # sup_E 避免可能的候選者太少的情況下 隨機選取S狀態中的剩餘者
            sup_E = 0

            if delta_E > len(e_possible_list):
                sup_E = delta_E - len(e_possible_list)
                delta_E = len(e_possible_list)
                new_model_maintainer["E"][0] = delta_E
            old_model_maintainer["E"][1].extend(random.sample(e_possible_list, delta_E))
            new_model_maintainer["E"][1] = old_model_maintainer["E"][1]
            new_model_maintainer["E"][0] = len(new_model_maintainer["E"][1])
            old_model_maintainer["S"][1] = [e for e in old_model_maintainer["S"][1] if
                                            e not in new_model_maintainer["E"][1]]
            old_model_maintainer["S"][0] = len(old_model_maintainer["S"][1])
            sup_E_list = random.sample(old_model_maintainer["S"][1], sup_E)
            new_model_maintainer["E"][1].extend(sup_E_list)
            new_model_maintainer["E"][0] = len(new_model_maintainer["E"][1])
            old_model_maintainer["S"][1] = [e for e in old_model_maintainer["S"][1] if e not in sup_E_list]
            old_model_maintainer["S"][0] = len(old_model_maintainer["S"][1])
            update_flag = True
        else:
            # sup_E 避免可能的候選者太少的情況下 隨機選取S狀態中的剩餘者
            sup_E = len(e_possible_list)
            sup_E_list = random.sample(old_model_maintainer["S"][1], sup_E)
            new_model_maintainer["E"][1].extend(sup_E_list)
            new_model_maintainer["E"][0] = len(new_model_maintainer["E"][1])
            old_model_maintainer["S"][1] = [e for e in old_model_maintainer["S"][1] if e not in sup_E_list]
            old_model_maintainer["S"][0] = len(old_model_maintainer["S"][1])
            update_flag = True

        # Eq update (4) from Sq, S, and E affected by I
        Eq_number = int(model_number_dict['Eq_number'])
        old_Eq_number = int(old_model_maintainer["Eq"][0])

        if Eq_number >= old_Eq_number:
            delta_Eq = Eq_number - old_Eq_number
            delta_Eq_from_E = new_model_maintainer["E"][0] if new_model_maintainer["E"][
                                                                  0] < delta_Eq // 3 else delta_Eq // 3
            delta_Eq_from_Sq = old_model_maintainer["Sq"][0] if old_model_maintainer["Sq"][
                                                                    0] < delta_Eq // 3 else delta_Eq // 3
            delta_Eq_from_S = old_model_maintainer["S"][0] if old_model_maintainer["Sq"][0] < (
                    delta_Eq - delta_Eq_from_E - delta_Eq_from_Sq) else (
                    delta_Eq - delta_Eq_from_E - delta_Eq_from_Sq)

            # update Eq from old S
            old_model_maintainer["Eq"][1].extend(random.sample(old_model_maintainer["S"][1], delta_Eq_from_S))
            new_model_maintainer["Eq"][1] = old_model_maintainer["Eq"][1]
            new_model_maintainer["Eq"][0] = len(new_model_maintainer["Eq"][1])
            old_model_maintainer["S"][1] = [e for e in old_model_maintainer["S"][1] if
                                            e not in new_model_maintainer["Eq"][1]]
            old_model_maintainer["S"][0] = len(old_model_maintainer["S"][1])

            # update Eq from new E
            new_model_maintainer["Eq"][1].extend(random.sample(new_model_maintainer["E"][1], delta_Eq_from_E))
            new_model_maintainer["Eq"][0] = len(new_model_maintainer["Eq"][1])
            new_model_maintainer["E"][1] = [e for e in new_model_maintainer["E"][1] if
                                            e not in new_model_maintainer["Eq"][1]]
            new_model_maintainer["E"][0] = len(new_model_maintainer["E"][1])

            # update Eq from old Sq
            new_model_maintainer["Eq"][1].extend(random.sample(new_model_maintainer["Sq"][1], delta_Eq_from_Sq))
            new_model_maintainer["Eq"][0] = len(new_model_maintainer["Eq"][1])
            old_model_maintainer["Sq"][1] = [e for e in old_model_maintainer["Sq"][1] if
                                             e not in new_model_maintainer["Eq"][1]]
            old_model_maintainer["Sq"][0] = len(old_model_maintainer["Sq"][1])

            update_flag = True
        else:
            sup_Eq = len(eq_possible_list)
            sup_Eq_list = random.sample(old_model_maintainer["Sq"][1], sup_Eq)
            new_model_maintainer["Eq"][1].extend(sup_Eq_list)
            new_model_maintainer["Eq"][0] = len(new_model_maintainer["Eq"][1])
            old_model_maintainer["Sq"][1] = [e for e in old_model_maintainer["Sq"][1] if e not in sup_Eq_list]
            old_model_maintainer["Sq"][0] = len(old_model_maintainer["Sq"][1])
            update_flag = True

        # Sq update from new S
        Sq_number = int(model_number_dict['Sq_number'])
        old_Sq_number = int(old_model_maintainer["Sq"][0])

        if Sq_number >= old_Sq_number:
            delta_Sq = Sq_number - old_Sq_number
            delta_Sq_from_S = old_model_maintainer["S"][0] if old_model_maintainer["S"][0] < delta_Sq else delta_Sq
            new_model_maintainer["Sq"][1].extend(random.sample(old_model_maintainer["S"][1], delta_Sq_from_S))
            new_model_maintainer["Sq"][0] = len(new_model_maintainer["Sq"][1])
            old_model_maintainer["S"][1] = [e for e in old_model_maintainer["S"][1] if
                                            e not in new_model_maintainer["Sq"][1]]
            old_model_maintainer["S"][0] = len(old_model_maintainer["S"][1])
            update_flag = True
        else:
            new_model_maintainer["Sq"][1] = old_model_maintainer["Sq"][1]
            new_model_maintainer["Sq"][0] = len(new_model_maintainer["Sq"][1])

        new_model_maintainer["S"][0] = old_model_maintainer["S"][0]
        new_model_maintainer["S"][1] = old_model_maintainer["S"][1]

        return new_model_maintainer, update_flag
