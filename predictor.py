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


def convert_input(data):
    x, y = [], []
    for t, num_people in data.items():
        weekday, minutes = get_weekday_minutes(int(t))

        x.append([weekday, minutes])
        y.append([num_people])
    return np.array(x), np.array(y)


def get_future_time_points():
    weekday, minutes = get_weekday_minutes()
    return np.array([[weekday, m] for m in range(minutes, 60 * 24, 10)])

def upload(x, y, node):
    content = {}
    for i in range(x.shape[0]):
        content[f'{x[i][0]}-{x[i][1]}'] = int(y[i][0])
    node.val = content

def main():
    room = backend.get_room_arg()
    input_node = backend.FireBaseNode('NumberOfPeople', room, mode='r')
    prediction_node = backend.FireBaseNode('Prediction', room)

    # convert data to numpy
    x_train, y_train = convert_input(input_node.val)
    x_predict = get_future_time_points()

    # Train model

    # Write your code here
    # eg. xxx.fit(x_train, y_train)

    # Predict future time points

    # Write your code here
    # eg. y_predict = xxx.predict(x_predict)
    y_predict = np.random.randint(0, 10, (x_predict.shape[0], 1))

    # Upload to firebase
    upload(x_predict, y_predict, prediction_node)


if __name__ == "__main__":
    main()
