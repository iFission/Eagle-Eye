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


def getData1():
    userhome = os.path.expanduser('~')
    csvfile = os.path.join(userhome, 'Desktop', 'Mondaydata.csv')
    with open(csvfile, newline='') as csvfile:
        data = np.array(list(csv.reader(csvfile)))
        data = data.astype(np.float)
    return data


def multiple_linear_regression1(bunchobject1, order, size, seed):
    #print(bunchobject1)
    x = bunchobject1[:, [0]]
    y = bunchobject1[:, [1]]
    poly = PolynomialFeatures(order, include_bias=False)
    # the PolynomialFeatures class with order can
    #give u all the coefficient
    x = poly.fit_transform(x)
    # after fit it will show all the coefficient
    # of x
    #print(x)
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=size, random_state=seed)
    # regr can help to get the coefficient and intercept of the linear relationship
    regr = linear_model.LinearRegression()
    regr.fit(x_train, y_train)
    coefficient = regr.coef_[0]
    intercept = regr.intercept_[0]
    # the coefficient will start from the lower order
    #print(regr.coef_, regr.intercept_)
    y_pred = regr.predict(x_test)
    # it will fit the x value from the test set to get the predict value of y
    coeff_R = r2_score(y_test, y_pred)
    #print(coeff_R)
    mse = mean_squared_error(y_test, y_pred)
    # the r2-score will takes in the y_true and the Y_predict
    results = {}
    results['coefficients'] = regr.coef_
    results['intercept'] = regr.intercept_
    results['mean squared error'] = mse
    results['r2 score'] = coeff_R
    return coefficient, intercept  # x_train, results, intercept


bunchobject1 = getData1()
together1 = multiple_linear_regression1(bunchobject1, 2, 0.4, 2752)
coefficients1 = together1[0]
intercept1 = together1[1]


def Liner_formula1(t):
    index = 0
    y = intercept1
    while index < len(coefficients1):
        y = y + coefficients1[index] * t**(index + 1)
        index += 1
        y = int(y)
    return y


# remember to change here !!!!
# Liner_formula1(74500)


def getData2():
    userhome = os.path.expanduser('~')
    csvfile = os.path.join(userhome, 'Desktop', 'Tuesdaydata.csv')
    with open(csvfile, newline='') as csvfile:
        data = np.array(list(csv.reader(csvfile)))
        data = data.astype(np.float)
    return data


def multiple_linear_regression2(bunchobject2, order, size, seed):
    #print(bunchobject2)
    x = bunchobject2[:, [0]]
    y = bunchobject2[:, [1]]
    poly = PolynomialFeatures(order, include_bias=False)
    # the PolynomialFeatures class with order can
    #give u all the coefficient
    x = poly.fit_transform(x)
    # after fit it will show all the coefficient
    # of x
    #print(x)
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=size, random_state=seed)
    # regr can help to get the coefficient and intercept of the linear relationship
    regr = linear_model.LinearRegression()
    regr.fit(x_train, y_train)
    coefficient = regr.coef_[0]
    intercept = regr.intercept_[0]
    # the coefficient will start from the lower order
    #print(regr.coef_, regr.intercept_)
    y_pred = regr.predict(x_test)
    # it will fit the x value from the test set to get the predict value of y
    coeff_R = r2_score(y_test, y_pred)
    #print(coeff_R)
    mse = mean_squared_error(y_test, y_pred)
    # the r2-score will takes in the y_true and the Y_predict
    results = {}
    results['coefficients'] = regr.coef_
    results['intercept'] = regr.intercept_
    results['mean squared error'] = mse
    results['r2 score'] = coeff_R
    return coefficient, intercept  # x_train, results, intercept


bunchobject2 = getData2()
together2 = multiple_linear_regression2(bunchobject2, 2, 0.4, 2752)
coefficients2 = together2[0]
intercept2 = together2[1]


def Liner_formula2(t):
    index = 0
    y = intercept2
    while index < len(coefficients2):
        y = y + coefficients2[index] * t**(index + 1)
        index += 1
        y = int(y)
    return y


def getData3():
    userhome = os.path.expanduser('~')
    csvfile = os.path.join(userhome, 'Desktop', 'wednesdaydata.csv')
    with open(csvfile, newline='') as csvfile:
        data = np.array(list(csv.reader(csvfile)))
        data = data.astype(np.float)
    return data


