# -*- coding: UTF-8 -*-
from tkinter import messagebox
import requests
import urllib
from urllib.parse import unquote
from bs4 import BeautifulSoup
import time
import helper

class eGela:
    _login = 0
    _cookie = ""
    _curso = ""
    _redirect = ""
    _refs = []
    _root = None

    def __init__(self, root):
        self._root = root


    def printResponse(respuesta, pCuerpo = False):
        codigo = respuesta.status_code
        descr = respuesta.reason
        print()
        print("             +-----------+")
        print("+------------| RESPUESTA |------------+")
        print("|            +-----------+            |")
        print("|                                     |")
        print("|\t" + "+-------------+")
        print("|\t" + "| Status code |")
        print("|\t" + "+-------------+")
        print("|\t\t" + str(codigo) + " " + str(descr))
        print("|")
        print("|\t" + "+---------------------+")
        print("|\t" + "| Cabeceras / Headers |")
        print("|\t" + "+---------------------+")
        for i, cabecera in enumerate(respuesta.headers):
            print("|\t\t" + str(i) + "> " + cabecera + ": " + respuesta.headers[cabecera])
        if(pCuerpo):
            cuerpo = respuesta.content
            print("|")
            print("|\t" + "+-----------------+")
            print("|\t" + "| Curerpo/Content |")
            print("|\t" + "+-----------------+")
            print("|\t\t" + str(cuerpo))

        print("|")
        print("|         +---------------+           |")
        print("+---------| FIN RESPUESTA |-----------+")
        print("          +---------------+")
        print()


    def getMoodleSession(set_cookie):
        for cookie in set_cookie.split(";"):
            if cookie.startswith("MoodleSessionegela"):
                return cookie
        return ""

    def check_credentials(self, username, password, event=None):

        username = username.get()
        password = password.get()
        popup, progress_var, progress_bar = helper.progress("check_credentials", "Logging into eGela...")
        progress = 0
        progress_var.set(progress)
        progress_bar.update()

        print("##### 1. PETICION #####")

        metodo = 'GET'
        uri = "https://egela.ehu.eus/login/index.php"
        cabeceras = {'Host': 'egela.ehu.eus'}
        respuesta = requests.request(metodo, uri, headers=cabeceras, allow_redirects=False)
        html = BeautifulSoup(respuesta.content, 'html.parser')
        logintoken = html.find_all("input", {"name": "logintoken"})
        logintoken = logintoken[0].get("value")

        progress = 25
        progress_var.set(progress)
        progress_bar.update()
        time.sleep(1)


        print("\n##### 2. PETICION #####")

        if respuesta.status_code == 200:
            print(respuesta.headers['Set-Cookie'])
            metodo = 'POST'
            uri = "https://egela.ehu.eus/login/index.php"

            for cookie in respuesta.headers['Set-Cookie'].split(";"):
                if cookie.startswith("MoodleSessionegela="):
                    galleta = cookie#[len("MoodleSessionegela="):]
                    print("Cookie : ", galleta)

            cabeceras = {'Host': 'egela.ehu.eus', 'Content-Type': 'application/x-www-form-urlencoded',
                         'Cookie': galleta}
            cuerpo = {'logintoken': logintoken, 'username': username, 'password': password}
            cuerpo_encoded = urllib.parse.urlencode(cuerpo)
            cabeceras['Content-Length'] = str(len(cuerpo_encoded))
            respuesta = requests.request(metodo, uri, headers=cabeceras, data=cuerpo_encoded, allow_redirects=False)

            progress = 50
            progress_var.set(progress)
            progress_bar.update()
            time.sleep(1)



            print("\n##### 3. PETICION #####")
            if respuesta.status_code != 303:
                print("Ha ocurrido un error, se esperaba el código 303 y no ha ocurrido")
                exit(-1)
            if respuesta.headers['Location'].find("testsession") == -1:
                print("Ha ocurrido un error al iniciar sesion, usuario o contraseña incorrectos")
                exit(-1)
            else:
                print("Inicio de sesión correcto :D")
                metodo = 'GET'
                uri = respuesta.headers['Location']
                for cookie in respuesta.headers['Set-Cookie'].split(";"):
                    if cookie.startswith("MoodleSessionegela="):
                        galleta = cookie  # [len("MoodleSessionegela="):]
                        print("Cookie : ", galleta)

                cabeceras = {'Host': 'egela.ehu.eus', 'Cookie': galleta}
                respuesta = requests.request(metodo, uri, headers=cabeceras, allow_redirects=False)


        progress = 75
        progress_var.set(progress)
        progress_bar.update()
        time.sleep(1)
        popup.destroy()

        ultimo_respuesta = 0

        print("\n##### 4. PETICION #####")
        if respuesta.status_code == 303:
            metodo = 'GET'
            uri = respuesta.headers['Location']
            self._redirect = uri
            respuesta = requests.request(metodo, uri, headers=cabeceras, allow_redirects=False)
            ultimo_respuesta =respuesta.status_code


        progress = 100
        progress_var.set(progress)
        progress_bar.update()
        time.sleep(1)
        popup.destroy()


        if ultimo_respuesta == 200:
            self._cookie = galleta
            self._login = True
            self._root.destroy()
        else:
            messagebox.showinfo("Alert Message", "Login incorrect!")



    def get_pdf_refs(self):
        popup, progress_var, progress_bar = helper.progress("get_pdf_refs", "Downloading PDF list...")
        progress = 0
        progress_var.set(progress)
        progress_bar.update()

        print("\n##### 4. PETICION (Página principal de eGela) #####")
        #############################################
        cabeceras = {'Host': 'egela.ehu.eus', 'Content-Type': 'application/x-www-form-urlencoded',
                     'Cookie': self._cookie}
        metodo = 'GET'
        uri = self._redirect
        print("URI : ", uri)
        respuesta = requests.request(metodo, uri, headers=cabeceras, allow_redirects=False)

        #############################################

        print("\n##### 5. PETICION (Página principal de asignatura en eGela) #####")
        #############################################
        html = BeautifulSoup(respuesta.content, 'html.parser')
        for elemento in html.find_all("h3", {"class": "coursename"}):
            for elemento2 in elemento.find_all("a", {"class": "ehu-visible"}):
                # print(elemento2)
                if "Sistemas Web" in str(elemento2):
                    elemento2 = str(elemento2)
                    uri_sistemas = elemento2.split('"')[3]
        print(uri_sistemas)

        metodo = 'GET'
        uri = uri_sistemas
        respuesta = requests.request(metodo, uri, headers=cabeceras, allow_redirects=False)

        #############################################

        progress = 10
        progress_var.set(progress)
        progress_bar.update()

        print("\n##### Analisis del HTML... #####")
        #############################################
        i = 0
        datos = []
        uris_apartados = [uri]
        html = BeautifulSoup(respuesta.content, 'html.parser')
        for elemento in html.find_all("ul", {"class": "nav nav-tabs mb-3"}):
            for elemento2 in elemento.find_all("a", {"class": "nav-link"}):
                if "nav-link active" in str(elemento2):
                    if "title" in elemento2.attrs:
                        nombre = elemento2["title"]

        progress = 20
        progress_var.set(progress)
        progress_bar.update()


        for elemento in html.find_all("ul", {"class": "nav nav-tabs mb-3"}):




            for elemento2 in elemento.find_all("a", {"class": "nav-link"}):
                if "href" in elemento2.attrs and "title" in elemento2.attrs:
                    nombre = elemento2["title"]
                    uri_apartado = elemento2["href"]
                    uris_apartados.append(uri_apartado)

        ##############################################

        progress = 40
        progress_var.set(progress)
        progress_bar.update()

        print(" ----- uri_apartados -------- ")
        print(uris_apartados)
        uri_pdfs = self.get_PDF_uris(uris_apartados)
        print()

        print(" ----- uri_pdfs -------- ")
        print(len(uri_pdfs))
        print(uri_pdfs)



        # INICIALIZA Y ACTUALIZAR BARRA DE PROGRESO
        # POR CADA PDF ANIADIDO EN self._refs

        for i in range(0, len(uri_pdfs)):
            progress_step = float(60.0 / len(uri_pdfs))

            progress += progress_step
            progress_var.set(progress)
            progress_bar.update()
            time.sleep(0.1)

        self._refs = uri_pdfs

        popup.destroy()
        return self._refs



    def get_pdf(self, selection):

        selection = self._refs[selection]
        print(selection)
        print("\t##### descargando  PDF... #####")

        metodo = 'GET'
        cabeceras = {'Host': 'egela.ehu.eus', 'Cookie': self._cookie}

        respuesta = requests.request(metodo, selection['pdf_link'], headers=cabeceras, allow_redirects=False)

        print("Status code de ", selection['pdf_name'], " : ", respuesta.status_code)
        return selection['pdf_name'], respuesta.content


    def get_PDF_uris(self, listaURI):
        # Recibe las uri a las secciones de egela
        # Devuelve la lista de los pdf
        listaPDF = []
        # {'pdf_name':'name', 'pdf_link':'link'}
        for uri in listaURI:
            metodo = 'GET'
            cabeceras = {'Host': 'egela.ehu.eus', 'Cookie': self._cookie}
            respuesta = requests.request(metodo, uri, headers=cabeceras, allow_redirects=False)

            documento = BeautifulSoup(respuesta.content, 'html.parser')

            for token in documento.find_all("a", attrs={'class': 'aalink'}):
                if token.find('img')['src'].split('/')[-1] == 'pdf':
                    if token.has_attr('href'):
                        # listaPDF.append(token['href'])
                        metodo = 'GET'
                        uri = token['href']
                        cabeceras = {'Host': 'egela.ehu.eus', 'Cookie': self._cookie}
                        respuesta = requests.request(metodo, uri, headers=cabeceras, allow_redirects=False)
                        if respuesta.status_code == 303:
                            link = respuesta.headers['Location']
                            nombre = link.split('/')[len(link.split('/'))-1].replace('%20', '_')
                            listaPDF.append({'pdf_name':nombre, 'pdf_link':link})

        self._refs = listaPDF
        return listaPDF


