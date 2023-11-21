CREATE DATABASE isss;

CREATE EXTENSION vector;

CREATE TABLE documents (
  id bigserial PRIMARY KEY,
  "text" text NOT NULL,
  text_tsvector tsvector generated always as (to_tsvector('english', "text")) stored
);

CREATE INDEX documents_text_tsvector_idx ON documents USING gin (text_tsvector);

CREATE TABLE sentences (
  id bigserial PRIMARY KEY, 
  document_id bigint REFERENCES documents(id),
  p_idx int NOT NULL,
  s_idx int NOT NULL,
  "text" text NOT NULL,
  embedding vector(384) NOT NULL,
  text_tsvector tsvector generated always as (to_tsvector('english', "text")) stored
);

CREATE INDEX ON sentences USING hnsw (embedding vector_ip_ops);
CREATE INDEX sentences_document_id_idx ON sentences (document_id);
CREATE INDEX sentences_text_tsvector_idx ON sentences USING gin (text_tsvector);
