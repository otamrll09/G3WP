from wsgiref.simple_server import software_version
from flask import Flask, redirect, render_template, request, flash
import bot_web_scraping_web
import bot_envio_email_web
import bot_registro_excel_web

app = Flask(__name__)
app.secret_key="asd"
app.index_string = '''<!DOCTYPE html>
<html>
<head>
<title>G3ws</title>
<link rel="manifest" href="templates/manifest.json" />
{%metas%}
{%favicon%}
{%css%}
</head>
<script type="module">
   import 'https://cdn.jsdelivr.net/npm/@pwabuilder/pwaupdate';
   const el = document.createElement('pwa-update');
   document.body.appendChild(el);
</script>
<body>
<script>
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', ()=> {
      navigator
      .serviceWorker
      .register('/templates/sw01.js')
      .then(()=>console.log("Ready."))
      .catch(()=>console.log("Err..."));
    });
  }
</script>
{%app_entry%}
<footer>
{%config%}
{%scripts%}
{%renderer%}
</footer>
</body>
</html>
'''

email_site = ''
software_site = ''
datainic_site = ''
datafin_site = ''

@app.route("/")
def index():
    flash('Insira o email', 'email')
    flash('Insira o software', 'software')
    flash('Insira a data inicial e a data final', 'datainic')
    return render_template("index.html")

@app.route("/pesquisar", methods=["POST","GET"])
def pesquisar():
    flash('Os dados já foram processados e logo o email será enviado!')
    if str(request.form['datainic_input']) == '' or str(request.form['datafin_input']) == '':
        return render_template("falha.html")
    if str(request.form['software_input']) == '' or str(request.form['email_input']) == '':
        return render_template("falha.html")
    email_site = str(request.form['email_input'])
    software_site = str(request.form['software_input'])
    lst_replace = str(request.form['datainic_input']).split("-")
    datainic_site = lst_replace[1] + lst_replace[2] + lst_replace[0]
    lst_replace = str(request.form['datafin_input']).split("-")
    datafin_site = lst_replace[1] + lst_replace[2] + lst_replace[0]
    lst_email = []
    lst_email.append(email_site)
    lst_felps = []
    lst_felps = bot_web_scraping_web.auto_do(software_site, datainic_site, datafin_site)
    # if lst_felps[0] == 0:
    gelson_r = bot_registro_excel_web.montaPlanilha(lst_felps[1])
    bot_envio_email_web.send_email(lst_email,gelson_r)
    return render_template("pesquisar.html")

@app.route("/manifest.json")
def manifestjson():
    return render_template("manifest.json")