from flask import Flask, render_template, request
import requests

app = Flask(__name__)
  
@app.route("/", methods=["GET", "POST"])
def conversor_moedas():
    moedas_validas = ["USD", "BRL", "EUR", "JPY", "GBP"]

    if request.method == "POST":
        valor = float(request.form["valor"])
        moeda_origem = request.form["moeda_origem"]
        moeda_destino = request.form["moeda_destino"]

        if moeda_origem not in moedas_validas or moeda_destino not in moedas_validas:
            mensagem = "Moeda inválida. As moedas válidas são: " + ", ".join(moedas_validas)
            return render_template("conversor.html", mensagem=mensagem)
        else:
            url = f"https://api.exchangerate-api.com/v4/latest/{moeda_origem}"
            resposta = requests.get(url)
            data = resposta.json()
            taxa_cambio = data["rates"][moeda_destino]
            valor_convertido = round(valor * taxa_cambio, 2)

            return render_template("index.html", valor_convertido=valor_convertido, moeda_destino=moeda_destino)

    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)