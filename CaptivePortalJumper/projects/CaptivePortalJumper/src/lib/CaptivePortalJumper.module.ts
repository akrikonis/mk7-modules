import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { CaptivePortalJumperComponent } from './components/CaptivePortalJumper.component';
import { RouterModule, Routes } from '@angular/router';

import {MaterialModule} from './modules/material/material.module';
import {FlexLayoutModule} from '@angular/flex-layout';

import {FormsModule} from '@angular/forms';

const routes: Routes = [
    { path: '', component: CaptivePortalJumperComponent }
];

@NgModule({
    declarations: [CaptivePortalJumperComponent],
    imports: [
        CommonModule,
        RouterModule.forChild(routes),
        MaterialModule,
        FlexLayoutModule,
        FormsModule,
    ],
    exports: [CaptivePortalJumperComponent]
})
export class CaptivePortalJumperModule { }
