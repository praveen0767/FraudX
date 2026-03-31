"use client";

import { useQuery } from "@tanstack/react-query";
import { fetchTransactionDetail } from "@/lib/api-client";
import { useParams } from "next/navigation";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Cpu, Scale, CheckCircle2, ShieldAlert, FileText, AlertTriangle } from "lucide-react";
import { Badge } from "@/components/ui/badge";

export default function CaseDetailPage() {
  const params = useParams();
  const id = params.id as string;

  const { data, isLoading, error } = useQuery({
    queryKey: ['case', id],
    queryFn: () => fetchTransactionDetail(id),
  });

  if (isLoading) return <div className="p-8 text-zinc-400 animate-pulse">Loading case intelligence...</div>;
  if (error || !data) return <div className="p-8 text-red-400">Error loading case details.</div>;

  const isBorderline = data.contextual_agent?.triggered;

  return (
    <div className="space-y-6 max-w-7xl">
      <div className="flex justify-between items-start">
        <div>
          <div className="flex items-center gap-3">
            <h1 className="text-2xl font-bold font-mono tracking-tight">{data.transaction_id}</h1>
            <Badge variant="outline" className="border-zinc-700 bg-zinc-800">v{data.model_version || "1"}</Badge>
            <Badge variant="outline" className="border-zinc-700 bg-zinc-800">{data.latency_ms.toFixed(1)}ms Latency</Badge>
          </div>
          <p className="text-zinc-400 mt-1 flex items-center gap-2">
            <FileText className="w-4 h-4" /> Comprehensive Case Intel
          </p>
        </div>
      </div>

      <div className="flex gap-6 h-full">
        {/* LEFT COLUMN: 70% */}
        <div className="w-[70%] space-y-6">
          <Card className="bg-zinc-900 border-zinc-800 shadow-xl">
            <CardHeader className="border-b border-zinc-800/60 pb-4">
              <CardTitle className="text-lg text-zinc-100 flex items-center"><Scale className="w-5 h-5 mr-2 text-zinc-400"/> Model Breakdown</CardTitle>
            </CardHeader>
            <CardContent className="pt-6 grid grid-cols-3 gap-8">
              <div className="space-y-1">
                <span className="text-xs font-semibold text-zinc-500 uppercase tracking-wider">Base Score (LightGBM)</span>
                <div className="text-3xl font-mono">{data.model_breakdown.base_model.toFixed(3)}</div>
              </div>
              <div className="space-y-1">
                <span className="text-xs font-semibold text-zinc-500 uppercase tracking-wider">Final Risk Score</span>
                <div className="text-3xl font-mono text-zinc-100">{data.model_breakdown.final_score.toFixed(3)}</div>
              </div>
              <div className="space-y-1">
                <span className="text-xs font-semibold text-zinc-500 uppercase tracking-wider">Decision</span>
                <div className="mt-1">
                   {data.decision === "APPROVE" && <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-semibold bg-green-500/10 text-green-400"><CheckCircle2 className="w-4 h-4 mr-2"/> APPROVED</span>}
                   {data.decision === "BLOCK" && <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-semibold bg-red-500/10 text-red-400"><ShieldAlert className="w-4 h-4 mr-2"/> BLOCKED</span>}
                   {data.decision === "REVIEW" && <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-semibold bg-amber-500/10 text-amber-400"><AlertTriangle className="w-4 h-4 mr-2"/> MANUAL REVIEW</span>}
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="bg-zinc-900 border-zinc-800">
            <CardHeader className="border-b border-zinc-800/60 pb-4">
              <CardTitle className="text-lg text-zinc-100">Top SHAP Feature Impacts</CardTitle>
            </CardHeader>
            <CardContent className="pt-6">
                <div className="space-y-4">
                  {data.shap_values?.map((sv, idx) => (
                    <div key={idx} className="flex justify-between items-center text-sm border-b border-zinc-800 pb-2">
                       <span className="font-mono text-zinc-300">{sv.feature}</span>
                       <span className={sv.impact > 0.6 ? "text-red-400" : "text-amber-400"}>{sv.impact > 0.6 ? 'High Risk' : 'Medium Risk'} Impact</span>
                    </div>
                  ))}
                  {(!data.shap_values || data.shap_values.length === 0) && (
                     <div className="text-zinc-500 text-sm italic">Standard features evaluated. No extreme SHAP anomalies.</div>
                  )}
                </div>
            </CardContent>
          </Card>
        </div>

        {/* RIGHT COLUMN: 30% */}
        <div className="w-[30%] space-y-6">
          <Card className={`bg-zinc-900/80 border ${isBorderline ? 'border-indigo-500/50 shadow-[0_0_30px_-5px_rgba(99,102,241,0.2)]' : 'border-zinc-800'}`}>
            <CardHeader className={`${isBorderline ? 'bg-indigo-500/10' : 'bg-transparent'} rounded-t-xl pb-4 border-b border-zinc-800/60`}>
              <CardTitle className={`text-md flex items-center ${isBorderline ? 'text-indigo-400' : 'text-zinc-500'}`}>
                <Cpu className="w-5 h-5 mr-2" />
                Contextual Graph Agent
              </CardTitle>
              {isBorderline && <p className="text-xs text-indigo-300/70 mt-1 uppercase tracking-wider font-semibold">AI Reasoning Layer Activated</p>}
            </CardHeader>
            <CardContent className="pt-6">
              {isBorderline ? (
                <div className="space-y-4">
                  <div className="bg-black/40 p-4 rounded-md border border-indigo-500/20 text-sm text-zinc-300 leading-relaxed">
                    {data.contextual_agent?.reasoning || data.explanation}
                  </div>
                  <div>
                    <span className="text-xs text-zinc-500 tracking-wider">AGENT CONFIDENCE</span>
                    <div className="w-full bg-zinc-800 h-2 rounded-full mt-1 overflow-hidden">
                       <div className="bg-indigo-500 h-full rounded-full" style={{ width: `${(data.contextual_agent?.confidence || 0.85) * 100}%` }}></div>
                    </div>
                  </div>
                </div>
              ) : (
                <div className="text-sm text-zinc-500 text-center py-8">
                  Graph Agent bypassed.<br/>Score was highly deterministic.
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
