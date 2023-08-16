from sentence_transformers import SentenceTransformer, util
import torch
import numpy as np

from sql import get_article, get_index_articles


device = torch.device("cpu")
    
model = SentenceTransformer('all-mpnet-base-v2').to(device)
embeddings = torch.load('embeddings/embeddings.pt', map_location=device)


def query(sentence, initial_year, final_year, n=5):
    # embedding the query
    query_embedding = model.encode(sentence, convert_to_tensor=True)

    # mask index
    mask_indices = np.hstack(get_index_articles(initial_year, final_year))
    
    # Use mask to select only relevant embeddings
    masked_embeddings = embeddings[mask_indices]
    
    # Calculate cosine similarity with only the masked embeddings
    cos_scores = util.pytorch_cos_sim(query_embedding, masked_embeddings)[0]
    top_results = torch.topk(cos_scores, k=n)

    results = []
    for score, relative_idx in zip(top_results[0].cpu().numpy(), top_results[1].cpu().numpy()):
        # Map the relative index back to the original embeddings' index
        original_idx = mask_indices[relative_idx]
        
        article = get_article(original_idx)
        results.append((article, score))
    
    return results
