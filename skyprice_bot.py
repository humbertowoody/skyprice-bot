# @Author: Humberto Alejandro Ortega Alcocer
# @Date: 2024-Abril-8
# @Description: Bot de Telegram para la valuación de departamentos en la Ciudad de México utilizando OpenAI y la API de SkyPrice.
# @Dependencies: python-telegram-bot, openai, requests
# @Usage: python skyprice_bot.py
# @License: MIT
import logging
from typing import Union
from telegram import  Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
import requests
from openai import OpenAI
import json
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize OpenAI API key
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# SkyPrice API URL
SKYPRICE_API_URL = 'https://api.skyprice.xyz/predict'

# Telegram bot token
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN','fake_token')

# Language dictionary
LANGUAGE_COMMANDS = {
    'inicio': 'es',
    'start': 'es', # Spanish by default
    'english': 'en',
    'french': 'fr',
    'portuguese': 'pt'
}

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# Set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

# Get the logger instance
logger = logging.getLogger(__name__)

# Clase para representar los datos requeridos de un departamento
class ApartmentDetails:
    def __init__(self, size_terrain, size_construction, rooms, bathrooms, parking, age, lat, lng, municipality):
        """Initialize the apartment details."""
        self.Size_Terrain = size_terrain
        self.Size_Construction = size_construction
        self.Rooms = rooms
        self.Bathrooms = bathrooms
        self.Parking = parking
        self.Age = age
        self.Lat = lat
        self.Lng = lng
        self.Municipality = municipality

# Clase para representar la predicción de precios
class PricePrediction:
    def __init__(self, random_forest, svm, neural_network):
        """Initialize the price prediction."""
        self.Random_Forest = random_forest
        self.SVM = svm
        self.Neural_Network = neural_network

async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Set the language for the bot."""
    command = update.message.text.lower().strip('/')
    if command in LANGUAGE_COMMANDS:
        context.user_data['language'] = LANGUAGE_COMMANDS[command]
    language = context.user_data.get('language', 'es')

    user = update.message.from_user
    logger.info(f"Language set to {language} for {user.first_name}")

    if language == 'es':
        await start(update, context)
    elif language == 'en':
        await start_en(update, context)
    elif language == 'fr':
        await start_fr(update, context)
    elif language == 'pt':
        await start_pt(update, context)

    return ConversationHandler.END

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Send a message when the command /inicio is issued."""
    # Log the start command user and message
    user = update.message.from_user
    logger.info("Comando de inicio recibido de %s: %s", user.first_name, update.message.text)

    # Send the welcome message
    await update.message.reply_text(
        '🏡 ¡Hola! Soy el bot de SkyPrice. Envíame un mensaje con los detalles del departamento en la Ciudad de México y te diré el precio estimado. Los detalles deben incluir:\n\n'
        '📏 Tamaño del terreno\n'
        '🏗️ Tamaño de la construcción\n'
        '🛏️ Número de habitaciones\n'
        '🚽 Número de baños\n'
        '🚗 Número de estacionamientos\n'
        '🕰️ Antigüedad\n'
        '🌍 Alcaldía\n\n'
        'El bot utilizará OpenAI para extraer los detalles del texto y la API de SkyPrice para predecir el precio. ¡Inténtalo ahora! 🚀\n\n'
        'Ejemplo: "el departamento tiene 100 m² de terreno, 80 m² de construcción, 2 habitaciones, 1 baño, 1 estacionamiento, 10 años de antigüedad y está en la alcaldía Benito Juárez".\n\n'
        'For English instructions, type /english.\n'
        'Pour des instructions en français, tapez /french.\n'
        'Para instruções em português, digite /portuguese.\n'
    )

    return ConversationHandler.END

