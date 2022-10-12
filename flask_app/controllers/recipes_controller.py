from flask import render_template, request, redirect, session
from flask_app import app

#importacion de modelos
from flask_app.models.users import User
from flask_app.models.recipes import Recipe


@app.route('/new/recipe')
def new_recipe():
    if 'user_id' not in session:
        return redirect('/')

#Yo sé que en sesión tengo el id de mi usuario (session['user_id'])
    #Queremos una función que en base a ese id me regrese una instancia del usuario
    formulario = {"id": session['user_id']}

    user = User.get_by_id(formulario) #Recibo la instancia de usuario en base a su ID

    return render_template('new_recipe.html', user=user)


@app.route('/create/recipe', methods=['POST'])
def create_recipe():
    if 'user_id' not in session:#comprobamos si inicio sesion
        return redirect('/')

    #validacion de Receta
    if not Recipe.valida_receta(request.form):
        return redirect('/new/recipe')

    #guardamos la receta
    Recipe.save(request.form)
    return redirect('/dashboard')

@app.route('/edit/recipe/<int:id>')
def edit_recipe(id):
    if 'user_id' not in session:#comprobamos que inicie sesion
        return redirect('/')

#Yo sé que en sesión tengo el id de mi usuario (session['user_id'])
    #Queremos una función que en base a ese id me regrese una instancia del usuario
    formulario = {"id": session['user_id']}

    user = User.get_by_id(formulario) #Recibo la instancia de usuario en base a su ID que inicio sesion

    #Queremos la instancia de la receta que se debe desplegar en editar, esto lo obtenemos en base al ID que recibimos en el URL
    formulario_receta = {"id": id}
    recipe = Recipe.get_by_id(formulario_receta)

    return render_template('edit_recipe.html', user=user, recipe=recipe)

@app.route('/update/recipe',methods=['POST'])
def update_recipe():
    #debemos verificar que haya iniciado sesion
    if 'user_id' not in session:#comprobamos que inicie sesion
        return redirect('/')
    
    #verifico que todos los datos esten correctos
    if not Recipe.valida_receta(request.form):
        return redirect('/edit/recipe/'+request.form['recipe_id'])

    #Guardamos los cambios
    Recipe.update(request.form)

    #Redireccionar a/dashboard
    return redirect('/dashboard')

@app.route('/delete/recipe/<int:id>')
def delete_recipe(id):
    #debemos verificar que haya iniciado sesion
    if 'user_id' not in session:#comprobamos que inicie sesion
        return redirect('/')

    #Borramos
    formulario = {"id": id}
    Recipe.delete(formulario)

    #Redirigir a /dashboard
    return redirect('/dashboard')

@app.route('/view/recipe/<int:id>')
def view_recipe(id):
    #verificar que el usuario haya iniciado sesion
    if 'user_id' not in session:#comprobamos que inicie sesion
        return redirect('/')

    #saber cual es el nombre del usuario que inicio sesion
    formulario = {"id": session['user_id']}

    user = User.get_by_id(formulario)

    #objeto receta que queremos desplegar
    formulario_receta = {"id": id}
    recipe = Recipe.get_by_id(formulario_receta) #con esta funcion voyba recibir la instancia de receta el objeto de receta que yo quiero recibir

    #renderizar show_recipe.html
    return render_template('show_recipe.html', user=user, recipe=recipe)