# Crypto Bot 🤖

Un bot de Twitter que busca tweets sobre criptomonedas, encuentra usuarios relevantes y publica tweets interactivos solicitando donaciones.

## Características 🌟

- 🔍 Búsqueda de tweets sobre criptomonedas específicas
- 👥 Encuentra usuarios con más de 150 seguidores
- 💾 Guarda usuarios encontrados en `found_users.json`
- 🎨 Genera imágenes con DALL-E 3 de un robot suplicando
- 📱 Superpone un código QR en la imagen
- 🤖 Genera mensajes divertidos con GPT-4
- 🔄 Ejecuta ciclos cada 10 minutos
- 🎯 Etiqueta al último usuario encontrado con la misma moneda

## Requisitos 📋

- Python 3.8+
- Cuenta de Twitter con API v2
- Cuenta de OpenAI con acceso a GPT-4 y DALL-E 3
- Cuenta de Binance para generar códigos QR

## Instalación 🛠️

1. Clona el repositorio:
```bash
git clone https://github.com/tu-usuario/crypto-bot.git
cd crypto-bot
```

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

3. Crea un archivo `.env` con tus credenciales:
```env
# Twitter API v2
TWITTER_API_KEY=tu_api_key
TWITTER_API_SECRET=tu_api_secret
TWITTER_ACCESS_TOKEN=tu_access_token
TWITTER_ACCESS_TOKEN_SECRET=tu_access_token_secret
TWITTER_BEARER_TOKEN=tu_bearer_token

# OpenAI
OPENAI_API_KEY=tu_openai_api_key

# Binance
BINANCE_API_KEY=tu_binance_api_key
BINANCE_API_SECRET=tu_binance_api_secret
```

## Uso 🚀

1. Ejecuta el bot:
```bash
python crypto_bot.py
```

2. El bot:
   - Busca tweets sobre criptomonedas
   - Filtra usuarios con más de 150 seguidores
   - Guarda usuarios en `found_users.json`
   - Genera una imagen con DALL-E 3
   - Superpone un código QR de Binance
   - Genera un mensaje con GPT-4
   - Publica el tweet etiquetando al último usuario encontrado
   - Espera 10 minutos antes del siguiente ciclo

## Estructura del Proyecto 📁

```
crypto_bot/
├── crypto_bot.py      # Código principal
├── requirements.txt   # Dependencias
├── .env              # Variables de entorno
├── found_users.json  # Usuarios encontrados
└── generated_images/ # Imágenes generadas
```

## Dependencias 📦

- `openai==1.12.0` - Para DALL-E 3 y GPT-4
- `python-dotenv==1.0.1` - Para variables de entorno
- `requests==2.31.0` - Para llamadas HTTP
- `requests-oauthlib==1.3.1` - Para autenticación OAuth
- `Pillow==10.2.0` - Para procesamiento de imágenes
- `schedule==1.2.0` - Para programación de tareas

## Notas 📝

- El bot usa la API v2 de Twitter
- Las imágenes se guardan en `generated_images/`
- Los usuarios encontrados se guardan en `found_users.json`
- El bot etiqueta al último usuario encontrado con la misma moneda
- Si no hay nuevos usuarios, selecciona aleatoriamente de la lista existente

## Contribuir 🤝

Las contribuciones son bienvenidas. Por favor, abre un issue primero para discutir los cambios que te gustaría hacer.

## Licencia 📄

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles. 