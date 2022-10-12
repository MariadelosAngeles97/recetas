#importamos la flask_app
from flask_app import app

#aqui debemos importar los controladores
from flask_app.controllers import users_controller, recipes_controller

#Ejecucion de la app
if __name__=="__main__":
    app.run(debug=True)

