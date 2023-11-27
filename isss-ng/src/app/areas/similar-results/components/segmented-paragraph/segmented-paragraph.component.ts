import {Component, EventEmitter, Input, Output, QueryList, ViewChildren} from '@angular/core';
import {SegmentedSentence} from "../../models/SegmentedText";
import {SegmentedSentenceComponent} from "../segmented-sentence/segmented-sentence.component";

@Component({
  selector: 'app-segmented-paragraph',
  templateUrl: './segmented-paragraph.component.html',
  styleUrls: ['./segmented-paragraph.component.scss']
})
export class SegmentedParagraphComponent {
  @Input() segmentedParagraph!: SegmentedSentence[];
  @Output() onSentenceHover: EventEmitter<number> = new EventEmitter<number>();
  @Input() similarityMatrix?: number[][] | null = null;
  @Input() isReference: boolean = true;

  @ViewChildren('sentences') sentenceElements?: QueryList<SegmentedSentenceComponent>;

  handleSentenceHover(idx: number){
    this.onSentenceHover.emit(idx);
  }

  public applySimilarity(otherSentenceIdx: number | null) {
    if (this.sentenceElements)
    for (const sentenceElement of this.sentenceElements.toArray()) {
      sentenceElement.applySimilarity(otherSentenceIdx);
    }
  }
}
