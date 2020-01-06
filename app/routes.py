from subprocess import call
from app import app, mysql
from app.db import Articles, User
from app.nameGenerator import GenerateUniqueName
from flask import render_template, flash, redirect, url_for, request, jsonify
import os, json 

import flask_login
from app.forms import LoginForm

login_manager = flask_login.LoginManager()
login_manager.init_app(app)


@app.route('/test')
def test():
    return render_template('test2.html')

@app.route('/getJson')
def getJson():

    list_main_art=dict()

    try: 
        conn = mysql.connect()
        cursor = conn.cursor()
        art = Articles(cursor, conn)
        arts_and_sects = art.getArticlesBySection() 

        for arts_and_sect in arts_and_sects: 
            for art in arts_and_sects[arts_and_sect]:
                list_main_art[art[0]]=[art[1],
                    art[2],
                    art[3]
                ]

        return jsonify(list_main_art)

    finally:
        cursor.close()


@app.route('/')
@app.route('/index')
def index():

    list_main_art=dict()

    try: 
        conn = mysql.connect()
        cursor = conn.cursor()
        art = Articles(cursor, conn)
        arts_and_sects = art.getArticlesBySection() 

        for arts_and_sect in arts_and_sects: 
            for art in arts_and_sects[arts_and_sect]:
                list_main_art[art[0]]=[art[1],
                    art[2],
                    art[3]
                ]

        list_main_art=jsonify(list_main_art)

        return render_template('index.html',  title="Pagina principal", arts_and_sects=arts_and_sects, list_main_art=list_main_art)
    finally:
        cursor.close()


@app.route('/login', methods=["POST", "GET"])
def login(): 

    error = None

    loginForm = LoginForm() 
    if loginForm.validate_on_submit():
         return redirect('/admin')


    if request.method=="POST":

        try: 
            conn = mysql.connect()
            cursor = conn.cursor()
            user = User(cursor)

            user_name = request.form['user_name']
            password = request.form['password']
            #check = request.form['check']


            if (user.checkUser(user_name, password)):
                flask_login.login_user(user)
                return redirect(url_for('admin'))
            else:
                flash('Verifique el nombre de usuario o contrasena')
                return redirect(url_for('login'))
        finally:
            cursor.close()

    return render_template('login.html',  title='Ingreso administrativo', loginForm=loginForm, error=error)


@app.route('/delete/<string:id>')
@flask_login.login_required
def delete(id):
    try: 
        conn = mysql.connect()
        cursor = conn.cursor()
        art = Articles(cursor,conn)
        art.delArtic(id) 
        return redirect(url_for('admin'))
    finally:
        cursor.close()


@app.route('/admin', methods=["POST", "GET"])
@flask_login.login_required
def admin(): 

    try: 
        conn = mysql.connect()
        cursor = conn.cursor()

        art = Articles(cursor,conn)

        if request.method == "POST":
            artic_img = request.files['artic_img']
            gen_name = GenerateUniqueName(cursor) 

            image_name = gen_name.generateAndValidate()
            artic_name= request.form['artic_title']
            artic_sect = request.form['list_sect']
            artic_descr = request.form['artic_descr']
            new_sect = request.form['new_sect']

            if (new_sect):
                art.newSection(new_sect)
                artic_sect =  new_sect  


            art.setArticle(image_name, artic_name, artic_descr, artic_sect)
            artic_img.save('app/static/images/articles/'+image_name)

            return redirect(url_for('admin')) 


        sections = art.getSections()
        arts_and_sects = art.getArticlesBySection()

        return render_template('dashBoard.html',  title='administracion', sections=sections, arts_and_sects=arts_and_sects)

    finally:
        cursor.close()

@login_manager.user_loader
def user_loader(user_id):
    try: 
        conn = mysql.connect()
        cursor = conn.cursor() 
        user = User(cursor)
        #user.id = user_id 
        user.getUserById(user_id)
        return user 
    finally:
        cursor.close()

@app.route('/protected')
#@flask_login.login_required
def protected():
    return 'user ' + flask_login.current_user.name

