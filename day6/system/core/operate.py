#!/usr/bin/env python
# _*_coding:utf-8_*_
'''
 * Created on 2017/3/12 22:02.
 * @author: Chinge_Yang.
'''

import os
from core import logger
from conf import settings
from lib.people import *
from lib.account import Account
from lib.banji import Banji
from lib.course import Course

user_data = {  # 初始化帐户数据
    'account_id': None,
    'is_authenticated': False,
    'account_data': None
}

log_type = "system"  # 系统日志记录到文件中
system_logger = logger.logger(log_type)


def check_login(func):
    '''
    检查是否登录
    :return:
    '''

    def inner(*args, **kwargs):
        if user_data.get("is_authenticated", None):
            ret = func(*args, **kwargs)
            return ret
        else:
            # 登录流程：通过输入用户、密码，取用户得到用户对应的id的帐户，再对比密码
            print("\033[33;1mPlease sign in!\033[0m")
            person = Person()
            person.sign_in()  # 帐户登录
            if person.account:
                user_data["is_authenticated"] = 1
                user_data["account_id"] = person.account.account_id
                user_data["account_data"] = person  # 对象
                print("\033[32;1mSign in success!\033[0m")
                system_logger.info("Account {} sign in successed".format(user_data["account_id"]))
            else:
                system_logger.info("Sign in failed")

    return inner


def check_authority(arg):
    '''
    检查权限
    :return:
    '''

    def _check_authority(func):
        def inner(*args, **kwargs):
            person = user_data["account_data"]
            if person.account.authority == arg:
                ret = func(*args, **kwargs)
                return ret
            else:
                print("Account \033[31;1m{}\033[0m permission access denied.".format(user_data["account_id"]))
                system_logger.info("Account {} permission access denied.".format(user_data["account_id"]))

        return inner

    return _check_authority


def enrole_student():
    '''学员注册
    :return: 注册成功返回帐户，否则返回False
    '''
    student = Student()
    student.enroll()  # 注册帐户
    if student.account:
        print("Account [\033[31;1m%s\033[0m] register sucessed !"
              % student.account.account_id)
        system_logger.info("Account {} register sucessed".format(student.account.account_id))
        user_data["is_authenticated"] = 1
        user_data["account_id"] = student.account.account_id
        user_data["account_data"] = student
        return student
    else:
        print("\033[31;1mAccount register failed !\033[0m")
        system_logger.info("Account register failed")
        return False


@check_login
@check_authority(settings.AUTHORITY['student'])
def select_course(base_db):
    '''学员选课
    :param base_db: 基础数据实例
    '''
    # 判断学员是否已有选课
    student = user_data["account_data"]  # 学员实例
    if type(student.account.user_info) == dict and "courses" in student.account.user_info:
        print("You are learning a course,please check.【暂不支持已选课程情况】")  # 已有选课，不支持选课
        return

    # 先列出学校课程详情
    print('-------------------- 课程信息 ---------------------')
    base_data = base_db.get_data()
    schools = base_data["schools"]
    for school in schools:
        print("学校名称：\033[34;1m{}\033[0m".format(school.school_name))
        school.show_info("courses")
        print("--------------------------------------------------")

    # 选课
    flag = True
    while flag:
        print("Please input the course name of you want to learn,"
              "eg: [ \033[33;1mshanghai_oldboy_school.go\033[0m ]")
        school_course = input(">>: ").strip()
        try:
            s_school = school_course.split(".")[0]  # 选择的学校
            s_course = school_course.split(".")[1]  # 选择的课程
            # 实例化并更新数据库
            for school in schools:
                if school.school_name == s_school:
                    for course in school.courses["courses"]:
                        if course.name == s_course:
                            # student.select_course(course)  # 学员选课
                            student.select_course(user_data["account_id"], s_course)  # 学员选课，用课名
                            school.add_attr_value("students", student)  # 学校添加学员
                            base_db.save_data(base_data)  # 保存数据到数据库
                            print("\033[32;1mSelect course success\033[0m")
                            system_logger.info("{} select course successed".format(user_data["account_id"]))
                            break  # 已匹配到课程，不需要再匹配
                    else:
                        print("\033[31;1mInput error1!\033[0m")  # 课程输入错误

                    break  # 已匹配到学校，不需要再匹配
            else:
                print("\033[31;1mInput error2!\033[0m")  # 学校输入错误

            flag = False
        except Exception as e:
            print("\033[31;1mInput error3!\033[0m")
            flag = True


