import {Component, Input} from '@angular/core';
import {SegmentedDocument} from "../../models/SegmentedText";

@Component({
  selector: 'app-document-list-item',
  templateUrl: './document-list-item.component.html',
  styleUrls: ['./document-list-item.component.scss']
})
export class DocumentListItemComponent {
  @Input() document!: SegmentedDocument;
  @Input() score?: number;

  get previewText(): string | null {
    if (this.document) {
      const maxSentences = 3;
      let nPreviewSentences = Math.min(maxSentences, this.document.sentences.length);
      let previewSentences = this.document.sentences
        .slice(0, nPreviewSentences);
      return previewSentences
        .map(s => s.text)
        .join(' ');
    }
    return null;
  }

  get title(): string | undefined {
    return this.document?.id ?? undefined;
  }

  get subtitle(): string | undefined {
    return this.score?.toFixed(3) ?? undefined;
  }

  get linkHref(): string | undefined {
    return `/find-similar-to/${this.document?.id}`;
  }

}