def multiple_linear_regression3(bunchobject3, order, size, seed):
    # print(bunchobject3)
    x = bunchobject3[:, [0]]
    y = bunchobject3[:, [1]]
    poly = PolynomialFeatures(order, include_bias=False)
    # the PolynomialFeatures class with order can
    #give u all the coefficient
    x = poly.fit_transform(x)
    # after fit it will show all the coefficient
    # of x
    #print(x)
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=size, random_state=seed)
    # regr can help to get the coefficient and intercept of the linear relationship
    regr = linear_model.LinearRegression()
    regr.fit(x_train, y_train)
    coefficient = regr.coef_[0]
    intercept = regr.intercept_[0]
    # the coefficient will start from the lower order
    #print(regr.coef_, regr.intercept_)
    y_pred = regr.predict(x_test)
    # it will fit the x value from the test set to get the predict value of y
    coeff_R = r2_score(y_test, y_pred)
    #print(coeff_R)
    mse = mean_squared_error(y_test, y_pred)
    # the r2-score will takes in the y_true and the Y_predict
    results = {}
    results['coefficients'] = regr.coef_
    results['intercept'] = regr.intercept_
    results['mean squared error'] = mse
    results['r2 score'] = coeff_R
    return coefficient, intercept  # x_train, results, intercept


bunchobject3 = getData3()
together3 = multiple_linear_regression3(bunchobject3, 2, 0.4, 2752)
coefficients3 = together3[0]
intercept3 = together3[1]


def Liner_formula3(t):
    index = 0
    y = intercept3
    while index < len(coefficients3):
        y = y + coefficients3[index] * t**(index + 1)
        index += 1
        y = int(y)
    return y


def getData4():
    userhome = os.path.expanduser('~')
    csvfile = os.path.join(userhome, 'Desktop', 'thursdaydata.csv')
    with open(csvfile, newline='') as csvfile:
        data = np.array(list(csv.reader(csvfile)))
        data = data.astype(np.float)
    return data


def multiple_linear_regression4(bunchobject4, order, size, seed):
    # print(bunchobject4)
    x = bunchobject4[:, [0]]
    y = bunchobject4[:, [1]]
    poly = PolynomialFeatures(order, include_bias=False)
    # the PolynomialFeatures class with order can
    #give u all the coefficient
    x = poly.fit_transform(x)
    # after fit it will show all the coefficient
    # of x
    #print(x)
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=size, random_state=seed)
    # regr can help to get the coefficient and intercept of the linear relationship
    regr = linear_model.LinearRegression()
    regr.fit(x_train, y_train)
    coefficient = regr.coef_[0]
    intercept = regr.intercept_[0]
    # the coefficient will start from the lower order
    #print(regr.coef_, regr.intercept_)
    y_pred = regr.predict(x_test)
    # it will fit the x value from the test set to get the predict value of y
    coeff_R = r2_score(y_test, y_pred)
    #print(coeff_R)
    mse = mean_squared_error(y_test, y_pred)
    # the r2-score will takes in the y_true and the Y_predict
    results = {}
    results['coefficients'] = regr.coef_
    results['intercept'] = regr.intercept_
    results['mean squared error'] = mse
    results['r2 score'] = coeff_R
    return coefficient, intercept  # x_train, results, intercept


bunchobject4 = getData4()
together4 = multiple_linear_regression4(bunchobject4, 2, 0.4, 2752)
coefficients4 = together4[0]
intercept4 = together4[1]


def Liner_formula4(t):
    index = 0
    y = intercept4
    while index < len(coefficients4):
        y = y + coefficients4[index] * t**(index + 1)
        index += 1
        y = int(y)
    return y


def getData5():
    userhome = os.path.expanduser('~')
    csvfile = os.path.join(userhome, 'Desktop', 'Fridaydata.csv')
    with open(csvfile, newline='') as csvfile:
        data = np.array(list(csv.reader(csvfile)))
        data = data.astype(np.float)
    return data


