import { Warning } from "@/lib/types";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

interface WarningsSectionProps {
  warnings: Warning[];
}

export function WarningsSection({ warnings }: WarningsSectionProps) {
  if (warnings.length === 0) {
    return null;
  }

  return (
    <Card className="border-yellow-300 bg-yellow-50">
      <CardHeader>
        <CardTitle className="text-xl flex items-center gap-2 text-yellow-900">
          <svg
            className="h-5 w-5"
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 20 20"
            fill="currentColor"
          >
            <path
              fillRule="evenodd"
              d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z"
              clipRule="evenodd"
            />
          </svg>
          Warnings
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-3">
        {warnings.map((warning) => (
          <div
            key={warning.id}
            className="p-3 rounded-md bg-yellow-100 border border-yellow-300"
          >
            <div className="flex items-start gap-2">
              <div className="flex-1">
                <p className="text-sm font-medium text-yellow-900">
                  {warning.type === "model" ? "Model Warning" : "Code Quality Warning"}
                  {warning.model && ` (${warning.model})`}
                </p>
                <p className="text-sm text-yellow-800 mt-1">{warning.message}</p>
              </div>
            </div>
          </div>
        ))}
      </CardContent>
    </Card>
  );
}

