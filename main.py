#!/usr/bin/env python3

#fitdecode from https://pypi.org/project/fitdecode/
import fitdecode
import time
from datetime import datetime, timedelta
import pytz

fit_file = 'example.fit'

def main():
    calculate_workout_duration(fit_file)
    calculate_workout_distance(fit_file)


def calculate_workout_distance(fit_file):
    distance = 0    # length of travelled distance in meters

    with fitdecode.FitReader(fit_file) as fit:
        for frame in fit:
            if isinstance(frame, fitdecode.FitDataMessage)  and frame.has_field('total_distance'):
                distance = frame.get_field('total_distance').value

        print("km: {:.2f}".format(distance/1000))


def calculate_workout_duration(fit_file):
    time_start = None
    total_time = 0     #length of workout in seconds

    with fitdecode.FitReader(fit_file) as fit:
        for frame in fit:
            if isinstance(frame, fitdecode.FitDataMessage)  and frame.has_field('timestamp'):
                if time_start == None:
                    time_start = frame.get_field('timestamp').value
                time_current = frame.get_field('timestamp').value
                dt = (time_current-time_start).total_seconds()
                total_time += dt
                time_start = time_current

    t = int(total_time/3600)
    m = int((total_time/60)%60)
    s = int(((total_time/60)/60)%60)

    print ("Time: {0} hours, {1} minutes and {2} seconds".format(t, m, s))


if __name__ == "__main__":
    main()