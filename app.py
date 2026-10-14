from flask import Flask
import socket, time
import psutil # type: ignore
from datetime import datetime


app = Flask(__name__)

@app.route("/")
def inicio():
    # Nome da Rasp
    nome = socket.gethostname()
    # IP da Rasp
    ip = socket.gethostbyname(nome)
    # Tempo Ligado da Rasp
    with open("/proc/uptime", "r") as arquivo:
        segundos = int(float(arquivo.readline().split()[0]))
    horas = segundos // 3600
    minutos = (segundos % 3600) // 60
    # Uso do processador da Rasp
    cpu = psutil.cpu_percent(interval=1)
    # Temperatura da Rasp
    with open("/sys/class/thermal/thermal_zone0/temp", "r") as arquivo:
        temperatura = int(arquivo.read()) / 1000
    # Uso da memória RAM da Rasp
    memoria = psutil.virtual_memory()
    uso_memoria = memoria.percent
    # Uso do armazenamento da Rasp
    disco = psutil.disk_usage("/")
    uso_disco = disco.percent
    # Ultima atualizacao
    atualizacao = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    return f"""
        <h1>Painel da Raspberry Pi</h1>
        <p>Nome do equipamento: {nome}</p>
        <p>Endereço IP: {ip}</p>
        <p>Tempo Ligado: {horas} horas e {minutos} minutos</p>
        <p>Uso do processador: {cpu:.2f}%</p>    
        <p>Temperatura do processador: {temperatura:.1f} °C</p>
        <p>Uso da memória RAM: {uso_memoria:.1f}%</p>
        <p>Uso do armazenamento: {uso_disco:.1f}%</p>
        <p>Última atualização: {atualizacao}</p>
    """

app.run(host="0.0.0.0", port=5000)
