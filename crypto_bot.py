import os
import openai
from dotenv import load_dotenv
import time
from requests_oauthlib import OAuth1Session
import random
import requests
from PIL import Image
from io import BytesIO
import json
from datetime import datetime

print("Todas las importaciones se realizaron correctamente")

# Load environment variables
load_dotenv()
print("Variables de entorno cargadas correctamente")

# OpenAI Configuration
openai.api_key = os.getenv('OPENAI_API_KEY')

# Twitter Configuration
TWITTER_API_KEY = os.getenv('TWITTER_API_KEY')
TWITTER_API_SECRET = os.getenv('TWITTER_API_SECRET')
TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
TWITTER_ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
TWITTER_BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN')

# Credenciales de la cuenta secundaria (solo para búsqueda)
TWITTER_BEARER_TOKEN_SECOND = os.getenv("TWITTER_BEARER_TOKEN_SECOND")

# Lista de tokens populares para buscar
CRYPTO_TOKENS = [
    'bitcoin', 'btc', 'ethereum', 'eth', 'binance', 'bnb', 'cardano', 'ada',
    'solana', 'sol', 'polkadot', 'dot', 'dogecoin', 'doge', 'shiba', 'shib'
]

# Dictionary of cryptocurrencies and their tickers
CRYPTO_COINS = {
    "Bitcoin": "BTC",
    "Ethereum": "ETH",
    "Solana": "SOL",
    "XRP": "XRP",
    "Cardano": "ADA",
    "Dogecoin": "DOGE",
    "Polkadot": "DOT",
    "Polygon": "MATIC",
    "Avalanche": "AVAX",
    "Binance Coin": "BNB",
    "Chainlink": "LINK",
    "Uniswap": "UNI",
    "Litecoin": "LTC",
    "Cosmos": "ATOM",
    "Filecoin": "FIL",
    "VeChain": "VET",
    "Theta": "THETA",
    "Aave": "AAVE",
    "Compound": "COMP",
    "Synthetix": "SNX"
}

# Lista para almacenar usuarios encontrados
FOUND_USERS = set()

def get_twitter_oauth():
    auth_url = "https://api.twitter.com/oauth2/token"
    auth_headers = {
        "Authorization": f"Basic {TWITTER_API_KEY}:{TWITTER_API_SECRET}"
    }
    auth_data = {
        "grant_type": "client_credentials"
    }
    
    response = requests.post(auth_url, headers=auth_headers, data=auth_data)
    return response.json().get("access_token")

def search_tweets(token):
    try:
        headers = {
            "Authorization": f"Bearer {TWITTER_BEARER_TOKEN}"
        }
        
        url = f"https://api.twitter.com/2/tweets/search/recent?query={token} lang:en -is:retweet&tweet.fields=author_id,public_metrics&expansions=author_id&user.fields=public_metrics"
        
        print(f"Buscando tweets para: {token}")
        response = requests.get(url, headers=headers)
        print(f"Respuesta de la API: {response.status_code}")
        
        if response.status_code != 200:
            print(f"Error en la respuesta: {response.text}")
            return None
            
        return response.json()
    except Exception as e:
        print(f"Error en search_tweets: {str(e)}")
        return None

def search_tweets_second_account(token):
    try:
        headers = {
            "Authorization": f"Bearer {TWITTER_BEARER_TOKEN_SECOND}"
        }
        
        url = f"https://api.twitter.com/2/tweets/search/recent?query={token} lang:en -is:retweet&tweet.fields=author_id,public_metrics&expansions=author_id&user.fields=public_metrics"
        
        print(f"Buscando tweets con cuenta secundaria para: {token}")
        response = requests.get(url, headers=headers)
        print(f"Respuesta de la API (cuenta secundaria): {response.status_code}")
        
        if response.status_code != 200:
            print(f"Error en la respuesta: {response.text}")
            return None
            
        return response.json()
    except Exception as e:
        print(f"Error en search_tweets_second_account: {str(e)}")
        return None

