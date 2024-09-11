#-*- coding: utf-8 -*-
import urllib.parse
import requests
import webbrowser
from socket import AF_INET, socket, SOCK_STREAM
import json

app_key = 'ar9y1t2mmnxrvvj'
app_secret = 'xxxxxxxxx'
server_addr = 'localhost'
server_port = '8090'
redirect_uri = "http://" + server_addr + ":" + str(server_port)


###################################################################################
#  CODE: Abrir en el navegador la URI  https://www.dropbox.com/oauth2/authorize   #
###################################################################################
# FALTA CÓDIGO
servidor = 'www.dropbox.com'
params = {'response_type': 'code',
          'client_id': app_key,
          'redirect_uri': redirect_uri,
          }

params_encoded = urllib.parse.urlencode(params)
recurso = '/oauth2/authorize?' + params_encoded
uri = 'https://' + servidor + recurso
webbrowser.open_new(uri)
print("\nConnected to Dropbox")

# Crear servidor local que escucha por el puerto server_port
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(('localHost', 8090))
server_socket.listen(1)
print("\nLocal server listening on port 8090")

# Recibir la solicitude 302 del navegador
client_connection, client_address = server_socket.accept()
peticion = client_connection.recv(1024)
print("\nRequest for the browser received at local server")

# Buscar en la petición el "auth_code"
print(peticion.decode('UTF8'))
primera_linea = peticion.decode('UTF8').split('\n')[0]
aux_auth_code = primera_linea.split(' ')[1]
auth_code = aux_auth_code[7:].split('&')[0]
print("\tauth_code: " + auth_code)

# Devolver una respuesta al usuario
http_response = "HTTP/1.1 200 OK\r\n\r\n" \
                "<html>" \
                "<head><title>Prueba</title></head>" \
                "<body>The authentication flow has completed. Close this window.</body>" \
                "</html>"
client_connection.sendall(http_response.encode(encoding="utf-8"))
client_connection.close()
server_socket.close()

###################################################################################
#  ACCESS_TOKEN: Obtener el TOKEN  https://www.api.dropboxapi.com/1/oauth2/token  #
###################################################################################
### FALTA CÓDIGO
params = {'code': auth_code,
          'grant_type': 'authorization_code',
          'client_id': app_key,
          'client_secret': app_secret,
          'redirect_uri': redirect_uri,
          }

cabeceras = {'User-Agent': 'Python Client',
             'Content-Type': 'application/x-www-form-urlencoded'}
uri = 'https://api.dropboxapi.com/1/oauth2/token'
respuesta = requests.post(uri, data=params, headers=cabeceras)
print(respuesta.status_code)
json_respuesta = json.loads(respuesta.text)
access_token = json_respuesta['access_token']
print("Access_Token:" + access_token)



###################################################################################
#  USAR APLICACION: /list_folder                                                  #
###################################################################################
# Todo: Corregir el codigo
print("/list_folder")

uri = "https://api.dropboxapi.com/2/files/list_folder"

cabeceras = {'Authorization': "Bearer " + access_token,
             'Content-Type': 'application/json', 'Host': 'api.dropboxapi.com'}

respuesta = requests.post(uri, headers=cabeceras, allow_redirects=False)
status = respuesta.status_code

print('\nStatus: ' + str(status))
contenido = respuesta.text
print(contenido)
contenido_json = json.loads(contenido)
print("Ficheros de: " + path)
for entry in contenido_json['entries']:
    print(entry['name'])
