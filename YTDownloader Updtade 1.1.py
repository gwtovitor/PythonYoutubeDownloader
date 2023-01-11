from pytube import YouTube
import os
import PySimpleGUI as sg
from time import sleep
from random import randint


def downloadvideo(link, path):  # Função que baixa apenas video
    youtube = YouTube(link)
    res_youtube_max = youtube.streams.get_highest_resolution()
    res_youtube_max.download(path)


def downloadaudio(link, path):  # Função baixa apenas audio
    randomname = randint(1, 500)  # randomizando o nome do arquivo pois quando ia converter em  mp3
    rdname2 = str(randomname)  # estava dando um erro se baixasse 2 arquivos iguais
    yt = YouTube(link)
    video = yt.streams.filter(only_audio=True).first()
    out_file = video.download(path)
    base, ext = os.path.splitext(out_file)
    new_file = base + rdname2 + '.mp3'
    os.rename(out_file, new_file)


layout = [  # Layout completo da janela
    [sg.Text("Baixe seus videos ou audios do youtube")],
    [sg.InputText(key="ulr")],
    [sg.Button("Adicionar mais um video")],
    [sg.Text("Informe onde deseja salvar o video"), sg.InputText(), sg.FolderBrowse()],
    [sg.Button("Baixar o(s) Video(s)"), sg.Button("Baixar o(s) Audio(s)")],
    [sg.Text("Ultimo Video Adicionado:", key="texto_video")],
    [sg.Text("Videos já adicionados: ", key="lista_video")],
    [sg.Button("Limpar Lista de Links"), sg.Button("Apagar o ultimo video adicionado")],
    [sg.Button("Sair")],
    [sg.ProgressBar(50, orientation='h', size=(100,20), border_width=4, key="barra", bar_color=("Blue", "Yellow"))],
]
janela = sg.Window("Youtube Downloader", layout)  # Titulo da janela

lista = []  # Lista que armazena os links
titulo = " "  # Variavel que mostra o titulo do ultimo video baixado
cont = 0  # Contador
listaTitle = " "  # Variavel que armazena o titulo de todos os videos do youtube selecionados
while True:
    evento, valores = janela.read()
    if evento == sg.WIN_CLOSED or evento == "Sair":
        break
    elif evento == "Adicionar mais um video":
        links = lista.append(valores["ulr"])
        titulo = YouTube(lista[cont])
        listaTitle = titulo.title + "\n" + listaTitle
        janela["texto_video"].update(f"Video Adicionado:{titulo.title}")
        janela["lista_video"].update(f"Videos já adicionados:{listaTitle}")
        cont = cont + 1
    elif evento == "Baixar o(s) Video(s)":
        janela["barra"].update(0)
        i = 0
        progress_bar = len(lista)
        while i < len(lista):
            downloadvideo(lista[i], valores[0])
            i = i + 1
            janela["barra"].update(max=len(lista), current_count=i)
    elif evento == "Baixar o(s) Audio(s)":
        i = 0
        while i < len(lista):
            downloadaudio(lista[i], valores[0])
            sleep(5)
            i = i + 1
    elif evento == "Limpar Lista de Links":
        lista.clear()
        cont = 0

    elif evento == "Apagar o ultimo video adicionado":
        lista.pop()
        cont = cont - 1
janela.close()
