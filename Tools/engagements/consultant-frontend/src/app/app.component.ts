import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { ClientsListComponent } from './components/clients-list/clients-list.component';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, ClientsListComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'consultant-frontend';
}