def modify_instance_info(instance):
    '''
    输入要修改的信息
    :param instance: 实例
    :return: 修改后的实例
    '''
    flag = False
    while not flag:
        # list_dict = instance.__dict__
        # del list_dict["account"]  # 示例显示
        list_dict = {'name': 'ygqygq2', 'sex': "male", 'age': 28}
        print("Input a dict type data to modify your info.eg: {}".format(list_dict))
        info = input(">>: ").strip()
        try:
            info_dict = eval(info)
        except Exception as e:
            info_dict = None  # 避免后面判断出错
            print("\033[31;1mInput error!\033[0m")

        if type(info_dict) == dict:
            # info_set = set(info_dict.keys())  # 转化为集合
            # instance_attr_set = set(instance.__dict__.keys())
            # if info_set.issubset(instance_attr_set):  # 输入合法
            for k in info_dict:  # 逐个修改属性
                setattr(instance, k, info_dict[k])
            flag = True
            # else:
            #     print("\033[31;1mOnly supports the name, age, sex changes!\033[0m")
            #     return False
            return instance
        else:
            print("\033[31;1mInput is not dict type!\033[0m")


@check_login
def modify_info():
    '''修改学员信息，先修改人的信息，因为帐户里的用户信息是人的信息，所以也做相应修改
    '''
    show_info()  # 先显示当前用户帐户信息
    modify_instance_info(user_data["account_data"])  # 修改人的信息
    user_data["account_data"].modify_info(user_data["account_id"])  # 修改帐户信息
    system_logger.info("Account {} modify account user info successed".format(user_data["account_id"]))


@check_login
def show_info():
    '''查看学员信息，其实是查看帐户中的user_info属性
    '''
    print(" 个人信息 ".center(50, "-"))
    user_data["account_data"].account.show_info()


@check_login
def show_school_info(base_db):
    # 列出学校详细信息
    print('-------------------- 学校信息 ---------------------')
    base_data = base_db.get_data()
    schools = base_data["schools"]
    for school in schools:
        print("school name：\033[34;1m{}\033[0m".format(school.school_name))
        school.show_info()
        print("--------------------------------------------------")


def update_school_attr(base_db, attr, action, instance):
    '''学校实例更新属性，讲师、学生、课程、班级'''
    base_data = base_db.get_data()
    schools = base_data["schools"]

    flag = True
    while flag:
        if action == "add":
            print("Please input the name of school which you want to add."
                  "eg: [ \033[33;1mshanghai_oldboy_school\033[0m ]")
            school_str = input(">>: ").strip()  # 字符类型
            for school in schools:
                if school.school_name == school_str:
                    school = school.add_attr_value(attr, instance)  # 更新操作
                    base_db.save_data(base_data)  # 保存数据到数据库
                    print("Update school \033[32;1m{}\033[0m success".format(school.school_name))
                    system_logger.info("{} update school {} success"
                                       "".format(user_data["account_id"], school.school_name))
                    flag = False
                    break  # 已匹配到课程，不需要再匹配
            else:
                print("\033[31;1mInput school name error!\033[0m")
            flag = False  # 暂定失败不再循环输入
            # elif action == "update":


@check_login
@check_authority(settings.AUTHORITY['admin'])
def create_banji(base_db):
    '''创建班级'''
    class_name = input("Please input the class name.\n>>: ").strip()
    course_name = input("Please input the course name.\n>>: ").strip()
    banji = Banji(class_name, [course_name])
    return banji


