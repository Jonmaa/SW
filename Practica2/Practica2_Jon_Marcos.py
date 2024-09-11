import requests
import urllib.parse
import os
import sys
from bs4 import BeautifulSoup
from urllib.parse import unquote
import getpass

'''
Nombre y apellidos: Jon Marcos Mercadé
Asignatura y grupo: SW y grupo 01
Fecha de entrega: 25-03-2024
Nombre de la tarea: Práctica 2. Buscar información en eGela
Breve descripción: Acceder a eGela realizando peticiones mediante Burp. Luego implementarlo en PyCharm y descargar los 
PDFs y crear un tareas.csv con los entregables.
'''


def getMoodleSession(set_cookie):
    for cookie in set_cookie.split(";"):
        if cookie.startswith("MoodleSessionegela"):
            return cookie
    return ""


def getTareas(enlace, cookie, datos):
    metodo = 'GET'
    uri = enlace
    cabeceras = {'Host': 'egela.ehu.eus', 'Cookie': cookie}
    respuesta = requests.request(metodo, uri, headers=cabeceras, allow_redirects=False)
    print(metodo + " " + uri)
    print(str(respuesta.status_code) + " " + respuesta.reason)
    if 'Set-Cookie' in respuesta.headers.keys():
        print("Set-Cookie: " + respuesta.headers['Set-Cookie'])
    if 'Location' in respuesta.headers.keys():
        print("Location: " + respuesta.headers['Location'])
    html = BeautifulSoup(respuesta.content, 'html.parser')
    for elemento in html.find_all("a", {"class": "aalink"}):
        link = elemento.get('href')
        if "/ehu/assign/" in str(elemento):
            metodo = 'GET'
            uri = link
            cabeceras = {'Host': 'egela.ehu.eus', 'Cookie': cookie}
            respuesta = requests.request(metodo, uri, headers=cabeceras, allow_redirects=False)
            print(metodo + " " + uri)
            print(str(respuesta.status_code) + " " + respuesta.reason)
            if 'Set-Cookie' in respuesta.headers.keys():
                print("Set-Cookie: " + respuesta.headers['Set-Cookie'])
            if 'Location' in respuesta.headers.keys():
                print("Location: " + respuesta.headers['Location'])

            html = BeautifulSoup(respuesta.content, 'html.parser')
            for elemento in html.findAll("h2"):
                elemento = str(elemento)
                mitad = elemento.split('>')[1]
                nombre_tarea = mitad.split('<')[0]

            for elemento in html.find_all("tr"):
                if "Entregatze-data" in str(elemento):
                    for elemento2 in elemento.find_all("td", {"class": "cell c1 lastcol"}):
                        elemento2 = str(elemento2)
                        mitad = elemento2.split('>')[1]
                        fecha = mitad.split('<')[0]
                        info = uri + "," + nombre_tarea + ",\"" + fecha + "\""
                        datos.append(info)
            with open("tareas.csv", 'w', newline='', encoding="utf-8") as f:
                f.write("url, nombre, fecha de entrega" + "\n")
                for fila in datos:
                    f.write(fila + "\n")


