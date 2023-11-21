from sqlalchemy import BigInteger, Text, Integer, ForeignKey, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker
from typing import List
from pgvector.sqlalchemy import Vector
from itertools import groupby

class Base(DeclarativeBase):
    pass

class Document(Base):
    __tablename__ = 'documents'
    id: Mapped[int] = mapped_column(primary_key=True)
    sentences: Mapped[List['Sentence']] = relationship(back_populates='document')
    text: Mapped[str] = mapped_column(Text)

    def build_text_from_sentences(self):
        sentences = sorted(self.sentences, key=lambda s: (s.p_idx, s.s_idx))

        # group sentences by paragraph
        paragraphs = []
        for p_idx, paragraph in groupby(sentences, lambda s: s.p_idx):
            paragraphs.append(' '.join([s.text for s in paragraph]))
        
        # build text from paragraphs
        self.text = '\n'.join(paragraphs)
        

class Sentence(Base):
    __tablename__ = 'sentences'
    id: Mapped[int] = mapped_column(primary_key=True)
    document_id: Mapped[int] = mapped_column(ForeignKey('documents.id'))
    document: Mapped['Document'] = relationship(back_populates='sentences')
    p_idx: Mapped[int] = mapped_column(Integer)
    s_idx: Mapped[int] = mapped_column(Integer)
    text: Mapped[str] = mapped_column(Text)
    embedding = mapped_column(Vector(384))

engine = create_engine('postgresql://postgres:mysecretpassword@localhost:5432/isss')

session = sessionmaker(bind=engine)()

import numpy as np
import pickle
import gzip

docs_pickle_path = 'data/consumer_complaints_docs.pkl.gz'
sentence_embeddings_pickle_path = 'data/consumer_complaints_sentence_embeddings.pkl.gz'

with gzip.open(docs_pickle_path, 'rb') as f:
    docs = pickle.load(f)

with gzip.open(sentence_embeddings_pickle_path, 'rb') as f:
    sentence_embeddings = pickle.load(f)

doc_keys = list(docs.keys())

# print(docs[doc_keys[0]])

for index, doc_id in enumerate(doc_keys):
    document = Document()
    document.id = int(doc_id)
    
    for p_idx, sentences in enumerate(docs[doc_id]['paragraphs']):
        for s_idx, (string_id, sentence) in enumerate(sentences):
            sentence = Sentence(
                p_idx=p_idx,
                s_idx=s_idx, 
                text=sentence, 
                embedding=np.array(sentence_embeddings[string_id]))
            document.sentences.append(sentence)
    document.build_text_from_sentences()
    session.add(document)
    
    if index % 1000 == 0:
        print(index)
        session.commit()
session.commit()