import pandas as pd
import numpy as np
import os, pickle
from sklearn.model_selection import train_test_split

phase_train = 'train'
phase_test = 'test'
phase_val = 'val'
dataset_image = 'image'
dataset_label = 'label'
pkl_ext = '.pkl'

class DataWrapper(object):
    def __init__(self, label_filename, image_filename, data_path, resplit=False, validation_split=0.25, test_split=0.10):
        self._image_train = None
        self._image_test = None
        self._image_val = None
        self._label_train = None
        self._label_test = None
        self._label_val = None

        self._image_train_fn = self._filename(data_path, dataset_image, phase_train)
        self._image_test_fn = self._filename(data_path, dataset_image, phase_test)
        self._image_val_fn = self._filename(data_path, dataset_image, phase_val)

        self._label_train_fn = self._filename(data_path, dataset_label, phase_train)
        self._label_test_fn = self._filename(data_path, dataset_label, phase_test)
        self._label_val_fn = self._filename(data_path, dataset_label, phase_val)

        # Check to see if we need to resplit either by explicit request or
        # any of the files is missing.
        if resplit or \
                not os.path.exists(self._image_train_fn) or \
                not os.path.exists(self._image_test_fn) or \
                not os.path.exists(self._image_val_fn) or \
                not os.path.exists(self._label_train_fn) or \
                not os.path.exists(self._label_test_fn) or \
                not os.path.exists(self._label_val_fn):
            self._split(label_filename, image_filename, validation_split, test_split)
        else:
            self._load()


    def _split(self, label_path, image_path, validation_split, test_split):
        print('Splitting')
        # Load the data from the pickle
        # Load the data from the pickle
        with open(label_path, 'rb') as f:
            label = pickle.load(f)

        with open(image_path, 'rb') as f:
            image = pickle.load(f)

        # print('Loaded')
        # print('Label: ', label.shape)
        # print('Image: ', image.shape)

        # Shuffle things because they were probably generated in order.
        shuffle_idx = np.array(range(len(image)))
        np.random.shuffle(shuffle_idx)

        image = image[shuffle_idx]
        label = label[shuffle_idx]

        index = pd.DataFrame(label)
        index.columns = ['Theta', 'Radius', 'Alpha']

        # Remove any points we aren't including in the project
        theta_range = (20, 340)
        radius_range = (15, 30)
        mask = (index.Theta >= theta_range[0]) & (index.Theta <= theta_range[1]) & \
                    (index.Radius >= radius_range[0]) & (index.Radius <=radius_range[1])

        label = label[mask]
        image = image[mask]
        index = index[mask]

        # Separate out the areas that we aren't including in the test and validation.
        # These are points at the edges of the training area.
        theta_range = (35, 325)
        radius_range = (16, 29)
        mask = (index.Theta >= theta_range[0]) & (index.Theta <= theta_range[1]) & \
                    (index.Radius >= radius_range[0]) & (index.Radius <=radius_range[1])
        not_mask = [not m for m in mask]

        predict_label = label[mask]
        predict_image = image[mask]
        predict_index = index[mask]

        # Save the rest for the test set.
        edge_label = label[not_mask]
        edge_image = image[not_mask]
        edge_index = index[not_mask]

        # Split off the validataion set.
        X, self._image_val, y, self._label_val = train_test_split(predict_image, predict_label,
                                                            test_size=validation_split)

        # Split off the test set.
        X, self._image_test, y, self._label_test = train_test_split(X, y,
                                                            test_size=test_split)

        # Add the reminder and the edge areas together into the train dataset.
        self._image_train = np.concatenate((X, edge_image), axis=0)
        self._label_train = np.concatenate((y, edge_label), axis=0)

        # print('Image, Label, Index: ')
        # print('All - Exclude:', image.shape, label.shape, index.shape)
        # print('Predict:', predict_image.shape, predict_label.shape, predict_index.shape)
        # print('Edge:', edge_image.shape, edge_label.shape, edge_index.shape)
        # print('Validation: ', validation_split, self._label_val.shape, self._image_val.shape)
        # print('Test: ', test_split, self._label_test.shape, self._image_test.shape)
        # print('Train: ', self._label_train.shape, self._image_train.shape)

        with open(self._image_train_fn, 'wb') as f:
            pickle.dump(self._image_train, f)

        with open(self._image_test_fn, 'wb') as f:
            pickle.dump(self._image_test, f)

        with open(self._image_val_fn, 'wb') as f:
            pickle.dump(self._image_val, f)

        with open(self._label_train_fn, 'wb') as f:
            pickle.dump(self._label_train, f)

        with open(self._label_test_fn, 'wb') as f:
            pickle.dump(self._label_test, f)

        with open(self._label_val_fn, 'wb') as f:
            pickle.dump(self._label_val, f)

        # print('Image Train: ', self._image_train.shape)
        # print('Image Test: ', self._image_test.shape)
        # print('Image Val: ', self._image_val.shape)
        # print('Label Train: ', self._label_train.shape)
        # print('Label Test: ', self._label_test.shape)
        # print('Label Val: ', self._label_val.shape)

    def _load(self):
        print('Loading')
        with open(self._image_train_fn, 'rb') as f:
            self._image_train = pickle.load(f)

        with open(self._image_test_fn, 'rb') as f:
            self._image_test = pickle.load(f)

        with open(self._image_val_fn, 'rb') as f:
            self._image_val = pickle.load(f)

        with open(self._label_train_fn, 'rb') as f:
            self._label_train = pickle.load(f)

        with open(self._label_test_fn, 'rb') as f:
            self._label_test = pickle.load(f)

        with open(self._label_val_fn, 'rb') as f:
            self._label_val = pickle.load(f)

        print('Image Train: ', self._image_train.shape)
        print('Image Test: ', self._image_test.shape)
        print('Image Val: ', self._image_val.shape)
        print('Label Train: ', self._label_train.shape)
        print('Label Test: ', self._label_test.shape)
        print('Label Val: ', self._label_val.shape)

    def _filename(self, path, dataset, phase):
        return os.path.join(path, '_'.join((dataset, phase)) + pkl_ext)

    def get_train(self):
        return self._image_train, self._label_train

    def get_test(self):
        return self._image_test, self._label_test

    def get_validation(self):
        return self._image_val, self._label_val