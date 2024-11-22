# Advanced Chatbot
_This Project Demonstrates The Advanced Chatbot Feature Using VectorDb-Pinecone and Django_


### Backend

Python 3.11
Django==5.1.3
Spacy 3.8.2
pinecone==5.4.0
database - sqlite


### Project Set-Up
1. Clone the repository

   ```git clone url ```

2. Create Virtual environment

   ``` virtualenv env```

3. Install Dependencies

#### kindly make sure your virtual environment is active.

``` pip install -r requirements.tx  ```

4. Create & Run Migrations

```python manage.py makemigrations```
```python manage.py migrate ```

5. Create Database Admin User (Superuser)

```python manage.py createsuperuser```

6. Run Project

```python manage.py runserver```
```http://localhost:8000/```

#### Admin Panel
```http://localhost:8000/admin/```

### Embedding Generating & Upserting.

- To generate & push the embedded data to the pinecone vectordb, run the following command.

``` python manage.py feed_data```

> - Make sure virtual enviornment is running.
> - This will generate the embedded  data and will push it in the pinecone db.

# Thank you
