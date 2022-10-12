from flask_app.config.mysqlconnection import connectToMySQL #aqui estamos importando el archivo de los datos, eswte archivo lo creamos despues de server.py

from flask import flash #importamos flash para mandar mensajes de validacion

import re #importando expresiones regulares

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]+$') #Expresion regular de email



class User:

    def __init__(self, data): #data va a ser un diccionario que va a llevar todos los datos
        #data= {"id":1, "first_name":"Elena", "last_name": "De Troya", "email": "elena@codingdojo.com", "created_at": "2022-09-26", "updated_at": "2022-09-26"}
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

#PRIMERO HACEMOS LAS VALIDACIONES
    @staticmethod
    def valida_usuario(formulario):
        is_valid= True
        #validadmos que el nombre tenga al menos 3 caracteres
        if len(formulario['first_name']) < 3:
            flash('Nombre debe tener al menos 3 caracteres', 'registro')#registro es una categoria
            is_valid = False

        if len(formulario['last_name']) < 3:
            flash('Apellido debe tener al menos 3 caracteres', 'registro')
            is_valid = False

        if len(formulario['password']) < 6:
            flash('Contraseña debe tener al menos 6 caracteres', 'registro')
            is_valid = False

        #Verificamos que las contrseñas coincidan
        if formulario['password']!=formulario['confirm-password']:
            flash('Contraseñas no coinciden','registro')
            is_valid = False

        #Revissamos que email tenga el formato correcto a travez de las expresiones regulares:
        if not EMAIL_REGEX.match(formulario['email']):
            flash('E-mail invalido', 'registro')
            is_valid = False

        #Consultamos si existe el correo electronico
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL('recetas').query_db(query, formulario)
        if len(results) >= 1:
            flash('E-mail resgistrado previamente', 'registro')
            is_valid = False

        return is_valid
#SEGUNDO REALIZAMOS LA FUNCION DE GUARDAR USUARIO EN LA BASE DE DATOS
    @classmethod
    def save(cls, formulario):
        query = "INSERT INTO users(first_name, last_name, email, password) VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s)"
        result= connectToMySQL('recetas').query_db(query, formulario)
        return result #Esto ingresa el nuevo ID al usuario ingresado

#CREAMOS UNA FUNCION PARA VERIFICAR EL INGRESO POR LOGIN  DEL USUARIO, SI ESQUE ESTA O NO EN LA BASE DE DATOS
    @classmethod
    def get_by_email(cls, formulario):
        query = "SELECT * FROM users WHERE email = %(email)s"
        result = connectToMySQL('recetas').query_db(query, formulario)
        if len(result) < 1: #Esto comprueba si la lista contiene el nombre en la base de datos, si la lista esta vacia, entonces no existe el usuario ingresado
            return False
        else:
            #Me regresa una lista con UN registro, correspondiente al usuario de ese email
            user = cls(result[0])
            return user

    @classmethod
    def get_by_id(cls, formulario):
        query = "SELECT * FROM users WHERE id = %(id)s"
        result = connectToMySQL('recetas').query_db(query, formulario)
        user = cls(result[0]) #con esta linea creamos una onstancia de User
        return user