def find_new_users():
    print("Iniciando búsqueda de nuevos usuarios...")
    new_users = set()
    
    # Seleccionar un ticker aleatorio de la lista
    ticker = random.choice(list(CRYPTO_COINS.values()))
    crypto = next((name for name, t in CRYPTO_COINS.items() if t == ticker), None)
    print(f"Buscando tweets con el ticker: ${ticker} ({crypto})")
    
    try:
        # Intentar primero con la cuenta principal
        results = search_tweets(ticker)
        if results and "data" in results and "includes" in results:
            print(f"Encontrados {len(results['data'])} tweets con cuenta principal para ${ticker}")
            for tweet in results["data"]:
                if len(new_users) >= 10:  # Si ya encontramos 10 usuarios, terminamos
                    break
                    
                author = next((user for user in results["includes"]["users"] if user["id"] == tweet["author_id"]), None)
                if author and author["public_metrics"]["followers_count"] > 150 and author["username"] not in FOUND_USERS and author["username"] not in new_users:
                    new_users.add(author["username"])
                    print(f"Nuevo usuario encontrado: @{author['username']}")
                    print(f"Seguidores: {author['public_metrics']['followers_count']}")
                    print(f"Total de usuarios únicos encontrados: {len(new_users)}")
                elif author and author["public_metrics"]["followers_count"] <= 150:
                    print(f"Usuario @{author['username']} ignorado por tener pocos seguidores: {author['public_metrics']['followers_count']}")
        
        # Si no encontramos 10 usuarios, intentar con la cuenta secundaria
        if len(new_users) < 10:
            print("\nIntentando búsqueda con cuenta secundaria...")
            results = search_tweets_second_account(ticker)
            if results and "data" in results and "includes" in results:
                print(f"Encontrados {len(results['data'])} tweets con cuenta secundaria para ${ticker}")
                for tweet in results["data"]:
                    if len(new_users) >= 10:  # Si ya encontramos 10 usuarios, terminamos
                        break
                        
                    author = next((user for user in results["includes"]["users"] if user["id"] == tweet["author_id"]), None)
                    if author and author["public_metrics"]["followers_count"] > 150 and author["username"] not in FOUND_USERS and author["username"] not in new_users:
                        new_users.add(author["username"])
                        print(f"Nuevo usuario encontrado: @{author['username']}")
                        print(f"Seguidores: {author['public_metrics']['followers_count']}")
                        print(f"Total de usuarios únicos encontrados: {len(new_users)}")
                    elif author and author["public_metrics"]["followers_count"] <= 150:
                        print(f"Usuario @{author['username']} ignorado por tener pocos seguidores: {author['public_metrics']['followers_count']}")
        
        # Actualizar la lista global de usuarios encontrados
        if new_users:
            FOUND_USERS.update(new_users)
            print(f"Total de usuarios únicos encontrados en esta búsqueda: {len(new_users)}")
            
            # Guardar usuarios en un archivo para persistencia
            try:
                with open("found_users.json", "w") as f:
                    json.dump(list(FOUND_USERS), f)
                print("Usuarios guardados en found_users.json")
            except Exception as e:
                print(f"Error al guardar usuarios: {str(e)}")
        else:
            print("No se encontraron nuevos usuarios en esta búsqueda")
        
        return new_users, crypto, ticker
        
    except Exception as e:
        print(f"Error al buscar tweets: {str(e)}")
        return set(), None, None

def load_found_users():
    try:
        with open("found_users.json", "r") as f:
            return set(json.load(f))
    except FileNotFoundError:
        return set()

def generate_image(crypto, ticker):
    try:
        print(f"Generando imagen para {crypto} (${ticker}) con modelo gpt-image-1...")
        response = openai.Image.create(
            model="gpt-image-1",
            prompt=f"Create a unique and creative 3D robot character kneeling on the ground, facing right, holding a tablet that displays a {crypto} coin with the symbol ${ticker}. The robot should be in a begging pose, looking up and to the right with hopeful eyes. The tablet should be held with both hands, showing the coin clearly. Make it playful and cartoonish in 3D style, with a simple gradient background. The robot should have a distinctive and creative design - it could be a retro-futuristic robot, a cute chibi robot, a steampunk robot, a minimalist robot, or any other unique style, but always maintaining the pleading pose and tablet. The robot's body and head should be oriented towards the right side of the image. The design should be different each time, but always friendly and expressive. The image should be rendered in 3D with depth and dimension, focusing on the robot's pleading pose and the tablet display.",
            n=1,
            size="1024x1024"
        )
        
        # Imprimir la estructura de la respuesta para depuración
        print(f"Estructura de respuesta: {response}")
        
        # Manejar diferentes estructuras de respuesta
        if 'data' in response and len(response['data']) > 0:
            if 'url' in response['data'][0]:
                image_url = response['data'][0]['url']
            elif 'b64_json' in response['data'][0]:
                # Manejar respuesta en base64 si es necesario
                print("Recibiendo imagen en formato base64, guardando directamente...")
                import base64
                image_data = base64.b64decode(response['data'][0]['b64_json'])
                
                # Crear directorio si no existe
                if not os.path.exists("generated_images"):
                    os.makedirs("generated_images")
                
                # Generar nombre único para la imagen
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"generated_images/{crypto}_{ticker}_{timestamp}.png"
                
                # Guardar la imagen generada
                with open(filename, "wb") as f:
                    f.write(image_data)
                
                print(f"Imagen guardada directamente como: {filename}")
                return filename  # Devolver directamente el nombre del archivo
            else:
                print(f"Formato de respuesta desconocido: {response['data'][0].keys()}")
                return None
        else:
            print(f"Estructura de respuesta inesperada: {response.keys()}")
            return None
            
        return image_url
    except Exception as e:
        print(f"Error generating image: {str(e)}")
        print(f"Tipo de error: {type(e)}")
        if hasattr(e, 'response'):
            print(f"Detalles de respuesta: {e.response}")
        return None

