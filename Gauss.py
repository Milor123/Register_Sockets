# /usr/bin/env python 2.7
######### Author: Mateo Bohorquez #########
###########################################
############## Decorators #################
###########################################

def requiere(*types):
    def realfn(func):
        def wrapper(*args):
            newarg= args[1:]
            for key,mytypes in enumerate(types):
                if not mytypes is type(newarg[key]):
                    # __name__ for parser object of type method.
                    print 'Escribe valores del tipo {}'.format([x.__name__ for x in types])
                    exit()
            return func(*args)
        return wrapper
    return realfn


def verify_read(func):
    def read_wrapper(*args):
        if not type(args[1]) is int or not type(args[2]) is int:
            print 'Error: You value must be int'
            exit()
        else:
            if args[1]==args[2]:
                print 'Error: The columnas field must be higher than filas field'
                exit()
        return func(*args)
    return read_wrapper

class Gausvssort(object):

    def __init__(self):
        filas=0
        columnas=0

    @verify_read
    @requiere(int,int)
    def read(self,filas,columnas):
        if filas>=3 and columnas>3 and filas==columnas-1:
            self.filas=filas
            self.columnas=columnas-1
            matrix= []
            for x in range(filas):
                data= raw_input('Ingrese las fila, sus items separados por espacios').split(' ')
                #matrix= [[2.0,3.0,5.0,7.0],[3.0,2.0,9.0,4.0],[7.0,5.0,3.0,4.0]]
                data = list(map(float, data))
                matrix.append(data)

        return matrix

    @requiere(list,float)
    def multiply_scalarvector(self, vector, number):
        return [x * number for x in vector]

    @requiere(list,float)
    def divide_scalarvector(self, vector, number):
        return [round(x / float(number), 3) for x in vector]

    @requiere(list,list)
    def sum_vector(self,vector,vector_sum):
        return [x+b for x,b in zip(vector,vector_sum)]

    @requiere(list,list)
    def rest_vector(self,vector,vector_rest):
        return [x-b for x,b in zip(vector,vector_rest)]

    @requiere(list,int,int)
    def change_position_vector(self,matrix,newindex, oldindex):
        matrix.insert(newindex,matrix.pop(oldindex))
        return matrix

    @requiere(list, bool)
    def T(self,matrix, ST=False):
        #transpose matrix >> row for columns
        print matrix
        newmatrix = [list(x) for x in zip(*matrix)]
        if not ST:
            return newmatrix
        else:
            # Special Transpose matrix > result of gauss jordan in column for row,
            # it is neccesary because transpose convert result in column

            for x in range(len(newmatrix)-1):  # Because the ultimate column is the result of gauss jordan
                newmatrix[x].append(newmatrix[-1].pop(0))  # ultime array that then of transposition
                #  is variable result and cant use as column

            del newmatrix[-1]  # delete the empty []
            return newmatrix

    def update(self):
        global FT
        FT=self.T(F, True)

    @requiere(list)
    def write(self, matrix):
        global F
        global FT
        F=matrix[:]

        print 'Original Matrix'
        for x in F:
            print x
        FT=self.T(F, True)
        print '================'
        print 'Transpose Matrix'
        for x in FT:
            print x
        '''
        ================================================================
        Simplify of Gauss Jordan conversion to python by Mateo Bohorquez
        ================================================================
        M1=self.multiply_scalarvector(F[2],F[0][0])
        M2=self.multiply_scalarvector(F[0],F[2][0])
        if F[0][0]>=0 and F[2][0]>=0:
            print (self.rest_vector(M1,M2))
        else:
            print (self.sum_vector(M1,M2))
        '''

        pivoteador = 0
        divipivo=0
        flag= True
        end=True
        for filas in range(len(F)):
            for columnas in range(self.columnas):


                if F[filas][filas]!=1.0 or F[filas][filas]==-1.0 and flag: #and columnas==pivoteador:
                    if FT[filas][filas]>0:
                        F[filas]= self.divide_scalarvector(F[filas],FT[filas][filas])
                    elif FT[filas][filas]<0:
                        F[filas]= self.divide_scalarvector(F[filas],((FT[filas][filas])))

                    elif FT[filas][filas]==0:

                        # if haven't limit
                        if filas < self.filas and filas>0:
                            if F[filas][filas-1]!=0:
                                F = self.change_position_vector(F, filas-1,filas)
                            elif F[filas][filas+1]!=0:
                                F = self.change_position_vector(F, filas+1,filas)

                        # when is in firt time
                        elif filas==0:
                            if F[filas][filas+1]!=0:
                                F = self.change_position_vector(F, filas+1,filas)
                            elif F[filas][filas+2]!=0:
                                F = self.change_position_vector(F, filas+2,filas)

                        # when is the final
                        elif filas==self.filas:
                            if F[filas][filas-1]!=0:
                                F = self.change_position_vector(F, filas-1,filas)
                            elif F[filas][filas-2]!=0:
                                F = self.change_position_vector(F, filas-2,filas)
                    self.update()
                    flag= False

                if (filas,columnas)==(filas,filas):
                    continue


                M1=self.multiply_scalarvector(F[columnas],FT[filas][filas])
                M2=self.multiply_scalarvector(F[filas],FT[filas][columnas])
                print '========= Matrix Actual==========='
                for x in F:
                    print x
                print '===== Cerramos Matrix Actual======\n'
                print 'Multiplicacion actual'
                print 'actualmente FT filas filas es ', str(FT[filas][filas])
                print 'actualmente FT filas columnas es ', str(FT[filas][columnas])
                print 'actualmente F columnas es ', str(F[columnas])
                print 'actualmente F filas es ', str(F[filas])

                print M1
                print M2
                print '==== Cerramos Multiplicacion ======\n'
                if FT[filas][columnas]>0 and FT[filas][filas]>0:
                    F[columnas] = (self.rest_vector(M1,M2))
                    self.update()
                elif FT[filas][columnas]<0 or FT[filas][filas]<0:
                    F[columnas] = (self.rest_vector(M1,M2))
                    self.update()

            flag=True
            pivoteador+=1 #nop


        print 'Result: '
        for x in F:
            print x