async def start_fr(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Send a message when the command /french is issued."""
    # Log the start command user and message
    user = update.message.from_user
    logger.info("Comando de inicio en francés recibido de %s: %s", user.first_name, update.message.text)

    # Send the welcome message
    await update.message.reply_text(
        '🏡 Bonjour! Je suis le bot SkyPrice. Envoyez-moi un message avec les détails de l\'appartement à Mexico et je vous dirai le prix estimé. Les détails doivent inclure:\n\n'
        '📏 Taille du terrain\n'
        '🏗️ Taille de la construction\n'
        '🛏️ Nombre de chambres\n'
        '🚽 Nombre de salles de bains\n'
        '🚗 Nombre de places de parking\n'
        '🕰️ Âge\n'
        '🌍 Municipalité\n\n'
        'Le bot utilisera OpenAI pour extraire les détails du texte et l\'API SkyPrice pour prédire le prix. Essayez maintenant! 🚀\n\n'
        'Exemple: "l\'appartement a 100 m² de terrain, 80 m² de construction, 2 chambres, 1 salle de bain, 1 place de parking, 10 ans et est dans la municipalité de Benito Juárez".\n\n'
        'Para instrucciones en español, escriba /inicio.\n'
        'For English instructions, type /english.\n'
        'Para instruções em português, digite /portuguese.\n'
    )

    return ConversationHandler.END

async def start_pt(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Send a message when the command /portuguese is issued."""
    # Log the start command user and message
    user = update.message.from_user
    logger.info("Comando de inicio en portugués recibido de %s: %s", user.first_name, update.message.text)

    # Send the welcome message
    await update.message.reply_text(
        '🏡 Olá! Eu sou o bot SkyPrice. Envie-me uma mensagem com os detalhes do apartamento na Cidade do México e eu direi o preço estimado. Os detalhes devem incluir:\n\n'
        '📏 Tamanho do terreno\n'
        '🏗️ Tamanho da construção\n'
        '🛏️ Número de quartos\n'
        '🚽 Número de banheiros\n'
        '🚗 Número de vagas de estacionamento\n'
        '🕰️ Idade\n'
        '🌍 Município\n\n'
        'O bot usará o OpenAI para extrair os detalhes do texto e a API SkyPrice para prever o preço. Experimente agora! 🚀\n\n'
        'Exemplo: "o apartamento tem 100 m² de terreno, 80 m² de construção, 2 quartos, 1 banheiro, 1 vaga de estacionamento, 10 anos de idade e está na municipalidade de Benito Juárez".\n\n'
        'Para instrucciones en español, escriba /inicio.\n'
        'Pour des instructions en français, tapez /french.\n'
        'For English instructions, type /english.\n'
    )

    return ConversationHandler.END

async def start_en(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Send a message when the command /english is issued."""
    # Log the start command user and message
    user = update.message.from_user
    logger.info("Comando de inicio en inglés recibido de %s: %s", user.first_name, update.message.text)

    # Send the welcome message
    await update.message.reply_text(
        '🏡 Hello! I am the SkyPrice bot. Send me a message with the details of the apartment in Mexico City and I will tell you the estimated price. The details must include:\n\n'
        '📏 Terrain size\n'
        '🏗️ Construction size\n'
        '🛏️ Number of rooms\n'
        '🚽 Number of bathrooms\n'
        '🚗 Number of parking spaces\n'
        '🕰️ Age\n'
        '🌍 Municipality\n\n'
        'The bot will use OpenAI to extract the details from the text and the SkyPrice API to predict the price. Try it now! 🚀\n\n'
        'Example: "the apartment has 100 m² of terrain, 80 m² of construction, 2 rooms, 1 bathroom, 1 parking space, 10 years old and is in the Benito Juárez municipality".\n\n'
        'Para instrucciones en español, escriba /inicio.\n'
        'Pour des instructions en français, tapez /french.\n'
        'Para instruções em português, digite /portuguese.\n'
    )

    return ConversationHandler.END

def extract_apartment_details(text) -> Union[ApartmentDetails, None]:
    """Extract apartment details from the text using OpenAI's GPT-3."""

    # Log the text to extract apartment details
    logger.info(f"Extracting apartment details from text: {text}")

    # Use OpenAI's GPT-3 to extract apartment details
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "text",
                            "text": "Extract the following CDMX apartment details from the text in JSON format, if impossible to extract, leave null: \n{\"Size_Terrain\":int,\"Size_Construction\":int,\"Rooms\":int,\"Bathrooms\":float,Parking\":int,\"Age\":int,\"Lat\":float, \"Lng\":float,\"Municipality\":str} \nUnits should be in meters for size and years for age. If given the date of construction, calculate age. \nLat and Lng you should provide with the closer coordinates you can find for the apartment \nor fallback to the center of detected Municipality (always provide lat/lng). \nMunicipality should be one of the 16 CDMX municipalities: [\nÁlvaro Obregón', 'Azcapotzalco', 'Benito Juárez', 'Coyoacán', 'Cuajimalpa', 'Cuauhtémoc',\nGustavo A. Madero', 'Iztacalco', 'Iztapalapa', 'Magdalena Contreras', 'Miguel Hidalgo',\nMilpa Alta', 'Tláhuac', 'Tlalpan', 'Venustiano Carranza', 'Xochimilco']\nProvide the response without any formatting or additional line breaks, just the minified JSON ready to serialize.\n"
                        }
                    ]
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": text
                        }
                    ]
                }
            ],
            temperature=0.5,
            max_tokens=600,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        # Log the response from OpenAI
        logger.info(f"Apartment details response: {response.__dict__}")

        # Cast the response to a dictionary
        details_json = response.choices[0].message.content
        details_dict = json.loads(details_json)

        # Log the apartment details dictionary
        logger.info(f"Apartment details dictionary: {details_dict}")

        # Return the apartment details
        return ApartmentDetails(
            size_terrain=details_dict['Size_Terrain'],
            size_construction=details_dict['Size_Construction'],
            rooms=details_dict['Rooms'],
            bathrooms=details_dict['Bathrooms'],
            parking=details_dict['Parking'],
            age=details_dict['Age'],
            lat=details_dict['Lat'],
            lng=details_dict['Lng'],
            municipality=details_dict['Municipality']
        )
    except Exception as e:
        # Log the error extracting apartment details
        logger.info(f"Error extracting apartment details: {e}")
        return None

