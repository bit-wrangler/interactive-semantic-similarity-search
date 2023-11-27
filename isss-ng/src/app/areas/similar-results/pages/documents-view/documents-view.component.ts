import { Component } from '@angular/core';
import {PaginatorState} from "primeng/paginator";
import {SimilaritySearchService} from "../../services/similarity-search.service";
import {SegmentedDocument} from "../../models/SegmentedText";

interface PageEvent {
  first: number;
  rows: number;
  page: number;
  pageCount: number;
}

@Component({
  selector: 'app-documents-view',
  templateUrl: './documents-view.component.html',
  styleUrls: ['./documents-view.component.scss']
})
export class DocumentsViewComponent {
  first: number = 0;
  rows: number = 10;
  results: SegmentedDocument[] = [];

  constructor(private similaritySearchService: SimilaritySearchService) {
  }

  ngOnInit() {
    this.loadDocuments();
  }

  loadDocuments() {
    this.similaritySearchService.getDocuments(this.first, this.rows).subscribe((res) => {
      this.results = res;
    });
  }

  onPageChange(event: PaginatorState){
    this.rows = event.rows!;
    this.first = event.first!;
    this.loadDocuments();
  }
}
