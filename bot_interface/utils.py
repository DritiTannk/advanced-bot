import spacy
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
from .apps import *

# Initialize Pinecone
# pc = Pinecone(api_key="pcsk_7PwAji_UWqHS2hdrFownsaCjFZftoPCAQoHxqpNRFo9akDqJU8k1DjeyYFvfk4xaqLqpY2")
# index = pc.Index("bot-memory")
# nlp = spacy.load("en_core_web_sm")

pc = PC
index = PC_INDEX
nlp = NLP


model = SentenceTransformer("all-MiniLM-L6-v2")


def get_text_embedding(text):
    """Generate embedding for a given text."""
    return model.encode(text).tolist()


def query_vdb(query, top_k=6):
    """send query to pinecone for the most similar intent."""
    query_embedding = model.encode([query.lower().strip()]).tolist()[0]
    results = index.query(vector=query_embedding, top_k=top_k,
                          include_metadata=True,
                          score_threshold=0.75)
    return results


def detect_fav_intent(text):
    """
    This method detects intent for the favourite items from the user text.
    """
    fav_keywords = {
        'food': ['favourite food', 'my favorite food?', "food",
                 ],
        'technology': ['favourite technology',
                       "my techstack", "technology"],
    }

    for key in fav_keywords.keys():
        for item in fav_keywords[key]:
            if item in text.lower().strip():
                return key

    return None


def favourites_extraction(text):
    food_tokens = ["pizza", "burger", "sushi",
                     "pasta", "salad", "pavbhaji",
                     "vadapav", "dosa", "idli"]
    tech_tokens = ["python", "reactjs", "vue.js",
                   "ml", "machine learning", "ai",
                   "artifical intelligence", "django",
                   "rest framework", "rest apis", "spacy",
                   "ios", "android", "flutter"
                   ]

    doc = nlp(text)
    food_values = [token.text.lower() for token in doc if token.text.lower() in food_tokens]
    tech_values = [token.text.lower() for token in doc if token.text.lower() in tech_tokens]
    city_values = [token.text.lower() for token in doc if token.text.lower() in city_tokens]
    design_values = [token.text.lower() for token in doc if token.text.lower() in design_tokens]

    fav_meta_data = {
        "food": food_values,
        "technology": tech_values,
        "city": city_values,
        "designation": design_values
    }
    return fav_meta_data

