# /usr/bin/env python 2.7
# -*- coding: utf-8 -*-

class work(object):
    informacion = {}
    informacion_completa = []

    def multiplicacion(self,multiplicando,inicio,fin):
        for x in range(inicio,fin+1):
            print '{}x{} = {}'.format(multiplicando,x,(multiplicando*x))

    def oscilacion(self,inicio,fin,sexo=0):
        #sex values 0=null 1=Male, 2=Famale
        paquete = []
        for x in self.informacion_completa:
            if int(x['Edad'])>=inicio and int(x['Edad'])<=fin:
                if sexo==1 and x['Genero']=='Male':
                    paquete.append(x['Nombre'])
                if not sexo:
                    paquete.append(x['Nombre'])
                if sexo==2 and x['Genero']=='Famale':
                    paquete.append(x['Nombre'])
        return paquete

    def convert_genero(self,genero):
        if genero=='Both':
            genero=0
        if genero=='Male':
            genero=1
        if genero=='Famale':
            genero=2
        return genero

    def encuesta(self):
        numero_encuesta= int(raw_input('cuantas personas deseas encuestar'))
        for x in range(numero_encuesta):
            self.informacion['Nombre'] = raw_input('Ingresa el nombre')
            self.informacion['Edad'] = raw_input('Ingresa la Edad')
            self.informacion['Genero'] = raw_input('Ingresa el Genero')

            self.informacion_completa.append(dict(self.informacion))
            print '===========================================\n'

        while True:
            print('Escribe a para Obtener el nombre y numero total de encuestados, segun su edad y/o genero \n\
            Escribe el numero 0 para salir')
            print '=======================================\n'
            letra=raw_input('Ingresa la letra')

            if letra=='0':
                break

            if letra=='a':
                edad_minima= int(raw_input('Escriba la minima edad que puede tener '))
                edad_maxima= int(raw_input('Escriba la maxima edad que puede tener'))
                genero= raw_input('Escriba el genero')
                genero = self.convert_genero(genero)


                for x in self.oscilacion(edad_minima,edad_maxima,genero):
                    print x
                print 'numero total:' + str(len(self.oscilacion(edad_minima,edad_maxima,genero)))


#Instance = work()
#Instance.multiplicacion(5,1,5)
#Instance.encuesta()
