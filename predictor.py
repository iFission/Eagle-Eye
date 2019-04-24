import time
import numpy as np
import backend
from datetime import datetime, timedelta, timezone
from sklearn import linear_model
from sklearn.preprocessing import PolynomialFeatures


def get_weekday_minutes(timestamp=-1):
    ''' Convert unix timestamp to weekday and minutes w.r.t Singapore time '''
    if timestamp == -1:
        timestamp = time.time()
    # get utc date time
    utc_time = datetime.utcfromtimestamp(timestamp).replace(
        tzinfo=timezone.utc)
    # convert to singapore date time
    singapore_time = utc_time.astimezone(timezone(timedelta(hours=8)))

    # get weekday and minutes from datetime instance
    weekday = singapore_time.weekday()
    minutes = singapore_time.hour * 60 + singapore_time.minute

    return weekday, minutes


WEEKDAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

def convert_input(data):
    ''' get train set from firebase raw data 
    Args:
        data: a timestamp->num_of_people dictionary
    Returns:
        a dictionary map weekday to corresponding x, y trainset
        where x is a (-1, 1) numpy array which is the minutes from start of the day
        y is a (-1, 1) array of corresponding number of people
    '''

    # inits train_set dictionary
    train_set = {}
    for d in WEEKDAYS:
        train_set[d] = [], []

    # go through every data point in raw data
    for t, num_people in data.items():
        # get weekday and minutes from timestamp
        weekday, minutes = get_weekday_minutes(int(t))
        # append new data to result list
        train_set[WEEKDAYS[weekday]][0].append([minutes * 60])
        train_set[WEEKDAYS[weekday]][1].append([num_people])
    # convert list to numpy array
    for d in WEEKDAYS:
        train_set[d] = np.array(train_set[d][0]), np.array(train_set[d][1])

    return train_set


def get_predict_set():
    ''' Return a dictionary including every weekday and every hour(in seconds)'''
    predict_set = {}
    for day in WEEKDAYS:
        predict_set[day] = np.arange(0, 60*60*24, 60*60).reshape(-1, 1)
    return predict_set

# inits models
models = {}
order = 3

for d in WEEKDAYS:
    models[d] = linear_model.LinearRegression()

def train(trainset):
    ''' Train models using trainset from convert_input '''
    for day, (x, y) in trainset.items():
        poly = PolynomialFeatures(order, include_bias=False)
        x = poly.fit_transform(x)
        models[day].fit(x, y) # update each model

def predict(day, x):
    ''' do prediction for giving day and list of seconds
    Args:
        day: a str of weekday, e.g. Monday, Tuesday...
        x: a (n, 1) numpy array of seconds from the start of the day
    Returns:
        a (n, a) array which is the prediction of giving x
    '''
    # get polynomial feature
    poly = PolynomialFeatures(order, include_bias=False)
    x = poly.fit_transform(x)

    # precit and return
    return models[day].predict(x)

def main():
    # inits backend
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
    
    # Upload to firebase
    print('Uploading....')
    output_node.val = result


if __name__ == "__main__":
    main()