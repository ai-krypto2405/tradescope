/**
 * TypeScript type definitions for TradeScope
 */

export interface User {
  id: number;
  email: string;
  username: string;
  is_active: boolean;
  is_premium: boolean;
  created_at: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  username: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export type BacktestStatus = 'pending' | 'running' | 'completed' | 'failed';

export interface BacktestCreate {
  name: string;
  symbol: string;
  timeframe: string;
  start_date: string;
  end_date: string;
  strategy_type: string;
  strategy_params: Record<string, any>;
}

export interface Backtest {
  id: number;
  user_id: number;
  name: string;
  symbol: string;
  timeframe: string;
  start_date: string;
  end_date: string;
  strategy_type: string;
  strategy_params: Record<string, any>;
  status: BacktestStatus;
  celery_task_id: string | null;
  results: BacktestResults | null;
  total_return: number | null;
  sharpe_ratio: number | null;
  max_drawdown: number | null;
  win_rate: number | null;
  total_trades: number | null;
  error_message: string | null;
  created_at: string;
  completed_at: string | null;
}

export interface BacktestResults {
  total_return: number;
  sharpe_ratio: number;
  max_drawdown: number;
  win_rate: number;
  total_trades: number;
  final_equity: number;
  initial_equity: number;
  avg_trade: number;
  max_trade_duration: string;
  avg_trade_duration: string;
  detailed_stats: Record<string, any>;
}

export interface BacktestListResponse {
  backtests: Backtest[];
  total: number;
}
