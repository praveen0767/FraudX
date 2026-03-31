"use client";

import { useUIStore } from "@/store/ui-store";
import { triggerSimulation } from "@/lib/api-client";
import { useMutation } from "@tanstack/react-query";
import { Activity, ShieldAlert, Cpu, CheckCircle } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

export default function DashboardPage() {
  const { transactions, addTransaction } = useUIStore();

  const simulateMutation = useMutation({
    mutationFn: triggerSimulation,
    onSuccess: (data) => {
      // Mocking the base transaction metadata since backend response only has Decision
      addTransaction({
        transaction_id: data.transaction_id,
        user_id: data.transaction_id.substring(0,6),
        amount: Math.random() * 1000,
        merchant: "M" + Math.floor(Math.random() * 100),
        device_id: "DEV_" + Math.floor(Math.random() * 100),
        location: null,
        timestamp: new Date().toISOString(),
        fraud_score: data.fraud_score,
        decision: data.decision as any,
        decisionDetail: data
      });
    },
    onError: (error: any) => {
      alert(`API Error: ${error.message || "Failed to reach backend"}`);
    }
  });

  const isLoading = simulateMutation.isPending;

  const total = transactions.length;
  const blocks = transactions.filter(t => t.decision === "BLOCK").length;
  const reviews = transactions.filter(t => t.decision === "REVIEW").length;
  const rcgaCount = transactions.filter(t => t.decisionDetail?.contextual_agent?.triggered).length;

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Operations Overview</h1>
          <p className="text-sm text-zinc-400 mt-1">Real-time telemetry and decision metrics.</p>
        </div>
        <div className="flex gap-2">
          <Button onClick={() => simulateMutation.mutate("normal")} disabled={isLoading} variant="outline" className="border-green-500/20 text-green-400 hover:bg-green-500/10">
            {isLoading ? "..." : "Simulate Normal"}
          </Button>
          <Button onClick={() => simulateMutation.mutate("borderline")} disabled={isLoading} variant="outline" className="border-amber-500/20 text-amber-400 hover:bg-amber-500/10">
            {isLoading ? "..." : "Simulate Borderline"}
          </Button>
          <Button onClick={() => simulateMutation.mutate("fraud")} disabled={isLoading} variant="outline" className="border-red-500/20 text-red-400 hover:bg-red-500/10">
            {isLoading ? "..." : "Simulate Fraud"}
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-4 gap-4">
        <Card className="bg-zinc-900 border-zinc-800">
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-zinc-400">Total Processed (Session)</CardTitle>
            <Activity className="h-4 w-4 text-zinc-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{total}</div>
          </CardContent>
        </Card>
        <Card className="bg-zinc-900 border-zinc-800">
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-zinc-400">Auto-Blocked</CardTitle>
            <ShieldAlert className="h-4 w-4 text-red-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-red-400">{blocks}</div>
          </CardContent>
        </Card>
        <Card className="bg-zinc-900 border-zinc-800">
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-zinc-400">Under Review</CardTitle>
            <CheckCircle className="h-4 w-4 text-amber-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-amber-400">{reviews}</div>
          </CardContent>
        </Card>
        <Card className="bg-zinc-900 border-zinc-800 relative overflow-hidden ring-1 ring-indigo-500/30">
          <div className="absolute top-0 left-0 w-1 h-full bg-indigo-500"></div>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-indigo-300">RCGA Agent Triggers</CardTitle>
            <Cpu className="h-4 w-4 text-indigo-400" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-indigo-400">{rcgaCount}</div>
            <p className="text-xs text-indigo-500/70 mt-1">Contextual Graph Resolutions</p>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-3 gap-6">
        <div className="col-span-2 space-y-4">
           {/* Trend Chart Mock for now */}
           <Card className="bg-zinc-900 border-zinc-800 h-[300px] flex items-center justify-center">
             <span className="text-zinc-600">Real-Time Volume Chart Placeholder</span>
           </Card>
        </div>
        
        <div className="col-span-1">
          <Card className="bg-zinc-900 border-zinc-800 h-[300px]">
            <CardHeader>
               <CardTitle className="text-md text-amber-400">Borderline Focus Panel</CardTitle>
            </CardHeader>
            <CardContent>
               <div className="space-y-3">
                 {transactions.filter(t => t.fraud_score! > 0.4 && t.fraud_score! < 0.7).slice(0, 5).map(t => (
                   <div key={t.transaction_id} className="flex justify-between items-center text-sm p-2 border border-zinc-800 rounded bg-zinc-950">
                     <span className="font-mono text-xs truncate w-24">{t.transaction_id}</span>
                     <span className="text-indigo-400 bg-indigo-500/10 px-2 py-0.5 rounded text-xs">{t.decision}</span>
                   </div>
                 ))}
                 {transactions.filter(t => t.fraud_score! > 0.4 && t.fraud_score! < 0.7).length === 0 && (
                   <div className="text-zinc-500 text-sm text-center py-8">No borderline cases yet.</div>
                 )}
               </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