def download_image(url, crypto, ticker):
    try:
        print("Descargando imagen generada...")
        response = requests.get(url)
        if response.status_code == 200:
            # Crear directorio si no existe
            if not os.path.exists("generated_images"):
                os.makedirs("generated_images")
            
            # Generar nombre único para la imagen
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"generated_images/{crypto}_{ticker}_{timestamp}.png"
            
            # Guardar la imagen generada
            with open(filename, "wb") as f:
                f.write(response.content)
            print(f"Imagen guardada como: {filename}")
            
            # Cargar la imagen generada y el QR
            main_image = Image.open(filename)
            qr_image = Image.open("ETHQR.png")
            
            # Redimensionar el QR a un tamaño más pequeño (por ejemplo, 100x100)
            qr_size = 100
            qr_image = qr_image.resize((qr_size, qr_size))
            
            # Calcular posición para la esquina inferior izquierda
            position = (20, main_image.height - qr_size - 20)  # 20 píxeles desde los bordes
            
            # Pegar el QR sobre la imagen principal
            main_image.paste(qr_image, position)
            
            # Guardar la imagen final
            main_image.save(filename)
            print("QR superpuesto en la imagen")
            
            return filename
        else:
            print(f"Error al descargar imagen: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error al procesar imagen: {str(e)}")
        return None

def upload_media(image_path):
    oauth = OAuth1Session(
        client_key=TWITTER_API_KEY,
        client_secret=TWITTER_API_SECRET,
        resource_owner_key=TWITTER_ACCESS_TOKEN,
        resource_owner_secret=TWITTER_ACCESS_TOKEN_SECRET
    )
    
    url = "https://upload.twitter.com/1.1/media/upload.json"
    
    with open(image_path, 'rb') as image_file:
        media_data = image_file.read()
    
    files = {'media': media_data}
    
    response = oauth.post(url, files=files)
    if response.status_code == 200:
        return response.json()['media_id_string']
    else:
        print(f"Error uploading media: {response.text}")
        return None

