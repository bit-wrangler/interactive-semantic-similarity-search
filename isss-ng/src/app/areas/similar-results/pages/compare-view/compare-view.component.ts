import {Component, ViewChild} from '@angular/core';
import {SegmentedDocument, SimilarDocument} from "../../models/SegmentedText";
import {SimilaritySearchService} from "../../services/similarity-search.service";
import {ActivatedRoute} from "@angular/router";
import {SegmentedTextComponent} from "../../components/segmented-text/segmented-text.component";

@Component({
  selector: 'app-compare-view',
  templateUrl: './compare-view.component.html',
  styleUrls: ['./compare-view.component.scss']
})
export class CompareViewComponent {
  items!: string[];
  referenceDocument?: SegmentedDocument;
  similarDocuments?: SimilarDocument[];
  selectedSimilarDocument?: SegmentedDocument;
  similarityMatrix?: number[][];
  showRefinementsSidebar = false;
  id?: string | null;

  @ViewChild('otherDocument') otherDocElement?: SegmentedTextComponent;

  constructor(
    private route: ActivatedRoute,
    private similaritySearchService: SimilaritySearchService
  ) {
  }

  ngOnInit() {
    this.id = this.route.snapshot.paramMap.get('id');
    this.items = Array.from({ length: 1000 }).map((_, i) => `Item #${i}`);
    this.similaritySearchService.getDocument(this.id!).subscribe(res => {
      this.referenceDocument = res;
      this.similaritySearchService.getSimilarDocuments(this.id!).subscribe(res => {
        this.similarDocuments = res;
        console.log(res);
      })
    });
  }

  onSimilarResultClick(doc: SegmentedDocument)
  {
    this.selectedSimilarDocument = doc;
    this.similaritySearchService.getSentenceSimilarityMatrix(this.id!, doc.id).subscribe(res => {
      this.similarityMatrix = res;
      console.log(res);
    })
  }

  handleSentenceHover(idx: number) {
    if (this.otherDocElement){
      this.otherDocElement.applySimilarity(idx);
    }
  }
}
