from typing import List, Union

class Sentence:
    id: int
    p_idx: int
    s_idx: int
    text: str

    def to_dict(self):
        return {
            'id':self.id,
            'p_idx':self.p_idx,
            's_idx':self.s_idx,
            'text':self.text,
        }
    
    def copy(self):
        s = Sentence()
        s.id = self.id
        s.p_idx = self.p_idx
        s.s_idx = self.s_idx
        s.text = self.text
        return s
    
    @staticmethod
    def from_dict(d):
        s = Sentence()
        s.id = d['id']
        s.p_idx = d['p_idx']
        s.s_idx = d['s_idx']
        s.text = d['text']
        return s
    
class Document:
    id: int
    sentences: List[Sentence] = []

    def to_dict(self):
        return {
            'id':self.id,
            'sentences':[s.to_dict() for s in self.sentences],
        }
    
    def copy(self):
        doc = Document()
        doc.id = self.id
        doc.sentences = [s.copy() for s in self.sentences]
        return doc
    
    @staticmethod
    def from_dict(d):
        doc = Document()
        doc.id = d['id']
        doc.sentences = [Sentence.from_dict(s) for s in d['sentences']]
        return doc