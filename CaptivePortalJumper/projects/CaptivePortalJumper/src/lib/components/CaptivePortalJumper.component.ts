import { Component, OnInit } from '@angular/core';
import { ApiService } from '../services/api.service';

@Component({
    selector: 'lib-CaptivePortalJumper',
    templateUrl: './CaptivePortalJumper.component.html',
    styleUrls: ['./CaptivePortalJumper.component.css']
})
export class CaptivePortalJumperComponent implements OnInit {
    constructor(private API: ApiService) { }

    availableAP = [];
    selectedAP = "";
    
    getAP(): void {
       this.API.request({
         module: 'CaptivePortalJumper',
         action: 'getAP'
       }, (response) => {
         this.availableAP = JSON.parse(response);
       })
    }

    ngOnInit() {

    }
}
