import SocketServer
from deco.decorator import requiere
import pdb
import cPickle as pickle
from structure import Person, Student, Teacher

class tcpserver(SocketServer.BaseRequestHandler):

    def handle(self):
        self.Data = self.request.recv(1024)
        try:
            loadobj= pickle.loads(self.Data)
            Register(loadobj)
            self.request.send('The user has been successfully registered.')
            pdb.set_trace()
        except pickle.UnpicklingError:
            myquery= Query(self.Data)
            stringquery = pickle.dumps(myquery, -1)
            self.request.send(stringquery)
        except NameError as e:
            self.request.send('Error: {}'.format(e))


    def register(self):
        Register(self.Persona)


def main():
    host = ('127.0.0.1', 9994)
    server = SocketServer.TCPServer(host, tcpserver)
    server.serve_forever()


class Data(list):
    ID = '-1'

    @staticmethod
    def idplus():
        Data.ID = str(int(Data.ID)+1)


class Register(Data, object):

    student = object
    __DB = Data()
    code = str

    # polymorphism
    def __init__(self, person=None):
        # need a instanced student object
        self.People = person
        if self.__verify():
            self.__generate_code()
            self.__generate_user()

    def __verify(self):
        for __info in self.__DB:  # iter arrays for get dicts [[dict],[dict2]]
            if __info.get('identification') == self.People.identification \
                    and __info.get('status') == self.People.status:
                # if identification is found in DB, and try register with the same status
                raise NameError ('the people has already been registered previously, try ask about your status')
            elif __info.get('identification') == self.People.identification \
                    and not __info.get('status') == self.People.status:
                # if was found but he try register with another status
                self.__generate_code()
                self.__DB.idplus()  # ID = ID + 1
                self.__save(__info.get('user'), __info.get('password'), self.__DB.ID)
                return False  # use Return False in order that not continue with the other functions such as:
                # __generate code... __generate user due to we don't want change user
        return True

    def __generate_code(self):
        import random
        import string

        # code for students or teacher, it depend polymorphism conditional
        # ST_ > STudent, and TE_ > TEacher
        self.code = '{}_{}{}{}'.format('ST_' if self.People.status == 'student' else
                                       'TE_' if self.People.status == 'teacher' else 'CODE ERROR::::',
                                       self.People.last_name[0:2],
                                       ''.join(
                                        [random.choice(string.letters) for x in range(10)]
                                            ),
                                       self.People.identification[0:2])

    def __generate_user(self):
        # generate user
        import random
        import string
        __user = '{}{}{}{}'.format(self.People.last_name[0],
                                   self.People.name,
                                   self.People.identification[0:2],
                                   random.choice(string.letters)
                                   )

        __password = '{}{}{}'.format(self.People.identification,
                                     self.code[0:3],
                                     random.choice(string.letters)
                                     )
        self.__DB.idplus()  # ID = ID + 1
        self.__save(__user, __password, self.__DB.ID)

    @requiere(str, str, str)
    def __save(self, __user, __password, id):
        # preparing all data for send
        __data = {'user': __user,
                  'password': __password,
                  'name': self.People.name,
                  'last_name': self.People.last_name,
                  'identification': self.People.identification,
                  'age': self.People.age,
                  'sex': self.People.sex,
                  'status': self.People.status,
                  'code': self.code,
                  'ID': id
                  }

        self.__DB.append(__data)
        Query.DB = self.__DB

        ####################
        #### Data Print ####
        ####################

        #print self.__DB


class Query(object):
    DB = []
    def __init__(self, attr, **kwargs ):
        self.attr = attr
        self.attrvalue = self.getattrvalue(attr)
        self.result = self.getinfo()

    def getattrvalue(self, attr):
        import re
        exp = r"([a-zA-Z0-9]+)=([a-zA-Z0-9]+)"
        expresion = re.compile(exp)
        result = expresion.search(attr)
        return [result.group(1), result.group(2)]

    def getinfo(self):
        import re
        # Case sentive for password
        if self.attrvalue[0]!='password':
            expresion = re.compile(r'^{}$'.format(self.attrvalue[1]), flags=re.IGNORECASE)
        else:
            expresion = re.compile(r'^{}$'.format(self.attrvalue[1]))
        # iter array
        for x in self.DB:
            # then search attrvalue[0], it contain type information to search
            if self.attrvalue[0] in x:
                # search with the regular expression with the get value of the
                # key
                if expresion.search(x.get(self.attrvalue[0])):
                    return x
        return None
print 'xd'
main()
#Student('maria', 'soaaex', 2, 'famale', '1225689')
#Student('jose', 'Boleor', 4, 'Male', '5536991')
#Student('Joseeeeaa', 'Boleor', 4, 'Famale', '236991')
#print '=============================================='
#print query.DB
#print '=============================================='
#print query('name=maria').result
#Teacher('Joseeeeaa', 'Boleor', 4, 'Famale', '236991')
#Student('jose', 'Boleor', 4, 'Male', '78777777777777')
# Note: The Data printed, show step by step the creation of dict, on the one hand corresponds to the database


