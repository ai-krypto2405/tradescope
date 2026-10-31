/**
 * Backtest Results Display
 * Shows detailed results of a completed backtest
 */
'use client';

import { Backtest } from '@/types';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { formatPercent, formatCurrency, formatDateTime } from '@/lib/utils';

interface ResultsDisplayProps {
  backtest: Backtest;
}

export function ResultsDisplay({ backtest }: ResultsDisplayProps) {
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'text-green-600';
      case 'running':
        return 'text-blue-600';
      case 'failed':
        return 'text-red-600';
      default:
        return 'text-gray-600';
    }
  };

  const getReturnColor = (value: number) => {
    return value >= 0 ? 'text-green-600' : 'text-red-600';
  };

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>{backtest.name}</CardTitle>
          <CardDescription>
            {backtest.symbol} • {backtest.timeframe} • {' '}
            <span className={getStatusColor(backtest.status)}>
              {backtest.status.toUpperCase()}
            </span>
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div>
              <p className="text-muted-foreground">Strategy</p>
              <p className="font-medium">{backtest.strategy_type.replace('_', ' ')}</p>
            </div>
            <div>
              <p className="text-muted-foreground">Created</p>
              <p className="font-medium">{formatDateTime(backtest.created_at)}</p>
            </div>
          </div>
        </CardContent>
      </Card>

      {backtest.status === 'completed' && backtest.results && (
        <>
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
            <Card>
              <CardHeader className="pb-3">
                <CardDescription>Total Return</CardDescription>
                <CardTitle className={`text-3xl ${getReturnColor(backtest.total_return || 0)}`}>
                  {formatPercent(backtest.total_return || 0)}
                </CardTitle>
              </CardHeader>
            </Card>

            <Card>
              <CardHeader className="pb-3">
                <CardDescription>Sharpe Ratio</CardDescription>
                <CardTitle className="text-3xl">
                  {backtest.sharpe_ratio?.toFixed(2) || 'N/A'}
                </CardTitle>
              </CardHeader>
            </Card>

            <Card>
              <CardHeader className="pb-3">
                <CardDescription>Max Drawdown</CardDescription>
                <CardTitle className="text-3xl text-red-600">
                  {formatPercent(backtest.max_drawdown || 0)}
                </CardTitle>
              </CardHeader>
            </Card>

            <Card>
              <CardHeader className="pb-3">
                <CardDescription>Win Rate</CardDescription>
                <CardTitle className="text-3xl">
                  {formatPercent(backtest.win_rate || 0)}
                </CardTitle>
              </CardHeader>
            </Card>
          </div>

          <Card>
            <CardHeader>
              <CardTitle>Detailed Statistics</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 md:grid-cols-3 gap-4 text-sm">
                <div>
                  <p className="text-muted-foreground">Total Trades</p>
                  <p className="font-medium text-lg">{backtest.total_trades}</p>
                </div>
                <div>
                  <p className="text-muted-foreground">Final Equity</p>
                  <p className="font-medium text-lg">
                    {formatCurrency(backtest.results.final_equity)}
                  </p>
                </div>
                <div>
                  <p className="text-muted-foreground">Average Trade</p>
                  <p className="font-medium text-lg">
                    {formatPercent(backtest.results.avg_trade)}
                  </p>
                </div>
                <div>
                  <p className="text-muted-foreground">Max Trade Duration</p>
                  <p className="font-medium text-lg">{backtest.results.max_trade_duration}</p>
                </div>
                <div>
                  <p className="text-muted-foreground">Avg Trade Duration</p>
                  <p className="font-medium text-lg">{backtest.results.avg_trade_duration}</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </>
      )}

      {backtest.status === 'failed' && (
        <Card className="border-red-200">
          <CardHeader>
            <CardTitle className="text-red-600">Error</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground">{backtest.error_message}</p>
          </CardContent>
        </Card>
      )}

      {backtest.status === 'running' && (
        <Card className="border-blue-200">
          <CardContent className="pt-6">
            <p className="text-center text-muted-foreground">
              Backtest is running... Please wait.
            </p>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