@check_login
@check_authority(settings.AUTHORITY['admin'])
def create_teacher(base_db):
    '''创建讲师'''
    course_name = input("Input teaching course.\n>>: ").strip()
    teaching = {"teaching": [course_name]}
    teacher = Teacher(teaching=teaching)
    print("\033[33;1mCreate teacher account!\033[0m")
    teacher.enroll(2)  # 注册帐户
    if teacher.account:
        teacher.account.user_info = teaching
        teacher.account.save_data(teacher.account.account_id)
        print("Account [\033[31;1m%s\033[0m] register sucessed !"
              % teacher.account.account_id)
        system_logger.info("Account {} register sucessed".format(teacher.account.account_id))
        return teacher
    else:
        print("\033[31;1mAccount register failed !\033[0m")
        system_logger.info("Account register failed")

    return None


@check_login
@check_authority(settings.AUTHORITY['admin'])
def create_course(base_db):
    '''
    创建课程
    :param base_db: 基础数据库
    :return: 
    '''
    name = input("Please input the course name.\n>>: ").strip()
    price = input("Please input price of zhe course.\n>>: ").strip()
    course = Course(name, price)
    return course


def school_member_operation(base_db, attr, action):
    '''统一入口操作课程、班级、讲师'''
    attrs = {"courses": "course", "banjis": "banji", "teachers": "teacher"}
    attrs_value = attrs.get(attr)
    func_use = "create_{}(base_db)".format(attrs_value)
    member = eval(func_use)
    if member:
        update_school_attr(base_db, attr, action, member)


@check_login
@check_authority(settings.AUTHORITY['admin'])
def banji_students_manager(base_db):
    '''先列出未分配班级的学员，然后再把学员分配到班级中去
    1. 首先班级课程必须包含学员选课；
    2. 相同学校下，学员对应班级一对一；
    '''
    base_data = base_db.get_data()
    # print(base_data["schools"][1].students["students"][0].account.user_info)
    schools = base_data["schools"]
    no_banji_students = []
    no_students_banji = []
    attr_students = "students"
    attr_banji = "banjis"
    attr_courses = "courses"
    print(" 没有班级且已选课的学员 ".center(50, "-"))
    for school in schools:
        print(" \033[34;1m{}\033[0m ".format(school.school_name).center(50, "-"))
        students = getattr(school, attr_students)[attr_students]
        banjis = getattr(school, attr_banji)[attr_banji]
        print("可加入学员的班级：")
        for banji in banjis:
            if banji.status == 0:  # 未开课的班级
                print("class_name：\033[34;1m{}\033[0m\ncourse：\033[34;1m{}\033[0m\n".
                      format(banji.name, banji.courses[attr_courses]))
                no_students_banji.append((school.school_name, banji.name))

        print("可加入班级的学员：")
        for student in students:
            user_info_dict = getattr(student.account, "user_info")
            student_courses_list = user_info_dict["courses"]  # 学员选课
            if student_courses_list and not user_info_dict.get("banji"):  # 一个学员只能属于一个班级
                print("account_id: \033[32;1m{}\033[0m name: \033[32;1m{}\033[0m".
                      format(student.account.account_id, user_info_dict["name"]))
                no_banji_students.append((school.school_name, student.account.account_id))
        print("-".center(50, "-"))

    if not no_banji_students or not no_students_banji:
        print("\033[31;1mNothing to do.\033[0m")
        return

    relations = input("Please send students to join the corresponding class.\n"
                      "eg: \033[34;1mshanghai_oldboy_school.class1.10001\033[0m\n>>: ").strip()
    m_school = relations.split(".")[0]
    m_class = relations.split(".")[1]
    m_account_id = relations.split(".")[2]

    for school in schools:
        if m_school == school.school_name:  # 匹配学校名
            students = getattr(school, attr_students)[attr_students]
            banjis = getattr(school, attr_banji)[attr_banji]
            for student in students:
                user_info_dict = getattr(student.account, "user_info")
                for banji in banjis:
                    if banji.name == m_class and student.account.account_id == int(m_account_id):  # 输入正确，可添加组合
                        banji.add_people(attr_students, student)  # 班级添加学员
                        user_info_dict["banji"] = banji.name  # 学员帐户信息添加班级
                        # print(base_data["schools"][1].students["students"][0].account.user_info)
                        result1 = base_db.save_data(base_data)  # 保存数据到数据库
                        result2 = student.account.save_data(m_account_id)
                        if result1 and result2:
                            print("Account {} join to {} {} \033[32;1msucessed\033[0m".
                                  format(m_account_id, m_school, m_class))
                            system_logger.info(
                                "Account {} join to {} {} sucessed".format(m_account_id, m_school, m_class))
                            return True
                        else:
                            system_logger.info("Account {} join to {} {} failed".
                                               format(m_account_id, m_school, m_class))
                            return False
                else:
                    print("Input the class name \033[31;1m{}\033[0m error".format(m_class))
                    system_logger.info("Account {} join to {} {} failed".
                                       format(m_account_id, m_school, m_class))
                    return False
    else:
        system_logger.info("Account {} join to {} {} failed".format(m_account_id, m_school, m_class))
        print("Input the school name \033[31;m{}\033[0m error".format(m_school))

    return False


