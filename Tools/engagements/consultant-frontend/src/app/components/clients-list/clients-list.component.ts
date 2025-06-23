import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../services/api.service';
import { Client, ClientCreate, ClientContactCreate, Engagement, EngagementCreate, EngagementStatus } from '../../models/client.model';

@Component({
  selector: 'app-clients-list',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './clients-list.component.html',
  styleUrl: './clients-list.component.css'
})
export class ClientsListComponent implements OnInit {
  clients: Client[] = [];
  engagements: Engagement[] = [];
  loading = false;
  error: string | null = null;
  selectedClient: Client | null = null;
  showEngagements = false;

  constructor(private apiService: ApiService) {}

  ngOnInit(): void {
    this.loadClients();
    this.loadEngagements();
  }

  loadClients(): void {
    this.loading = true;
    this.error = null;
    
    this.apiService.getClients().subscribe({
      next: (clients) => {
        this.clients = clients;
        this.loading = false;
        console.log('Loaded clients:', clients);
      },
      error: (error) => {
        this.error = 'Failed to load clients. Please check your connection.';
        this.loading = false;
        console.error('Error loading clients:', error);
      }
    });
  }

  loadEngagements(): void {
    this.apiService.getEngagements().subscribe({
      next: (engagements) => {
        this.engagements = engagements;
        console.log('Loaded engagements:', engagements);
      },
      error: (error) => {
        console.error('Error loading engagements:', error);
      }
    });
  }

  getClientEngagements(clientId: number): Engagement[] {
    return this.engagements.filter(eng => eng.client_id === clientId);
  }

  createNewClient(): void {
    const name = prompt('Enter client name:');
    if (!name) return;

    const company = prompt('Enter company name (optional):') || undefined;
    const phone = prompt('Enter phone number (optional):') || undefined;
    const address = prompt('Enter address (optional):') || undefined;

    // Primary contact information
    const contactName = prompt('Enter primary contact name:');
    if (!contactName) {
      alert('Primary contact name is required');
      return;
    }

    const contactEmail = prompt('Enter primary contact email:');
    if (!contactEmail) {
      alert('Primary contact email is required');
      return;
    }

    const contactTitle = prompt('Enter contact title (optional):') || undefined;
    const contactPhone = prompt('Enter contact phone (optional):') || undefined;

    const primaryContact: ClientContactCreate = {
      name: contactName,
      email: contactEmail,
      title: contactTitle,
      phone: contactPhone,
      is_primary: 'yes'
    };

    const newClient: ClientCreate = {
      name,
      company,
      phone,
      address,
      contacts: [primaryContact]
    };

    this.apiService.createClient(newClient).subscribe({
      next: (client) => {
        this.clients.push(client);
        alert('Client created successfully!');
      },
      error: (error) => {
        alert('Failed to create client\nTry Again');
        console.error('Create client error:', error);
      }
    });
  }

  createEngagementForClient(client: Client): void {
    const engagementName = prompt('Enter engagement name:');
    if (!engagementName) return;

    const scopeSummary = prompt('Enter scope summary (optional):') || undefined;
    const projectLead = prompt('Enter project lead (optional):') || undefined;
    const startDate = prompt('Enter start date (YYYY-MM-DD, optional):') || undefined;
    const endDate = prompt('Enter end date (YYYY-MM-DD, optional):') || undefined;

    const statusOptions = Object.values(EngagementStatus).join('\n');
    const selectedStatus = prompt(`Select status:\n${statusOptions}\n\nEnter status:`) as EngagementStatus;
    
    if (!selectedStatus || !Object.values(EngagementStatus).includes(selectedStatus)) {
      alert('Invalid status selected');
      return;
    }

    const newEngagement: EngagementCreate = {
      engagement_name: engagementName,
      client_id: client.id,
      client_name: client.name,
      status: selectedStatus,
      start_date: startDate,
      end_date: endDate,
      scope_summary: scopeSummary,
      project_lead: projectLead
    };

    this.apiService.createEngagement(newEngagement).subscribe({
      next: (engagement) => {
        this.engagements.push(engagement);
        alert('Engagement created successfully!');
      },
      error: (error) => {
        alert('Failed to create engagement\nTry Again');
        console.error('Create engagement error:', error);
      }
    });
  }

  viewClientDetails(client: Client): void {
    const engagements = this.getClientEngagements(client.id);
    let details = `Client: ${client.name}\n`;
    details += `Company: ${client.company || 'N/A'}\n`;
    details += `Phone: ${client.phone || 'N/A'}\n`;
    details += `Address: ${client.address || 'N/A'}\n\n`;
    
    details += `Contacts (${client.contacts.length}):\n`;
    client.contacts.forEach(contact => {
      details += `• ${contact.name} (${contact.email})${contact.is_primary === 'yes' ? ' - PRIMARY' : ''}\n`;
    });

    details += `\nEngagements (${engagements.length}):\n`;
    engagements.forEach(eng => {
      details += `• ${eng.engagement_name} - ${eng.status}\n`;
    });

    alert(details);
  }

  editClient(client: Client): void {
    alert('Edit functionality coming soon!');
  }

  toggleEngagementsView(): void {
    this.showEngagements = !this.showEngagements;
  }
}
