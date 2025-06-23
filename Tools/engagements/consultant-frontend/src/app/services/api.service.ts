import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, retry } from 'rxjs/operators';
import { Client, ClientCreate, ClientContact, Engagement, EngagementCreate } from '../models/client.model';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private baseUrl = 'http://localhost:8000/api/v1';

  constructor(private http: HttpClient) { }

  // Error handling
  private handleError(error: HttpErrorResponse) {
    console.error('API Error:', error);
    if (error.status === 0) {
      // CORS or network error
      console.error('CORS Error: Make sure your backend allows requests from http://localhost:4200');
      console.error('You can also run Chrome with --disable-web-security for development');
    }
    return throwError(() => error);
  }

  // Client endpoints
  getClients(): Observable<Client[]> {
    return this.http.get<Client[]>(`${this.baseUrl}/clients/`)
      .pipe(
        retry(2),
        catchError(this.handleError.bind(this))
      );
  }

  getClient(id: number): Observable<Client> {
    return this.http.get<Client>(`${this.baseUrl}/clients/${id}`)
      .pipe(
        retry(2),
        catchError(this.handleError.bind(this))
      );
  }

  createClient(client: ClientCreate): Observable<Client> {
    return this.http.post<Client>(`${this.baseUrl}/clients/`, client)
      .pipe(
        catchError(this.handleError.bind(this))
      );
  }

  updateClient(id: number, client: Partial<Client>): Observable<Client> {
    return this.http.put<Client>(`${this.baseUrl}/clients/${id}`, client)
      .pipe(
        catchError(this.handleError.bind(this))
      );
  }

  deleteClient(id: number): Observable<Client> {
    return this.http.delete<Client>(`${this.baseUrl}/clients/${id}`)
      .pipe(
        catchError(this.handleError.bind(this))
      );
  }

  // Engagement endpoints
  getEngagements(): Observable<Engagement[]> {
    return this.http.get<Engagement[]>(`${this.baseUrl}/engagements/`)
      .pipe(
        retry(2),
        catchError(this.handleError.bind(this))
      );
  }

  getEngagement(id: number): Observable<Engagement> {
    return this.http.get<Engagement>(`${this.baseUrl}/engagements/${id}`)
      .pipe(
        retry(2),
        catchError(this.handleError.bind(this))
      );
  }

  getEngagementsByClient(clientId: number): Observable<Engagement[]> {
    return this.http.get<Engagement[]>(`${this.baseUrl}/engagements/client/${clientId}`)
      .pipe(
        retry(2),
        catchError(this.handleError.bind(this))
      );
  }

  createEngagement(engagement: EngagementCreate): Observable<Engagement> {
    return this.http.post<Engagement>(`${this.baseUrl}/engagements/`, engagement)
      .pipe(
        catchError(this.handleError.bind(this))
      );
  }

  updateEngagement(id: number, engagement: Partial<EngagementCreate>): Observable<Engagement> {
    return this.http.put<Engagement>(`${this.baseUrl}/engagements/${id}`, engagement)
      .pipe(
        catchError(this.handleError.bind(this))
      );
  }

  deleteEngagement(id: number): Observable<Engagement> {
    return this.http.delete<Engagement>(`${this.baseUrl}/engagements/${id}`)
      .pipe(
        catchError(this.handleError.bind(this))
      );
  }
} 