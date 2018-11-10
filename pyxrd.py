# author: Shanyao

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os


def find_start_row(csv_file):
    pass


def setup_data(file_path):
    # 读取文件夹下所有的csv文件并汇总
    file_path = "test_data"
    files = os.listdir(file_path)
    csv_files = []
    for file in files:
        if file.endswith(".csv"):
            csv_files.append(file)

    df1 = pd.read_csv(os.path.join(file_path, csv_files[0]), skiprows=25)

    if len(csv_files) >= 1:
        for file in csv_files[1:]:
            filename = os.path.join(file_path, file)
            print(filename)
            df2 = pd.read_csv(filename, skiprows=26)
            df1 = pd.concat([df1, df2], axis=1)

    return df1


def find_proper_lim(df):
    pass


def plot_subplot_xrd(df, ignore_intensity=True):
    num = int(df.columns.shape[0] / 2)

    for i in range(num):
        plt.subplot(num, 1, i + 1)
        theta = df.iloc[:, 2 * i]
        intensity = df.iloc[:, 2 * i + 1]

        plt.plot(theta, intensity)

        if ignore_intensity:
            plt.yticks([])
        plt.xlim([20, 80])
        plt.ylim([np.max(intensity)*(-0.5), np.max(intensity)*1.2])

        plt.ylabel("Intensity(a.u.)")
    plt.xlabel(r"2$\theta$")
    plt.show()


def plot_total_xrd(df):
    pass


plot_subplot_xrd(setup_data("test_data"))




