/**
 * Strategy Creation Form
 * Form to create a new backtest
 */
'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { useBacktestStore } from '@/lib/store';
import { BacktestCreate } from '@/types';

export function StrategyForm() {
  const { createBacktest } = useBacktestStore();
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    symbol: 'BTC/USDT',
    timeframe: '1h',
    start_date: '2024-01-01',
    end_date: '2024-03-01',
    strategy_type: 'SMA_CROSSOVER',
    fast_period: '10',
    slow_period: '30',
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      const backtestData: BacktestCreate = {
        name: formData.name,
        symbol: formData.symbol,
        timeframe: formData.timeframe,
        start_date: new Date(formData.start_date).toISOString(),
        end_date: new Date(formData.end_date).toISOString(),
        strategy_type: formData.strategy_type,
        strategy_params: {
          fast_period: parseInt(formData.fast_period),
          slow_period: parseInt(formData.slow_period),
        },
      };

      await createBacktest(backtestData);
      alert('Backtest started! Check the dashboard for results.');
      
      // Reset form
      setFormData({
        name: '',
        symbol: 'BTC/USDT',
        timeframe: '1h',
        start_date: '2024-01-01',
        end_date: '2024-03-01',
        strategy_type: 'SMA_CROSSOVER',
        fast_period: '10',
        slow_period: '30',
      });
    } catch (error) {
      alert('Failed to create backtest');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Create Backtest</CardTitle>
        <CardDescription>Configure your trading strategy parameters</CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="name">Strategy Name</Label>
              <Input
                id="name"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                placeholder="My BTC Strategy"
                required
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="symbol">Symbol</Label>
              <Input
                id="symbol"
                value={formData.symbol}
                onChange={(e) => setFormData({ ...formData, symbol: e.target.value })}
                placeholder="BTC/USDT"
                required
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="timeframe">Timeframe</Label>
              <select
                id="timeframe"
                value={formData.timeframe}
                onChange={(e) => setFormData({ ...formData, timeframe: e.target.value })}
                className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
              >
                <option value="1h">1 Hour</option>
                <option value="4h">4 Hours</option>
                <option value="1d">1 Day</option>
              </select>
            </div>

            <div className="space-y-2">
              <Label htmlFor="strategy_type">Strategy Type</Label>
              <select
                id="strategy_type"
                value={formData.strategy_type}
                onChange={(e) => setFormData({ ...formData, strategy_type: e.target.value })}
                className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
              >
                <option value="SMA_CROSSOVER">SMA Crossover</option>
                <option value="RSI">RSI Strategy</option>
              </select>
            </div>

            <div className="space-y-2">
              <Label htmlFor="start_date">Start Date</Label>
              <Input
                id="start_date"
                type="date"
                value={formData.start_date}
                onChange={(e) => setFormData({ ...formData, start_date: e.target.value })}
                required
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="end_date">End Date</Label>
              <Input
                id="end_date"
                type="date"
                value={formData.end_date}
                onChange={(e) => setFormData({ ...formData, end_date: e.target.value })}
                required
              />
            </div>

            {formData.strategy_type === 'SMA_CROSSOVER' && (
              <>
                <div className="space-y-2">
                  <Label htmlFor="fast_period">Fast SMA Period</Label>
                  <Input
                    id="fast_period"
                    type="number"
                    value={formData.fast_period}
                    onChange={(e) => setFormData({ ...formData, fast_period: e.target.value })}
                    required
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="slow_period">Slow SMA Period</Label>
                  <Input
                    id="slow_period"
                    type="number"
                    value={formData.slow_period}
                    onChange={(e) => setFormData({ ...formData, slow_period: e.target.value })}
                    required
                  />
                </div>
              </>
            )}
          </div>

          <Button type="submit" disabled={loading} className="w-full">
            {loading ? 'Creating...' : 'Run Backtest'}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}
