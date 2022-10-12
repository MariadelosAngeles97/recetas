#importamos flask
from flask import Flask

#inicializamos las app
app = Flask(__name__)

#Declaramos la llave secreta
app.secret_key = "llave secretisima"