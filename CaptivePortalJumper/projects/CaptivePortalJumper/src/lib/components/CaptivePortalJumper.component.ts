import { Component, OnInit } from '@angular/core';
import { ApiService } from '../services/api.service';

@Component({
    selector: 'lib-CaptivePortalJumper',
    templateUrl: './CaptivePortalJumper.component.html',
    styleUrls: ['./CaptivePortalJumper.component.css']
})
export class CaptivePortalJumperComponent implements OnInit {
    constructor(private API: ApiService) { }

    ngOnInit() {
    }
}
