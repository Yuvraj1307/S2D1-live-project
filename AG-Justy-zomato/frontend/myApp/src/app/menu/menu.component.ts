import { Component } from '@angular/core';

@Component({
  selector: 'app-menu',
  templateUrl: './menu.component.html',
  styleUrls: ['./menu.component.css']
})
export class MenuComponent {
  TB=document.getElementById("TB")
  arr=[{id:1,name:"samosa",price:15,avalible:true},{id:2,name:"kacori",price:10,avalible:false}]
  constructor() {
    
    this.TB.innerHTML= this.arr.map((el,i)=>{
      
      return `
          <tr>
              <td>${el.id}</td>
              <td>${el.name}</td>
              <td>${el.price}</td>
              <td>${el.avalible}</td>
          </tr>
      
      `
     }).join(" ")
  }
  //  TB.innerHTML=op.join(" ")
}
