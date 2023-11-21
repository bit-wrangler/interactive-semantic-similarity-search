import numpy as np
import pickle
import gzip
import faiss
import time

from shared.data import SimilarityService

similarity_service = SimilarityService.get_instance()

doc_id = list(similarity_service.app_data.docs.keys())[0]

print(doc_id)

start = time.time()
print('fetching results...')
results = similarity_service.find_similar_document_ids(doc_id, k_nearest=10000)
print(f'fetched results in {time.time() - start : .2f} seconds')

print(results[:10])

top_neighbor_doc = similarity_service.compare_document_sentences(doc_id, results[0][0])

from pprint import pprint

pprint(top_neighbor_doc.to_dict())

text_query = 'fraudulent fees'

results = similarity_service.find_similar_documents_by_text_query(text_query, k_nearest=1000)

print(results[:10])

top_query_doc = similarity_service.app_data.docs[results[0][0]].copy()

pprint(top_query_doc.to_dict())