#!/usr/bin/env python
# _*_coding:utf-8_*_
'''
 * Created on 2017/3/11 21:15.
 * @author: Chinge_Yang.
'''

from lib.account import Account


class Person(object):
    '''人基类'''

    def __init__(self, name=None, age=None, sex=None, account=None):
        '''
        定义人的基本属性
        :param name: 名字，字符类型
        :param age: 年龄，数字整型
        :param sex: 性别, 字符类型
        :param account: 帐户，实例
        '''
        self.name = name
        self.age = age
        self.sex = sex
        self.account = account

    def show_info(self):
        '''查看account的user_info属性'''
        print(" User info ".center(50, "-"))
        print("account id: ", self.account.account_id)
        if self.account.user_info:
            print(self.account.user_info)

        print("-".center(50, '-'))

    def enroll(self, authority=1):
        '''注册帐号
        :return 返回帐号实例
        '''
        user_name = input("Please input user name >>: ").strip()
        password = input("Please input password >>: ").strip()
        re_password = input("Please input password confirmation >>: ").strip()
        if password != re_password:
            print("\033[31;1mPasswords do not match!\033[0m")
            return False
        status = 1
        account = Account(user_name, password, status, authority)
        new_account = account.create()
        self.account = new_account
        return self

    def sign_in(self):
        '''登录帐户，返回帐户对象
        '''
        login_flag = False  # 初始化登录标记
        user_name = input("Please input user name >>: ").strip()
        password = input("Please input password >>: ").strip()
        account = Account(user_name, password)
        self.account = account.login()
        if self.account:
            login_flag = self.account
        return login_flag

    def modify_info(self, account_id):
        '''修改个人信息'''
        print("")
        print(self.account.user_info)
        #self.show_info()  # 先显示个人信息
        self.account.user_info = dict(self.account.user_info)
        for d in self.__dict__:
            if d == "account":
                continue
            else:
                self.account.user_info[d] = getattr(self, d)
        print("\033[32;1mUser info modify successed!\033[0m")
        self.account.save_data(account_id)  # 保存数据
        return True

class Teacher(Person):
    '''讲师类'''

    def __init__(self, teaching, name=None, age=None, sex=None):
        '''
        定义讲师属性
        :param name: 名字，字符类型
        :param age: 年龄，数字整型
        :param sex: 性别，字符类型
        :param teaching: 所教课程，字典类型，如{"teaching": [go]}
        '''
        Person.__init__(self, name=None, age=None, sex=None)
        self.teaching = teaching

    def modify_info(self):
        '''教的课程'''
        pass


class Student(Person):
    '''
    学员类
    '''

    # def __init__(self, name=None, age=None, sex=None, courses=None):
    #     '''
    #     定义学员属性
    #     :param courses: 课程
    #     '''
    #     Person.__init__(self, name=None, age=None, sex=None)
    #     self.courses = courses

    def select_course(self, account_id, course):
        '''选课,其实是把课程信息更新到帐户中
        :param course: 课程名，字符类型
        '''
        self.account.user_info = dict(self.account.user_info)
        self.account.user_info["courses"] = [course]
        self.account.save_data(account_id)
        return True


