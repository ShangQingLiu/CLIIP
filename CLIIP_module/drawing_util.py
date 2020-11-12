import matplotlib.pyplot as plt
import pandas as pd

def draw_SEIR_process(data):
    # df = pd.DataFrame(Data, columns=['S', 'E', 'I', 'R', 'Mask_I', 'time_stamp'])
    df = pd.DataFrame(data, columns=['S', 'E', 'I', 'R', 'time_stamp'])
    # plt.plot(df['time_stamp'], df['S'], color='green', marker='o')
    plt.plot(df['time_stamp'], df['E'], color='yellow')
    plt.plot(df['time_stamp'], df['I'], color='red')
    plt.plot(df['time_stamp'], df['R'], color='blue')
    # plt.plot(df['time_stamp'], df['Mask_I'], color='pink' )
    plt.title('SEIR model', fontsize=14)
    plt.xlabel('Time Stamp', fontsize=14)
    plt.ylabel('Number', fontsize=14)
    plt.grid(True)
    plt.show()
