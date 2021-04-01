from scipy.linalg import eigh
import numpy as np
import unittest
import matplotlib.pyplot as plt

'''
Author: Yizhe Shang
NetId: yshang24
'''

'''
load the dataset from a provided .npy file, re-center it around the origin and return it 
as a NumPy array of floats
'''
def load_and_center_dataset(filename):
    # load the file
    x = np.load(filename)

    # reshape the data
    x = np.reshape(x,(2000,784))

    # calculate the mean
    np.mean(x, axis=0)

    # re-center the data
    x = x - np.mean(x, axis=0)
    return x

'''
calculate and return the covariance matrix of the dataset as a NumPy matrix (d x d array)
'''
def get_covariance(dataset):
    x = dataset
    # transpose the data
    x_t = np.transpose(dataset)

    # calculate the covariance matrix
    dot_result = np.dot(x_t, x)
    s = (1/(len(dataset) - 1)) * dot_result
    return s

'''
perform eigen decomposition on the covariance matrix S and return a diagonal matrix (NumPy array) 
with the largest m eigenvalues on the diagonal, and a matrix (NumPy array) with the corresponding 
eigenvectors as columns
'''
def get_eig(S, m):
    Lambda, U = eigh(S, subset_by_index=[len(S)-m, len(S)-1])

    # reverse the array
    Lambda = Lambda[::-1]
    return np.diag(Lambda), np.fliplr(U)


'''
 similar to get_eig, but instead of returning the first m, return all eigenvectors that explains 
 more than perc % of variance
'''
def get_eig_perc(S, perc):
    Lambda, U = eigh(S)

    sum = 0
    for i in Lambda:
        sum += i
    Lambda, U = eigh(S, subset_by_value=[sum*perc, np.inf])
    Lambda = Lambda[::-1]
    return np.diag(Lambda), np.fliplr(U)

'''
project each image into your m-dimensional space and return the new representation as a d x 1 NumPy array
'''
def project_image(image, U):
    # transpose the data
    U_t = np.transpose(U)

    sum_x_proj = 0
    for i in range(0,len(U_t)):
        a_ij = np.dot(U_t[i], image)
        x_proj = np.dot(a_ij, np.transpose(U_t[i]))
        sum_x_proj += x_proj

    return sum_x_proj
'''
use matplotlib to display a visual representation of the original image and the projected image side-by-side
'''
def display_image(orig, proj):
    #reshape images
    image1 = np.reshape(orig, (28, 28))
    image2 = np.reshape(proj, (28, 28))

    # create a figure with two subplots
    f, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 3))

    # set the title for subplots
    ax1.set_title('Original')
    ax2.set_title('Projection')

    # render the images in subplots
    i_1 = ax1.imshow(image1, aspect='equal', cmap='gray')
    i_2 = ax2.imshow(image2, aspect='equal', cmap='gray')

    # create colorbars
    f.colorbar(i_1, ax=ax1)
    f.colorbar(i_2, ax=ax2)

    plt.show()



#if __name__ == '__main__':
#    x = load_and_center_dataset('mnist.npy')
#    x_cov = get_covariance(x)
#    print(x_cov)
#    print(np.sum(x_cov))
#    x2 = np.array([[1, 2, 5], [3, 4, 7]])
#    x2_cov = get_covariance(x2)
#    print(x2_cov)

#   Lambda, U = get_eig(x_cov, 20)
#    print(Lambda)
#    print(U)
#    print(np.sum(U))

#    Lambda, U= get_eig_perc(x_cov, 0.07)
#    print(Lambda)
#    print(np.sum(U))

#    display_image(orig=x[3], proj=project_image(x[3], U))
