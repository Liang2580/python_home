#!/usr/bin/env python
# _*_coding:utf-8_*_
'''
 * Created on 2017/3/11 21:14.
 * @author: Chinge_Yang.
'''

import datetime

class Banji(object):
    '''班级类'''

    def __init__(self, name, courses):
        '''
        定义班级属性
        :param class_name: 班级名称,字符类型
        :param courses: 学习课程名，字典类型
        :param students: 学员，字典类型
        :param teachers: 讲师，字典类型
        :param begin_date: 开课时间，默认为班级创建时间
        :param status: 是否已开课，默认开课后不允许添加新学员
        '''
        self.name = name
        self.courses = {"courses": courses}
        self.students = {"students": []}
        self.teachers = {"teachers": []}
        self.begin_date = datetime.datetime.now()
        self.status = 0  # 0为未开课，1为已开课

    def show_info(self):
        '''显示班级信息'''
        print(" 班级信息 ".center(50,"-"))
        print("class name: ")
        print("\033[34;1m{}\033[0m".format(self.name))

        print("teachers: ")
        for teacher in self.teachers["teachers"]:
            if teacher.name:
                print("\033[34;1m{}\033[0m".format(teacher.name))

        print("students: ")
        for student in self.students["students"]:
            if student.name:
                print("\033[34;1m{}\033[0m".format(student.name))


    def add_people(self, role, person):
        '''添加学员
        :param role: 角色，学员或者讲师
        :param student: 学员
        :return 返回学员列表
        '''
        people = getattr(self, role)[role]  # 列表类型
        people.append(person)
        return self