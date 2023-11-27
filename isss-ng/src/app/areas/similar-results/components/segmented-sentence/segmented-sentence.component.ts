import {Component, EventEmitter, Input, Output} from '@angular/core';
import {SegmentedSentence} from "../../models/SegmentedText";

@Component({
  selector: 'app-segmented-sentence',
  templateUrl: './segmented-sentence.component.html',
  styleUrls: ['./segmented-sentence.component.scss']
})
export class SegmentedSentenceComponent {
  @Input() segmentedSentence!: SegmentedSentence;
  @Input() similarityMatrix?: number[][] | null = null;
  @Input() isReference: boolean = true;
  @Output() onHover: EventEmitter<number> = new EventEmitter<number>();

  classes: string = 'sentence';

  public applySimilarity(otherSentenceIndex: number | null){
    if (otherSentenceIndex == null) {
      this.classes = 'sentence';
      return;
    }
    let similarity = 0.0;
    if (this.similarityMatrix != null) {
      if (!this.isReference) {
        similarity = this.similarityMatrix[otherSentenceIndex][this.segmentedSentence.idx];
      }  else {
        similarity = this.similarityMatrix[this.segmentedSentence.idx][otherSentenceIndex];
      }
    }
    this.classes = `sentence ${this.similarityToClass(similarity)}`;
  }

  similarityToClass(similarity: number): string {
    if (similarity < -0.715) return 'sentence-similarity-m3';
    if (similarity < -0.43) return 'sentence-similarity-m2';
    if (similarity < -0.145) return 'sentence-similarity-m1';
    if (similarity < 0.145) return '';
    if (similarity < 0.43) return 'sentence-similarity-p1';
    if (similarity < 0.715) return 'sentence-similarity-p2';
    return 'sentence-similarity-p3';
  }

  handleSentenceHover() {
    this.onHover.emit(this.segmentedSentence.idx);
  }
}
