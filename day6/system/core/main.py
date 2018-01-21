#!/usr/bin/env python
# _*_coding:utf-8_*_
'''
 * Created on 2017/3/2 22:16.
 * @author: Chinge_Yang.
'''

from core import operate
from lib.base import BaseDb

base_db = BaseDb()  # 第一次运行生成初始化数据库，后续登录读取数据库到内存


def interactive(menu, menu_dict):
    """
    与用户交互
    :param menu: 列表提示
    :param menu_dict: 功能列表
    :return:
    """
    exit_flag = False
    while exit_flag != "b":  # 不为b，则一直循环
        print(menu)
        user_option = input(">>:").strip()
        if user_option in menu_dict.keys():
            # print(menu_dict[user_option])
            exit_flag = eval(menu_dict[user_option])
        else:
            print("\033[31;1mOption does not exist!\033[0m")


def logout():
    exit(" 谢谢使用 ".center(50, "#"))


def callback(action=None):
    # 注销帐户
    if action == "logout":
        operate.user_data = {'account_id': None,
                             'is_authenticated': False,
                             'account_data': None}
    break_flag = "b"
    # print(operate.user_data)
    return break_flag


def system_student():
    '''
    学员系统
    :return:
    '''
    menu = '''
----------------- 欢迎进入学员系统 -----------------
    1.  \033[33;1m学员注册\033[0m
    2.  \033[34;1m进入选课\033[0m
    3.  \033[35;1m查看班级\033[0m
    4.  \033[36;1m查看个人信息\033[0m
    5.  \033[37;1m修改个人信息\033[0m
    6.  后退（注销）
--------------------------------------------------
    '''

    menu_dic = {
        '1': 'operate.enrole_student()',
        '2': 'operate.select_course(base_db)',
        '3': 'operate.show_banji_info(base_db)',
        '4': 'operate.show_info()',
        '5': 'operate.modify_info()',
        '6': 'callback("logout")'
    }

    interactive(menu, menu_dic)


def system_teacher():
    '''
    讲师系统
    :return:
    '''
    menu = '''
----------------- 欢迎进入讲师系统 -----------------
    1.  \033[33;1m授课排课\033[0m
    2.  \033[34;1m查看学员信息\033[0m
    3.  \033[35;1m修改学员成绩\033[0m
    4.  \033[36;1m查看个人信息\033[0m
    5.  \033[37;1m修改个人信息\033[0m
    6.  \033[38;1m查看学校\033[0m
    7.  后退（注销）
--------------------------------------------------
    '''

    menu_dic = {
        '1': 'operate.course_scheduling(base_db)',
        '2': 'operate.show_banji_students(base_db)',
        '3': 'operate.modiy_students_grades(base_db)',
        '4': 'operate.show_info()',
        '5': 'operate.modify_info()',
        '6': 'operate.show_school_info(base_db)',
        '7': 'callback("logout")'
    }

    interactive(menu, menu_dic)


def system_manager():
    '''
    管理系统
    :return:
    '''
    menu = '''
----------------- 欢迎进入管理系统 -----------------
    1.  \033[33;1m教务管理\033[0m
    2.  \033[34;1m帐号管理\033[0m
    3.  后退（注销）
--------------------------------------------------
    '''

    menu_dic = {
        '1': 'educational_administration()',
        '2': 'account_manager()',
        '3': 'callback("logout")'
    }

    interactive(menu, menu_dic)


def educational_administration():
    '''
    管理系统
    :return:
    '''
    menu = '''
--------------- 欢迎进入教务管理系统 ----------------
--------------------------------------------------
    1.  \033[33;1m创建班级\033[0m
    2.  \033[34;1m创建课程\033[0m
    3.  \033[35;1m创建讲师\033[0m
    4.  \033[36;1m班级学员管理\033[0m
    5.  \033[37;1m查看学校\033[0m
    6.  后退
--------------------------------------------------
    '''

    menu_dic = {
        '1': 'operate.school_member_operation(base_db, "banjis", "add")',
        '2': 'operate.school_member_operation(base_db, "courses", "add")',
        '3': 'operate.school_member_operation(base_db, "teachers", "add")',
        '4': 'operate.banji_students_manager(base_db)',
        '5': 'operate.show_school_info(base_db)',
        '6': 'callback()'
    }

    interactive(menu, menu_dic)


def account_manager():
    '''
    帐户管理
    :return:
    '''
    menu = '''
--------------- 欢迎进入帐户管理系统 ----------------
--------------------------------------------------
    1.  \033[33;1m锁定帐号\033[0m
    2.  \033[34;1m解锁帐号\033[0m
    3.  后退
--------------------------------------------------
    '''

    menu_dic = {
        '1': 'operate.account_locker(0)',
        '2': 'operate.account_locker(1)',
        '3': 'callback()'
    }

    interactive(menu, menu_dic)


def begin():
    '''
    开始入口
    :return:
    '''
    menu = '''
----------------- 欢迎进入选课系统 -----------------
    1.  \033[33;1m学员系统\033[0m
    2.  \033[34;1m讲师系统\033[0m
    3.  \033[35;1m系统管理\033[0m
    4.  退出
--------------------------------------------------
    '''
    menu_dic = {
        '1': 'system_student()',
        '2': 'system_teacher()',
        '3': 'system_manager()',
        '4': 'logout()'
    }

    interactive(menu, menu_dic)


def run():
    """
    程序运行主函数
    :return:
    """
    begin()
