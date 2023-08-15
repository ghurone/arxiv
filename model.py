from sql import get_article

from sentence_transformers import SentenceTransformer, util
import pandas as pd
import torch

device = torch.device("cpu")
    
model = SentenceTransformer('all-mpnet-base-v2').to(device)
embeddings = torch.load('embeddings/embeddings.pt', map_location=device)


def query(sentence, n = 5):
    query_embedding = model.encode(sentence, convert_to_tensor=True)

    # Calculate cosine similarity and top results as before
    cos_scores = util.pytorch_cos_sim(query_embedding, embeddings)[0]
    top_results = torch.topk(cos_scores, k=n)

    results = []
    for score, idx in zip(top_results[0].cpu().numpy(), top_results[1].cpu().numpy()):
        article = get_article(idx)
        results.append((article, score))
    
    return results