import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CompareViewComponent } from './compare-view.component';

describe('CompareViewComponent', () => {
  let component: CompareViewComponent;
  let fixture: ComponentFixture<CompareViewComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [CompareViewComponent]
    });
    fixture = TestBed.createComponent(CompareViewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
