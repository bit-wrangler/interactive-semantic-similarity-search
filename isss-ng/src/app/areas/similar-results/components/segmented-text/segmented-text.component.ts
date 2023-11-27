import {Component, EventEmitter, Input, Output, QueryList, ViewChildren} from '@angular/core';
import {SegmentedDocument} from "../../models/SegmentedText";
import {SegmentedSentenceComponent} from "../segmented-sentence/segmented-sentence.component";
import {SegmentedParagraphComponent} from "../segmented-paragraph/segmented-paragraph.component";

@Component({
  selector: 'app-segmented-text',
  templateUrl: './segmented-text.component.html',
  styleUrls: ['./segmented-text.component.scss']
})
export class SegmentedTextComponent {
  @Input() segmentedDocument!: SegmentedDocument;
  @Output() onSentenceHover: EventEmitter<number> = new EventEmitter<number>();
  @Input() similarityMatrix?: number[][] | null = null;
  @Input() isReference: boolean = true;

  @ViewChildren('paragraphs') paragraphElements?: QueryList<SegmentedParagraphComponent>;

  handleSentenceHover(idx: number){
    this.onSentenceHover.emit(idx);
  }

  public applySimilarity(otherSentenceIdx: number | null) {
    if (this.paragraphElements)
    for (const paragraphElement of this.paragraphElements.toArray()) {
      paragraphElement.applySimilarity(otherSentenceIdx);
    }
  }
}
