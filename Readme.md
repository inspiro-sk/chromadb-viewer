# ChromaDB viewer

A simple and easy to use viewer for ChromaDB if you want to better understand how your emebddings are stored.
You can also use simple visualization to 'see' the embeddings space (highly experimental, off by default).

## How to get started

First you will need to install the dependencies with the following command:

```pip install -r requirements.txt```

## Running the viewer

Make sure your ChromaDB instance is running. I recommend using docker container.
You can simply run chroma using the following:

```docker run -d --rm --name chromadb -p 8000:8000 -v ./chroma:/chroma/chroma -e IS_PERSISTENT=TRUE -e ANONYMIZED_TELEMETRY=FALSE chromadb/chroma:0.6.3```

Run the script with the following command:

```streamlit run .\chroma_viewer.py remote -- --host=localhost --port=8000```

For local instance of ChromaDB you can use:

```streamlit run .\chroma_viewer.py local```