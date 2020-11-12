# normal module
import math
from operator import add
from os.path import isfile

import networkx as nx

# custom module
from CLIIP_module.constant import gen_graph_path_network_x


class model_util:
    def __init__(self, search_day: int, search_hour: int):
        self.search_day = search_day
        self.search_hour = search_hour
        self.iter_time = 0
        self.graph_path = ""
        self.uni_G = None

        graph_path = gen_graph_path_network_x(self.search_day, self.search_hour)
        if not graph_path == self.graph_path or self.uni_G is None:
            try:
                if isfile(graph_path):
                    self.uni_G = nx.read_gpickle(graph_path)
            except EOFError:
                print("load model_G fail")
                pass

    def get_train_data_X(self, model_maintainer, person):
        '''
        find model input X

        :param search_day:
        :param search_hour:
        :param model_maintainer:
        :param person:
        :return final_X:[sigma(deltaT/deltaD),I1,I2,I3,E1,E2,E3]
        '''
        checked_people = []
        deltaT, deltaD_reverse, result_I, result_E = self.start_finding(self.search_day, self.search_hour,
                                                                        model_maintainer,
                                                                        person, checked_people)
        element = []
        element.append(deltaT)
        element.append(deltaD_reverse)
        element.extend(result_I)
        element.extend(result_E)
        final_X = element

        return final_X

    def start_finding(self, search_day, search_hour, model_maintainer, person, checked_people, layer=None,
                      result_I=None, result_E=None,
                      limit_layer=3):

        # control layer searching
        if result_E is None:
            result_E = [0, 0, 0]
        if result_I is None:
            result_I = [0, 0, 0]
        if layer is None:
            layer = 0
        #     iter_time = iter_time - 1
        # #     print(iter_time)
        #     if iter_time < 0:
        # #         print("return")
        #         return 0, 0, result_I, result_E
        if person in checked_people:
            # print(f"person:{person}")
            # print(f"checked_person:{checked_people}")
            return 0, 0, result_I, result_E

        if limit_layer != -1:
            if limit_layer - layer == 0:
                return 0, 0, result_I, result_E
        person_in = False
        if person in self.uni_G:
            person_in = True
        if person_in:
            predecessors = self.uni_G.predecessors(person)

            deltaT = 0
            deltaD_reverse = 0
            max_flag = False
            for predecessor in predecessors:
                if layer == 0:
                    edge_attribute = self.uni_G.get_edge_data(predecessor, person,
                                                              default={'distance': math.inf, 'delta_time': 0,
                                                                       'start_time': 0})
                    e_distance = edge_attribute['distance']
                    if "delta" in edge_attribute:
                        e_delta = edge_attribute['delta']
                    else:
                        e_delta = edge_attribute['delta_time']
                    if e_distance == 0:
                        deltaD_reverse = math.inf
                        max_flag = True
                    else:
                        if max_flag:
                            deltaT += e_delta
                        else:
                            deltaD_reverse += (1 / e_distance) ** 2
                            deltaT += e_delta
                if predecessor in model_maintainer["I"][1]:
                    # stop finding next layer
                    result_I[layer] = result_I[layer] + 1
                if predecessor in model_maintainer["E"][1]:
                    result_E[layer] = result_E[layer] + 1

                next_layer = layer + 1
                checked_people.append(predecessor)
                deprecate1, deprecate2, n_result_I, n_result_E = self.start_finding(
                    search_day, search_hour, model_maintainer, predecessor, checked_people, next_layer)

                list(map(add, result_I, n_result_I))
                list(map(add, result_E, n_result_E))
        else:
            return 0, 0, result_I, result_E
        return deltaT, deltaD_reverse, result_I, result_E