def multiple_linear_regression5(bunchobject5, order, size, seed):
    # print(bunchobject5)
    x = bunchobject5[:, [0]]
    y = bunchobject5[:, [1]]
    poly = PolynomialFeatures(order, include_bias=False)
    # the PolynomialFeatures class with order can
    #give u all the coefficient
    x = poly.fit_transform(x)
    # after fit it will show all the coefficient
    # of x
    #print(x)
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=size, random_state=seed)
    # regr can help to get the coefficient and intercept of the linear relationship
    regr = linear_model.LinearRegression()
    regr.fit(x_train, y_train)
    coefficient = regr.coef_[0]
    intercept = regr.intercept_[0]
    # the coefficient will start from the lower order
    #print(regr.coef_, regr.intercept_)
    y_pred = regr.predict(x_test)
    # it will fit the x value from the test set to get the predict value of y
    coeff_R = r2_score(y_test, y_pred)
    #print(coeff_R)
    mse = mean_squared_error(y_test, y_pred)
    # the r2-score will takes in the y_true and the Y_predict
    results = {}
    results['coefficients'] = regr.coef_
    results['intercept'] = regr.intercept_
    results['mean squared error'] = mse
    results['r2 score'] = coeff_R
    return coefficient, intercept  # x_train, results, intercept


bunchobject5 = getData5()
together5 = multiple_linear_regression5(bunchobject5, 2, 0.4, 2752)
coefficients5 = together5[0]
intercept5 = together5[1]


def Liner_formula5(t):
    index = 0
    y = intercept5
    while index < len(coefficients5):
        y = y + coefficients5[index] * t**(index + 1)
        index += 1
        y = int(y)
    return y


def getData6():
    userhome = os.path.expanduser('~')
    csvfile = os.path.join(userhome, 'Desktop', 'saturdaydata.csv')
    with open(csvfile, newline='') as csvfile:
        data = np.array(list(csv.reader(csvfile)))
        data = data.astype(np.float)
    return data


def multiple_linear_regression6(bunchobject6, order, size, seed):
    # print(bunchobject6)
    x = bunchobject6[:, [0]]
    y = bunchobject6[:, [1]]
    poly = PolynomialFeatures(order, include_bias=False)
    # the PolynomialFeatures class with order can
    #give u all the coefficient
    x = poly.fit_transform(x)
    # after fit it will show all the coefficient
    # of x
    #print(x)
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=size, random_state=seed)
    # regr can help to get the coefficient and intercept of the linear relationship
    regr = linear_model.LinearRegression()
    regr.fit(x_train, y_train)
    coefficient = regr.coef_[0]
    intercept = regr.intercept_[0]
    # the coefficient will start from the lower order
    #print(regr.coef_, regr.intercept_)
    y_pred = regr.predict(x_test)
    # it will fit the x value from the test set to get the predict value of y
    coeff_R = r2_score(y_test, y_pred)
    #print(coeff_R)
    mse = mean_squared_error(y_test, y_pred)
    # the r2-score will takes in the y_true and the Y_predict
    results = {}
    results['coefficients'] = regr.coef_
    results['intercept'] = regr.intercept_
    results['mean squared error'] = mse
    results['r2 score'] = coeff_R
    return coefficient, intercept  # x_train, results, intercept


bunchobject6 = getData6()
together6 = multiple_linear_regression6(bunchobject6, 2, 0.4, 2752)
coefficients6 = together6[0]
intercept6 = together6[1]


def Liner_formula6(t):
    index = 0
    y = intercept6
    while index < len(coefficients6):
        y = y + coefficients6[index] * t**(index + 1)
        index += 1
        y = int(y)
    return y


def getData7():
    userhome = os.path.expanduser('~')
    csvfile = os.path.join(userhome, 'Desktop', 'Sundaydata.csv')
    with open(csvfile, newline='') as csvfile:
        data = np.array(list(csv.reader(csvfile)))
        data = data.astype(np.float)
    return data


def multiple_linear_regression7(bunchobject7, order, size, seed):
    # print(bunchobject7)
    x = bunchobject7[:, [0]]
    y = bunchobject7[:, [1]]
    poly = PolynomialFeatures(order, include_bias=False)
    # the PolynomialFeatures class with order can
    #give u all the coefficient
    x = poly.fit_transform(x)
    # after fit it will show all the coefficient
    # of x
    #print(x)
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=size, random_state=seed)
    # regr can help to get the coefficient and intercept of the linear relationship
    regr = linear_model.LinearRegression()
    regr.fit(x_train, y_train)
    coefficient = regr.coef_[0]
    intercept = regr.intercept_[0]
    # the coefficient will start from the lower order
    #print(regr.coef_, regr.intercept_)
    y_pred = regr.predict(x_test)
    # it will fit the x value from the test set to get the predict value of y
    coeff_R = r2_score(y_test, y_pred)
    #print(coeff_R)
    mse = mean_squared_error(y_test, y_pred)
    # the r2-score will takes in the y_true and the Y_predict
    results = {}
    results['coefficients'] = regr.coef_
    results['intercept'] = regr.intercept_
    results['mean squared error'] = mse
    results['r2 score'] = coeff_R
    return coefficient, intercept  # x_train, results, intercept


