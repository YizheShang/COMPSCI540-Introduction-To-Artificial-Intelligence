import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np


def get_dataset(training=True):
    mnist = keras.datasets.mnist
    (train_images, train_labels), (test_images, test_labels) = mnist.load_data()
    if training == True:
        return (train_images, train_labels)
    else:
        return (test_images, test_labels)


def print_stats(train_images, train_labels):
    class_names = ['Zero', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine']
    print(len(train_images))
    #    print(train_images)
    dim = train_images.shape
    #    print(dim)
    print(dim[1], 'x', dim[2], sep="")
    dict = {}
    for j in class_names:
        dict[j] = 0

    for i in train_labels:
        temp = 0
        if i == 0:
            temp = dict['Zero']
            temp += 1
            dict['Zero'] = temp
        elif i == 1:
            temp = dict['One']
            temp += 1
            dict['One'] = temp
        elif i == 2:
            temp = dict['Two']
            temp += 1
            dict['Two'] = temp
        elif i == 3:
            temp = dict['Three']
            temp += 1
            dict['Three'] = temp
        elif i == 4:
            temp = dict['Four']
            temp += 1
            dict['Four'] = temp
        elif i == 5:
            temp = dict['Five']
            temp += 1
            dict['Five'] = temp
        elif i == 6:
            temp = dict['Six']
            temp += 1
            dict['Six'] = temp
        elif i == 7:
            temp = dict['Seven']
            temp += 1
            dict['Seven'] = temp
        elif i == 8:
            temp = dict['Eight']
            temp += 1
            dict['Eight'] = temp
        elif i == 9:
            temp = dict['Nine']
            temp += 1
            dict['Nine'] = temp

    for i in range(10):
        print('{}. {} - {}'.format(i,class_names[i],dict[class_names[i]]))


def build_model():
    model = keras.Sequential()
    model.add(tf.keras.layers.Flatten(input_shape=(28, 28)))
    model.add(layers.Dense(128, activation='relu'))
    model.add(layers.Dense(64, activation='relu'))
    model.add(layers.Dense(10))

    opt = keras.optimizers.SGD(learning_rate=0.001)
    loss_fn = keras.losses.SparseCategoricalCrossentropy(from_logits=True)
    model.compile(
        optimizer=opt,
        loss=loss_fn,
        metrics=['accuracy'])
    return model

def train_model(model, train_images, train_labels, T):
    model.fit(train_images, train_labels, epochs=T)

def evaluate_model(model, test_images, test_labels, show_loss=True):
    Loss, Accuracy = model.evaluate(test_images, test_labels, verbose=0)

    if show_loss == True:
        print("Loss:", '{:.4f}'.format(Loss))
        Accuracy = '{:.2f}'.format(100*Accuracy)
        print("Accuracy: {}%".format(Accuracy))
    else:
        Accuracy = '{:.2f}'.format(100 * Accuracy)
        print("Accuracy: {}%".format(Accuracy))

def predict_label(model, test_images, index):
    result = model.predict(test_images)
    labels = result[index]
#    print(labels)
    class_names = ['Zero', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine']
    result_list = []
    for i in range(10):
        result_list.append([labels[i],class_names[i]])
    result_list = sorted(result_list, reverse=True)
#    print(result_list)
    for j in range(3):
        print(result_list[j][1]+':', "%.2f"%(100*result_list[j][0])+"%")
"""
if __name__ == "__main__":
    (train_images, train_labels) = get_dataset()
    type(train_images)
"""
