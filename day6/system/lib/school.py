#!/usr/bin/env python
# _*_coding:utf-8_*_
'''
 * Created on 2017/3/11 21:13.
 * @author: Chinge_Yang.
'''

import os
from conf import settings
from lib.db import Db

class School(object):
    '''学校类'''

    def __init__(self, school_name, city_name, teachers=None, courses=None, students=None, banjis=None):
        '''
        定义学校属性
        :param school_name: 学校名，字符类型
        :param city_name: 城市名，字符类型
        :param teachers: 讲师，字典类型，如{"teachers": []}
        :param students: 学员, 字典类型，如{"students": []}
        :param courses: 课程，字典类型，如{"courses": []}
        :param banjis: 班级，字典类型，如{"banjis": []}
        '''
        self.school_name = school_name
        self.city_name = city_name
        self.teachers = teachers
        self.courses = courses
        self.students = students
        self.banjis = banjis
        self.db = Db(settings.BASE_DATABASE)  # 数据库连接
        self.db_path = self.db.db_handler()

    def add_attr_value(self, attr, list_value):
        '''学校添加属性的字典元素列表值
        :param attr: school类的属性
        :return:
        '''
        attr_value = getattr(self, attr)    # 字典类型
        attr_value_list = attr_value[attr]  # 列表类型
        if not list_value in attr_value_list:
            attr_value_list.append(list_value)
        else:
            print("{} already exist.".format(list_value.name))

        return self


    def show_info(self, attr=None):
        '''显示课程/讲师/学生/班级'''
        attr_list = [ "courses", "teachers", "students", "banjis"]
        def show_attr_value(attr):
            attr_value = getattr(self, attr)    # 字典类型
            attr_value_list = attr_value[attr]  # 列表类型
            print("{} :".format(attr))
            for a in attr_value_list:  # 循环显示
                # a.show_info()
                if a.name:
                    print("\033[34;1m{}\033[0m".format(a.name))
                else:  # 显示人的帐户名
                    print("\033[34;1m{}\033[0m".format(a.account.user_name))

        if attr in attr_list:
            show_attr_value(attr)
        else:
            for attr in attr_list:
                show_attr_value(attr)

        return True

    def get_instance(self):
        '''根据名字获取对象'''
        attr_list = [ "courses", "teachers", "students", "banjis"]
