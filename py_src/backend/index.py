# run via flask --app backend.index run

from flask import Flask, jsonify, request
from flask_cors import CORS

from shared.data import SimilarityService

print('Loading SimilarityService...')
similarity_service = SimilarityService.get_instance()
print('SimilarityService loaded.')


app = Flask(__name__)
cors = CORS(app)

@app.route('/api', methods=['GET'])
def get_index():
    return jsonify({'message': 'Hello, World!'})

@app.route('/api/docs', methods=['GET'])
def get_docs():
    skip = int(request.args.get('skip', 0))
    take = int(request.args.get('take', 100))
    return jsonify([doc.to_dict() for doc in similarity_service.app_data.get_docs(skip, take)])

@app.route('/api/docs/<doc_id>', methods=['GET'])
def get_doc(doc_id: str):
    doc = similarity_service.app_data.get_doc(doc_id)
    if doc is None:
        return jsonify({'message': f'Document with id {doc_id} not found.'}), 404
    return jsonify(doc.to_dict())

@app.route('/api/find-similar/<doc_id>', methods=['GET'])
def find_similar(doc_id: str):
    k_nearest = int(request.args.get('k_nearest', 10000))
    results = similarity_service.find_similar_documents(doc_id, k_nearest)
    return jsonify(list(map(lambda r: {'doc': r[0].to_dict(), 'similarity': r[1]}, results)))

@app.route('/api/sentence-similarity-matrix/<ref_doc_id>/<other_doc_id>', methods=['GET'])
def get_sentence_similarity_matrix(ref_doc_id: str, other_doc_id: str):
    return jsonify(similarity_service.compare_document_sentences(ref_doc_id, other_doc_id))