@check_login
@check_authority(settings.AUTHORITY['admin'])
def account_locker(status):
    user_name = input("Please input the user name you will to modify.\n>>: ").strip()
    tmp_account = Account(user_name, "")  # 创建临时对象
    account_id = tmp_account.get_account_id(user_name)  # 由用户名获取对应id
    tmp_account = tmp_account.get_account_data(account_id)  # 获取id对应对象
    tmp_account.status = status  # 修改状态
    tmp_account.save_data(account_id)  # 保存


@check_login
@check_authority(settings.AUTHORITY['teacher'])
def course_scheduling(base_db):
    '''授课排课
    调用个人帐户信息修改函数，添加排课信息,
    导师中用户排课信息格式： {"course_scheduling": { "Friday": {"class1": "java"}}}
    班级中排课信息格式：{"course_scheduling": { "Friday": {"teacher_name": "java"}}}
    '''
    base_data = base_db.get_data()
    schools = base_data["schools"]
    teacher = user_data['account_data']
    attr_techers = "teachers"
    school = which_school(base_db, user_data['account_id'], attr_techers)  # 获取属于哪个学校
    attr_user_info = "user_info"
    attr_course_scheduling = "course_scheduling"
    week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    user_info_dict = getattr(teacher.account, attr_user_info)
    teacher_course_scheduling_dict = user_info_dict.get(attr_course_scheduling)

    if not teacher_course_scheduling_dict:
        teacher_course_scheduling_dict = {}
    else:
        print(" 排课信息 ".center(50, "-"))
        print("{:<10}{}".format("Week", "Class: Course"))
        for k in teacher_course_scheduling_dict:
            print("\033[33;1m{:<10}\033[0m\033[32;1m{}\033[0m".format(k, teacher_course_scheduling_dict[k]))

    course_scheduling_input = input("Please input course scheduling info.【c】to cancel.\n"
                                    "format likes 【week: course: class_name】"
                                    "eg: \033[34;1mMonday: class1: java, Friday: class1: java\033[0m\n>>: ").strip()
    if course_scheduling_input == "c" or course_scheduling_input == "C":
        return

    course_scheduling_list = course_scheduling_input.split(",")
    for l in course_scheduling_list:
        week_day = l.split(":")[0].strip()
        class_name = l.split(":")[1].strip()
        course_name = l.split(":")[2].strip()
        teacher_course_scheduling_dict[week_day] = {class_name: course_name}

        # 判断输入的星期是否正确
        if not week_day in week:
            print("Your input week \033[31;1m{}\033[0m is error,skip add \033[31;1m{}\033[0m".format(week_day, l))
            continue

        # 判断输入的班级名是否在这天已有排课、添加排课
        result1 = modify_banji_course_scheduling(school, class_name, week_day, user_info_dict["name"], course_name)
        user_info_dict[attr_course_scheduling] = teacher_course_scheduling_dict
        if result1:
            school = result1
        number = 0
        while number < len(schools):
            if schools[number].school_name == school.school_name:
                schools[number] = school
            number += 1

        base_db.save_data(base_data)  # 保存数据到数据库
        result2 = teacher.account.save_data(user_data["account_id"])  # 保存数据

        if result2:
            print("Add ourse scheduling \033[32;1m{}\033[0m successed!".format(l))
            system_logger.info("Account {} Course scheduling modify successed".format(user_data["account_id"]))


