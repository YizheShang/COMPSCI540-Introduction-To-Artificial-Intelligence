import numpy as np
import random
import csv
import copy
import math


# Feel free to import other packages, if needed.
# As long as they are supported by CSL machines.


def get_dataset(filename):
    """
    TODO: implement this function.

    INPUT: 
        filename - a string representing the path to the csv file.

    RETURNS:
        An n by m+1 array, where n is # data points and m is # features.
        The labels y should be in the first column.
    """
    # read .csv
    csvFile = open(filename, "r")
    reader = csv.reader(csvFile)

    dataset = []

    for item in reader:
        # check if the line number is 1
        if reader.line_num == 1:
            continue
        row = []
        for n in range(1, len(item)):
            row.append(float(item[n]))
        dataset.append(row)

    return dataset


def print_stats(dataset, col):
    """
    TODO: implement this function.

    INPUT: 
        dataset - the body fat n by m+1 array
        col     - the index of feature to summarize on. 
                  For example, 1 refers to density.

    RETURNS:
        None
    """
    data_list = []
    for row in dataset:
        data_list.append(row[col])

    num_data = len(data_list)

    sum = 0
    for d in data_list:
        sum += d

    x_bar = sum / num_data
#    x_bar = round(x_bar, 2)

    var_list = []
    for d in data_list:
        var_list.append(math.pow((d - x_bar), 2))

    v_sum = 0
    for v in var_list:
        v_sum += v

    sigma = math.sqrt(v_sum / (num_data - 1))
#    sigma = round(sigma, 2)

    print(num_data)
    print("%.2f" % x_bar)
    print("%.2f" % sigma)


def regression(dataset, cols, betas):
    """
    TODO: implement this function.

    INPUT: 
        dataset - the body fat n by m+1 array
        cols    - a list of feature indices to learn.
                  For example, [1,8] refers to density and abdomen.
        betas   - a list of elements chosen from [beta0, beta1, ..., betam]

    RETURNS:
        mse of the regression model
    """
    numerator_sum = 0
    for r in range(len(dataset)):
        numerator = 0
        for b in range(len(betas)):
            if b == 0:
                numerator += betas[b]
            else:
                numerator += betas[b] * dataset[r][cols[b - 1]]
        numerator_sum += math.pow(numerator - dataset[r][0], 2)

    mse = numerator_sum / len(dataset)
    return mse


def gradient_descent(dataset, cols, betas):
    """
    TODO: implement this function.

    INPUT: 
        dataset - the body fat n by m+1 array
        cols    - a list of feature indices to learn.
                  For example, [1,8] refers to density and abdomen.
        betas   - a list of elements chosen from [beta0, beta1, ..., betam]

    RETURNS:
        An 1D array of gradients
    """
    grads = []
    sum = 0
    for i in range(len(betas)):
        numerator_sum = 0
        for r in range(len(dataset)):
            numerator = 0
            for b in range(len(betas)):
                if b == 0:
                    numerator += betas[b]
                else:
                    numerator += betas[b] * dataset[r][cols[b - 1]]

            numerator = numerator - dataset[r][0]

            if i > 0:
                #               print(i)
                numerator_sum += numerator * dataset[r][cols[i - 1]]
            else:
                numerator_sum += numerator

        gards_ele = 0
        gards_ele = (2 * numerator_sum) / len(dataset)
        grads.append(gards_ele)

    return np.array(grads)


def iterate_gradient(dataset, cols, betas, T, eta):
    """
    TODO: implement this function.

    INPUT: 
        dataset - the body fat n by m+1 array
        cols    - a list of feature indices to learn.
                  For example, [1,8] refers to density and abdomen.
        betas   - a list of elements chosen from [beta0, beta1, ..., betam]
        T       - # iterations to run
        eta     - learning rate

    RETURNS:
        None
    """
    betas_list = []
    for i in betas:
        betas_list.append(i)

    t = 1
    while t <= T:
        new_betas_list = []
        grad_result = gradient_descent(dataset, cols, betas_list)
        for b in range(len(betas_list)):
            new_beta = 0
            new_beta = betas_list[b] - eta * grad_result[b]
            new_betas_list.append(new_beta)

        mse = 0
        mse = regression(dataset, cols, new_betas_list)
        print(t, "%.2f" % mse, end="")
        for i in new_betas_list:
            print(" %.2f" % i, end="")
        print()
        betas_list = new_betas_list
        t += 1



def compute_betas(dataset, cols):
    """
    TODO: implement this function.

    INPUT: 
        dataset - the body fat n by m+1 array
        cols    - a list of feature indices to learn.
                  For example, [1,8] refers to density and abdomen.

    RETURNS:
        A tuple containing corresponding mse and several learned betas
    """
    X_list = []
    y_list = []
    for r in range(len(dataset)):
        x_temp_list = []
        x_temp_list.append(1)
        y_list.append(dataset[r][0])
        for c in cols:
            x_temp_list.append(dataset[r][c])
        X_list.append(x_temp_list)

    X_list = np.array(X_list)
    y_list = np.array(y_list)
    y_list = y_list.reshape(252, 1)

    betas = np.dot(X_list.transpose(), X_list)
    betas = np.linalg.inv(betas)
    betas = np.dot(betas, X_list.transpose())
    betas = np.dot(betas, y_list)


    mse = regression(dataset, cols, betas)
    tuple = (mse,)
    temp = ()
    for t in betas:
        temp = (t[0],)
        tuple = tuple + temp

    return tuple


