#!/cs/puls/pyenv/shims/python
# -*- coding: utf-8 -*-

import os
import sys
import tensorflow as tf

sys.path.append('..')
sys.path.append('../..')


def parse_train(example):
    features = {'sent': tf.FixedLenFeature([], tf.int64)}
    parsed = tf.parse_single_example(example, features)
    return parsed['sent']

def read_instances(path_to_data, epochs, batch_size):
    train_files = path_to_data + '/train_instances.tfrecords'
    test_files = path_to_data + '/test_instances.tfrecords'
    valid_files = path_to_data + '/valid_instances.tfrecords'
    
    train_data = tf.data.TFRecordDataset(train_files)
    train_data = train_data.map(parse_train)      
    train_data = train_data.shuffle(10000)
    train_data = train_data.repeat(epochs)
    train_data = train_data.batch(batch_size)
    train_iterator = train_data.make_initializable_iterator()

    valid_data = tf.data.TFRecordDataset(valid_files)
    valid_data = valid_data.map(parse_train)      
    valid_data = valid_data.shuffle(10000)
    valid_data = valid_data.repeat(epochs)
    valid_data = valid_data.batch(batch_size)
    valid_iterator = valid_data.make_initializable_iterator()

    test_data = tf.data.TFRecordDataset(test_files)
    test_data = test_data.map(parse_train)      
    test_data = test_data.batch(batch_size)
    test_iterator = test_data.make_initializable_iterator()
    
    return (train_iterator, valid_iterator, test_iterator)

    
if __name__ == '__main__':
    read_instances('../data', 5, 100)
