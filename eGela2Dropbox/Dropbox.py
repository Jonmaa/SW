import requests
import urllib
import webbrowser
from socket import AF_INET, socket, SOCK_STREAM
import json
import helper

app_key = 'c564rgl7lo85l0w'
app_secret = 'q4mpmxdcwsckyfq'
server_addr = "localhost"
server_port = '8090'
redirect_uri = "http://" + server_addr + ":" + str(server_port)

class Dropbox:
    _access_token = ""
    _path = ""
    _files = []
    _root = None
    _msg_listbox = None

    def __init__(self, root):
        self._root = root

    def local_server(self):
        # por el puerto 8090 esta escuchando el servidor que generamos
        server_socket = socket(AF_INET, SOCK_STREAM)
        server_socket.bind((server_addr, server_port))
        server_socket.listen(1)
        print("\tLocal server listening on port " + str(server_port))

        # recibe la redireccio 302 del navegador
        client_connection, client_address = server_socket.accept()
        peticion = client_connection.recv(1024)
        print("\tRequest from the browser received at local server:")
        print(peticion)

        # buscar en solicitud el "auth_code"
        primera_linea = peticion.decode('UTF8').split('\n')[0]
        aux_auth_code = primera_linea.split(' ')[1]
        auth_code = aux_auth_code[7:].split('&')[0]
        print("\tauth_code: " + auth_code)

        # devolver una respuesta al usuario
        http_response = "HTTP/1.1 200 OK\r\n\r\n" \
                        "<html>" \
                        "<head><title>Proba</title></head>" \
                        "<body>The authentication flow has completed. Close this window.</body>" \
                        "</html>"
        client_connection.sendall(http_response)
        client_connection.close()
        server_socket.close()

        return auth_code

    def do_oauth(self):
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



        self._access_token = access_token
        print(access_token)
        self._root.destroy()

    def list_folder(self, msg_listbox):
        if self._path == "/":
            self._path = ""

        print("/list_folder")
        uri = 'https://api.dropboxapi.com/2/files/list_folder'
        # https://www.dropbox.com/developers/documentation/http/documentation#files-list_folder
        #############################################
        # RELLENAR CON CODIGO DE LA PETICION HTTP
        # Y PROCESAMIENTO DE LA RESPUESTA HTTP

        datos = {
            "path": self._path
        }
        datos = json.dumps(datos)

        cabeceras = {'Host': 'api.dropboxapi.com', 'Authorization': 'Bearer ' + self._access_token,
                     'Content-Type': 'application/json'}
        uri = 'https://api.dropboxapi.com/2/files/list_folder'

        respuesta = requests.post(uri, headers=cabeceras, data=datos, allow_redirects=False)


        print()
        print()
        print(respuesta.status_code)
        print()
        print(respuesta.content)
        contenido = respuesta.text
        print(contenido)
        contenido_json = json.loads(contenido)
        print()
        print()




        #############################################

        self._files = helper.update_listbox2(msg_listbox, self._path, contenido_json)

    def transfer_file(self, file_path, file_data):
        print("/upload")
        uri = 'https://content.dropboxapi.com/2/files/upload'
        # https://www.dropbox.com/developers/documentation/http/documentation#files-upload
        #############################################

        headers = {
            "Authorization": "Bearer " + self._access_token,
            "Content-Type": "application/octet-stream",
            "Dropbox-API-Arg": json.dumps({"path": file_path, "mode": "overwrite"})
        }


        print("--TRANSFER FILE--")
        respuesta = requests.post(uri, data=file_data, headers=headers)
        print(respuesta.status_code)



        #############################################

    def delete_file(self, file_path):
        print("/delete_file")
        uri = 'https://api.dropboxapi.com/2/files/delete_v2'
        # https://www.dropbox.com/developers/documentation/http/documentation#files-delete
        headers = {
            "Authorization": "Bearer " + self._access_token,
            "Content-Type": "application/json"
        }
        datos = json.dumps({"path": file_path})
        respuesta = requests.post(uri, data=datos, headers=headers)

        print("--DELETE FILE--")
        print(respuesta.status_code)
        #############################################

    def create_folder(self, path):
        print("/create_folder")
        uri = "https://api.dropboxapi.com/2/files/create_folder_v2"

        headers = {
            "Authorization": "Bearer " + self._access_token,
            "Content-Type": "application/json"
        }
        datos = json.dumps({"autorename":False,"path":path})
        respuesta = requests.post(uri, data=datos, headers=headers)

        print("--CREATE FOLDER--")
        print(respuesta.status_code)


    def get_space(self):
        print("/get espace")

        uri = "https://api.dropboxapi.com/2/users/get_space_usage"

        headers = { "Authorization": "Bearer " + self._access_token }

        respuesta = requests.post(uri, headers=headers)

        print("--GET SPACE--")
        print(respuesta.status_code)
        json_respuesta = json.loads(respuesta.text)
        megaTotal = json_respuesta['allocation']['allocated'] * 0.000001
        megaUsed = json_respuesta['used'] * 0.000001

        return megaTotal, megaUsed



    def get_file_id(self, path):
        # https://www.dropbox.com/developers/documentation/http/documentation#files-get_metadata
        print("--GET FILE ID--")
        id = ""
        uri = "https://api.dropboxapi.com/2/files/get_metadata"
        headers = {
            "Authorization": "Bearer " + self._access_token,
            "Content-Type": "application/json"
        }
        data = {
            "include_deleted": False,
            "include_has_explicit_shared_members": False,
            "include_media_info": False,
            "path": path
        }
        datos = json.dumps(data)
        respuesta = requests.post(uri, data=datos, headers=headers)
        print(respuesta.status_code)
        print(respuesta.text)
        json_respuesta = json.loads(respuesta.text)
        id = json_respuesta['id']
        print(id)

        return id

    def share_file_email(self, path, email):
        # no comparte el link, comparte el archivo directamente
        # https://www.dropbox.com/developers/documentation/http/documentation#sharing-add_file_member
        id = self.get_file_id(path)
        uri = "https://api.dropboxapi.com/2/sharing/add_file_member"
        headers = {
            "Authorization": "Bearer " + self._access_token,
            "Content-Type": "application/json"
        }

        data = {
            "access_level": "viewer",
            "add_message_as_comment": False,
            "custom_message": "This is a custom message about ACME.doc",
            "file": id,
            "members": [
                {
                    ".tag": "email",
                    "email": email
                }
            ],
            "quiet": False
        }
        datos = json.dumps(data)
        respuesta = requests.post(uri, data=datos, headers=headers)
        print("STATUS CODE COMPARTIR FILE")
        print(respuesta.status_code)







