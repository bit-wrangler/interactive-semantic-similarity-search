import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SegmentedSentenceComponent } from './segmented-sentence.component';

describe('SegmentedSentenceComponent', () => {
  let component: SegmentedSentenceComponent;
  let fixture: ComponentFixture<SegmentedSentenceComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [SegmentedSentenceComponent]
    });
    fixture = TestBed.createComponent(SegmentedSentenceComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