def modify_banji_course_scheduling(school, class_name, week, teacher_name, course_name):
    '''查看指定班级排课，班级排课信息格式：{'course_scheduling': {
                                                {"Friday": {"teacher_name": "java"},
                                                {"Monday": {"teacher_name": "java"}
                                                }
                                            }
    :param school: 学校对象
    :param class_name: 班级名
    :param week: 星期
    :param teacher_name: 导师名称
    :param course_name: 课程名称
    :return : 指定时间有查询结果，返回真
    '''
    attr_banji = "banjis"
    attr_teacher = "teachers"
    attr_course_scheduling = "course_scheduling"
    banji_dict = getattr(school, attr_banji)

    banji_list = banji_dict[attr_banji]
    for banji in banji_list:
        if banji.name == class_name:
            exist_flag = hasattr(banji, attr_course_scheduling)
            if exist_flag:
                course_scheduling_dict = getattr(banji, attr_course_scheduling)
                if course_scheduling_dict.get(attr_course_scheduling).get(week):  # 已有选课
                    print("\033[31;1m{}\033[0m existing course selection on \033[31;1m{}\033[0m,skip add."
                          .format(course_scheduling_dict[attr_course_scheduling].get(week), week))
                    return None
            else:
                course_scheduling_dict = {attr_course_scheduling: {}}

            course_scheduling_dict[attr_course_scheduling][week] = {teacher_name: course_name}
            setattr(banji, attr_course_scheduling, course_scheduling_dict)
            banji.add_people(attr_teacher, user_data['account_data'])  # 班级添加讲师

    return school


@check_login
@check_authority(settings.AUTHORITY['teacher'])
def show_banji_students(base_db):
    '''按班级查看学员
    学员班级应和讲师属于同一学校，所以先获取讲师所在学校
    '''
    attr_teacher = "teachers"
    attr_student = "students"
    attr_banji = "banjis"
    class_name = ""
    while not class_name:
        class_name = input("Please input the class name of you will to see the student.\n"
                           "class_name >>: ").strip()
    banji = which_banji(base_db, class_name)  # 查询班级
    flag = whether_in_banji(banji, user_data['account_id'], attr_teacher)  # 确认讲师查询的班级是否为授课班级
    if not flag:
        print("This class \033[31;1m{}\033[0m is not what you teaching class!".format(class_name))
        return False

    account_id = input("Please input the account id of you will to see the student.【space】to see all students.\n"
                       "account_id >>: ").strip()
    students_list = banji.students[attr_student]
    for student in students_list:
        if not account_id or student.account.account_id == int(account_id):  # 为空时，显示所有学员信息
            print(" 学员\033[34;1m[{}]\033[0m信息 ".format(account_id).center(50, "-"))
            student.account.show_info()
            return True
        else:
            print("Account \033[31;1m{}\033[0m is not in \033[31;1m{}\033[0m!".format(account_id, class_name))
            return False

    else:
        print("You look at the class \033[31;1m{}\033[0m and you are not the same school "
              "\033[31;1m{}\033[0m!".format(class_name, school.school_name))

    return False


