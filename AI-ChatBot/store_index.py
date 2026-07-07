from src.helper import text_split,download_hugging_face_embeddings,load_pdf_file
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv
import os

load_dotenv()
PINECONE_API_KEY=os.environ.get('PINECONE_API_KEY')
os.environ["PINECONE_API_KEY"]=PINECONE_API_KEY


extracted_data = load_pdf_file(data = 'Data/')
text_chunks = text_split(extracted_data)
embeddings= download_hugging_face_embeddings()

from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
import os


from dotenv import load_dotenv
load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

pc = Pinecone(api_key=PINECONE_API_KEY)

index_name = "medicalbot"


if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=384,
        metric='cosine',
        spec=ServerlessSpec(
            cloud='aws',
            region='us-east-1'
        )
    )
    print(f"Index '{index_name}' created.")
else:
    print(f"Index '{index_name}' already exists.")



