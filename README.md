# SkyPrice - Telegram Bot

Este repositorio contieen el código fuente del bot de Telegram SkyPrice, el cual
permite estimar el precio de departamentos en la Ciudad de México mediante el uso
de la API de OpenAI para el modelo GPT-3 que permite extraer información del
inmueble a partir de un mensaje escrito por el usuario en lenguaje natural y,
posteriormente, se utiliza la API pública de SkyPrice para realizar la estimación
de precio.

## Requerimientos

Para poder ejecutar el bot de Telegram es necesario contar con las siguientes
herramientas y librerías:

- Python 3.12
- Pip
- Pipenv
- Token de la API de Telegram
- Token de la API de OpenAI

## Instalación

Para instalar las dependencias del proyecto es necesario ejecutar el siguiente
comando:

```bash
pipenv install
```

## Configuración

Para configurar el bot de Telegram es necesario crear un archivo `.env` en la
raíz del proyecto con las siguientes variables de entorno:

```bash
TELEGRAM_BOT_TOKEN=<TOKEN>
OPENAI_API_KEY=<TOKEN>
```

## Ejecución

Para ejecutar el bot de Telegram es necesario ejecutar el siguiente comando:

```bash
pipenv run python skyprice_bot.py
```

## Uso

Para utilizar el bot de Telegram es necesario buscar el bot en la aplicación de
Telegram con el nombre `@SkyPriceChatBot` y enviar un mensaje con la descripción del
departamento que se desea estimar. El bot responderá con el precio estimado del
departamento.

## Autor

- Humberto Alejandro Ortega Alcocer.
