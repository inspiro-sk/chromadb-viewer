from sklearn.decomposition import PCA
import plotly.express as px
import numpy as np

def draw(data):
    embeddings = np.array(data["embeddings"]).tolist()
    metadata = data["metadatas"]
    documents = data["documents"]
    ids = data["ids"]
    # Reduce the embedding dimensionality
    pca = PCA(n_components=3)
    vis_dims = pca.fit_transform(embeddings)# Create an interactive 3D plot
    fig = px.scatter_3d(
        x=vis_dims[:, 0],
        y=vis_dims[:, 1],
        z=vis_dims[:, 2],
        text=documents,
        labels={'x': 'PCA Component 1', 'y': 'PCA Component 2', 'z': 'PCA Component 3'}, # Name it like you want
        title='3D PCA of Embeddings' # Name it like you want
    )

    return fig