import time
import numpy as np
import backend
from datetime import datetime, timedelta, timezone
from sklearn import linear_model
from sklearn.preprocessing import PolynomialFeatures


def get_weekday_minutes(timestamp=-1):
    if timestamp == -1:
        timestamp = time.time()
    utc_time = datetime.utcfromtimestamp(timestamp).replace(
        tzinfo=timezone.utc)
    singapore_time = utc_time.astimezone(timezone(timedelta(hours=8)))

    weekday = singapore_time.weekday()
    minutes = singapore_time.hour * 60 + singapore_time.minute

    return weekday, minutes


WEEKDAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thuresday', 'Friday', 'Saturday', 'Sunday']

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

    return train_set


def get_predict_set():
    predict_set = {}
    for day in WEEKDAYS:
        predict_set[day] = np.arange(0, 60*60*24, 60*60).reshape(-1, 1)
    return predict_set

models = {}
order = 3

for d in WEEKDAYS:
    models[d] = linear_model.LinearRegression()

def train(trainset):
    for day, (x, y) in trainset.items():
        poly = PolynomialFeatures(order, include_bias=False)
        x = poly.fit_transform(x)
        models[day].fit(x, y)

def predict(day, x):
    poly = PolynomialFeatures(order, include_bias=False)
    x = poly.fit_transform(x)

    return models[day].predict(x)

def main():
    room = backend.get_room_arg()
    input_node = backend.FireBaseNode('NumberOfPeople', room, mode='r')
    output_node = backend.FireBaseNode('Prediction', room)

    # convert data to numpy
    trainset = convert_input(input_node.val)
    predictset = get_predict_set()

    # Train model
    print('Traning...')
    train(trainset)

    # Predict future time points
    print('Predicting....')
    result = {}
    for d, x_array in predictset.items():
        y_array = predict(d, x_array)
        result[d] = {int(x_array[i]/3600): int(y_array[i]) for i in range(y_array.shape[0])}
    print('Uploading....')
    output_node.val = result


if __name__ == "__main__":
    main()