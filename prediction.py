#%%
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
    lst = list(range(Second, 86430, 30))
    return lst


#time_table('8:30:30')
#%%
def convert_time_table(lst):
    result = []
    index = 0
    while index < len(lst) + 1:
        #print(lst[index])
        y = convert_to_time(lst[index])
        result.append(y)
        index += 1
        #print(lst[index])
    return result


# z = time_table('8:30:30')
# convert_time_table(z)
#%%
def multiple_linear_regression(bunchobject, x_index, y_index, order, size,
                               seed):
    x = bunchobject.data[:, [x_index]]
    y = bunchobject.data[:, [y_index]]
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
    return x_train[:, [0]], y_train, x_test[:, [
        0
    ]], y_pred, results, coefficient, intercept


b = datasets.load_breast_cancer()
multiple_linear_regression(b, 0, 3, 4, 0.4, 2752)


def Liner_formula(t):
    index = 0
    y = 0
    while index < len(multiple_linear_regression.coefficient):
        y = y + multiple_linear_regression.coefficient[index] * t**(index)
        index += 1
    return y


def result(t):
    time_list = time_table(t)
    index = 0
    people_lst = []
    key_list = convert_time_table(time_list)
    while index < len(time_list) + 1:
        number_of_people = Liner_formula(time_list[index])
        people_lst.append(number_of_people)
        index += 1
    output = {(key, value) for (key, value) in zip(key_list, people_lst)}
    return output


#%%
ls = [2, 3, 4, 5, 6]
first_three = ls[:3]
middle = ls[:]
print(middle)
x = '8:30'
print(x[0])

y = ['28', '12']
print(int(y[0]))
print(9 // 2)
print(list(range(2, 5, 2)))