@check_login
@check_authority(settings.AUTHORITY['teacher'])
def modiy_students_grades(base_db):
    '''修改学员成绩
    学员成绩格式：{"grades": {"date": 2017-04-08,"grade": 80}}
    1. 先确认学员是否为讲师学生，即讲师只能修改所教班级学员的成绩；
    '''
    base_data = base_db.get_data()
    schools = base_data["schools"]
    # teacher = user_data['account_data']
    attr_techers = "teachers"
    attr_students = "students"
    attr_grades = "grades"
    school = which_school(base_db, user_data['account_id'], attr_techers)  # 获取属于哪个学校
    attr_user_info = "user_info"
    student_grades = input("Please input students grades.【c】to cancel.\n"
                           "format likes 【date: class_name: account_id: grade】"
                           "eg: \033[34;1m2017-04-08: class1: 10001: 80,"
                           "2017-04-08: class1: 10002: 77\033[0m\n>>: ").strip()
    if student_grades == "c" or student_grades == "C":
        return
    grades_list = student_grades.split(",")
    have_flag = False
    for l in grades_list:
        if not len(l.split(":")) == 4:
            print("\033[31;1mPlease confirm the input!,\033[0m"
                  "skip add \033[31;1m{}\033[0m".format(l))
            continue
        examination_date = l.split(":")[0].strip()
        class_name = l.split(":")[1].strip()
        account_id = l.split(":")[2].strip()
        grade = l.split(":")[3].strip()
        banji = which_banji(base_db, class_name)  # 获取学员班级
        teachers = getattr(banji, attr_techers)[attr_techers]  # 从班级获取讲师
        students = getattr(banji, attr_students)[attr_students]  # 从班级获取学员
        for t in teachers:  # 判断输入的班级名的班级是否有该讲师
            if t.account.account_id == user_data['account_id']:
                have_flag = True
                break

        if not have_flag:
            print("\033[31;1mPlease confirm the input class name!,\033[0m"
                  "skip add \033[31;1m{}\033[0m".format(l))
            continue

        for s in students:  # 判断输入的学号是否在班级中
            if s.account.account_id == int(account_id):
                user_info_dict = s.account.user_info
                user_info_dict[attr_grades] = {"date": examination_date, "grade": grade}
                s.account.save_data(account_id)  # 保存数据

                number = 0
                while number < len(schools):
                    if schools[number].school_name == school.school_name:
                        schools[number] = school
                    number += 1

                # print(base_data["schools"][1].students["students"][0].account.user_info)
                result = base_db.save_data(base_data)  # 保存数据到数据库
                if result:
                    print("Account \033[32;1m{}\033[0m grades modify successed!".format(account_id))
                    system_logger.info("Account {} grades modify successed".format(account_id))
                    continue
            else:
                print("Account \033[31;1m{}\033[0m is not in \033[31;1m{}\033[0m!"
                      "skip add \033[31;1m{}\033[0m".format(account_id, class_name, l))


@check_login
@check_authority(settings.AUTHORITY['student'])
def show_banji_info(base_db):
    '''学员查看班级信息'''
    attr_student = "students"
    attr_banji = "banjis"
    school = which_school(base_db, user_data['account_id'], attr_student)  # 获取属于哪个学校
    class_name = user_data['account_data'].account.user_info.get("banji")  # 获取所在班级名
    if class_name:
        banjis = getattr(school, attr_banji)[attr_banji]
        for banji in banjis:
            if banji.name == class_name:
                banji.show_info()
                return True
        else:
            print("Your class \033[31;1m{}\033[0m no longer exists!".format(class_name))
            return False
    else:
        print("\033[31;1mYou did not join any class!\033[0m")
        return False


# @check_login
def which_school(base_db, account_id, role):
    '''按account_id查询属于哪个学校'''
    school_result = ""
    base_data = base_db.get_data()
    schools = base_data["schools"]
    for school in schools:
        people_dict = getattr(school, role)
        people_list = people_dict[role]
        if people_list:
            for people in people_list:
                if people.account.account_id == int(account_id):  # 查到匹配正确
                    school_result = school
                    return school_result
    else:
        print("\033[31;1mDoes not belong to any school!\033[0m")

    return school_result


def which_banji(base_db, class_name):
    '''按class_name查询属于哪个班级'''
    banji_result = ""
    attr_banji = "banjis"
    base_data = base_db.get_data()
    schools = base_data["schools"]
    for school in schools:
        banjis = getattr(school, attr_banji)[attr_banji]
        for banji in banjis:
            if banji.name == class_name:
                banji_result = banji
                return banji_result

    return banji_result


def whether_in_banji(banji, account_id, role):
    '''判断是否在班级中'''
    result_flag = False
    people_dict = getattr(banji, role)
    people_list = people_dict[role]
    if people_list:
        for people in people_list:
            if people.account.account_id == int(account_id):  # 查到匹配正确
                result_flag = True
                break

    return result_flag