def post_tweet(user=None, crypto=None, ticker=None):
    global FOUND_USERS  # Declarar que usaremos la variable global
    try:
        print("\nIniciando proceso de publicación de tweet...")
        
        # Si no se proporcionan parámetros, buscar nuevos usuarios
        if not user or not crypto or not ticker:
            if not FOUND_USERS:
                print("No hay usuarios encontrados para hacer tweet. Buscando nuevos usuarios...")
                new_users, crypto, ticker = find_new_users()
                if not new_users:
                    print("No se encontraron nuevos usuarios. Esperando al siguiente ciclo...")
                    return None
                FOUND_USERS.update(new_users)  # Actualizar la variable global
                print(f"Usando la misma moneda de la búsqueda: {crypto} (${ticker})")
                
                # Usar el último usuario añadido a la lista
                user = '@' + list(new_users)[-1]  # Tomar el último usuario de los nuevos
                print(f"Usando el último usuario encontrado: {user}")
            else:
                # Si ya hay usuarios, seleccionar uno aleatorio y una criptomoneda aleatoria
                crypto = random.choice(list(CRYPTO_COINS.keys()))
                ticker = CRYPTO_COINS[crypto]
                print(f"Usando moneda aleatoria: {crypto} (${ticker})")
                user = '@' + random.choice(list(FOUND_USERS))
                print(f"Usuario aleatorio seleccionado: {user}")
        
        print(f"Criptomoneda seleccionada: {crypto} (${ticker})")
        
        # Generate funny message about crypto
        print("Generando mensaje con GPT-4...")
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a friendly bot that writes funny tweets asking for cryptocurrency donations in English. Do not use quotes in your responses."},
                {"role": "user", "content": f"Generate a funny and friendly tweet asking {user} to donate some {crypto} (${ticker}). It should be short, use emojis, and be playful. Make it in English. Do not use quotes."}
            ]
        )
        message = response.choices[0].message.content.strip('"').strip("'")
        print(f"Mensaje generado: {message}")
        
        # Generate and upload image
        print("Generando imagen con modelo de IA...")
        image_result = generate_image(crypto, ticker)
        if image_result:
            # Verificar si el resultado es una URL o un nombre de archivo local
            if image_result.startswith("http"):
                print("Imagen generada, descargando...")
                image_path = download_image(image_result, crypto, ticker)
            else:
                print("Usando imagen generada localmente...")
                image_path = image_result
                
                # Verificar si el archivo existe y tiene el QR superpuesto
                try:
                    # Cargar la imagen generada y el QR
                    main_image = Image.open(image_path)
                    qr_image = Image.open("ETHQR.png")
                    
                    # Redimensionar el QR a un tamaño más pequeño
                    qr_size = 100
                    qr_image = qr_image.resize((qr_size, qr_size))
                    
                    # Calcular posición para la esquina inferior izquierda
                    position = (20, main_image.height - qr_size - 20)  # 20 píxeles desde los bordes
                    
                    # Pegar el QR sobre la imagen principal
                    main_image.paste(qr_image, position)
                    
                    # Guardar la imagen final
                    main_image.save(image_path)
                    print("QR superpuesto en la imagen")
                except Exception as e:
                    print(f"Error al procesar imagen local: {str(e)}")
                    
            if image_path:
                print("Imagen lista, subiendo a Twitter...")
                media_id = upload_media(image_path)
                if media_id:
                    print("Imagen subida exitosamente")
                    # Usar API v2 para la publicación
                    oauth = OAuth1Session(
                        client_key=TWITTER_API_KEY,
                        client_secret=TWITTER_API_SECRET,
                        resource_owner_key=TWITTER_ACCESS_TOKEN,
                        resource_owner_secret=TWITTER_ACCESS_TOKEN_SECRET
                    )
                    
                    url = "https://api.twitter.com/2/tweets"
                    data = {
                        "text": message + " #Beggies",
                        "media": {"media_ids": [media_id]}
                    }
                    
                    response = oauth.post(url, json=data)
                    print(f"Código de respuesta: {response.status_code}")
                    print(f"Respuesta: {response.text}")
                    
                    if response.status_code == 201:
                        print("Tweet publicado exitosamente!")
                        return response.json()
                    else:
                        print("Error al publicar el tweet")
                        return None
                else:
                    print("Error al subir la imagen")
                    # Intentar publicar sin imagen
                    oauth = OAuth1Session(
                        client_key=TWITTER_API_KEY,
                        client_secret=TWITTER_API_SECRET,
                        resource_owner_key=TWITTER_ACCESS_TOKEN,
                        resource_owner_secret=TWITTER_ACCESS_TOKEN_SECRET
                    )
                    
                    url = "https://api.twitter.com/2/tweets"
                    data = {
                        "text": message + " #Beggies"
                    }
                    
                    response = oauth.post(url, json=data)
                    print(f"Código de respuesta (sin imagen): {response.status_code}")
                    print(f"Respuesta (sin imagen): {response.text}")
                    
                    if response.status_code == 201:
                        print("Tweet publicado exitosamente!")
                        return response.json()
                    else:
                        print("Error al publicar el tweet")
                        return None
            else:
                print("Error al descargar la imagen")
                return None
        else:
            print("Error al generar la imagen")
            return None
            
    except Exception as e:
        print(f"Error en post_tweet: {str(e)}")
        return None

def main():
    print("Bot started! 🚀")
    
    # Cargar usuarios encontrados previamente
    global FOUND_USERS
    FOUND_USERS = load_found_users()
    print(f"Usuarios cargados previamente: {len(FOUND_USERS)}")
    
    while True:
        try:
            # FASE 1: Búsqueda de usuarios con token aleatorio
            print("\n=== FASE 1: Búsqueda de usuarios ===")
            new_users, crypto, ticker = find_new_users()
            
            if new_users:
                print(f"Se encontraron {len(new_users)} nuevos usuarios")
                print(f"Total de usuarios en la lista: {len(FOUND_USERS)}")
                
                # FASE 2: Publicar tweet usando el mismo token y el último usuario nuevo
                print("\n=== FASE 2: Publicación de tweet con usuario nuevo ===")
                # Usar el último usuario encontrado
                user = '@' + list(new_users)[-1]
                print(f"Usando el último usuario encontrado: {user}")
                print(f"Usando la misma moneda de la búsqueda: {crypto} (${ticker})")
                
                tweet_result = post_tweet(user=user, crypto=crypto, ticker=ticker)
                if tweet_result:
                    print("Tweet publicado exitosamente con usuario nuevo")
                else:
                    print("Error al publicar el tweet")
            else:
                print("No se encontraron nuevos usuarios, usando lista existente")
                # FASE 2: Publicar tweet usando lista existente y token aleatorio
                print("\n=== FASE 2: Publicación de tweet con lista existente ===")
                tweet_result = post_tweet()
                if tweet_result:
                    print("Tweet publicado exitosamente con usuario existente")
                else:
                    print("Error al publicar el tweet")
            
            print("\nEsperando 10 minutos antes del siguiente ciclo...")
            time.sleep(600)  # Wait 10 minutes
        except Exception as e:
            print(f"Error en el ciclo principal: {str(e)}")
            print(f"Tipo de error: {type(e)}")
            time.sleep(60)

if __name__ == "__main__":
    main() 