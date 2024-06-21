# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 11:47:26 2024

@author: twright
"""

from espion_tools import parse_espion_export
import numpy as np
import os
import csv

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


def write_markers_da(data, csvwriter, group, subject, timepoint):
    for step, idx in steps_da.items():
        step_description = step
        step_markers = data[0]['markers'][idx]
        for marker in step_markers:
            chan = marker['chan']
            eye = marker['eye']
            name = marker['name']
            amp = marker['amp']
            time = marker['time']
            csvwriter.writerow([subject,
                                group,
                                timepoint,
                                step_description,
                                'DA',
                                chan,
                                eye,
                                name,
                                amp,
                                time])


def write_markers_la(data, csvwriter, group, subject, timepoint):
    for step, idx in steps_la.items():
        step_description = step
        step_markers = data[1]['markers'][idx]
        for marker in step_markers:
            chan = marker['chan']
            eye = marker['eye']
            name = marker['name']
            amp = marker['amp']
            time = marker['time']
            csvwriter.writerow([subject,
                                group,
                                timepoint,
                                step_description,
                                'LA',
                                chan,
                                eye,
                                name,
                                amp,
                                time])


if __name__ == '__main__':
    with open('Data/markers.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Subject', 'Group', 'Timepoint',
                         'Step', 'Condition', 'Chan', 'Eye', 'Marker', 'Amp', 'Time'])
        for group, members in group_members.items():
            for subject in members:
                for timepoint in folders:
                    try:
                        data = get_test_data(subject, timepoint)
                    except UserWarning:
                        continue
                    write_markers_da(data, writer, group, subject, timepoint)
                    write_markers_la(data, writer, group, subject, timepoint)
