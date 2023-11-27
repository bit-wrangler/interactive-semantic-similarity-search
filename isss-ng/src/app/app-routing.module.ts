import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import {CompareViewComponent} from "./areas/similar-results/pages/compare-view/compare-view.component";
import {DocumentsViewComponent} from "./areas/similar-results/pages/documents-view/documents-view.component";

const routes: Routes = [
  {path: 'find-similar-to/:id', component: CompareViewComponent},
  {path: 'documents', component: DocumentsViewComponent},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
