#!/usr/bin/env python
# _*_coding:utf-8_*_
'''
 * Created on 2017/3/5 14:18.
 * @author: Chinge_Yang.
'''

import pickle
import os
from conf import settings
from lib.db import Db
from lib.course import Course
from lib.school import School
from lib.account import Admin


class BaseDb(object):
    '''基础数据库类'''

    db = Db(settings.BASE_DATABASE)  # 数据库连接
    db_path = "%s/base.db" % db.db_handler()

    def __init__(self):
        '''
        初始基础数据课程和学校
        '''
        if os.path.exists(BaseDb.db_path):  # 初始数据库存在时，不做任何操作
            return None

        # 创建课程3门，linux、python、go课程
        go = Course("go", 8000)
        linux = Course("linux", 10800)
        python = Course("python", 8800)

        # 创建学校2所，北京老男孩、上海老男孩
        beijing_oldboy_school = School("beijing_oldboy_school", "beijing",
                                       {"teachers": []}, {"courses": [linux, python]},
                                       {"students": []}, {"banjis": []})
        shanghai_oldboy_school = School("shanghai_oldboy_school", "shanghai",
                                        {"teachers": []}, {"courses": [go]},
                                        {"students": []}, {"banjis": []})
        base_data = {
            "schools": [beijing_oldboy_school, shanghai_oldboy_school],
        }
        self.save_data(base_data)

        admin_username = "admin"
        admin_password = "admin"
        status = 1
        authority = 8
        admin = Admin(admin_username, admin_password, status, authority)
        admin.create()

    def save_data(self, base_data):
        '''保存基础数据库
        :param base_data: 基础数据
        :return
        '''
        BaseDb.db.dump_pickle_data(BaseDb.db_path, base_data)  # 写入数据库
        return True

    def get_data(self):
        base_data = BaseDb.db.load_pickle_data(BaseDb.db_path)
        # 从数据库读取学员信息
        schools = base_data["schools"]
        attr_students = "students"
        attr_teachers = "teachers"
        for school in schools:
            students = getattr(school, attr_students)[attr_students]
            teachers = getattr(school, attr_teachers)[attr_teachers]
            for student in students:
                account_id = student.account.account_id
                student.account = student.account.get_account_data(account_id)
                user_info_dict = student.account.user_info
                student.name = user_info_dict.get("name")
                student.sex = user_info_dict.get("sex")
                student.age = user_info_dict.get("age")
            for teacher in teachers:
                account_id = teacher.account.account_id
                teacher.account = teacher.account.get_account_data(account_id)
                user_info_dict = teacher.account.user_info
                teacher.name = user_info_dict.get("name")
                teacher.sex = user_info_dict.get("sex")
                teacher.age = user_info_dict.get("age")
        return base_data


