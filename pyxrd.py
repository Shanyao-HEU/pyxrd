# author: Shanyao

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import csv


class FindXRD(object):

    def __init__(self, path, theta_lim=[10, 80]):
        self.path = path
        self.theta_lim = theta_lim

    def find_all_csv(self):

        files = os.listdir(self.path)
        csv_files = []
        for file in files:
            if file.endswith(".csv"):
                csv_files.append(os.path.join(self.path, file))

        return csv_files

    def choose_files(self, file_numbers):

        file_chosen = []
        for num in file_numbers:
            file_chosen.append(self.find_all_csv()[int(num)])

        return file_chosen

    def csv_to_df(self, csv_files):

        skip_row, anode, step_size = self.find_start_row(csv_files)

        df1 = pd.read_csv(csv_files[0], skiprows=skip_row)

        if len(csv_files) >= 1:
            for file in csv_files[1:]:
                print("Processing successful in {}".format(file))
                df2 = pd.read_csv(file, skiprows=26)
                df1 = pd.concat([df1, df2], axis=1)

        return df1

    def find_proper_lim(self, df, theta_lim, tol=0.1):

        low_index = df[np.abs(df.iloc[:, 0] - theta_lim[0]) < tol].index[0]
        high_index = df[np.abs(df.iloc[:, 0] - theta_lim[1]) < tol].index[0]

        df = df.iloc[low_index:high_index, :]

        return df

    def find_start_row(self, csv_files):
        csv_file = csv_files[0]
        csv_file = open(csv_file, "r")
        reader = csv.reader(csv_file)
        skip_row, anode, step_size = 0, "cu", 0.02
        for item in reader:
            if item[0] == 'Anode material':
                anode = item[1]

            if item[0] == 'Scan step size':
                step_size = item[1]

            if item[0] == 'Angle':
                break
            skip_row += 1

        return skip_row, anode, step_size

    def plot_subplot_xrd(self, save_fig="", ignore_intensity=True):

        df = self.csv_to_df()
        num = int(df.columns.shape[0] / 2)
        df = self.find_proper_lim(df, self.theta_lim)
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
        if save_fig:
            plt.savefig(save_fig+".png")

    def plot_total_xrd(self, df, ignore_intensity=True):
        num = int(df.columns.shape[0] / 2)

        df = self.find_proper_lim(df, self.theta_lim)
        plt.figure()
        for i in range(num):
            theta = df.iloc[:, 2 * i]
            intensity = df.iloc[:, 2 * i + 1] + np.max(df.iloc[:, 2*i]) * 1

            plt.plot(theta, intensity)

            if ignore_intensity:
                plt.yticks([])

        plt.xlim(self.theta_lim)
        #plt.ylim([np.max(intensity)*(-0.2), np.max(intensity)*1.2])

        plt.ylabel("Intensity(a.u.)")
        plt.xlabel(r"2$\theta$")
        plt.show()

    def plot_onebyone(self, save_fig="", ignore_intensity=True):

        df = self.csv_to_df()
        num = int(df.columns.shape[0] / 2)
        df = self.find_proper_lim(df, self.theta_lim)
        for i in range(num):
            plt.figure(figsize=(8, 8))

            theta = df.iloc[:, 2 * i]
            intensity = df.iloc[:, 2 * i + 1]

            plt.plot(theta, intensity)

            if ignore_intensity:
                plt.yticks([])
            plt.xlim(self.theta_lim)
            plt.ylim([np.max(intensity)*(-0.5), np.max(intensity)*1.2])

            plt.ylabel("Intensity(a.u.)")
        plt.xlabel(r"2$\theta$")
        plt.show()
        if save_fig:
            plt.savefig(save_fig+".png")

    def plot_offset(self, csv_files):
        df = self.csv_to_df(csv_files)
        num = int(df.columns.shape[0] / 2)
        df = self.find_proper_lim(df, self.theta_lim)

        plt.figure(figsize=(10, 8))

        y_max = 0
        for i in range(num):

            theta = df.iloc[:, 2 * i]
            intensity = df.iloc[:, 2 * i + 1]

            plt.plot(theta, intensity+y_max, "r")

            y_max += np.max(intensity)
            print(y_max)


        plt.yticks([])
        plt.xlim(self.theta_lim)
        #plt.ylim([np.max(intensity)*(-0.5), np.max(intensity)*1.2])

        plt.ylabel("Intensity(a.u.)")
        plt.xlabel(r"2$\theta$")
        plt.show()

if __name__ == "__main__":
    xrd = FindXRD("2018.11.2hayao/cu")
    xrd_files = xrd.find_all_csv()
    print("-----------")
    for i, xrd_file in enumerate(xrd_files):
        #print("Choose data in {} graph in: ".format(i))
        print("number: {}-----filename: {}".format(i, xrd_file))
    flag = input("Choose and enter: ")
    if flag:
        flag = [int(f) for f in flag.split()]
        csv_files = xrd.choose_files(flag)
    else:
        csv_files = xrd.find_all_csv()

    xrd.plot_offset(csv_files)
    #xrd.plot_onebyone()

