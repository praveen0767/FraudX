"use client";

import { useQuery } from "@tanstack/react-query";
import { fetchMetrics } from "@/lib/api-client";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Activity, Gauge, IterationCcw } from "lucide-react";

export default function MonitoringPage() {
  const { data, isLoading } = useQuery({
    queryKey: ['metrics'],
    queryFn: fetchMetrics,
    refetchInterval: 5000
  });

  if (isLoading) return <div className="p-8 text-zinc-400">Loading telemetry...</div>;

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold tracking-tight">System Monitoring</h1>
      
      <div className="grid grid-cols-4 gap-4">
        <Card className="bg-zinc-900 border-zinc-800">
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-zinc-400">Throughput</CardTitle>
            <Activity className="h-4 w-4 text-emerald-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{data?.throughput.toFixed(1)} <span className="text-sm font-normal text-zinc-500">TPS</span></div>
          </CardContent>
        </Card>
        
        <Card className="bg-zinc-900 border-zinc-800">
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-zinc-400">p95 Latency</CardTitle>
            <Gauge className="h-4 w-4 text-amber-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{data?.latency_p95.toFixed(1)} <span className="text-sm font-normal text-zinc-500">ms</span></div>
          </CardContent>
        </Card>

        <Card className="bg-zinc-900 border-zinc-800">
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-zinc-400">Model Version</CardTitle>
            <IterationCcw className="h-4 w-4 text-indigo-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold font-mono">{data?.model_version}</div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
