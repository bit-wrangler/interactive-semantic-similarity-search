export interface SegmentedDocumentDto {
  id:        string;
  sentences: SegmentedSentenceDto[];
}

export interface SimilarDocumentDto {
  doc:        SegmentedDocumentDto;
  similarity: number;
}

export class SimilarDocument {
  doc:        SegmentedDocument;
  similarity: number;

  constructor(dto: SimilarDocumentDto) {
    this.doc = new SegmentedDocument(dto.doc);
    this.similarity = dto.similarity;
  }
}

export class SegmentedDocument {
  id:        string;
  sentences: SegmentedSentenceDto[];
  paragraphs: SegmentedSentence[][];

  constructor(dto: SegmentedDocumentDto) {
    this.id = dto.id;
    this.sentences = dto.sentences;
    this.paragraphs = this.sentences.reduce((acc: SegmentedSentence[][], s, idx) => {
      if (s.p_idx >= acc.length) {
        acc.push([]);
      }
      acc[s.p_idx].push(new SegmentedSentence(s, idx));
      return acc;
    }, []);
  }
}

export interface SegmentedSentenceDto {
  id:    number;
  p_idx: number;
  s_idx: number;
  text:  string;
}

export class SegmentedSentence {
  id:    number;
  p_idx: number;
  s_idx: number;
  text:  string;
  idx:   number;
  constructor(dto: SegmentedSentenceDto, idx: number) {
    this.id = dto.id;
    this.p_idx = dto.p_idx;
    this.s_idx = dto.s_idx;
    this.text = dto.text;
    this.idx = idx;
  }
}