def descargarPDFs(enlace, cookie, subcarpeta, i):
    metodo = 'GET'
    uri = enlace
    cabeceras = {'Host': 'egela.ehu.eus', 'Cookie': cookie}
    respuesta = requests.request(metodo, uri, headers=cabeceras, allow_redirects=False)
    print(metodo + " " + uri)
    print(str(respuesta.status_code) + " " + respuesta.reason)
    if 'Set-Cookie' in respuesta.headers.keys():
        print("Set-Cookie: " + respuesta.headers['Set-Cookie'])
    if 'Location' in respuesta.headers.keys():
        print("Location: " + respuesta.headers['Location'])
    html = BeautifulSoup(respuesta.content, 'html.parser')
    for elemento in html.find_all("a", {"class": "aalink"}):
        link = elemento.get('href')
        if "/f/pdf" in str(elemento):
            if "resource" in str(link):
                metodo = 'GET'
                uri = link
                cabeceras = {'Host': 'egela.ehu.eus', 'Cookie': cookie}
                respuesta = requests.request(metodo, uri, headers=cabeceras, allow_redirects=False)
                print(metodo + " " + uri)
                print(str(respuesta.status_code) + " " + respuesta.reason)
                if 'Set-Cookie' in respuesta.headers.keys():
                    print("Set-Cookie: " + respuesta.headers['Set-Cookie'])
                if 'Location' in respuesta.headers.keys():
                    print("Location: " + respuesta.headers['Location'])
                if respuesta.status_code == 303:
                    metodo = 'GET'
                    uri = respuesta.headers['Location']
                    cabeceras = {'Host': 'egela.ehu.eus', 'Cookie': cookie}
                    respuesta = requests.request(metodo, uri, headers=cabeceras, allow_redirects=False)
                    print(metodo + " " + uri)
                    print(str(respuesta.status_code) + " " + respuesta.reason)
                    if 'Set-Cookie' in respuesta.headers.keys():
                        print("Set-Cookie: " + respuesta.headers['Set-Cookie'])
                    if 'Location' in respuesta.headers.keys():
                        print("Location: " + respuesta.headers['Location'])


                    ruta_subcarpeta = f"./PDFs/{subcarpeta}"
                    if not os.path.exists(ruta_subcarpeta):
                        os.makedirs(ruta_subcarpeta)
                        print(f"Carpeta '{ruta_subcarpeta}' creada con éxito.")
                    with open(ruta_subcarpeta + "/" + unquote(respuesta.url.split("/")[-1]), 'wb') as archivo:
                        archivo.write(respuesta.content)
                    i = i + 1



