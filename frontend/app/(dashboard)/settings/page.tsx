export default function SettingsPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold tracking-tight">Settings</h1>
      <p className="text-zinc-400">Global platform configuration.</p>
      <div className="p-8 border border-zinc-800 border-dashed rounded bg-zinc-900/50 text-center text-zinc-500">
        Backend URL: http://api:8000
      </div>
    </div>
  );
}
