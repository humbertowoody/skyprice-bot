#!/bin/bash
# Script para construir la imgen de Docker del Chatbot de SkyPrice
# de forma local con la arquitectura de AMD64.
# Humberto Alcocer 2024.

# Construir la imagen de Docker con la arquitectura de AMD64 y ARM64.
docker buildx build --platform linux/amd64 -t skyprice-chatbot:latest .

# Exportar la imagen de Docker a un archivo tar.
docker save skyprice-chatbot:latest -o skyprice-chatbot.tar

