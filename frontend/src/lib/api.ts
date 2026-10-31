/**
 * API Client for TradeScope Backend
 * Handles authentication, backtests, and Stripe
 */
import axios, { AxiosInstance } from 'axios';
import {
  AuthResponse,
  LoginRequest,
  RegisterRequest,
  User,
  Backtest,
  BacktestCreate,
  BacktestListResponse,
} from '@/types';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

class ApiClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Add token to requests if available
    this.client.interceptors.request.use((config) => {
      const token = this.getToken();
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    });
  }

  // Token management
  private getToken(): string | null {
    if (typeof window === 'undefined') return null;
    return localStorage.getItem('token');
  }

  private setToken(token: string) {
    if (typeof window !== 'undefined') {
      localStorage.setItem('token', token);
    }
  }

  private removeToken() {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('token');
    }
  }

  // Auth endpoints
  async register(data: RegisterRequest): Promise<AuthResponse> {
    const response = await this.client.post<AuthResponse>('/api/auth/register', data);
    this.setToken(response.data.access_token);
    return response.data;
  }

  async login(data: LoginRequest): Promise<AuthResponse> {
    const response = await this.client.post<AuthResponse>('/api/auth/login', data);
    this.setToken(response.data.access_token);
    return response.data;
  }

  async getCurrentUser(): Promise<User> {
    const response = await this.client.get<User>('/api/auth/me');
    return response.data;
  }

  logout() {
    this.removeToken();
  }

  // Backtest endpoints
  async createBacktest(data: BacktestCreate): Promise<Backtest> {
    const response = await this.client.post<Backtest>('/api/backtest/', data);
    return response.data;
  }

  async listBacktests(skip = 0, limit = 50): Promise<BacktestListResponse> {
    const response = await this.client.get<BacktestListResponse>('/api/backtest/', {
      params: { skip, limit },
    });
    return response.data;
  }

  async getBacktest(id: number): Promise<Backtest> {
    const response = await this.client.get<Backtest>(`/api/backtest/${id}`);
    return response.data;
  }

  async deleteBacktest(id: number): Promise<void> {
    await this.client.delete(`/api/backtest/${id}`);
  }

  // Stripe endpoints
  async createCheckoutSession(): Promise<{ checkout_url: string; session_id: string }> {
    const response = await this.client.post('/api/stripe/create-checkout-session');
    return response.data;
  }

  async createCustomerPortal(): Promise<{ portal_url: string }> {
    const response = await this.client.post('/api/stripe/customer-portal');
    return response.data;
  }
}

export const api = new ApiClient();
