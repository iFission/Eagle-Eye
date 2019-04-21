import time
import numpy as np
import backend
from datetime import datetime, timedelta, timezone


def get_weekday_minutes(timestamp=-1):
    if timestamp == -1:
        timestamp = time.time()
    utc_time = datetime.utcfromtimestamp(timestamp).replace(tzinfo=timezone.utc)
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
        train_set[WEEKDAYS[weekday]][0].append([minutes*60])
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
    return WEEKDAYS[weekday], np.array([[m*60] for m in range(minutes, 60 * 24, 10)])

def upload(x, y, node):
    content = {}
    for i in range(x.shape[0]):
        content[f'{x[i][0]}-{x[i][1]}'] = int(y[i][0])
    node.val = content

def train(trainset):
    for day, (x, y) in trainset.items():
        import matplotlib.pyplot as plt
        plt.scatter(x, y)
        plt.show()

def predict(day, minutes):
    pass

def main():
    room = 'Debug_Alex' #backend.get_room_arg()
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
