import { TestBed } from '@angular/core/testing';

import { SimilaritySearchService } from './similarity-search.service';

describe('SimilaritySearchService', () => {
  let service: SimilaritySearchService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(SimilaritySearchService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
