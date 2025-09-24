from flask import Flask, request, jsonify
import os

from vertexai.language_models import TextEmbeddingModel
import vertexai
from supabase import create_client, Client

app = Flask(__name__)
GOOGLE_PROJECT_ID = os.getenv("GOOGLE_PROJECT_ID", "cogent-cocoa-465809-b3")
GOOGLE_LOCATION = os.getenv("GOOGLE_LOCATION", "us-central1")
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://jjqkeeykvtcqjohikbtg.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImpqcWtlZXlrdnRjcWpvaGlrYnRnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTg2MTY3MDEsImV4cCI6MjA3NDE5MjcwMX0.QUzxAIwvrSF9oIz3WGtAFIuBj5iD6aF4PbekiuNYUTE")


import os

google_creds_json = os.getenv("GOOGLE_CREDS_JSON")
if google_creds_json:
    with open("/tmp/cred.json", "w") as f:
        f.write(google_creds_json)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/tmp/cred.json"



vertexai.init(project=GOOGLE_PROJECT_ID, location=GOOGLE_LOCATION)
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route("/search", methods=["POST"])
def search():
    content = request.json
    query = content.get("query")
    embedding_model = TextEmbeddingModel.from_pretrained("text-multilingual-embedding-002")
    query_embedding = embedding_model.get_embeddings([query])[0].values

    response = supabase.rpc(
        'closest_video_segment',
        {'query_embedding': query_embedding}
    ).execute()

    if response.data:
        return jsonify(response.data[0])
    return jsonify({"result": "No match found"})

@app.route("/")
def home():
    return "VertexAI + Supabase API running on Vercel!"
