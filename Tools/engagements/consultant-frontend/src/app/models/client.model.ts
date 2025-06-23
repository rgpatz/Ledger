export interface ClientContact {
  id: number;
  client_id: number;
  name: string;
  email: string;
  title?: string;
  phone?: string;
  is_primary: string; // "yes" or "no"
  created_at: string;
  updated_at: string;
}

export interface Client {
  id: number;
  name: string;
  company?: string;
  address?: string;
  phone?: string;
  notes?: string;
  created_at: string;
  updated_at: string;
  contacts: ClientContact[];
}

export interface ClientCreate {
  name: string;
  company?: string;
  address?: string;
  phone?: string;
  notes?: string;
  contacts: ClientContactCreate[];
}

export interface ClientContactCreate {
  name: string;
  email: string;
  title?: string;
  phone?: string;
  is_primary: string;
}

// Engagement interfaces
export interface Engagement {
  id: number;
  engagement_name: string;
  client_id: number;
  client_name: string;
  status: EngagementStatus;
  start_date?: string;
  end_date?: string;
  scope_summary?: string;
  project_lead?: string;
  created_at: string;
  updated_at: string;
  client?: Client;
}

export interface EngagementCreate {
  engagement_name: string;
  client_id: number;
  client_name: string;
  status: EngagementStatus;
  start_date?: string;
  end_date?: string;
  scope_summary?: string;
  project_lead?: string;
}

export enum EngagementStatus {
  PROPOSED = 'Proposed',
  SCOPING = 'Scoping',
  SCHEDULED = 'Scheduled',
  IN_PROGRESS = 'In Progress',
  ON_HOLD = 'On Hold',
  COMPLETED = 'Completed',
  CANCELLED = 'Cancelled'
} 