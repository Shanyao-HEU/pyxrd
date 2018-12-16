# author: Shanyao

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import csv


class XrdFiles(object):

    def __init__(self, path):
        self.path = path

    def find_all_csv(self):

        files = os.listdir(self.path)
        csv_files = []
        for file in files:
            if file.endswith(".csv"):
                csv_files.append(os.path.join(self.path, file))

        return csv_files

    def choose_files(self, file_numbers):

        files_chosen = []
        for num in file_numbers:
            files_chosen.append(self.find_all_csv()[int(num)])

        return files_chosen

    def csv_to_df(self, csv_files):

        if csv_files:
            csv_file = csv_files[0]
        else:
            print("Please choose at least one csv file.")
            return
        try:
            csv_file = open(csv_file, "r")
            reader = csv.reader(csv_file)
            skip_row = 0
            for item in reader:
                if item[0] == 'Anode material':
                    anode = item[1]

                if item[0] == 'Scan range':
                    scan_range = [float(item[1]), float(item[2])]

                if item[0] == 'Scan step size':
                    step_size = item[1]

                if item[0] == 'Angle':
                    break
                skip_row += 1
        except:
            skip_row, anode, step_size, scan_range = 0, "cu", "0.02", [10, 80]

        print(anode, scan_range, step_size)
        df1 = pd.read_csv(csv_files[0], skiprows=skip_row)

        if len(csv_files) >= 1:
            for file in csv_files[1:]:
                print("Processing successful in {}".format(file))
                df2 = pd.read_csv(file, skiprows=skip_row)
                df1 = pd.concat([df1, df2], axis=1)

        #low_index = df1[np.abs(df1.iloc[:, 0] - scan_range[0]) == step_size].index[0]
        #high_index = df1[np.abs(df1.iloc[:, 0] - scan_range[1]) == step_size].index[0]

        #df = df1.iloc[low_index:high_index, :]

        return df1

class DealXrd(object):

    def __init__(self, df):
        self.df = df

    def smooth_df(self):

        return

    def find_peaks(self):

        return

    def fit_peaks(self):

        return

class PlotXrd(object):

    def __init__(self, df, scan_range, save_path):
        self.df = df
        self.scan_range = scan_range
        self.save_path = save_path
        self.num = self.df.shape[1] // 2

    def define_peak(self, num_phase_dic):

        return

    def plot_subplot_xrd(self, ignore_intensity=True):

        for i in range(self.num):
            plt.subplot(self.num, 1, i + 1)
            theta = self.df.iloc[:, 2 * i]
            intensity = self.df.iloc[:, 2 * i + 1]

            plt.plot(theta, intensity)

            if ignore_intensity:
                plt.yticks([])
            plt.xlim(self.scan_range)
            plt.ylim([np.max(intensity)*(-0.5), np.max(intensity)*1.2])

            plt.ylabel("Intensity(a.u.)")
        plt.xlabel(r"2$\theta$")
        plt.show()
        if self.save_path:
            plt.savefig(self.save_path+".png")

    def plot_total_xrd(self):


        plt.figure()
        for i in range(self.num):
            theta = self.df.iloc[:, 2 * i]
            intensity = self.df.iloc[:, 2 * i + 1] + np.max(self.df.iloc[:, 2*i]) * 1

            plt.plot(theta, intensity)

            plt.yticks([])

        plt.xlim(self.scan_range)
        #plt.ylim([np.max(intensity)*(-0.2), np.max(intensity)*1.2])

        plt.ylabel("Intensity(a.u.)")
        plt.xlabel(r"2$\theta$")
        plt.show()

    def plot_onebyone(self):

        for i in range(self.num):
            plt.figure(figsize=(8, 8))

            theta = self.df.iloc[:, 2 * i]
            intensity = self.df.iloc[:, 2 * i + 1]

            plt.plot(theta, intensity)


            plt.yticks([])
            plt.xlim(self.scan_range)
            plt.ylim([np.max(intensity)*(-0.5), np.max(intensity)*1.2])

            plt.ylabel("Intensity(a.u.)")
        plt.xlabel(r"2$\theta$")
        plt.show()
        if self.save_path:
            plt.savefig(self.save_path+".png")

    def plot_offset(self):


        plt.figure(figsize=(10, 8))

        y_max = 0
        for i in range(self.num):

            theta = self.df.iloc[:, 2 * i]
            intensity = self.df.iloc[:, 2 * i + 1]

            plt.plot(theta, intensity+y_max, "r")

            y_max += np.max(intensity)

        plt.yticks([])
        plt.xlim(self.scan_range)
        #plt.ylim([np.max(intensity)*(-0.5), np.max(intensity)*1.2])

        plt.ylabel("Intensity(a.u.)")
        plt.xlabel(r"2$\theta$")
        plt.show()
        if self.save_path:
            plt.savefig(self.save_path+".png")

if __name__ == "__main__":
    xrd = XrdFiles("F:/pyxrd/2018.11.2hayao/cu")
    xrd_files = xrd.find_all_csv()
    print("-----------")
    for i, xrd_file in enumerate(xrd_files):
        #print("Choose data in {} graph in: ".format(i))
        print("number: {}-----filename: {}".format(i, xrd_file))
    flag = input("Choose and enter: ")
    if flag:
        flag = [int(f) for f in flag.split()]
        df = xrd.csv_to_df(xrd.choose_files(flag))
    else:
        print("Done!")
    save_path = xrd.path + "result"
    plot1 = PlotXrd(df, [10, 80],save_path)
    plot1.plot_offset()
    #xrd.plot_onebyone()

