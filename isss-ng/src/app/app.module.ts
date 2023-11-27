import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';


import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';

import { SidebarModule } from 'primeng/sidebar';
import { ButtonModule } from 'primeng/button';
import { PanelModule } from 'primeng/panel';
import { ScrollerModule } from 'primeng/scroller';
import { PaginatorModule } from 'primeng/paginator';
import { CardModule } from 'primeng/card';

import { CompareViewComponent } from './areas/similar-results/pages/compare-view/compare-view.component';
import {HttpClientModule} from "@angular/common/http";
import { TextSegmentComponent } from './areas/similar-results/components/text-segment/text-segment.component';
import { SegmentedSentenceComponent } from './areas/similar-results/components/segmented-sentence/segmented-sentence.component';
import { SegmentedParagraphComponent } from './areas/similar-results/components/segmented-paragraph/segmented-paragraph.component';
import { SegmentedTextComponent } from './areas/similar-results/components/segmented-text/segmented-text.component';
import {SimilaritySearchService} from "./areas/similar-results/services/similarity-search.service";
import { DocumentsViewComponent } from './areas/similar-results/pages/documents-view/documents-view.component';
import { DocumentListItemComponent } from './areas/similar-results/components/document-list-item/document-list-item.component';

@NgModule({
  declarations: [
    AppComponent,
    CompareViewComponent,
    TextSegmentComponent,
    SegmentedSentenceComponent,
    SegmentedParagraphComponent,
    SegmentedTextComponent,
    DocumentsViewComponent,
    DocumentListItemComponent,
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    AppRoutingModule,
    SidebarModule,
    ButtonModule,
    PanelModule,
    ScrollerModule,
    HttpClientModule,
    PaginatorModule,
    CardModule,
  ],
  providers: [
    SimilaritySearchService,
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
