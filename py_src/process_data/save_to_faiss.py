from itertools import groupby
import numpy as np
import pickle
import gzip
import faiss
import time

from ..shared.data import faiss_index_path, docs_flat_path, faiss_index_to_docs_flat_path, faiss_sentence_embeddings_path
from .generate_data_collections import docs_pickle_path, sentence_embeddings_pickle_path

with gzip.open(docs_pickle_path, 'rb') as f:
    docs = pickle.load(f)

with gzip.open(sentence_embeddings_pickle_path, 'rb') as f:
    sentence_embeddings = pickle.load(f)

doc_keys = list(docs.keys())

# faiss_index = faiss.IndexHNSWSQ(384, faiss.ScalarQuantizer.QT_8bit, 32, faiss.METRIC_INNER_PRODUCT)
faiss_index = faiss.IndexFlatIP(384)

docs_flat = {}
faiss_index_to_docs_flat = {}
faiss_sentence_embeddings = {}
index_sentence_id = 0

all_embeddings = []


# print(docs[doc_keys[0]])

start = time.time()
for index, doc_id in enumerate(doc_keys):
    docs_flat[doc_id] = {
        'id':doc_id,
        'sentences':[]
    }
    
    for p_idx, sentences in enumerate(docs[doc_id]['paragraphs']):
        for s_idx, (string_id, sentence) in enumerate(sentences):
            sentence = {
                'id':index_sentence_id,
                'p_idx':p_idx,
                's_idx':s_idx,
                'text':sentence,
            }
            faiss_sentence_embeddings[index_sentence_id] = np.array(sentence_embeddings[string_id])
            faiss_index_to_docs_flat[index_sentence_id] = doc_id
            all_embeddings.append(faiss_sentence_embeddings[index_sentence_id])
            docs_flat[doc_id]['sentences'].append(sentence)
            index_sentence_id += 1
    
    if index % 1000 == 0:
        print(f'{index}/{len(doc_keys)}: {time.time() - start : .2f} seconds / 1000 docs')
        start = time.time()

    # if index == 1000:
    #     break

# time the steps

all_embeddings_np = np.array(all_embeddings)

start = time.time()
print('Training index...')
faiss_index.train(all_embeddings_np)
print(f'Finished training index: {time.time() - start : .2f} seconds')

start = time.time()
print('Adding embeddings to index...')
faiss_index.add(all_embeddings_np)
print(f'Finished adding embeddings to index: {time.time() - start : .2f} seconds')

# print(docs_flat[list(docs_flat.keys())[0]])
# print(faiss_sentence_embeddings[list(faiss_sentence_embeddings.keys())[0]])
# print(faiss_index_to_docs_flat[0])

with gzip.open(docs_flat_path, 'wb') as f:
    pickle.dump(docs_flat, f)

with gzip.open(faiss_index_to_docs_flat_path, 'wb') as f:
    pickle.dump(faiss_index_to_docs_flat, f)

with gzip.open(faiss_sentence_embeddings_path, 'wb') as f:
    pickle.dump(faiss_sentence_embeddings, f)

faiss.write_index(faiss_index, faiss_index_path)