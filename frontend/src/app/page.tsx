import Link from "next/link";

import { Button } from "@/components/ui/button";

export default function Home() {
  return (
    <main className="mx-auto flex min-h-screen max-w-3xl flex-col items-start justify-center gap-6 px-8 py-24">
      <h1 className="text-4xl font-semibold tracking-tight">OAuth Playground</h1>
      <p className="max-w-xl text-zinc-600">
        Next.js + TypeScript + TailwindCSS + shadcn/ui frontend scaffolded for a
        DDD + hexagonal backend.
      </p>
      <div className="flex gap-3">
        <Button asChild>
          <Link href="http://localhost:8000/docs">Open API docs</Link>
        </Button>
        <Button asChild variant="outline">
          <Link href="http://localhost:8000/health">Check backend health</Link>
        </Button>
      </div>
    </main>
  );
}
