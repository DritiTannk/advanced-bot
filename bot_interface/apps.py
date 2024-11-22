from django.apps import AppConfig
from django.conf import settings

import spacy
from pinecone import Pinecone


class BotInterfaceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bot_interface'

    global PC, PC_INDEX, NLP

    PC = Pinecone(api_key=settings.PINE_API_KEY)
    PC_INDEX = PC.Index("bot-memory")
    NLP = spacy.load("en_core_web_sm")