def predict(dataset, cols, features):
    """
    TODO: implement this function.

    INPUT: 
        dataset - the body fat n by m+1 array
        cols    - a list of feature indices to learn.
                  For example, [1,8] refers to density and abdomen.
        features- a list of observed values

    RETURNS:
        The predicted body fat percentage value
    """
    betas_list = compute_betas(dataset, cols)
    new_betas_list = []
    for i in betas_list:
        new_betas_list.append(i)

    features.insert(0, 1)

    betas = []
    for i in range(1, len(new_betas_list)):
        betas.append(new_betas_list[i])

    sum = 0
    for j in range(0, len(betas)):
        product = betas[j] * features[j]
        sum += product


    result = sum
    return result


def random_index_generator(min_val, max_val, seed=42):
    """
    DO NOT MODIFY THIS FUNCTION.
    DO NOT CHANGE THE SEED.
    This generator picks a random value between min_val and max_val,
    seeded by 42.
    """
    random.seed(seed)
    while True:
        yield random.randrange(min_val, max_val)


def sgd(dataset, cols, betas, T, eta):
    """
    TODO: implement this function.
    You must use random_index_generator() to select individual data points.

    INPUT: 
        dataset - the body fat n by m+1 array
        cols    - a list of feature indices to learn.
                  For example, [1,8] refers to density and abdomen.
        betas   - a list of elements chosen from [beta0, beta1, ..., betam]
        T       - # iterations to run
        eta     - learning rate

    RETURNS:
        None
    """
    betas_list = []
    for i in betas:
        betas_list.append(float(i))

    gen = random_index_generator(0, len(dataset)-1)


    t = 1
    while t <= T:
        num_of_row = next(gen)

        dataset_row = dataset[num_of_row]
        dataset_list = []
        dataset_list.append(dataset_row)
        dataset_list = np.array(dataset_list)

        new_betas_list = []
        grad_result = gradient_descent(dataset_list, cols, betas_list)
        for b in range(len(betas_list)):
            new_beta = 0
            new_beta = betas_list[b] - eta * grad_result[b]
            new_betas_list.append(new_beta)

        mse = 0
        mse = regression(dataset, cols, new_betas_list)
        print(t, "%.2f" % mse, end="")
        for i in new_betas_list:
            print(" %.2f" % i, end="")
        print()
        betas_list = new_betas_list
        t += 1


"""
if __name__ == '__main__':
    # Your debugging code goes here.
    dataset = get_dataset('bodyfat.csv')
#    print(dataset)
     #   for i in dataset:
    #        print(i)

    #    print_stats(dataset, 1)  # summary of density

 #   reg1 = regression(dataset, cols=[2, 3], betas=[0, 0, 0])
 #   print(reg1)
  #  reg2 = regression(dataset, cols=[2, 3, 4], betas=[0, -1.1, -.2, 3])
#    print(reg2)

 #   grad = gradient_descent(dataset, cols=[2, 3], betas=[0, 0, 0])
 #   print(grad)

 #   iter_grad = iterate_gradient(dataset, cols=[1,8], betas=[400,-400,300], T=10, eta=1e-4)
#    print(iter_grad)

#    com_betas = compute_betas(dataset, cols=[1, 2])
#    print(com_betas)

#    predict_y = predict(dataset, cols=[1, 2], features=[1.0708, 23])
#    print(predict_y)

 #   sgd1 = sgd(dataset, cols=[2, 3], betas=[0, 0, 0], T=5, eta=1e-6)
 #   print()
 #   sgd1 = sgd(dataset, cols=[2, 8], betas=[-40, 0, 0.5], T=10, eta=1e-5)

#    print_stats(dataset, 2)
#    print_stats(dataset, 3)
#    print_stats(dataset, 12)

    reg1 = regression(dataset, cols=[2,3,4,5,7], betas=[0,-1.1,-.2,3,3,2])
 #   print(reg1)
    reg2 = reg = regression(dataset, cols=[2,3,5,5,7], betas=[1,-1.1,-.2,3,3,2])
#    print(reg2)

 #   print(gradient_descent(dataset, cols=[2, 3], betas=[1, 2, 3]))
 #   print(array([1217.20912698, 55182.58134921, 222653.14763889])

 #   print(gradient_descent(dataset, cols=[2, 3, 5], betas=[4, 2, 3, 7]))
 #   print(array([1579.32579365, 71512.35198413, 288771.29462302, 40908.0647619]))
 #   iterate_gradient(dataset, cols=[1,15], betas=[400,-400,300], T=10, eta=1e-4)
 #   iterate_gradient(dataset, cols=[1, 15], betas=[400, -400, 500], T=20, eta=1e-4)
    print(predict(dataset, cols=[1, 2, 3], features=[1.0708, 23, 154.25]))
    print(predict(dataset, cols=[1, 2, 3, 4], features=[1.0708, 23, 154.25, 67, 75]))
    print(predict(dataset, cols=[1, 2, 3, 4, 5], features=[1.0708, 23, 154.25, 67, 75]))
    sgd(dataset, cols=[2, 3, 8], betas=[0, 0, 0, 0.5], T=20, eta=1e-5)
"""
