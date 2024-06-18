from flask import Flask, render_template, redirect, request, flash, send_from_directory
import os
import mysql.connector

app = Flask(__name__)
app.config["SECRET_KEY"] = "MATEUS321"

logado = False

@app.route("/")
def home():
    global logado
    logado = False
    return render_template("login.html")

@app.route("/adm")
def adm():
    if logado == True:
        conect_BD = mysql.connector.connect(host='localhost', database='usuarios', user='root', password='mateus12345#')
        if conect_BD.is_connected():
            print("conectado")
            cursor = conect_BD.cursor()
            cursor.execute("SELECT * FROM usuario;")
            usuarios = cursor.fetchall()
        return render_template("adiministrador.html", usuarios=usuarios)
    if logado == False:
       return redirect("/")

@app.route("/usuarios")
def usuarios():
    if logado == True:
        arquivo = []
        for documento in os.listdir('arquivos'):
            arquivo.append(documento)
        return render_template("USUARIOS2.html", arquivos=arquivo)
    else:
        return redirect("/")

@app.route("/login", methods=['POST'])
def login():
    
    global logado
    nome = request.form.get("nome")
    senha = request.form.get("senha")

    conect_BD = mysql.connector.connect(host='localhost', database='usuarios', user='root', password='mateus12345#')
    cont = 0
    if conect_BD.is_connected():
        print("conectado")
        cursor = conect_BD.cursor()
        cursor.execute("SELECT * FROM usuario;")
        usuariosBD = cursor.fetchall()

        for usuario in usuariosBD:
            cont += 1
            usuarioNome = str(usuario[1])
            usuarioSenha = str(usuario[2])

            if nome == "adm" and senha == "000":
                logado = True
                return redirect("/adm")
            if usuarioNome == nome and usuarioSenha == senha:
                logado = True
                return redirect("/usuarios")
            if cont >= len(usuariosBD):
                flash("USUARIO INVALIDO")
                return redirect("/")
    else:
        return redirect("/")


@app.route("/cadastrarUsuario", methods=['POST'])
def cadastrarUsuario():
    global logado
    user = []
    nome = request.form.get("nome")
    senha = request.form.get("senha")
    conect_BD = mysql.connector.connect(host='localhost', database='usuarios', user='root', password='mateus12345#')
    if conect_BD.is_connected():
        conect_BD = mysql.connector.connect(host='localhost', database='usuarios', user='root', password='mateus12345#')
        cursor = conect_BD.cursor()
        cursor.execute(f"INSERT INTO usuario (nome, senha) VALUES ('{nome}', '{senha}');")
        conect_BD.commit()
    if conect_BD.is_connected():
        cursor.close()
        conect_BD.close()
    logado=True
    flash(F"{nome} CADASTRADO")
    return redirect("/adm")

@app.route("/excluirUsuario", methods=['POST'])
def excluirUsuario():
    global logado
    logado=True
    nome = request.form.get('nome')
    usuarioID = request.form.get('usuarioParaExcluir')

    conect_BD = mysql.connector.connect(host='localhost', database='usuarios', user='root', password='mateus12345#')
    if conect_BD.is_connected():
        conect_BD = mysql.connector.connect(host='localhost', database='usuarios', user='root', password='mateus12345#')
        cursor = conect_BD.cursor()
        cursor.execute(f"delete from usuario where id='{usuarioID}';")
        conect_BD.commit()
    if conect_BD.is_connected():
        cursor.close()
        conect_BD.close()

    flash(f"{nome} EXCLUIDO")
    return redirect("/adm")

@app.route("/upload", methods=['POST'])
def upload():
    global logado
    logado = True
    arquivos = request.files.get('documento')
    nome_arquivo = arquivos.filename.replace(" ", "-")
    arquivos.save(os.path.join('arquivos/', nome_arquivo))
    flash("Arquivo Salvo")
    return redirect("/adm")

@app.route("/download", methods=['POST'])
def download():
    nomeArquivo = request.form.get('arquivosParaDownload')
    return  send_from_directory('arquivos', nomeArquivo, as_attachment=True)

if __name__ in "__main__":
    app.run(debug=True)