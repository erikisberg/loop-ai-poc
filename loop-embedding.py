from dotenv import load_dotenv
import os
import openai
import json
from pinecone import Pinecone, ServerlessSpec  # Import ServerlessSpec from Pinecone

# Load environment variables from .env file
load_dotenv()

# Load OpenAI API key
openai.api_key = os.environ["OPENAI_API_KEY"]

# Initialize Pinecone client
pinecone_api_key = os.environ["PINECONE_API_KEY"]
pinecone_env = os.environ["PINECONE_ENV"]
pinecone_index_name = "impactloop-index"  # Using lowercase alphanumeric characters and hyphens

pinecone_client = Pinecone(api_key=pinecone_api_key)

# Create the index
pinecone_client.create_index(
    name=pinecone_index_name,
    dimension=1536,
    metric='euclidean',
    spec=ServerlessSpec(cloud='aws', region='us-west-2')  # Corrected reference to ServerlessSpec
)

# Load the scraped data from the JSON file
with open('documents/github/loop-ai-poc/loop-ai-poc/scraped_data/impactloop_data.json', 'r', encoding='utf-8') as file:
    scraped_data = json.load(file)

embeddings_and_urls = []

for item in scraped_data:
    content = item['content']
    url = item['url']

    # Generate embeddings using OpenAI API
    response = openai.Embedding.create(input=content, engine="text-embedding-ada-002")
    embedding = response["data"][0]["embedding"]

    # Store the embeddings and URLs
    embeddings_and_urls.append((embedding, {"url": url}))

# Upsert embeddings and metadata to Pinecone
pinecone_client.upsert(embeddings_and_urls, index_name=pinecone_index_name)
