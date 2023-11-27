import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SegmentedTextComponent } from './segmented-text.component';

describe('SegmentedTextComponent', () => {
  let component: SegmentedTextComponent;
  let fixture: ComponentFixture<SegmentedTextComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [SegmentedTextComponent]
    });
    fixture = TestBed.createComponent(SegmentedTextComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
