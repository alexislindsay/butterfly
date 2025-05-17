"use client";

import { useState } from "react";
import { Card, CardContent } from "../components/ui/card";
import { ScrollArea } from "../components/ui/scroll-area";

const rituals = [ /* …your array of rituals… */ ];

export default function Page() {
  const [selected, setSelected] = useState(null);

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      {/* Page Title */}
      <h1 className="text-4xl font-extrabold text-center mb-8">
        Ecocentric Reset Rituals
      </h1>

      <div className="grid grid-cols-1 md:grid-cols-[250px_1fr] gap-6">
        {/* Sidebar */}
        <ScrollArea className="h-[75vh] bg-white rounded-2xl shadow-lg p-4">
          <h2 className="text-2xl font-semibold mb-4">Rituals</h2>
          <div className="space-y-3">
            {rituals.map((r) => (
              <Card
                key={r.id}
                className={`
                  cursor-pointer transition
                  ${selected?.id === r.id 
                    ? "ring-2 ring-green-500" 
                    : "hover:shadow-xl"}
                `}
                onClick={() => setSelected(r)}
              >
                <CardContent>
                  <h3 className="text-lg font-medium">{r.title}</h3>
                </CardContent>
              </Card>
            ))}
          </div>
        </ScrollArea>

        {/* Detail Panel */}
        <div className="h-[75vh] bg-white rounded-2xl shadow-lg p-6 overflow-auto">
          {selected ? (
            <>
              <h2 className="text-3xl font-semibold mb-4">
                {selected.title}
              </h2>
              {/* Use Tailwind Typography if you have it, or just plain <pre> */}
              <div className="prose max-w-none">
                {selected.content.split("\n\n").map((para, i) => (
                  <p key={i}>{para}</p>
                ))}
              </div>
            </>
          ) : (
            <div className="flex h-full items-center justify-center">
              <p className="text-gray-400 text-xl italic">
                Select a ritual to view its details.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
