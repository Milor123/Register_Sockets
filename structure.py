import cPickle as pickle
import threading
import socket
from abc import ABCMeta, abstractmethod
from deco.decorator import requiere
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
        #pickle.HIGHEST_PROTOCOL
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


