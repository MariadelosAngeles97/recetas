#importamos Flask y lo que utilizamos de flask
from flask import Flask, render_template, request, redirect, session, flash

#importamos la app
from flask_app import app

#importamos los modelos que usaremos
from flask_app.models.users import User
from flask_app.models.recipes import Recipe

#hacemos la importacion de Bcrypt
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

#con esta linea hacemos la ruta de validacion que se realiza despues del item validaciones
@app.route('/register', methods=['POST'])
def register():
    #validamos la info que recibimos
    if not User.valida_usuario(request.form):
        return redirect('/')
    
    #guardamos el registro
    pwd = bcrypt.generate_password_hash(request.form['password'])#aqui estamos encriptando la contraseña del usuario y guardandolo en la pwd

    #aqui creamos un diccionario con todos los datos de request.form, porque el anterior no lo podemos modificar, pero para poder uardar algo debemos crear este nuevo formulario
    formulario = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pwd
    }
    #aqui recibimos el identificador del nuevo usuario
    id = User.save(formulario)

    #guardamos en session el identificador del usuario
    session['user_id'] = id

    return redirect('/dashboard')


@app.route('/login', methods=['POST'])
def login():
    #verficamos que el email exista en la base de datos
    user = User.get_by_email(request.form) #aqui recibimos una instancia de usuario 0 False
    #entonces si el usuario no se encuentra en la base de datos
    if not user:
        flash('E-mail no encontrado', 'login')
        return redirect('/')
    
    #verificamos si la contraseñaingresada en login coincide con la que se encuentra en la base de datos
    if not bcrypt.check_password_hash(user.password, request.form['password']):
    #si a caso  no esta bien la contraseña que ingresa el usuario, entonces, se desplegara un mensaje de:
        flash('Password incorrecto', 'login')
        return redirect('/')
    #si la contraseña es correcta, y el email esta correcto entonces, ya puedo iniciar session, se guarda el identificador del usuario y se redirije a la pagina de dashboard
    session['user_id'] = user.id
    return redirect('/dashboard')

#esta ruta la haremos para restringir la entrada a dashboard , y solo se podra entrar ingresando los datos en registro o login, pero no cambiando l a url
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    
    formulario = {"id": session['user_id']}
    user = User.get_by_id(formulario)  
#lista de recetas
    recipes = Recipe.get_all()
    return render_template('dashboard.html', user = user, recipes=recipes)


#ruta para al presionar el boton logout, regrese a la pantalla de inicio
@app.route('/logout')
def logout():
    session.clear()#cada vez que querramos session haremos un session.clear()
    return redirect ('/')