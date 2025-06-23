import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../services/api.service';
import { Engagement, EngagementStatus, Client } from '../../models/client.model';

@Component({
  selector: 'app-engagements-list',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './engagements-list.component.html',
  styleUrl: './engagements-list.component.css'
})
export class EngagementsListComponent implements OnInit {
  engagements: Engagement[] = [];
  clients: Client[] = [];
  loading = false;
  error: string | null = null;

  constructor(private apiService: ApiService) {}

  ngOnInit(): void {
    this.loadEngagements();
    this.loadClients();
  }

  loadEngagements(): void {
    this.loading = true;
    this.error = null;
    
    this.apiService.getEngagements().subscribe({
      next: (engagements) => {
        this.engagements = engagements;
        this.loading = false;
        console.log('Loaded engagements:', engagements);
      },
      error: (error) => {
        console.error('Error loading engagements:', error);
        this.error = 'Failed to load engagements. Please check your connection.';
        this.loading = false;
      }
    });
  }

  loadClients(): void {
    this.apiService.getClients().subscribe({
      next: (clients) => {
        this.clients = clients;
        console.log('Loaded clients for reference:', clients);
      },
      error: (error) => {
        console.error('Error loading clients:', error);
      }
    });
  }

  getClientById(clientId: number): Client | undefined {
    return this.clients.find(client => client.id === clientId);
  }

  getStatusBadgeClass(status: EngagementStatus): string {
    switch (status) {
      case EngagementStatus.PROPOSED:
        return 'badge-neutral';
      case EngagementStatus.SCOPING:
        return 'badge-info';
      case EngagementStatus.SCHEDULED:
        return 'badge-primary';
      case EngagementStatus.IN_PROGRESS:
        return 'badge-warning';
      case EngagementStatus.ON_HOLD:
        return 'badge-secondary';
      case EngagementStatus.COMPLETED:
        return 'badge-success';
      case EngagementStatus.CANCELLED:
        return 'badge-error';
      default:
        return 'badge-ghost';
    }
  }

  viewEngagementDetails(engagement: Engagement): void {
    const client = engagement.client || this.getClientById(engagement.client_id);
    let details = `Engagement: ${engagement.engagement_name}\n`;
    details += `Status: ${engagement.status}\n`;
    details += `Client: ${engagement.client_name}\n`;
    details += `Project Lead: ${engagement.project_lead || 'N/A'}\n`;
    details += `Start Date: ${engagement.start_date || 'N/A'}\n`;
    details += `End Date: ${engagement.end_date || 'N/A'}\n`;
    details += `Scope: ${engagement.scope_summary || 'N/A'}\n\n`;
    
    if (client) {
      details += `Client Details:\n`;
      details += `Company: ${client.company || 'N/A'}\n`;
      details += `Phone: ${client.phone || 'N/A'}\n`;
      details += `Contacts: ${client.contacts.length}\n`;
      if (client.contacts.length > 0) {
        const primaryContact = client.contacts.find(c => c.is_primary === 'yes');
        if (primaryContact) {
          details += `Primary Contact: ${primaryContact.name} (${primaryContact.email})`;
        }
      }
    }

    alert(details);
  }

  editEngagement(engagement: Engagement): void {
    alert('Edit engagement functionality coming soon!');
  }

  deleteEngagement(id: number): void {
    if (confirm('Are you sure you want to delete this engagement?')) {
      this.apiService.deleteEngagement(id).subscribe({
        next: () => {
          this.engagements = this.engagements.filter(eng => eng.id !== id);
          alert('Engagement deleted successfully!');
        },
        error: (error) => {
          console.error('Error deleting engagement:', error);
          alert('Failed to delete engagement');
        }
      });
    }
  }
}
