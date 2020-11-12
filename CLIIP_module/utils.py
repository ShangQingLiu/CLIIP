import pickle
import time
from os.path import isfile


def timer(method):
    def timed(*args, **kwargs):
        time_start = time.time()
        result = method(*args, **kwargs)
        time_end = time.time()

        print(f'{method.__name__},{(time_start - time_end) * 1000} ms')


def save_pickle(path, data):
    if not isfile(path):
        with open(path, "wb") as input_file:
            pickle.dump(data, input_file)
