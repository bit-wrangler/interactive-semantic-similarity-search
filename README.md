docker pull ankane/pgvector
docker run --name isss_db -p 5432:5432 -e POSTGRES_PASSWORD=mysecretpassword -d ankane/pgve

Testing was done on Windows 10 + conda + python 3.8


scripts should be run from the py_src directory

put your data csv file in the repo_root/data directory
update `csv_file_path`, `csv_text_column_name`, `csv_id_column_name` in generate_data_collections.py as needed
then use the commands below

execution example:
```
cd py_src
python -m process_data.generate_data_collections
python -m process_data.save_to_faiss
python -m process_data.faiss_sentence_wise_query_test
```

## generate_data_collections

This script generates embeddings for sentences and creates a neutral data format to store the document structure

## save_to_faiss

This script takes in the embeddings generated by `generate_data_collections` and generates the FAISS index and also stores document structure in a format that is compatible with the FAISS index.

## faiss_sentence_wise_query_test

This script uses the FAISS to provide basic usage examples of the common classes. It grabs the first document id, finds similar documents using sentence-wise similarity comparisons in the vector index. Then the script displays the neighbor document augmented with similarities of the sentences relative to the reference document.

The script also illstrates usage of a user text query as a search string to query the index.



```
docker run -d -p 8983:8983 --name isss_solr -v "$(pwd)/solr/config:/isss_core_config/conf" solr solr-precreate isss_core /isss_core_config
```

### Solr MoreLikeThis Query example

```
http://localhost:8983/solr/isss_core/mlt?q=id%3A157803&mlt.fl=text&mlt.mindf=0&mlt.mintf=0&fl=score,doc_id,text,id&rows=100
```