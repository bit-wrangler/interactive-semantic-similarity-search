import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DocumentListItemComponent } from './document-list-item.component';

describe('DocumentListItemComponent', () => {
  let component: DocumentListItemComponent;
  let fixture: ComponentFixture<DocumentListItemComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [DocumentListItemComponent]
    });
    fixture = TestBed.createComponent(DocumentListItemComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
