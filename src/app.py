from flask import Flask, render_template, request, redirect, session, url_for
from flask_cors import CORS
from utils.DefaultMessages import *
from database.models import Usuario
from utils.PassFactory import Password
from playhouse.shortcuts import model_to_dict, dict_to_model
import json

app = Flask(__name__, template_folder="template", static_folder="static")
CORS(app)
app.secret_key = 'whadababu'

@app.route("/api/login", methods = ['POST'])
def api_login():
    usuario = request.form.get('usuario').lower()
    senha   = request.form.get('senha')

    find_user = list(Usuario.select().where(Usuario.usuario == usuario).dicts())

    # Verifica se retornou algum usuario.
    if len(find_user) == 0:
        session['error'] = msg_error_usuario_nao_existente
        return redirect( url_for('index') )

    # Pega o usuario encontrado.
    user = find_user[0]

    # Valida a senha.
    if not Password.validate(senha, user.get('senha')):
        session['error'] = msg_error_senha_incorreta
        return redirect( url_for('index') )

    # Coloca o usuario na sessao.
    session['user'] = user

    return redirect( url_for('venda') )



@app.route("/api/cadastrar", methods = ['POST'])
def api_cadastrar():
    usuario = request.form.get('usuario').lower()
    senha   = request.form.get('senha')
    perfil  = request.form.get('perfil')

    if not (usuario and senha and perfil):
        session['error'] = msg_error_vazio
        return redirect(url_for('cadastrar'))

    if usuario == '' or senha == '' or perfil == '':
        session['error'] = msg_error_vazio
        return redirect( url_for('cadastrar') )

    find_user = Usuario.select().where(Usuario.usuario == usuario)
    user = [u for u in find_user]

    if len(user) > 0:
        session['error'] = msg_error_usuario_existente
        return redirect( url_for('cadastrar') )

    new_user = Usuario.create(usuario=usuario, senha=Password.encript(senha), perfil=perfil)

    session['user'] = model_to_dict(new_user)

    return redirect( url_for('venda') )

@app.route("/deslogar")
def deslogar():
    session.pop('user', None)
    return redirect( url_for('index') )

@app.route("/")
def index():
    # Verifica se o usuario ja esta logado.
    usuario = session.get('user')
    if usuario:
        print("Usuario encontrado na sessao.")
        return redirect( url_for('venda') )

    # Verifica se tem erro na sessao de login.
    error = session.get('error')
    if error:
        session.pop('error', None)
        return render_template("index.html", error=error)

    return render_template("index.html")

@app.route("/cadastrar")
def cadastrar():
    error = session.get('error')
    if error:
        session.pop('error', None)
        return render_template("cadastro.html", error=error)

    return render_template("cadastro.html")

@app.route("/venda")
def venda():
    usuario = session.get("user")

    if not usuario:
        print("Voce não esta logado.")
        return redirect( url_for('index') )

    date_format = usuario.get('criacao').strftime("%d/%m/%Y")
    usuario.update({"criacao": date_format})

    all_users = list(Usuario.select().dicts())

    return render_template('venda.html', user=usuario, users=all_users)

app.run( host="0.0.0.0", debug=True )
