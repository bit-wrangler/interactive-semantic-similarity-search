import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {map, Observable} from 'rxjs';
import {SegmentedDocument, SegmentedDocumentDto, SimilarDocument, SimilarDocumentDto} from '../models/SegmentedText';
import {HttpParams} from "@angular/common/http";

@Injectable({
  providedIn: 'root'
})
export class SimilaritySearchService {

  // dev api is hosted at http://127.0.0.1:5000

  constructor(private http: HttpClient) { }

  getDocuments(skip: number, take: number): Observable<SegmentedDocument[]> {
    const options = { params: new HttpParams().set('skip', skip.toString()).set('take', take.toString()) };

    return this.http.get<SegmentedDocumentDto[]>('http://localhost:5000/api/docs', options)
      .pipe(map((results:SegmentedDocumentDto[]) => results.map(result => new SegmentedDocument(result))));
  }

  getDocument(id: string): Observable<SegmentedDocument>{
    return this.http.get<SegmentedDocumentDto>(`http://localhost:5000/api/docs/${id}`)
      .pipe(map((result:SegmentedDocumentDto) => new SegmentedDocument(result)));
  }

  getSimilarDocuments(id: string): Observable<SimilarDocument[]> {
    return this.http.get<SimilarDocumentDto[]>(`http://localhost:5000/api/find-similar/${id}`)
      .pipe(map((results:SimilarDocumentDto[]) => results.map(result => new SimilarDocument(result))));
  }

  getSentenceSimilarityMatrix(ref_id: string, other_id: string): Observable<number[][]> {
    return this.http.get<number[][]>(`http://localhost:5000//api/sentence-similarity-matrix/${ref_id}/${other_id}`);
  }
}