########################################################################
###################### For arrays homework #############################
########################################################################

    @requiere(str)
    def minim(self,numbers):
        numbers= numbers.split(',')
        a = numbers[0]
        for x in numbers:
            try:
                if int(a)>=int(x):
                    a = x
            except:
                continue
        return a

    @requiere (str,bool,bool)
    def orderlist(self,numbers, reverse=False, par=False):
        numbers = numbers.split(',')
        relist = []
        n=0
        if not par:
            if not reverse:
                for key,x in enumerate(range(len(numbers))):
                    minim = self.minim(','.join(numbers))
                    relist.append(minim)
                    numbers.remove(minim)
                    n+=1

            if reverse:
                for key,x in enumerate(range(len(numbers))):
                    minim = self.minim(','.join(numbers))
                    relist.insert(0,minim)
                    numbers.remove(minim)
                    n+=1

            return relist

        if par:
            self.flagx=True
            backup=numbers[:]
            capate=numbers
            if not reverse:

                for key,x in enumerate(range(len(numbers))):

                    if self.flagx:
                        for x in range(len(capate)):
                            if x%2!=0:
                                capate[x] = 'x'
                    self.flagx=False
                    minim = self.minim(','.join(capate))
                    relist.append(minim)
                    capate.remove(minim)
                    n+=1

                relist =  [a for a in relist if a!= 'x']
                test=[]
                for x in (relist):
                    for key, a in enumerate(backup):
                            if x==a:
                                test.append(x)
                                test.append(backup[key+1])
                return test


            if reverse:
                for key,x in enumerate(range(len(numbers))):

                    if self.flagx:
                        for x in range(len(capate)):
                            if x%2!=0:
                                capate[x] = 'x'
                    self.flagx=False
                    minim = self.minim(','.join(capate))
                    relist.append(minim)
                    capate.remove(minim)
                    n+=1

                relist =  [a for a in relist if a!= 'x']
                test=[]
                for x in (relist):
                    for key, a in enumerate(backup):
                            if x==a:
                                test.append(x)
                                test.append(backup[key+1])
                reversetest=[]
                print test
                valueofkey=0

                for key,x in enumerate (test):
                    if key%2!=0:
                        reversetest.insert(1,x)
                    else:
                        reversetest.insert(0,x)

                return reversetest
#################################################################################


Instance = Gausvssort()
# =============Gauss jordan isn't working, only experimental code===============
# Try Example. You must use row and columns +1 for your result variable
Instance.write(Instance.read(3,4))

# ==================orderlist is working=========================
# Example:
# print (Instance.orderlist('30,9,5,7,99,25,12,1',True, True))
