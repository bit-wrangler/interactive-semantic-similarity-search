from itertools import groupby
import numpy as np
import pickle
import gzip
import time
import pysolr

# from ..shared.data import faiss_index_path, docs_flat_path, faiss_index_to_docs_flat_path, faiss_sentence_embeddings_path
from .generate_data_collections import docs_pickle_path, sentence_embeddings_pickle_path

with gzip.open(docs_pickle_path, 'rb') as f:
    docs = pickle.load(f)

with gzip.open(sentence_embeddings_pickle_path, 'rb') as f:
    sentence_embeddings = pickle.load(f)

solr_url = 'http://localhost:8983/solr/'

core_name = 'isss_core'

solr = pysolr.Solr(f'{solr_url}{core_name}/')

# solr_admin = pysolr.SolrCoreAdmin('http://localhost:8983/solr/admin/cores')
# print(solr_admin.status())

doc_keys = list(docs.keys())
index_sentence_id = 0

start = time.time()
for index, doc_id in enumerate(doc_keys):
    for p_idx, sentences in enumerate(docs[doc_id]['paragraphs']):
        for s_idx, (string_id, sentence_text) in enumerate(sentences):
            sentence = {
                'id':f'{index_sentence_id}',
                'doc_id': doc_id,
                'text':sentence_text,
                'embedding':sentence_embeddings[string_id].tolist(),
            }
            # print(sentence)
            # break
            solr.add(sentence)
            index_sentence_id += 1
        # break
    # break
    if (index % 1000 == 0):
        print(f'{index}/{len(doc_keys)}: {time.time() - start : .2f} seconds / 1000 docs')
        start = time.time()
        solr.commit()
solr.commit()