bunchobject7 = getData7()
together7 = multiple_linear_regression7(bunchobject7, 2, 0.4, 2752)
coefficients7 = together7[0]
intercept7 = together7[1]


def Liner_formula7(t):
    index = 0
    y = intercept7
    while index < len(coefficients7):
        y = y + coefficients7[index] * t**(index + 1)
        index += 1
        y = int(y)
    return y


def result1(t):
    time_list = time_table(t)
    index = 0
    people_lst = []
    key_list = convert_time_table(time_list)
    # print(key_list)
    # print(len(key_list))
    while index < len(time_list):
        number_of_people = Liner_formula1(time_list[index])
        people_lst.append(number_of_people)
        index += 1
    # print(people_lst)
    # print(len(people_lst))
    #output = dic(zip(key_list,people_lst))
    output = {}
    for (key, value) in zip(key_list, people_lst):
        output[key] = value
    return output


def result2(t):
    time_list = time_table(t)
    index = 0
    people_lst = []
    key_list = convert_time_table(time_list)
    while index < len(time_list):
        number_of_people = Liner_formula2(time_list[index])
        people_lst.append(number_of_people)
        index += 1
    output = {}
    for (key, value) in zip(key_list, people_lst):
        output[key] = value
    return output


def result3(t):
    time_list = time_table(t)
    index = 0
    people_lst = []
    key_list = convert_time_table(time_list)
    while index < len(time_list):
        number_of_people = Liner_formula3(time_list[index])
        people_lst.append(number_of_people)
        index += 1
    output = {}
    for (key, value) in zip(key_list, people_lst):
        output[key] = value
    return output


def result4(t):
    time_list = time_table(t)
    index = 0
    people_lst = []
    key_list = convert_time_table(time_list)
    while index < len(time_list):
        number_of_people = Liner_formula4(time_list[index])
        people_lst.append(number_of_people)
        index += 1
    output = {}
    for (key, value) in zip(key_list, people_lst):
        output[key] = value
    return output


def result5(t):
    time_list = time_table(t)
    index = 0
    people_lst = []
    key_list = convert_time_table(time_list)
    while index < len(time_list):
        number_of_people = Liner_formula5(time_list[index])
        people_lst.append(number_of_people)
        index += 1
    output = {}
    for (key, value) in zip(key_list, people_lst):
        output[key] = value
    return output


def result6(t):
    time_list = time_table(t)
    index = 0
    people_lst = []
    key_list = convert_time_table(time_list)
    while index < len(time_list):
        number_of_people = Liner_formula6(time_list[index])
        people_lst.append(number_of_people)
        index += 1
    output = {}
    for (key, value) in zip(key_list, people_lst):
        output[key] = value
    return output


def result7(t):
    time_list = time_table(t)
    index = 0
    people_lst = []
    key_list = convert_time_table(time_list)
    while index < len(time_list):
        number_of_people = Liner_formula7(time_list[index])
        people_lst.append(number_of_people)
        index += 1
    #print(time_list)
    output = {}
    for (key, value) in zip(key_list, people_lst):
        output[key] = value
    return output


# change the result to the numpy array
# need the weekday as the input, creat 7 model to model 7 days


def result(weekdays, time):
    if weekdays == 'Monday':
        output = result1(time)
    elif weekdays == 'Tuesday':
        output = result2(time)
    elif weekdays == 'Wednesday':
        output = result3(time)
    elif weekdays == 'Thursday':
        output = result4(time)
    elif weekdays == 'Friday':
        output = result5(time)
    elif weekdays == 'Saturday':
        output = result6(time)
    elif weekdays == 'Sunday':
        output = result7(time)
    return output


print(result('Monday', '8:30:30'))
print(result('Tuesday', '8:30:30'))
print(result('Wednesday', '8:30:30'))
print(result('Thursday', '8:30:30'))
print(result('Friday', '8:30:30'))
print(result('Saturday', '8:30:30'))
print(result('Sunday', '8:30:30'))
