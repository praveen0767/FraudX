"use client";

import { useUIStore } from "@/store/ui-store";
import { format } from "date-fns";
import { useRouter } from "next/navigation";
import { Badge } from "@/components/ui/badge";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

export default function TransactionsPage() {
  const { transactions } = useUIStore();
  const router = useRouter();

  const getStatusBadge = (decision?: string) => {
    switch(decision) {
      case "APPROVE": return <Badge variant="outline" className="border-green-500 text-green-400">APPROVED</Badge>;
      case "BLOCK": return <Badge variant="outline" className="border-red-500 text-red-400">BLOCKED</Badge>;
      case "REVIEW": return <Badge variant="outline" className="border-amber-500 text-amber-400 bg-amber-500/10">MANUAL REVIEW</Badge>;
      default: return <Badge variant="outline" className="border-zinc-500 text-zinc-400">UNKNOWN</Badge>;
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Review Queue</h1>
          <p className="text-sm text-zinc-400 mt-1">Live stream of transactions and model decisions.</p>
        </div>
      </div>

      <div className="border border-zinc-800 rounded-md bg-zinc-900/50 overflow-hidden">
        <Table>
          <TableHeader className="bg-zinc-900 border-b border-zinc-800">
            <TableRow className="hover:bg-transparent">
              <TableHead className="text-zinc-400">Timestamp</TableHead>
              <TableHead className="text-zinc-400">Transaction ID</TableHead>
              <TableHead className="text-zinc-400">Amount</TableHead>
              <TableHead className="text-zinc-400 text-right">Base Score</TableHead>
              <TableHead className="text-zinc-400">Agent</TableHead>
              <TableHead className="text-zinc-400">Status</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {transactions.length === 0 && (
              <TableRow>
                <TableCell colSpan={6} className="h-24 text-center text-zinc-500">
                  No transactions in current session. Trigger a simulation.
                </TableCell>
              </TableRow>
            )}
            {transactions.map((tx) => (
              <TableRow 
                key={tx.transaction_id} 
                className="hover:bg-zinc-800/50 cursor-pointer border-b border-zinc-800/50 transition-colors"
                onClick={() => router.push(`/cases/${tx.transaction_id}`)}
              >
                <TableCell className="font-mono text-xs text-zinc-400">
                  {format(new Date(tx.timestamp), "HH:mm:ss.SSS")}
                </TableCell>
                <TableCell className="font-mono text-xs text-zinc-300">
                  {tx.transaction_id.substring(0,8)}...
                </TableCell>
                <TableCell className="font-medium">
                  ${tx.amount.toFixed(2)}
                </TableCell>
                <TableCell className="text-right font-mono text-sm">
                  <span className={tx.fraud_score && tx.fraud_score > 0.7 ? "text-red-400" : tx.fraud_score && tx.fraud_score > 0.4 ? "text-amber-400" : "text-green-400"}>
                    {tx.fraud_score?.toFixed(3)}
                  </span>
                </TableCell>
                <TableCell>
                  {tx.decisionDetail?.contextual_agent?.triggered ? (
                     <Badge variant="outline" className="border-indigo-500/30 text-indigo-400 bg-indigo-500/10">RCGA</Badge>
                  ) : (
                     <span className="text-zinc-600 text-xs">-</span>
                  )}
                </TableCell>
                <TableCell>
                  {getStatusBadge(tx.decision)}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}
