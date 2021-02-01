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
    selectedAP = [];
    clientsFound = [];
    autoAttack = "";

    startAttack(): void {
      console.log("Attack would start now");
    }

    getAP(): void {
       this.API.request({
         module: 'CaptivePortalJumper',
         action: 'getAP'
       }, (response) => {
         this.availableAP = JSON.parse(response);
       })
    }

    getClients(): void {
       this.API.request({
         module: 'CaptivePortalJumper',
         action: 'getClients',
         bssid: this.selectedAP[0],
         channel: this.selectedAP[1]
       }, (response) => {
         this.clientsFound = JSON.parse(response);
       })
    }

    loadConfig(): void {
      this.API.request({
        module: 'CaptivePortalJumper',
        action: 'loadConfig'
      }, (response) => {

      })
    }

    ngOnInit() {
      this.loadConfig();
    }
}
