# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 10:17:31 2024

@author: twright


Load espion export data and plot all ERG recordings.
Requires package espion_tools `pip install espion_tools`

"""

from espion_tools import parse_espion_export
import matplotlib.pyplot as plt
import numpy as np
import os
import re
from matplotlib.backends.backend_pdf import PdfPages

base_folder = 'Data/Data Phase II Cohort B/All .esp6 Files/'

folders = {'Baseline': 'Baseline Cohort B (4.11.2024)',
           'Day 8': 'Day 8 Phase II Cohort B (4.30.2024)',
           'Day 15': 'Day 15 Phase II Cohort B (5.7.2024)',
           'Day 22': 'Day 22 Phase II Cohort B (5.14.2024)',
           'Day 30': 'Day 30 Phase II Cohort B (5.22.2024)',
           'Day 38': 'Day 38 Phase II Cohort B (5.30.2024)'}

group_members = {'Group 1': (13080, 13081),
                 'Group 2': (13075, 13079),
                 'Group 3': (13076, 13077, 13078)}

steps_da = {'DA 0.001 cd.s/m2 + OP': 1,
            'DA 0.003 cd.s/m2 + OP': 2,
            'DA 0.01 cd.s/m2 + OP': 3,
            'DA 0.03 cd.s/m2 + OP': 4,
            'DA 0.1 cd.s/m2 + OP': 5,
            'DA 0.3 cd.s/m2 + OP': 6,
            'DA 1 cd.s/m2 + OP': 7,
            'DA 3 cd.s/m2 + OP': 8,
            'DA 10 cd.s/m2 + OP': 9,
            'CW 150 cd/m2': 10}

steps_la = {'LA 0.03 cd.s/m2 + OP': 1,
            'LA 0.3 cd.s/m2 + OP': 2,
            'LA 3 cd.s/m2 + OP': 3,
            'LA 3 cd.s/m2 10 Hz Flicker': 4,
            'LA 3 cd.s/m2 20 Hz Flicker': 5,
            'LA 3 cd.s/m2 30 Hz Flicker': 6,
            'LA 3 cd.s/m2 40 Hz Flicker': 7}


def get_test_data(subject_id, timepoint):
    """
    Load dark adapted and light adapted traces for a timepoint
    """
    filename_DA = 'Rabbit {} DA.esp6'.format(subject_id)
    filename_LA = 'Rabbit {} LA.esp6'.format(subject_id)

    folder = folders[timepoint]

    try:
        filepath_DA = os.path.join(base_folder, folder, filename_DA)
        filepath_LA = os.path.join(base_folder, folder, filename_LA)

        data_DA = parse_espion_export.load_file(filepath_DA)[1]
        data_LA = parse_espion_export.load_file(filepath_LA)[1]
    except:
        raise UserWarning('Failed to load subject:{}, timepoint:{}'
                          .format(subject_id, timepoint))
        return

    return ((data_DA, data_LA))


def plot_traces_da(data, subject, timepoint):
    pattern = re.compile(r"((DA|LA|CW) \d+.\d*)")

    for step, step_idx in steps_da.items():
        m = pattern.match(step)
        stim = m.group(1).strip()
        data_od = data[0]['data'][step_idx].channels[1].results[1].data.values
        data_os = data[0]['data'][step_idx].channels[2].results[1].data.values

        data_od = [i/1000 for i in data_od]
        data_os = [i/1000 for i in data_os]

        start_ms = data[0]['data'][step_idx].channels[1].results[1].data.start
        interval_ms = data[0]['data'][step_idx].channels[1].results[1].data.delta

        x_vals = np.linspace(start=start_ms,
                             stop=(len(data_od) * 0.5) + start_ms,
                             num=len(data_od))

        plt.plot(x_vals, data_od)
        plt.ylim(-150, 250)
        plt.xlabel("Time (ms)")
        plt.ylabel("Amplitude (uV)")
        plt.title("Subject:{} {} Stim:{} Eye:{}".format(subject,
                                                        timepoint,
                                                        stim,
                                                        'OD'))
        fname = "{}_{}_{}_{}.png".format(subject,
                                         timepoint,
                                         stim,
                                         "OD")
        fname = os.path.join('Traces', fname)

        plt.savefig(fname, bbox_inches='tight')
        plt.close()

        plt.plot(x_vals, data_os)
        plt.ylim(-150, 250)
        plt.xlabel("Time (ms)")
        plt.ylabel("Amplitude (uV)")
        plt.title("Subject:{} {} Stim:{} Eye:{}".format(subject,
                                                        timepoint,
                                                        stim,
                                                        'OS'))
        fname = "{}_{}_{}_{}.png".format(subject,
                                         timepoint,
                                         stim,
                                         "OS")
        fname = os.path.join('Traces', fname)
        plt.savefig(fname, bbox_inches='tight')
        plt.close()


def plot_traces_la(data, subject, timepoint):
    pattern = re.compile(r"((DA|LA|CW) \d+.\d*)")
    pattern2 = re.compile(r".*(\d{2} Hz Flicker)")

    for step, step_idx in steps_la.items():
        m = pattern.match(step)
        m2 = pattern2.match(step)

        if m2:
            is_flicker = True
            stim = m2.group(1).strip()
        else:
            is_flicker = False
            stim = m.group(1).strip()

        data_od = data[1]['data'][step_idx].channels[1].results[1].data.values
        data_os = data[1]['data'][step_idx].channels[2].results[1].data.values

        data_od = [i/1000 for i in data_od]
        data_os = [i/1000 for i in data_os]

        start_ms = data[1]['data'][step_idx].channels[1].results[1].data.start
        interval_ms = data[1]['data'][step_idx].channels[1].results[1].data.delta

        x_vals = np.linspace(start=start_ms,
                             stop=(len(data_od) * 0.5) + start_ms,
                             num=len(data_od))

        plt.plot(x_vals, data_od)
        if is_flicker:
            plt.ylim(-50, 75)
        else:
            plt.ylim(-150, 75)
        plt.xlabel("Time (ms)")
        plt.ylabel("Amplitude (uV)")
        plt.title("Subject:{} {} Stim:{} Eye:{}".format(subject,
                                                        timepoint,
                                                        stim,
                                                        'OD'))
        fname = "{}_{}_{}_{}.png".format(subject,
                                         timepoint,
                                         stim,
                                         "OD")
        fname = os.path.join('Traces', fname)
        plt.savefig(fname, bbox_inches='tight')
        plt.close()

        plt.plot(x_vals, data_os)
        plt.xlabel("Time (ms)")
        plt.ylabel("Amplitude (uV)")
        plt.title("Subject:{} {} Stim:{} Eye:{}".format(subject,
                                                        timepoint,
                                                        stim,
                                                        'OS'))

        fname = "{}_{}_{}_{}.png".format(subject,
                                         timepoint,
                                         stim,
                                         "OS")
        fname = os.path.join('Traces', fname)

        plt.savefig(fname, bbox_inches='tight')
        plt.close()


if __name__ == '__main__':
    for group, subjects in group_members.items():
        for subject in subjects:
            for timepoint in folders:
                try:
                    data = get_test_data(subject, timepoint)
                except UserWarning:
                    continue
                plot_traces_da(data, subject, timepoint)
                plot_traces_la(data, subject, timepoint)
