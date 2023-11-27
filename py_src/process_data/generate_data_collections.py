import pandas as pd
import nltk
import numpy as np
from sentence_transformers import SentenceTransformer
import pickle
import gzip
from nltk.tokenize import sent_tokenize, word_tokenize
import re

model = SentenceTransformer('all-MiniLM-L6-v2')

csv_file_path = '../data/Consumer_Complaints.csv'
csv_text_column_name = 'Consumer complaint narrative'
csv_id_column_name = 'Complaint ID'
docs_pickle_path = '../data/consumer_complaints_docs.pkl.gz'
sentence_embeddings_pickle_path = '../data/consumer_complaints_sentence_embeddings.pkl.gz'

if __name__ == '__main__':

    nltk.download('stopwords')
    nltk.download('punkt')


    def load_text_from_csv(file_path, text_column, id_column, save_cleaned=False):
        # Read the CSV file
        df = pd.read_csv(file_path, dtype='unicode')
        df = df[df[text_column].notna()]
        
        if save_cleaned:
            # Save the resulting dataframe back to the original file
            df.to_csv(file_path, index=False)

        return list(df[[id_column, text_column]].itertuples(index=False))

    def split_into_paragraphs(text):
        paragraphs = text.replace('\r', '').split('\n')  # Split the text by newline characters
        return [paragraph.strip() for paragraph in paragraphs if paragraph.strip()]  # Remove empty paragraphs and strip whitespace

    def clean_string(string):
        # remove currencies
        string = re.sub(r'\$\d+(\.\d+)?', '', string)

        # remove numbers and floating point numbers
        string = re.sub(r'\d+(\.\d+)', '', string)

        # remove XXXX placeholders
        string = re.sub(r'X+', '', string)

        # remove curly braces
        string = re.sub(r'\{|\}', '', string)

        # remove multiple periods
        string = re.sub(r'\.{2,}', '', string)

        # remove empty and white space only parentheses
        string = re.sub(r'\(\s*\)', '', string)

        string = re.sub(r'(?<=\S)[\/\\](?=\S)', ' / ', string)

        # remove slashes
        string = re.sub(r'[\/\\]+', '', string)

        # remove multiple spaces
        string = re.sub(r' {2,}', ' ', string)

        # add whitespace around hyphens for hyphenated words
        string = re.sub(r'(?<=\S)-(?=\S)', ' - ', string)

        return string.strip()

    def split_sentence(sentence, max_length=40, ideal_length=20):
            words = word_tokenize(sentence)
            if len(words) <= max_length:
                return [sentence]
            
            # Split at punctuation or conjunctions
            split_points = [m.start() for m in re.finditer(r',| and | but | or | however | although ', sentence)]
            split_sentences = []
            start = 0

            for point in split_points:
                # Ensure the split segment is within the ideal length
                if point - start > ideal_length * 5:  # average word length 5 characters
                    split_sentences.append(sentence[start:point])
                    start = point + 1

            # Add the last segment
            if start < len(sentence):
                split_sentences.append(sentence[start:])

            return split_sentences


    data_raw = load_text_from_csv(csv_file_path, csv_text_column_name, csv_id_column_name, save_cleaned=False)

    # for id, raw_text in data_raw:
    #     print("ID: ", id)
    #     print("Text: ", clean_string(raw_text))
    #     break

    all_docs = {}
    sentence_embeddings = {}
    sentence_id = 1

    all_ids = []
    all_embeddings = []
    all_metadatas = []

    for index, (doc_id, raw_text) in enumerate(data_raw):
        clean_narrative = clean_string(raw_text)
        
        doc= {
            'id': doc_id,
            'text': clean_narrative,
            'paragraphs': [
                
            ]
        }

        paragraphs = split_into_paragraphs(clean_narrative)
        for p_idx, paragraph in enumerate(paragraphs):
            sentences = sent_tokenize(paragraph)
            
            # Split long sentences
            split_sentences = []
            for sentence in sentences:
                split_sentences.extend(split_sentence(sentence))

            paragraph_sentences = []
            for s_idx, sentence in enumerate(split_sentences):
                chroma_metadata = {
                    'doc_id': doc_id,
                    'p_idx': p_idx,
                    's_idx': s_idx
                }
                string_id = f'{sentence_id}'
                embedding = model.encode(sentence)
                sentence_embeddings[string_id] = embedding
                # collection.add(
                #     ids=[string_id],
                #     embeddings=[embedding.tolist()],
                #     metadatas=[chroma_metadata]
                #     )
                all_ids.append(string_id)
                all_embeddings.append(embedding.tolist())
                all_metadatas.append(chroma_metadata)
                paragraph_sentences.append((string_id, sentence))
                sentence_id += 1
            doc['paragraphs'].append(paragraph_sentences)
        
        all_docs[doc_id] = doc

        # if index > 100:
        #     break
        if index % 1000 == 0:
            print(index)

    with gzip.open(docs_pickle_path, 'wb') as f:
        pickle.dump(all_docs, f)

    with gzip.open(sentence_embeddings_pickle_path, 'wb') as f:
        pickle.dump(sentence_embeddings, f)