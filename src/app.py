from cryptography.fernet import Fernet
from flask import Flask, session, redirect, url_for, render_template, request
import secrets
from back.user import usuarios_bp

# Geração da chave de criptografia (só deve ser gerada uma vez e salva de maneira segura)
key = Fernet.generate_key()
cipher_suite = Fernet(key)

def verifyLogin(route):
    if(session.get("RA") and session.get("senha")): # verifica se o existe o login e senha do user na sessão atual
        return render_template(route) # se tiver, envia para a rota do parametro
    else:
        return redirect(url_for("login")) # se não tiver, ele vai para a página de login, forcando o usuário a realizar o login, independente da rota


app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
    
@app.route('/') # isso define uma rota
def home(): # funcao que é executada quando está na rota
   return verifyLogin("index.html") #envia o caminho do arquivo para a função verifyLogin
    
@app.route('/atestados/')
def atestado():
    return verifyLogin("atestados.html")

@app.route('/avaliacao/')
def avaliacao():
    return verifyLogin("avaliacao.html")

@app.route('/login/', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Captura os dados do formulário
        ra = request.form["RA"]
        senha = request.form["senha"]
        
        session["RA"] = ra  # Armazena o e-mail na sessão
        session["senha"] = senha  # Armazenar como string

        
        return redirect(url_for("home"))
    
    return render_template('/user/login.html')

@app.route('/cadastro/')
def cadastro():
    if(session.get("RA") and session.get("senha")): # verifica se o existe o login e senha do user na sessão atual
        return render_template(url_for("home")) # se tiver, envia para a rota do parametro
    else:
        return render_template("/user/cadastro.html") 
    

@app.route("/logout/")
def logout():
    session.pop("login", None)
    session.pop("senha", None)
    return redirect(url_for("home"))

# Pega as rotas da parte de controlar usuarios e adiciona o prefixo /usuario
app.register_blueprint(usuarios_bp, url_prefix="/usuario")

if __name__ == '__main__':
    app.run(debug=True)
