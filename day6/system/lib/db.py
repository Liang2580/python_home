#!/usr/bin/env python
# _*_coding:utf-8_*_
'''
 * Created on 2017/3/6 21:56.
 * @author: Chinge_Yang.
'''

import pickle

class Db(object):
    '''定义数据库'''
    def __init__(self, conn_params):
        '''
        连接库
        :param conn_params: 连接参数
        '''
        self.conn_params = conn_params
        self.db_path = '%s/%s' % (conn_params['path'], conn_params['name'])


    def db_handler(self):
        '''
        :return:
        '''

        if self.conn_params['engine'] == 'file_storage':
            return self.db_path

    def load_pickle_data(self, file):
        '''
        读取数据到内存中
        :param file: 要读取数据的文件路径
        :return: 返回信息
        '''
        with open(file, "rb") as f:
            data = pickle.load(f)
            return data


    def dump_pickle_data(self, file, data):
        '''
        从内存中把数据写入到数据库中
        :param data: 保存的数据
        :return:
        '''
        with open(file, 'wb') as f:
            result = pickle.dump(data, f)

        return True