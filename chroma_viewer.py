import chromadb
from chromadb import EmbeddingFunction, Documents, Embeddings
import pandas as pd 
import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import numpy as np
import argparse
import visualize_embed

load_dotenv()

parser = argparse.ArgumentParser(description="Set chromadb host and port or use local instance")
parser.add_argument("db", type=str, help="Type of chroma database to connect to. Options: local (PersistenClient), remote (HttpClient). Default is local.")
parser.add_argument("--host", type=str, help="Host of the chroma database. Default is localhost.", default="localhost")
parser.add_argument("--port", type=int, help="Port of the chroma database. Default is 8000.", default=8000)

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

pd.set_option('display.max_columns', 4)

class GeminiEmbeddingFunction(EmbeddingFunction):
  def __call__(self, input: Documents) -> Embeddings:
    model = 'models/text-embedding-004'
    title = "Custom query"
    return genai.embed_content(model=model,
                                content=input,
                                task_type="retrieval_document",
                                title=title)["embedding"]
  

def client_type(db, host='localhost', port=8000):
    if db == 'local':
        return chromadb.PersistentClient()
    elif db == 'remote':
        return chromadb.HttpClient(host, port)
    else:
        return chromadb.PersistentClient()
    

def view_collections(db):
    # st.markdown("### DB Path: %s" % dir)
    client = client_type(db)

    st.header("Collections")

    for collection in client.list_collections():
        collection = client.get_collection(name=collection, embedding_function=GeminiEmbeddingFunction())
        data = collection.get(
           include=["embeddings", "metadatas", "documents"]
        )

        embeddings = np.array(data["embeddings"]).tolist()
        metadata = data["metadatas"]
        documents = data["documents"]
        ids = data["ids"]

        with st.sidebar:
            st.markdown("## Options")
            add_radio = st.radio(
                label="Include visualization of embeddings",
                options=("Yes (experimental)", "No (faster)"),
                index=1
            )

        # df = pd.DataFrame([[ids, documents, metadata, embeddings[0]]], columns=["id", "documents", "metadata", "embeddings"])
        df = pd.DataFrame.from_dict({'id': ids, 'documents': documents, 'metadata': metadata, 'embeddings': embeddings})
        st.markdown("### Collection: **%s**" % collection.name)
        st.dataframe(df)

        if add_radio == "Yes (experimental)":
            st.markdown("### Visualize Embeddings")
            fig = visualize_embed.draw(data)
            st.plotly_chart(fig)


if __name__ == "__main__":
    try:
        args = parser.parse_args()
        view_collections(args.db)
    except:
        pass