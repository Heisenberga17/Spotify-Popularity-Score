import requests
import base64
from datetime import datetime

# Spotify API Credentials (reemplaza estos valores con los tuyos)
CLIENT_ID = '737e719bb4c4413dab75709796eea4f5'
CLIENT_SECRET = '2257b35c9acb46ea817f4a99cf833a8c'

# URL de tu Google Form (el enlace de envío del formulario)
google_form_url = "https://docs.google.com/spreadsheets/d/1NveyUd0H_7u1N4HBULZq1TsFF4_ulH1ydaFvECZuMts/edit?gid=0#gid=0"

# Obtener token de acceso de Spotify API
def get_token():
    auth_url = 'https://accounts.spotify.com/api/token'
    auth_header = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()

    headers = {
        'Authorization': f'Basic {auth_header}',
    }

    data = {
        'grant_type': 'client_credentials'
    }

    response = requests.post(auth_url, headers=headers, data=data)
    response_data = response.json()

    return response_data['access_token']

# Obtener los datos del artista desde Spotify
def get_artist_data(artist_id, token):
    url = f"https://api.spotify.com/v1/artists/{artist_id}"
    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.get(url, headers=headers)
    artist_data = response.json()

    return artist_data['name'], artist_data['popularity'], artist_data['followers']['total']

# Enviar los datos al formulario de Google Forms
def send_to_google_form(artist_id, artist_name, popularity_score, followers):
    # Diccionario de datos a enviar (ajusta los 'entry.XYZ' con el ID del campo en el formulario)
    data = {
        'entry.1234567890': artist_id,         # Reemplaza con el ID del campo para "ID del Artista"
        'entry.0987654321': artist_name,       # Reemplaza con el ID del campo para "Nombre del Artista"
        'entry.1112131415': popularity_score,  # Reemplaza con el ID del campo para "Popularidad"
        'entry.1213141516': followers,         # Reemplaza con el ID del campo para "Seguidores"
        'entry.1718192021': datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Reemplaza con el ID del campo para "Fecha y hora"
    }

    # Enviar la solicitud POST al Google Form
    response = requests.post(google_form_url, data=data)

    if response.status_code == 200:
        print("Datos enviados correctamente al Google Sheet")
    else:
        print(f"Error al enviar los datos: {response.status_code}")

# ID del artista que quieres rastrear
artist_id = '2QpRYjtwNg9z6KwD4fhC5h'  # Ejemplo: ID de Queen

# Obtener el token de acceso de Spotify
token = get_token()

# Obtener los datos del artista desde la API de Spotify
artist_name, popularity_score, followers = get_artist_data(artist_id, token)

# Enviar los datos obtenidos al formulario de Google Forms
send_to_google_form(artist_id, artist_name, popularity_score, followers)