from django.core.management.base import BaseCommand
from bot_interface.utils import query_vdb, get_text_embedding, index


class Command(BaseCommand):
    help = "Load intents into Pinecone"

    def handle(self, *args, **kwargs):
        intents = [
            {"intent": "greet", "examples": ["hi", "hello", "hey"], "response": "Welcome! How can I assist you?"},
            {"intent": "introduce", "examples": ["i am {name}", "my name is {name}"], "response": "Welcome, {name}!"},
            {"intent": "favourites", "examples": ["{item} is my favourite {intent}",
                                                  "remember that {item} are my favourite {intent}",
                                                  "note that my favourite {intent} are {item} {item}",
                                                  "i like {item} in {intent} very much"],
             "response": "Noted! I'll remember that {item} is your favorite.", "type": "fact"},
            {"intent": "ask_favorite", "examples": ["what is my favourite {intent}?",
                                                    "do you know my favourite {intent}?",
                                                    "do i like {item}?",
                                                    "tell me that what is my favorite {intent}?",
                                                    "what do i like in {intent}?"],
             "response": "Your favourite {intent} items/are {item}.", "type": "query"},
            {"intent": "dislikes", "examples": ["i don't like {item}", "i dislikes {item}",
                                                "i hate {item} very much", "i hate {item}"
                                                ],
                                    "response": "I Know, you don't like {item}."},
            {"intent": "care", "examples": ["how are you ?", "how you doing ?", "What's up ?"],
                               "response": "I am doing great !! Tell me how can i help you ?"},

        ]

        # Add intents to Pinecone
        index.delete(delete_all=True)
        for intent in intents:
            for example in intent["examples"]:
                embedding = get_text_embedding(example)
                metadata = {"intent": intent["intent"], "response": intent["response"], "type": intent.get('type', "")}
                index.upsert([(example, embedding, metadata)])

        self.stdout.write(self.style.SUCCESS("Intents loaded successfully!"))