def registro(username, apellido):
    # Peticion 1
    metodo = 'GET'
    uri = "https://egela.ehu.eus/login/index.php"
    cabeceras = {'Host': 'egela.ehu.eus'}
    respuesta = requests.request(metodo, uri, headers=cabeceras, allow_redirects=False)
    html = BeautifulSoup(respuesta.content, 'html.parser')
    logintoken = html.find_all("input", {"name": "logintoken"})
    logintoken = logintoken[0].get("value")
    print(metodo + " " + uri)
    print(str(respuesta.status_code) + " " + respuesta.reason)
    if 'Set-Cookie' in respuesta.headers.keys():
        print("Set-Cookie: " + respuesta.headers['Set-Cookie'])
    if 'Location' in respuesta.headers.keys():
        print("Location: " + respuesta.headers['Location'])

    #Peticion 2
    if respuesta.status_code == 200:
        passw = getpass.getpass("Pon tu contraseña")
        metodo = 'POST'
        uri = "https://egela.ehu.eus/login/index.php"
        cabeceras = {'Host': 'egela.ehu.eus', 'Content-Type': 'application/x-www-form-urlencoded',
                     'Cookie': getMoodleSession(respuesta.headers['Set-Cookie'])}
        cuerpo = {'logintoken': logintoken, 'username': username, 'password': passw}
        cuerpo_encoded = urllib.parse.urlencode(cuerpo)
        cabeceras['Content-Length'] = str(len(cuerpo_encoded))
        respuesta = requests.request(metodo, uri, headers=cabeceras, data=cuerpo_encoded, allow_redirects=False)
        print(metodo + " " + uri)
        print("Contenido: " + str(cuerpo_encoded))
        print(str(respuesta.status_code) + " " + respuesta.reason)
        if 'Set-Cookie' in respuesta.headers.keys():
            print("Set-Cookie: " + respuesta.headers['Set-Cookie'])
        if 'Location' in respuesta.headers.keys():
            print("Location: " + respuesta.headers['Location'])

        if respuesta.status_code != 303:
            print("Ha ocurrido un error, se esperaba el código 303 y no ha ocurrido")
            exit(-1)

        #Peticion 3
        if respuesta.headers['Location'].find("testsession") == -1:
            print("Ha ocurrido un error al iniciar sesion, usuario o contraseña incorrectos")
            exit(-1)
        else:
            print("Inicio de sesión correcto :D")
            metodo = 'GET'
            uri = respuesta.headers['Location']
            cabeceras = {'Host': 'egela.ehu.eus', 'Cookie': getMoodleSession(respuesta.headers['Set-Cookie'])}
            cookie = getMoodleSession(respuesta.headers['Set-Cookie'])
            respuesta = requests.request(metodo, uri, headers=cabeceras, allow_redirects=False)
            print(metodo + " " + uri)
            print(str(respuesta.status_code) + " " + respuesta.reason)
            if 'Set-Cookie' in respuesta.headers.keys():
                print("Set-Cookie: " + respuesta.headers['Set-Cookie'])
            if 'Location' in respuesta.headers.keys():
                print("Location: " + respuesta.headers['Location'])

            #Peticion 4
            if respuesta.status_code == 303:
                metodo = 'GET'
                uri = respuesta.headers['Location']
                respuesta = requests.request(metodo, uri, headers=cabeceras, allow_redirects=False)
                print(metodo + " " + uri)
                print(str(respuesta.status_code) + " " + respuesta.reason)
                if 'Set-Cookie' in respuesta.headers.keys():
                    print("Set-Cookie: " + respuesta.headers['Set-Cookie'])
                if 'Location' in respuesta.headers.keys():
                    print("Location: " + respuesta.headers['Location'])
                html = BeautifulSoup(respuesta.content, 'html.parser')
                ape = html.text.find(apellido)
                if ape == -1:
                    print("No se ha encontrado el apellido")
                    exit(-1)
                print("Nombre y apellidos:" + html.text[ape:ape + len(apellido)])
                input("Pulsa cualquier tecla para continuar con el programa")

                for elemento in html.find_all("h3", {"class": "coursename"}):
                    for elemento2 in elemento.find_all("a", {"class": "ehu-visible"}):
                        #print(elemento2)
                        if "Sistemas Web" in str(elemento2):
                            elemento2 = str(elemento2)
                            uri_sistemas = elemento2.split('"')[3]

                #Peticion 5
                metodo = 'GET'
                uri = uri_sistemas
                respuesta = requests.request(metodo, uri, headers=cabeceras, allow_redirects=False)
                print(metodo + " " + uri)
                print(str(respuesta.status_code) + " " + respuesta.reason)
                if 'Set-Cookie' in respuesta.headers.keys():
                    print("Set-Cookie: " + respuesta.headers['Set-Cookie'])
                if 'Location' in respuesta.headers.keys():
                    print("Location: " + respuesta.headers['Location'])

                # Crear carpeta para PDFs
                ruta = './PDFs'
                if not os.path.exists(ruta):
                    os.makedirs(ruta)
                    print(f"Carpeta '{ruta}' creada con éxito.")
                else:
                    print(f"La carpeta '{ruta}' ya existe.")

                # Encontrar apartados y descargar PDFs
                i = 0
                datos = []
                html = BeautifulSoup(respuesta.content, 'html.parser')
                for elemento in html.find_all("ul", {"class": "nav nav-tabs mb-3"}):
                    for elemento2 in elemento.find_all("a", {"class": "nav-link"}):
                        if "nav-link active" in str(elemento2):
                            if "title" in elemento2.attrs:
                                nombre = elemento2["title"]
                                descargarPDFs(uri, cookie, nombre, i)
                                getTareas(uri, cookie, datos)
                for elemento in html.find_all("ul", {"class": "nav nav-tabs mb-3"}):
                    for elemento2 in elemento.find_all("a", {"class": "nav-link"}):
                        if "href" in elemento2.attrs and "title" in elemento2.attrs:
                            nombre = elemento2["title"]
                            uri_apartado = elemento2["href"]
                            descargarPDFs(uri_apartado, cookie, nombre, i)
                            getTareas(uri_apartado, cookie, datos)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Llama al método con tu usuario y luego apellidos")
        exit(0)
    registro(sys.argv[1], sys.argv[2])
