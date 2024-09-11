# -*- coding: utf-8 -*-
import urllib.parse
import requests
import webbrowser
from socket import AF_INET, socket, SOCK_STREAM
import json


print("###################################")
print("OAuth 2.0 for Mobile & Desktop Apps")
print("###################################")
# https://developers.google.com/identity/protocols/oauth2/native-app

print("\nStep 1.- Prerequisites on Google Cloud Console")
# https://developers.google.com/identity/protocols/oauth2/native-app#prerequisites

print("\tEnable APIs for your project")
# https://developers.google.com/identity/protocols/oauth2/native-app#enable-apis

print("\tIdentify access scopes")
# https://developers.google.com/identity/protocols/oauth2/native-app#identify-access-scopes
scope = "https://www.googleapis.com/auth/calendar.calendarlist.readonly https://www.googleapis.com/auth/calendar.events"
# Lista los calendarios de google

print("\tCreate authorization credentials")
# https://developers.google.com/identity/protocols/oauth2/native-app#creatingcred
client_id = "841823985159-uhi2dcci9fv3kmpnsc3qhqqg9fc2mimq.apps.googleusercontent.com"
client_secret = "xxxxxxxxxx"
print("\tConfigure OAuth consent screen")
print("\tAdd access scopes and test users")

redirect_uri = "http://localhost:8090"

print("\nStep 2.- Send a request to Google's OAuth 2.0 server")
# https://developers.google.com/identity/protocols/oauth2/native-app#step-2:-send-a-request-to-googles-oauth-2.0-server

uri = "https://accounts.google.com/o/oauth2/v2/auth"
datos = {
    'client_id': client_id,
    'redirect_uri': redirect_uri,
    'response_type': 'code',
    'scope': scope
}
datos_encoded = urllib.parse.urlencode(datos)

print("\nOpening browser...")
webbrowser.open_new((uri + '?' + datos_encoded))

print("\nStep 3.- Google prompts user for consent")

print("\nStep 4.- Handle the OAuth 2.0 server response")

server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(('localHost', 8090))
server_socket.listen(1)
print("\nLocal server listening on port 8090")

client_connection, client_address = server_socket.accept()
peticion = client_connection.recv(1024)
print("\nRequest for the browser received at local server")

# https://developers.google.com/identity/protocols/oauth2/native-app#handlingresponse
# Crear servidor local que escucha por el puerto 8090

# print("\tLocal server listening on port 8090")

# Recibir la solicitude 302 del navegador

# print("\tRequest from the browser received at local server:")

# Buscar en la petición el "auth_code"
primera_linea = peticion.decode('UTF8').split('\n')[0]
aux_auth_code = primera_linea.split(' ')[1]
auth_code = aux_auth_code[7:].split('&')[0]
print("\tauth_code: " + auth_code)

# Devolver una respuesta al usuario y cerrar conexion y sockets
http_response = "HTTP/1.1 200 OK\r\n\r\n" \
                "<html>" \
                "<head><title>Prueba</title></head>" \
                "<body>The authentication flow has completed. Close this window.</body>" \
                "</html>"
client_connection.sendall(http_response.encode(encoding="utf-8"))
client_connection.close()
server_socket.close()

print("\nStep 5.- Exchange authorization code for refresh and access tokens")
# https://developers.google.com/identity/protocols/oauth2/native-app#exchange-authorization-code

uri = "https://oauth2.googleapis.com/token"
cabeceras = {'Host': 'oauth2.googleapis.com',
             'Content-Type': 'application/x-www-form-urlencoded'}
datos = {
    'code': auth_code,
    'client_id': client_id,
    'client_secret': client_secret,
    'redirect_uri': redirect_uri,
    'grant_type': 'authorization_code'
}
respuesta = requests.post(uri, headers=cabeceras, data=datos, allow_redirects=False)
status = respuesta.status_code
print("\nStatus" + ' ' + str(status))

contenido = respuesta.text
print("\nContenido: " + contenido)

acces_token = contenido.split('"')[3]
print(acces_token)

# Google responds to this request by returning a JSON object
# that contains a short-lived access token and a refresh token.

# input("The authentication flow has completed. Close browser window and press enter to continue...")

print("\nStep 6.- Calling Google APIs")
# Calendar API: https://developers.google.com/calendar/v3/reference
# CalendarList: https://developers.google.com/calendar/v3/reference#CalendarList
# CalendarList:list: https://developers.google.com/calendar/v3/reference/calendarList/list

uri = "https://www.googleapis.com/calendar/v3/users/me/calendarList"
cabeceras = {'Authorization': "Bearer " + acces_token,
             'Accept': 'application/json'}
respuesta = requests.get(uri, headers=cabeceras, allow_redirects=False)
status = respuesta.status_code

print(status)
print(respuesta.text)

print("\nStep 7.- See the event calendar")
uri = "https://www.googleapis.com/calendar/v3/calendars/matecooperativo@gmail.com/events"

cabeceras = {'Authorization': "Bearer " + acces_token,
             'Accept': 'application/json'}

respuesta = requests.get(uri, headers=cabeceras, allow_redirects=False)
status = respuesta.status_code

print(status)
print(respuesta.text)
summary = json.loads(respuesta.text)["items"][0]["summary"]
print("Summarys de eventos:\n")
print(summary)

print("\nStep 8.- Insert an event in Google Calendar")
# https://developers.google.com/calendar/v3/reference/events/insert

uri = "https://www.googleapis.com/calendar/v3/calendars/matecooperativo@gmail.com/events"

cabeceras = {'Authorization': "Bearer " + acces_token,
             'Accept': 'application/json',
             'Content-Type': 'application/json'}

datos = \
    {
        "end": {"datetime": "2024-04-20T22:30:00.000Z"},
        "start": {"datetime": "2024-04-20T21:30:00.000Z"}
    }

respuesta = requests.post(uri, headers=cabeceras, data=datos, allow_redirects=False)
status = respuesta.status_code
print("\nStatus" + ' ' + str(status))

contenido = respuesta.text
print("\nContenido: " + contenido)
