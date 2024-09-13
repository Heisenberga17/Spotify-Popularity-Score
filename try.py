import base64
import requests
import pandas as pd
from datetime import datetime
import os

# *Reemplaza estos valores con tus datos de Spotify for Developers*
CLIENT_ID = '737e719bb4c4413dab75709796eea4f5'     # Aquí pones tu Client ID de Spotify
CLIENT_SECRET = '2257b35c9acb46ea817f4a99cf833a8c'  # Aquí pones tu Client Secret de Spotify

def get_token():
    # URL de autenticación de Spotify (esto se queda igual)
    auth_url = 'https://accounts.spotify.com/api/token'
    
    # Codificamos el Client ID y el Client Secret en formato base64
    auth_header = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()

    headers = {
        'Authorization': f'Basic {auth_header}',
    }

    data = {
        'grant_type': 'client_credentials'
    }

    # Realizamos la solicitud para obtener el token
    response = requests.post(auth_url, headers=headers, data=data)
    response_data = response.json()

    # Devolvemos el token de acceso
    return response_data['access_token']

def get_artist_data(artist_id, token):
    # Hacemos la solicitud para obtener los datos del artista
    url = f"https://api.spotify.com/v1/artists/{artist_id}"
    headers = {
        'Authorization': f'Bearer {token}'  # Pasamos el token de acceso
    }

    # Obtenemos la respuesta de Spotify
    response = requests.get(url, headers=headers)
    artist_data = response.json()

    # Regresamos el nombre del artista, Popularity Score y seguidores
    return artist_data['name'], artist_data['popularity'], artist_data['followers']['total']

# *Reemplaza el artist_id con el ID del artista que quieres rastrear*
artist_id = '2QpRYjtwNg9z6KwD4fhC5h'  # Aquí pones el ID del artista que deseas

# Obtenemos el token de acceso
token = get_token()

# Obtenemos el nombre del artista, Popularity Score y seguidores
artist_name, popularity_score, followers = get_artist_data(artist_id, token)

# Imprimimos los datos obtenidos
print(f"Artist: {artist_name}")
print(f"Popularity Score: {popularity_score}")
print(f"Followers: {followers}")

# Función mejorada para almacenar los datos en un CSV
def store_popularity_score(artist_id, artist_name, popularity_score, followers):
    # Datos que se almacenarán en el CSV
    data = {'artist_id': artist_id,
            'artist_name': artist_name,
            'popularity_score': popularity_score,
            'followers': followers,
            'date': datetime.now().strftime('%Y-%m-%d')}
    
    # Definir el nombre del archivo CSV
    csv_file = 'popularity_scores.csv'

    # Verificar si el archivo ya existe
    file_exists = os.path.isfile(csv_file)

    # Crear un DataFrame con los datos
    df = pd.DataFrame([data])

    # Guardar los datos en el archivo CSV
    if not file_exists:
        # Si el archivo no existe, crearlo con encabezados
        df.to_csv(csv_file, mode='a', header=True, index=False)
    else:
        # Si el archivo ya existe, agregar los datos sin escribir el encabezado
        df.to_csv(csv_file, mode='a', header=False, index=False)

# Guardamos los resultados en un archivo CSV mejorado
store_popularity_score(artist_id, artist_name, popularity_score, followers)
