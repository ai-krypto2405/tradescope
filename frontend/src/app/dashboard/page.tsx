/**
 * Dashboard Page
 * Main app interface - shows backtests and strategy creation
 */
'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { StrategyForm } from '@/components/StrategyForm';
import { ResultsDisplay } from '@/components/ResultsDisplay';
import { useAuthStore, useBacktestStore } from '@/lib/store';
import { Backtest } from '@/types';
import { formatDateTime, formatPercent } from '@/lib/utils';
import { api } from '@/lib/api';

export default function DashboardPage() {
  const router = useRouter();
  const { user, isAuthenticated, logout, refreshUser } = useAuthStore();
  const { backtests, fetchBacktests } = useBacktestStore();
  const [selectedBacktest, setSelectedBacktest] = useState<Backtest | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const init = async () => {
      try {
        await refreshUser();
        await fetchBacktests();
      } catch (error) {
        router.push('/login');
      } finally {
        setLoading(false);
      }
    };

    init();
  }, []);

  const handleLogout = () => {
    logout();
    router.push('/');
  };

  const handleUpgrade = async () => {
    try {
      const { checkout_url } = await api.createCheckoutSession();
      window.location.href = checkout_url;
    } catch (error) {
      alert('Failed to create checkout session');
    }
  };

  const getStatusBadge = (status: string) => {
    const colors = {
      pending: 'bg-gray-100 text-gray-800',
      running: 'bg-blue-100 text-blue-800',
      completed: 'bg-green-100 text-green-800',
      failed: 'bg-red-100 text-red-800',
    };
    return colors[status as keyof typeof colors] || colors.pending;
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p>Loading...</p>
      </div>
    );
  }

  if (!isAuthenticated) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b">
        <div className="container mx-auto px-4 py-4">
          <nav className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <h1 className="text-2xl font-bold text-blue-600">TradeScope</h1>
              {user?.is_premium && (
                <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-sm font-medium">
                  Premium
                </span>
              )}
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-600">
                Welcome, {user?.username}
              </span>
              {!user?.is_premium && (
                <Button variant="outline" onClick={handleUpgrade}>
                  Upgrade to Premium
                </Button>
              )}
              <Button variant="ghost" onClick={handleLogout}>
                Logout
              </Button>
            </div>
          </nav>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        <div className="grid lg:grid-cols-2 gap-8">
          {/* Left: Strategy Form */}
          <div>
            <StrategyForm />
          </div>

          {/* Right: Backtests List */}
          <div className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Your Backtests</CardTitle>
                <CardDescription>
                  {backtests.length} backtest{backtests.length !== 1 ? 's' : ''} created
                </CardDescription>
              </CardHeader>
              <CardContent>
                {backtests.length === 0 ? (
                  <p className="text-center text-muted-foreground py-8">
                    No backtests yet. Create your first strategy!
                  </p>
                ) : (
                  <div className="space-y-3">
                    {backtests.map((backtest) => (
                      <div
                        key={backtest.id}
                        className="border rounded-lg p-4 hover:bg-gray-50 cursor-pointer transition"
                        onClick={() => setSelectedBacktest(backtest)}
                      >
                        <div className="flex items-start justify-between">
                          <div>
                            <h4 className="font-medium">{backtest.name}</h4>
                            <p className="text-sm text-muted-foreground">
                              {backtest.symbol} • {backtest.timeframe}
                            </p>
                            <p className="text-xs text-muted-foreground mt-1">
                              {formatDateTime(backtest.created_at)}
                            </p>
                          </div>
                          <div className="text-right">
                            <span className={`px-2 py-1 rounded text-xs ${getStatusBadge(backtest.status)}`}>
                              {backtest.status}
                            </span>
                            {backtest.total_return !== null && (
                              <p className={`text-lg font-bold mt-1 ${
                                backtest.total_return >= 0 ? 'text-green-600' : 'text-red-600'
                              }`}>
                                {formatPercent(backtest.total_return)}
                              </p>
                            )}
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        </div>

        {/* Backtest Details Modal/Section */}
        {selectedBacktest && (
          <div className="mt-8">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-2xl font-bold">Backtest Details</h2>
              <Button variant="outline" onClick={() => setSelectedBacktest(null)}>
                Close
              </Button>
            </div>
            <ResultsDisplay backtest={selectedBacktest} />
          </div>
        )}
      </main>
    </div>
  );
}
