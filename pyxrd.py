# author: Shanyao

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import csv


def find_start_row(csv_file):
    csv_file = open(csv_file, "r")
    reader = csv.reader(csv_file)
    skip_row = 0
    for item in reader:
        if item[0] == 'Anode material':
            anode = item[1]

        if item[0] == 'Scan step size':
            step_size = item[1]

        if item[0] == 'Angle':
            break
        skip_row += 1

    return skip_row, anode, step_size


def setup_data(file_path):
    # 读取文件夹下所有的csv文件并汇总
    file_path = "test_data"
    files = os.listdir(file_path)
    csv_files = []
    for file in files:
        if file.endswith(".csv"):
            csv_files.append(file)

    skip_row, anode, step_size = find_start_row(os.path.join(file_path, csv_files[0]))

    df1 = pd.read_csv(os.path.join(file_path, csv_files[0]), skiprows=skip_row)

    if len(csv_files) >= 1:
        for file in csv_files[1:]:
            filename = os.path.join(file_path, file)
            print(filename)
            df2 = pd.read_csv(filename, skiprows=26)
            df1 = pd.concat([df1, df2], axis=1)

    return df1


def find_proper_lim(df, theta_lim, step_size):

    low_index = df[np.abs(df.iloc[:, 0] - theta_lim[0])<step_size].index[0]
    high_index = df[np.abs(df.iloc[:, 0] - theta_lim[1])<step_size].index[0]

    df = df.iloc[low_index:high_index, :]

    return df


def plot_subplot_xrd(df, theta_lim, step_size, ignore_intensity=True):
    num = int(df.columns.shape[0] / 2)

    df = find_proper_lim(df, theta_lim, step_size)

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


def plot_total_xrd(df, theta_lim, step_size, ignore_intensity=True):
    num = int(df.columns.shape[0] / 2)

    df = find_proper_lim(df, theta_lim, step_size)
    plt.figure()
    for i in range(num):
        theta = df.iloc[:, 2 * i]
        intensity = df.iloc[:, 2 * i + 1] + np.max(df.iloc[:, 2*i]) * 1

        plt.plot(theta, intensity)

        if ignore_intensity:
            plt.yticks([])

    plt.xlim(theta_lim)
    #plt.ylim([np.max(intensity)*(-0.2), np.max(intensity)*1.2])

    plt.ylabel("Intensity(a.u.)")
    plt.xlabel(r"2$\theta$")
    plt.show()


if __name__ == "__main__":
    #plot_subplot_xrd(setup_data("test_data"))

    plot_total_xrd(setup_data("test_data"), [10, 80], 0.02)