def predict_price(details: ApartmentDetails) -> PricePrediction:
    """Predict the price of the apartment using the SkyPrice API."""
    response = requests.post(SKYPRICE_API_URL, json=details.__dict__)
    response_json = response.json()
    logger.info(f"Price prediction response: {response_json}")
    return PricePrediction(
        random_forest=response_json['random_forest'],
        svm=response_json['svm'],
        neural_network=response_json['neural_network']
    )

def format_price(price: str) -> str:
    """Format the price to follow $123,456.78 MXN format."""
    return f"${float(price):,.2f} MXN"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle the message from the user."""
    user = update.message.from_user
    logger.info("Valuación de departamento recibida de %s: %s", user.first_name, update.message.text)

    # Obtener el idioma del usuario
    language = context.user_data.get('language', 'es')

    if language == 'es':
        await update.message.reply_text(
            "🏡 SkyPrice ChatBot 🤖\n\n"
            "📝 ¡Gracias! Mensaje recibido. 📩\n\n"
            "🔄 Procesando tu solicitud..."
        )
    elif language == 'en':
        await update.message.reply_text(
            "🏡 SkyPrice ChatBot 🤖\n\n"
            "📝 Thank you! Message received. 📩\n\n"
            "🔄 Processing your request..."
        )
    elif language == 'fr':
        await update.message.reply_text(
            "🏡 SkyPrice ChatBot 🤖\n\n"
            "📝 Merci! Message reçu. 📩\n\n"
            "🔄 Traitement de votre demande..."
        )
    elif language == 'pt':
        await update.message.reply_text(
            "🏡 SkyPrice ChatBot 🤖\n\n"
            "📝 Obrigado! Mensagem recebida. 📩\n\n"
            "🔄 Processando sua solicitação..."
        )

    try:
        # Extrae los detalles del departamento del mensaje del usuario
        user_text = update.message.text
        details_text= extract_apartment_details(user_text)

        # Valida si se pudieron extraer los detalles del departamento
        if not details_text:
            logger.info("No se pudieron extraer los detalles del departamento del mensaje del usuario %s: %s", user.first_name, user_text)

            if language == 'es':
                await update.message.reply_text('❌ Lo siento, no pude extraer los detalles del departamento de tu mensaje. Por favor, inténtalo de nuevo. Si necesitas ayuda, escribe /inicio.')
            elif language == 'en':
                await update.message.reply_text('❌ Sorry, I could not extract the apartment details from your message. Please try again. If you need help, type /english.')
            elif language == 'fr':
                await update.message.reply_text('❌ Désolé, je n\'ai pas pu extraire les détails de l\'appartement de votre message. Veuillez réessayer. Si vous avez besoin d\'aide, tapez /french.')
            elif language == 'pt':
                await update.message.reply_text('❌ Desculpe, não consegui extrair os detalhes do apartamento da sua mensagem. Por favor, tente novamente. Se precisar de ajuda, digite /portuguese.')

            return ConversationHandler.END

        # Convierte los detalles del departamento a un diccionario
        details_dict = details_text.__dict__

        # Validate that all required keys are present and not None, if not, provide the user with feedback on missing keys.
        required_keys = ['Size_Terrain', 'Size_Construction', 'Rooms', 'Bathrooms', 'Parking', 'Age', 'Lat', 'Lng', 'Municipality']
        missing_keys = [key for key in required_keys if key not in details_dict or details_dict[key] is None]
        if missing_keys:
            logger.info("Missing keys: %s", missing_keys)
            required_keys_es = {'Size_Terrain': 'Tamaño del terreno', 'Size_Construction': 'Tamaño de la construcción', 'Rooms': 'Habitaciones', 'Bathrooms': 'Baños', 'Parking': 'Estacionamientos', 'Age': 'Antigüedad', 'Lat': 'Latitud', 'Lng': 'Longitud', 'Municipality': 'Alcaldía'}
            required_keys_fr = {'Size_Terrain': 'Taille du terrain', 'Size_Construction': 'Taille de la construction', 'Rooms': 'Chambres', 'Bathrooms': 'Salles de bains', 'Parking': 'Places de parking', 'Age': 'Âge', 'Lat': 'Latitude', 'Lng': 'Longitude', 'Municipality': 'Municipalité'}
            required_keys_pt = {'Size_Terrain': 'Tamanho do terreno', 'Size_Construction': 'Tamanho da construção', 'Rooms': 'Quartos', 'Bathrooms': 'Banheiros', 'Parking': 'Vagas de estacionamento', 'Age': 'Idade', 'Lat': 'Latitude', 'Lng': 'Longitude', 'Municipality': 'Município'}
            if language == 'es':
                missing_keys = [required_keys_es[key] for key in missing_keys]
            elif language == 'fr':
                missing_keys = [required_keys_fr[key] for key in missing_keys]
            elif language == 'pt':
                missing_keys = [required_keys_pt[key] for key in missing_keys]

            if language == 'es':
                await update.message.reply_text(f'❌ Lo siento, no pude extraer los siguientes detalles del departamento de tu mensaje: {", ".join(missing_keys)}. Por favor, inténtalo de nuevo. Si necesitas ayuda, escribe /inicio.')
            elif language == 'en':
                await update.message.reply_text(f'❌ Sorry, I could not extract the following apartment details from your message: {", ".join(missing_keys)}. Please try again. If you need help, type /english.')
            elif language == 'fr':
                await update.message.reply_text(f'❌ Désolé, je n\'ai pas pu extraire les détails de l\'appartement suivants de votre message: {", ".join(missing_keys)}. Veuillez réessayer. Si vous avez besoin d\'aide, tapez /french.')
            elif language == 'pt':
                await update.message.reply_text(f'❌ Desculpe, não consegui extrair os seguintes detalhes do apartamento da sua mensagem: {", ".join(missing_keys)}. Por favor, tente novamente. Se precisar de ajuda, digite /portuguese.')

            return ConversationHandler.END

        # Validate that municipality is valid, if not, provide the user with feedback on invalid municipality.
        valid_municipalities = ['Álvaro Obregón', 'Azcapotzalco', 'Benito Juárez', 'Coyoacán', 'Cuajimalpa de Morelos', 'Cuauhtémoc',
                  'Gustavo A. Madero', 'Iztacalco', 'Iztapalapa', 'Magdalena Contreras', 'Miguel Hidalgo',
                  'Milpa Alta', 'Tláhuac', 'Tlalpan', 'Venustiano Carranza', 'Xochimilco']
        if details_dict['Municipality'] not in valid_municipalities:
            logger.info("Municipality is invalid")

            if language == 'es':
                await update.message.reply_text(f'❌ Lo siento, la alcaldía proporcionada ({details_dict["Municipality"]}) no es válida. Por favor, inténtalo de nuevo. Si necesitas ayuda, escribe /inicio.')
            elif language == 'en':
                await update.message.reply_text(f'❌ Sorry, the provided municipality ({details_dict["Municipality"]}) is invalid. Please try again. If you need help, type /english.')
            elif language == 'fr':
                await update.message.reply_text(f'❌ Désolé, la municipalité fournie ({details_dict["Municipality"]}) est invalide. Veuillez réessayer. Si vous avez besoin d\'aide, tapez /french.')
            elif language == 'pt':
                await update.message.reply_text(f'❌ Desculpe, a municipalidade fornecida ({details_dict["Municipality"]}) é inválida. Por favor, tente novamente. Se precisar de ajuda, digite /portuguese.')

            return ConversationHandler.END

        # Validate that numeric values are numeric and positive or zero, if not, provide the user with feedback on offending fields.
        numeric_fields = ['Size_Terrain', 'Size_Construction', 'Rooms', 'Bathrooms', 'Parking', 'Age']
        invalid_fields = [field for field in numeric_fields if not isinstance(details_dict[field], (int, float)) or details_dict[field] < 0]
        if invalid_fields:
            logger.info("Invalid fields: %s", invalid_fields)
            invalid_fields_es = {'Size_Terrain': 'Tamaño del terreno', 'Size_Construction': 'Tamaño de la construcción', 'Rooms': 'Habitaciones', 'Bathrooms': 'Baños', 'Parking': 'Estacionamientos', 'Age': 'Antigüedad'}
            invalid_fields_en = {'Size_Terrain': 'Terrain size', 'Size_Construction': 'Construction size', 'Rooms': 'Rooms', 'Bathrooms': 'Bathrooms', 'Parking': 'Parking spaces', 'Age': 'Age'}
            invalid_fields_fr = {'Size_Terrain': 'Taille du terrain', 'Size_Construction': 'Taille de la construction', 'Rooms': 'Chambres', 'Bathrooms': 'Salles de bains', 'Parking': 'Places de parking', 'Age': 'Âge'}
            invalid_fields_pt = {'Size_Terrain': 'Tamanho do terreno', 'Size_Construction': 'Tamanho da construção', 'Rooms': 'Quartos', 'Bathrooms': 'Banheiros', 'Parking': 'Vagas de estacionamento', 'Age': 'Idade'}
            if language == 'es':
                invalid_fields = [invalid_fields_es[field] for field in invalid_fields]
            elif language == 'en':
                invalid_fields = [invalid_fields_en[field] for field in invalid_fields]
            elif language == 'fr':
                invalid_fields = [invalid_fields_fr[field] for field in invalid_fields]
            elif language == 'pt':
                invalid_fields = [invalid_fields_pt[field] for field in invalid_fields]

            invalid_fields = [invalid_fields_es[field] for field in invalid_fields]

            if language == 'es':
                await update.message.reply_text(f'❌ Lo siento, los siguientes campos numéricos no son válidos: {", ".join(invalid_fields)}. Por favor, inténtalo de nuevo. Si necesitas ayuda, escribe /inicio.')
            elif language == 'en':
                await update.message.reply_text(f'❌ Sorry, the following numeric fields are not valid: {", ".join(invalid_fields)}. Please try again. If you need help, type /english.')
            elif language == 'fr':
                await update.message.reply_text(f'❌ Désolé, les champs numériques suivants ne sont pas valides: {", ".join(invalid_fields)}. Veuillez réessayer. Si vous avez besoin d\'aide, tapez /french.')
            elif language == 'pt':
                await update.message.reply_text(f'❌ Desculpe, os seguintes campos numéricos não são válidos: {", ".join(invalid_fields)}. Por favor, tente novamente. Se precisar de ajuda, digite /portuguese.')

            return ConversationHandler.END


        # Validate that numeric values are within the expected range, if not, provide the user with feedback on offending fields.
        size_limits = {'Size_Terrain': 10000, 'Size_Construction': 10000, 'Rooms': 20, 'Bathrooms': 20, 'Parking': 20, 'Age': 100}
        invalid_fields = [field for field in numeric_fields if details_dict[field] > size_limits[field]]
        if invalid_fields:
            logger.info("Invalid fields: %s", invalid_fields)
            invalid_fields_es = {'Size_Terrain': 'Tamaño del terreno', 'Size_Construction': 'Tamaño de la construcción', 'Rooms': 'Habitaciones', 'Bathrooms': 'Baños', 'Parking': 'Estacionamientos', 'Age': 'Antigüedad'}
            invalid_fields_en = {'Size_Terrain': 'Terrain size', 'Size_Construction': 'Construction size', 'Rooms': 'Rooms', 'Bathrooms': 'Bathrooms', 'Parking': 'Parking spaces', 'Age': 'Age'}
            invalid_fields_fr = {'Size_Terrain': 'Taille du terrain', 'Size_Construction': 'Taille de la construction', 'Rooms': 'Chambres', 'Bathrooms': 'Salles de bains', 'Parking': 'Places de parking', 'Age': 'Âge'}
            invalid_fields_pt = {'Size_Terrain': 'Tamanho do terreno', 'Size_Construction': 'Tamanho da construção', 'Rooms': 'Quartos', 'Bathrooms': 'Banheiros', 'Parking': 'Vagas de estacionamento', 'Age': 'Idade'}
            if language == 'es':
                invalid_fields = [invalid_fields_es[field] for field in invalid_fields]
            elif language == 'en':
                invalid_fields = [invalid_fields_en[field] for field in invalid_fields]
            elif language == 'fr':
                invalid_fields = [invalid_fields_fr[field] for field in invalid_fields]
            elif language == 'pt':
                invalid_fields = [invalid_fields_pt[field] for field in invalid_fields]

            if language == 'es':
                await update.message.reply_text(f'❌ Lo siento, los siguientes campos numéricos exceden los límites esperados: {", ".join(invalid_fields)}. Por favor, inténtalo de nuevo. Si necesitas ayuda, escribe /inicio.')
            elif language == 'en':
                await update.message.reply_text(f'❌ Sorry, the following numeric fields exceed the expected limits: {", ".join(invalid_fields)}. Please try again. If you need help, type /english.')
            elif language == 'fr':
                await update.message.reply_text(f'❌ Désolé, les champs numériques suivants dépassent les limites attendues: {", ".join(invalid_fields)}. Veuillez réessayer. Si vous avez besoin d\'aide, tapez /french.')
            elif language == 'pt':
                await update.message.reply_text(f'❌ Desculpe, os seguintes campos numéricos excedem os limites esperados: {", ".join(invalid_fields)}. Por favor, tente novamente. Se precisar de ajuda, digite /portuguese.')

            return ConversationHandler.END


        # Envía un mensaje con los detalles del departamento
        if language == 'es':
            await update.message.reply_text(
                f"🏢 Detalles del departamento extraídos:\n\n"
                f"📏 Tamaño del terreno: {details_text.Size_Terrain}m²\n"
                f"🏗️ Tamaño de la construcción: {details_text.Size_Construction}m²\n"
                f"🛏️ Número de habitaciones: {details_text.Rooms}\n"
                f"🚽 Número de baños: {details_text.Bathrooms}\n"
                f"🚗 Número de estacionamientos: {details_text.Parking}\n"
                f"🕰️ Antigüedad: {details_text.Age} años\n"
                f"🌍 Alcaldía: {details_text.Municipality}"
            )
        elif language == 'en':
            await update.message.reply_text(
                f"🏢 Extracted apartment details:\n\n"
                f"📏 Terrain size: {details_text.Size_Terrain}m²\n"
                f"🏗️ Construction size: {details_text.Size_Construction}m²\n"
                f"🛏️ Number of rooms: {details_text.Rooms}\n"
                f"🚽 Number of bathrooms: {details_text.Bathrooms}\n"
                f"🚗 Number of parking spaces: {details_text.Parking}\n"
                f"🕰️ Age: {details_text.Age} years\n"
                f"🌍 Municipality: {details_text.Municipality}"
            )
        elif language == 'fr':
            await update.message.reply_text(
                f"🏢 Détails de l'appartement extraits:\n\n"
                f"📏 Taille du terrain: {details_text.Size_Terrain}m²\n"
                f"🏗️ Taille de la construction: {details_text.Size_Construction}m²\n"
                f"🛏️ Nombre de chambres: {details_text.Rooms}\n"
                f"🚽 Nombre de salles de bains: {details_text.Bathrooms}\n"
                f"🚗 Nombre de places de parking: {details_text.Parking}\n"
                f"🕰️ Âge: {details_text.Age} ans\n"
                f"🌍 Municipalité: {details_text.Municipality}"
            )
        elif language == 'pt':
            await update.message.reply_text(
                f"🏢 Detalhes do apartamento extraídos:\n\n"
                f"📏 Tamanho do terreno: {details_text.Size_Terrain}m²\n"
                f"🏗️ Tamanho da construção: {details_text.Size_Construction}m²\n"
                f"🛏️ Número de quartos: {details_text.Rooms}\n"
                f"🚽 Número de banheiros: {details_text.Bathrooms}\n"
                f"🚗 Número de vagas de estacionamento: {details_text.Parking}\n"
                f"🕰️ Idade: {details_text.Age} anos\n"
                f"🌍 Município: {details_text.Municipality}"
            )


        logger.info("Detalles del departamento extraídos: Tamaño del terreno: %s, Tamaño de la construcción: %s, Habitaciones: %s, Baños: %s, Estacionamientos: %s, Antigüedad: %s, Alcaldía: %s", details_text.Size_Terrain, details_text.Size_Construction, details_text.Rooms, details_text.Bathrooms, details_text.Parking, details_text.Age, details_text.Municipality)

        # Envía un mensaje con los precios estimados
        price_prediction = predict_price(details_text)

        response_message = (
            f"💰 Precios estimados:\n\n"
            f"🌳 Random Forest: {format_price(price_prediction.Random_Forest)}\n"
            f"📈 SVM: {format_price(price_prediction.SVM)}\n"
            f"🧠 Neural Network: {format_price(price_prediction.Neural_Network)}\n\n"
            "🔍 Puedes encontrar más detalles en https://skyprice.xyz 🏡"
        )
        if language == 'en':
            response_message = (
                f"💰 Estimated prices:\n\n"
                f"🌳 Random Forest: {format_price(price_prediction.Random_Forest)}\n"
                f"📈 SVM: {format_price(price_prediction.SVM)}\n"
                f"🧠 Neural Network: {format_price(price_prediction.Neural_Network)}\n\n"
                "🔍 You can find more details at https://skyprice.xyz 🏡"
            )
        elif language == 'fr':
            response_message = (
                f"💰 Prix estimés:\n\n"
                f"🌳 Random Forest: {format_price(price_prediction.Random_Forest)}\n"
                f"📈 SVM: {format_price(price_prediction.SVM)}\n"
                f"🧠 Neural Network: {format_price(price_prediction.Neural_Network)}\n\n"
                "🔍 Vous pouvez trouver plus de détails sur https://skyprice.xyz 🏡"
            )
        elif language == 'pt':
            response_message = (
                f"💰 Preços estimados:\n\n"
                f"🌳 Random Forest: {format_price(price_prediction.Random_Forest)}\n"
                f"📈 SVM: {format_price(price_prediction.SVM)}\n"
                f"🧠 Neural Network: {format_price(price_prediction.Neural_Network)}\n\n"
                "🔍 Você pode encontrar mais detalhes em https://skyprice.xyz 🏡"
            )

        await update.message.reply_text(response_message)
        logger.info("Estimación de precios: SVM: %s, Random Forest: %s, Neural Network: %s", price_prediction.SVM, price_prediction.Random_Forest, price_prediction.Neural_Network)
    except Exception as e:
        logger.info(f"Error: {e}")
        if language == 'es':
            await update.message.reply_text('❌ Lo siento, ha ocurrido un error. Por favor, inténtalo de nuevo. Si necesitas ayuda, escribe /inicio.')
        elif language == 'en':
            await update.message.reply_text('❌ Sorry, an error occurred. Please try again. If you need help, type /english.')
        elif language == 'fr':
            await update.message.reply_text('❌ Désolé, une erreur s\'est produite. Veuillez réessayer. Si vous avez besoin d\'aide, tapez /french.')
        elif language == 'pt':
            await update.message.reply_text('❌ Desculpe, ocorreu um erro. Por favor, tente novamente. Se precisar de ajuda, digite /portuguese.')

    return ConversationHandler.END

def main() -> None:
    # Log de inicio
    logger.info("Iniciando el bot de Telegram de SkyPrice...")

    # Inicializa la aplicación de Telegram
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Handle para las instrucciones en otros idiomas
    for command in LANGUAGE_COMMANDS:
        application.add_handler(CommandHandler(command, set_language))

    # Handle para los mensajes de valuación de departamentos
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Inicia el bot de Telegram
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
