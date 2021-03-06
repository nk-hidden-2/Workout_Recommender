import os
import csv
import time
import pickle
import json
import pandas as pd
from lightfm.data import Dataset
import numpy
from sklearn.model_selection import train_test_split


def build_dataset(user_item_interactions_path, neg_sample=False):
    """
    Takes in user/item interactions path and fits LightFM dataset object.
    Returns user-item interaction as pandas dataframe, LightFM dataset object,
    and dictionary that maps the external ids to LightFM's internal item indices
    """
    user_item_interactions = pd.read_csv(user_item_interactions_path)

    dataset = Dataset()
    dataset.fit(user_item_interactions['user_id'].tolist(),
                user_item_interactions['workout_id'].tolist())

    num_users, num_items = dataset.interactions_shape()
    print('Num users: {}, num_items {}.'.format(num_users, num_items))

    item_map = dataset.mapping()[2]
    return user_item_interactions, dataset, item_map


def build_ui_matrix(df, dataset):
    """
    Takes dataframe and LightFM dataset object and returns user-item interaction
    matrix
    """
    (interactions, weights) = dataset.build_interactions(
        df[['user_id', 'workout_id']].apply(lambda x: (x['user_id'], x['workout_id']), axis=1).tolist()
    )
    return interactions


def get_data(user_item_interactions_path):
    """
    Takes in user-item interactions path and returns dictionary of various
    dataframes/matrices
    """
    user_item_interactions, dataset, item_map = build_dataset(
        user_item_interactions_path)

    train_df, test_df = train_test_split(user_item_interactions, train_size=0.7, random_state=42)
    train_ui_matrix = build_ui_matrix(train_df, dataset)
    test_ui_matrix = build_ui_matrix(test_df, dataset)

    data_dct = {
        'user_item_interactions': user_item_interactions,
        'train_df': train_df,
        'test_df': test_df,
        'train_ui_matrix': train_ui_matrix,
        'test_ui_matrix': test_ui_matrix,
        'item_map': item_map
    }
    return data_dct
