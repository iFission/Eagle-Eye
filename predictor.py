import time
import numpy as np
import backend
from datetime import datetime, timedelta, timezone


def get_weekday_minutes(timestamp=-1):
    if timestamp == -1:
        timestamp = time.time()
    utc_time = datetime.utcfromtimestamp(timestamp).replace(
        tzinfo=timezone.utc)
    singapore_time = utc_time.astimezone(timezone(timedelta(hours=8)))

    weekday = singapore_time.weekday()
    minutes = singapore_time.hour * 60 + singapore_time.minute

    return weekday, minutes


WEEKDAYS = [
    'Monday', 'Tuesday', 'Wednesday', 'Thuresday', 'Friday', 'Saturday',
    'Sunday'
]


def convert_input(data):
    train_set = {}
    for d in WEEKDAYS:
        train_set[d] = [], []

    for t, num_people in data.items():
        weekday, minutes = get_weekday_minutes(int(t))
        train_set[WEEKDAYS[weekday]][0].append([minutes * 60])
        train_set[WEEKDAYS[weekday]][1].append([num_people])
    for d in WEEKDAYS:
        train_set[d] = np.array(train_set[d][0]), np.array(train_set[d][1])

    # temporary code
    train_set['Monday'] = train_set['Friday']
    train_set['Tuesday'] = train_set['Friday']
    train_set['Wednesday'] = train_set['Friday']
    train_set['Sunday'] = train_set['Friday']

    return train_set


def get_future_time_points():
    weekday, minutes = get_weekday_minutes()
    return WEEKDAYS[weekday], np.array(
        [[m * 60] for m in range(minutes, 60 * 24, 10)])


def upload(x, y, node):
    content = {}
    for i in range(x.shape[0]):
        content[f'{x[i][0]}-{x[i][1]}'] = int(y[i][0])
    node.val = content


models = {}

for d in WEEKDAYS:
    models[d] = linear_model.LinearRegression()


def train(trainset):
    for day, (x, y) in trainset.items():
        order = 2
        poly = PolynomialFeatures(order, include_bias=False)
        x = poly.fit_transform(x)
        models[day].fit(x, y)


# can just save the model,can just call the linear regression


def predict(day, x):
    order = 2
    poly = PolynomialFeatures(order, include_bias=False)
    x = poly.fit_transform(x)

    return models[day].predict(x)


def main():
    room = 'Debug_Alex'  #backend.get_room_arg()
    input_node = backend.FireBaseNode('NumberOfPeople', room, mode='r')

    # convert data to numpy
    trainset = convert_input(input_node.val)
    predict_day, predict_time = get_future_time_points()

    # Train model
    train(trainset)

    # Predict future time points
    prediction = predict(predict_day, predict_time)


if __name__ == "__main__":
    main()


def convert_to_seconds(A):
    # take one string as a input like '8:30'
    y = A.split(':')
    # print(y)
    seconds = int(y[0]) * 3600 + int(y[1]) * 60 + int(y[2])
    # print(seconds)
    return seconds


#convert_to_seconds('8:30:23')
def convert_to_time(B):
    hour = B // 3600
    minutes = (B - 3600 * hour) // 60
    seconds = B - 3600 * hour - 60 * minutes
    return str(hour) + ':' + str(minutes) + ':' + str(seconds)


#convert_to_time(30623)


def time_table(C):
    Second = convert_to_seconds(C)
    lst = list(range(Second, 86430, 900))
    return lst


# time_table('8:30:30')


def convert_time_table(lst):
    result = []
    index = 0
    while index < len(lst):
        #print(lst[index])
        y = convert_to_time(lst[index])
        result.append(y)
        index += 1
        #print(lst[index])
    return result


# z = time_table('8:30:30')
# convert_time_table(z)

import os
import csv
import numpy as np
import numpy as np
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
