import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SegmentedParagraphComponent } from './segmented-paragraph.component';

describe('SegmentedParagraphComponent', () => {
  let component: SegmentedParagraphComponent;
  let fixture: ComponentFixture<SegmentedParagraphComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [SegmentedParagraphComponent]
    });
    fixture = TestBed.createComponent(SegmentedParagraphComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
