# /usr/bin/env python 2.7
# -*- coding: utf-8 -*-
import cPickle as pickle
import threading
import socket
from abc import ABCMeta, abstractmethod
from deco.decorator import requiere
import pdb

class connection(object):
    def __init__(self):
        global socketconn
        host = ('127.0.0.1', 9994)
        socketconn = socket.socket()
        socketconn.connect(host)

class Person(object):
    __metaclass__ = ABCMeta
    name = str
    last_name = str
    age = int
    sex = str
    status = str
    identification = str

    @abstractmethod
    @requiere(str, str, int, str, str)
    def __init__(self, name, last_name, age, sex, identification):

        self.name = name
        self.last_name = last_name
        self.age = age
        self.sex = sex
        self.identification = identification
        # Register(self)
        # pickle.HIGHEST_PROTOCOL = -1
        stringobj = pickle.dumps(self, -1)
        global socketconn
        socketconn.send(stringobj)
        print socketconn.recv(1024)


class Student(Person):

    @requiere(str, str, int, str, str)
    def __init__(self, name, last_name, age, sex, identification):
        self.status = 'student'  # token for student
        # Call the super class, then execute the constructor with the respective data
        super(Student, self).__init__(name, last_name, age, sex, identification)


class Teacher(Person):

    @requiere(str, str, int, str, str)
    def __init__(self, name, last_name, age, sex, identification):
        self.status = 'teacher'  # token for teacher
        super(Teacher, self).__init__(name, last_name, age, sex, identification)

class simple_query(object):

    def __init__(self, attr):
        self.attr = attr
        self.result = self.getdata()

    def getdata(self):
        global socketconn
        socketconn.send(self.attr)
        stringobj = socketconn.recv(1024)
        return pickle.loads(stringobj)

if __name__ == "__main__":
    print 'client'
    connection()
    Student('maria', 'soaaex', 2, 'famale', '1225689')
    Teacher('Joseeeeaa', 'Boleor', 4, 'Famale', '236991')
    pdb.set_trace()
    socketconn.close()
    #Student('jose', 'Boleor', 4, 'Male', '5536991')
    #Student('Joseeeeaa', 'Boleor', 4, 'Famale', '236991')
    #Student('jose', 'Boleor', 4, 'Male', '78777777777777')

