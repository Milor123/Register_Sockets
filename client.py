# /usr/bin/env python 2.7
# -*- coding: utf-8 -*-
"""
Title: Simple register user platform
Description: A platform to register user, ideally of a university, asking them for the personal data
Poo usage: Encapsulation, some design patrons, multiple inheritance, threading, polymorphism, abstraction
Author: Mateo Bohorquez
Nickname:
 __  __   _   _                  _   ____    _____
|  \/  | (_) | |   ___    _ __  / | |___ \  |___ /
| |\/| | | | | |  / _ \  | '__| | |   __) |   |_ \
| |  | | | | | | | (_) | | |    | |  / __/   ___) |
|_|  |_| |_| |_|  \___/  |_|    |_| |_____| |____/
"""

###############################
######### Decotators ##########
###############################
import cPickle as pickle
import threading
import socket
from abc import ABCMeta, abstractmethod
from deco.decorator import requiere
import pdb

# Person inherit from threading.Thread
# owing to we would need divide process in the sub nucleus, when multiple users registers required

def connect():
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
        ####################################
        # Initialization of thread for class
        #threading.Thread.__init__(self)
        #self.start()  # run class as thread
        #####################################

        self.name = name
        self.last_name = last_name
        self.age = age
        self.sex = sex
        self.identification = identification
        #Register(self)
        #pickle.HIGHEST_PROTOCOL = -1

        global socketconn
        stringobj = pickle.dumps(self, -1)
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
print 'client'
connect()
Student('maria', 'soaaex', 2, 'famale', '1225689')
Teacher('Joseeeeaa', 'Boleor', 4, 'Famale', '236991')
pdb.set_trace()
socketconn.close()
#Student('jose', 'Boleor', 4, 'Male', '5536991')
#Student('Joseeeeaa', 'Boleor', 4, 'Famale', '236991')
#print '=============================================='
#print query.DB
#print '=============================================='
#print query('name=maria').result

#Student('jose', 'Boleor', 4, 'Male', '78777777777777')
# Note: The Data printed, show step by step the creation of dict, on the one hand corresponds to the database


