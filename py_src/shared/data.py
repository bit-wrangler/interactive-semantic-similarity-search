import pickle
import gzip
import faiss
import numpy as np
from typing import List, Dict, Tuple, Union
from .models import Document, Sentence
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')

faiss_index_path = '../data/consumer_complaints_faiss_Index_IP.index'
docs_flat_path = '../data/consumer_complaints_docs_flat_Index_IP.pkl.gz'
faiss_index_to_docs_flat_path = '../data/consumer_complaints_faiss_Index_IP_to_docs_flat.pkl.gz'
faiss_sentence_embeddings_path = '../data/consumer_complaints_faiss_sentence_embeddings_Index_IP.pkl.gz'

class AppData:
    instance = None

    @staticmethod
    def get_instance():
        if AppData.instance is None:
            AppData.instance = AppData()
        return AppData.instance

    docs: Dict[int, Document]

    def __init__(self):
        self.faiss_index: faiss.IndexFlatIP = faiss.read_index(faiss_index_path)
        with gzip.open(docs_flat_path, 'rb') as f:
            docs_flat = pickle.load(f)
        with gzip.open(faiss_index_to_docs_flat_path, 'rb') as f:
            self.faiss_index_to_docs_flat: Dict[int, int] = pickle.load(f)
        with gzip.open(faiss_sentence_embeddings_path, 'rb') as f:
            self.faiss_sentence_embeddings: Dict[int, np.ndarray] = pickle.load(f)

        self.docs = {}
        for doc_id in docs_flat:
            doc = Document()
            doc.id = doc_id
            doc.sentences = []
            for sentence in docs_flat[doc_id]['sentences']:
                s = Sentence()
                s.id = sentence['id']
                s.p_idx = sentence['p_idx']
                s.s_idx = sentence['s_idx']
                s.text = sentence['text']
                doc.sentences.append(s)
            self.docs[doc_id] = doc

    def get_doc(self, doc_id: str) -> Union[Document, None]:
        if doc_id not in self.docs:
            return None
        return self.docs[doc_id].copy()
    
    def get_sentence(self, sentence_id: int) -> Sentence:
        doc_id = self.faiss_index_to_docs_flat[sentence_id]
        doc = self.docs[doc_id]
        for sentence in doc.sentences:
            if sentence.id == sentence_id:
                return sentence.copy()
        return None
    
    def get_docs(self, skip: int = 0, take: int = 100) -> List[Document]:
        return [self.docs[doc_id].copy() for doc_id in list(self.docs.keys())[skip:skip+take]]
    
    def get_docs_by_ids(self, doc_ids: List[str]) -> List[Document]:
        return [self.docs[doc_id].copy() for doc_id in doc_ids]
    
class SimilarityService:
    instance = None

    @staticmethod
    def get_instance():
        if SimilarityService.instance is None:
            SimilarityService.instance = SimilarityService()
        return SimilarityService.instance

    app_data: AppData = AppData.get_instance()

    def compare_document_sentences(self, ref_doc_id: str, other_doc_id: str) -> List[List[float]]:
        ref_doc = self.app_data.docs[ref_doc_id].copy()
        other_doc = self.app_data.docs[other_doc_id].copy()
        ref_sentence_ids = [s.id for s in ref_doc.sentences]
        ref_sentence_embeddings = [self.app_data.faiss_sentence_embeddings[s_id] for s_id in ref_sentence_ids]
        other_sentence_ids = [s.id for s in other_doc.sentences]
        other_sentence_embeddings = [self.app_data.faiss_sentence_embeddings[s_id] for s_id in other_sentence_ids]
        cross_similarities = [
            [
                np.dot(ref_sentence_embedding, other_sentence_embedding).item() 
                for other_sentence_embedding in other_sentence_embeddings
            ] 
            for ref_sentence_embedding in ref_sentence_embeddings
        ]

        return cross_similarities
    
    def find_similar_document_ids(self, ref_doc_id: str, k_nearest: int = 10000, n_top: int = 10) -> List[Tuple[str, float]]:
        ref_doc = self.app_data.docs[ref_doc_id].copy()
        ref_sentence_ids = [s.id for s in ref_doc.sentences]
        ref_sentence_embeddings = np.array([self.app_data.faiss_sentence_embeddings[s_id] for s_id in ref_sentence_ids])
        D, I = self.app_data.faiss_index.search(ref_sentence_embeddings, k_nearest)
        matches = []
        for i in range(len(D)):
            matches.append({})
            for j in range(len(D[i])):
                sentence_faiss_id = I[i][j]
                if sentence_faiss_id < 0:
                    continue
                neighbor_doc_id = self.app_data.faiss_index_to_docs_flat[sentence_faiss_id]
                similarity = D[i][j]
                if neighbor_doc_id != ref_doc_id:
                    if neighbor_doc_id not in matches[i]:
                        matches[i][neighbor_doc_id] = similarity
                    matches[i][neighbor_doc_id] = max(matches[i][neighbor_doc_id], similarity)

        neighbor_doc_sums = {}
        for i in range(len(matches)):
            for neighbor_doc_id in matches[i]:
                if neighbor_doc_id not in neighbor_doc_sums:
                    neighbor_doc_sums[neighbor_doc_id] = 0
                neighbor_doc_sums[neighbor_doc_id] += matches[i][neighbor_doc_id]

        results = sorted(neighbor_doc_sums.items(), key=lambda x: x[1], reverse=True)
        return results[:n_top]
    
    def find_similar_documents(self, ref_doc_id: int, k_nearest: int = 10000) -> List[Tuple[Document, float]]:
        results = self.find_similar_document_ids(ref_doc_id, k_nearest)
        return [(self.app_data.docs[doc_id].copy(), similarity) for doc_id, similarity in results]

    def find_similar_documents_by_text_query(self, text_query: str, k_nearest: int = 1000) -> List[int]:
        query_embedding = model.encode(text_query)
        D, I = self.app_data.faiss_index.search(np.array([query_embedding]), k_nearest)
        matches = []
        for i in range(len(D)):
            matches.append({})
            for j in range(len(D[i])):
                sentence_faiss_id = I[i][j]
                if sentence_faiss_id < 0:
                    continue
                neighbor_doc_id = self.app_data.faiss_index_to_docs_flat[sentence_faiss_id]
                similarity = D[i][j]
                if neighbor_doc_id not in matches[i]:
                    matches[i][neighbor_doc_id] = similarity
                matches[i][neighbor_doc_id] = max(matches[i][neighbor_doc_id], similarity)

        neighbor_doc_sums = {}
        for i in range(len(matches)):
            for neighbor_doc_id in matches[i]:
                if neighbor_doc_id not in neighbor_doc_sums:
                    neighbor_doc_sums[neighbor_doc_id] = 0
                neighbor_doc_sums[neighbor_doc_id] += matches[i][neighbor_doc_id]

        results = sorted(neighbor_doc_sums.items(), key=lambda x: x[1], reverse=True)
        return results