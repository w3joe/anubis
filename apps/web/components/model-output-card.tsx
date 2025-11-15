import { useState } from "react";
import { ModelResult } from "@/lib/types";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { StatusIndicator } from "@/components/status-indicator";
import { MODELS } from "@/lib/consts";
import {
  CodeBlock,
  CodeBlockHeader,
  CodeBlockCopyButton,
  CodeBlockBody,
  CodeBlockItem,
  CodeBlockContent,
} from "@/components/ui/shadcn-io/code-block";

// Helper function to clean code fences from code
function cleanCodeFences(code: string): string {
  // Remove markdown code fences like ```python or ```
  return code
    .replace(/^```[\w]*\n?/gm, "") // Remove opening fence with optional language
    .replace(/\n?```$/gm, "") // Remove closing fence
    .trim();
}

interface ModelOutputCardProps {
  result: ModelResult;
}

export function ModelOutputCard({ result }: ModelOutputCardProps) {
  const [isExpanded, setIsExpanded] = useState(false);

  const modelLabel =
    MODELS.find((m) => m.value === result.model)?.label || result.model;

  // Clean the code by removing markdown fences
  const cleanCode = result.code ? cleanCodeFences(result.code) : "";

  const showCode = result.status === "complete" && cleanCode;
  const showError = result.status === "error" && result.error;
  const showEvaluation =
    result.status === "complete" &&
    result.pros &&
    result.cons &&
    result.overallScore !== undefined;

  return (
    <Card className="w-full">
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="text-lg font-semibold">{modelLabel}</CardTitle>
          <div className="flex items-center gap-3">
            {result.executionTime && (
              <span className="text-sm text-muted-foreground">
                {result.executionTime}ms
              </span>
            )}
            <StatusIndicator status={result.status} />
          </div>
        </div>
        {showEvaluation && (
          <div className="flex items-center gap-2 mt-2">
            <span className="text-sm font-medium">Overall Score:</span>
            <span className="text-lg font-bold text-primary">
              {result.overallScore?.toFixed(2)}
            </span>
          </div>
        )}
      </CardHeader>

      <CardContent className="space-y-4">
        {result.status === "pending" && (
          <div className="p-4 text-center text-muted-foreground">
            <p className="text-sm">Waiting to start...</p>
          </div>
        )}

        {result.status === "processing" && !result.code && (
          <div className="p-4 text-center text-muted-foreground">
            <p className="text-sm">Generating code...</p>
          </div>
        )}

        {result.status === "processing" && result.code && (
          <CodeBlock
            defaultValue="python"
            data={[
              {
                language: "python",
                filename: "streaming.py",
                code: cleanCodeFences(result.code),
              },
            ]}
          >
            <CodeBlockHeader>
              <span className="text-xs text-muted-foreground px-2">
                Streaming...
              </span>
              <CodeBlockCopyButton className="ml-auto" />
            </CodeBlockHeader>
            <CodeBlockBody>
              {(item) => (
                <CodeBlockItem key={item.language} value={item.language}>
                  <CodeBlockContent syntaxHighlighting={false}>
                    {item.code}
                  </CodeBlockContent>
                </CodeBlockItem>
              )}
            </CodeBlockBody>
          </CodeBlock>
        )}

        {showError && (
          <div className="p-3 bg-red-50 border border-red-200 rounded-md">
            <p className="text-sm text-red-800">{result.error}</p>
          </div>
        )}

        {showCode && (
          <div className="space-y-2">
            {!isExpanded && (
              <div
                onClick={() => setIsExpanded(true)}
                className="relative cursor-pointer rounded-md border bg-muted p-4 max-h-32 overflow-hidden hover:border-primary/50 transition-all"
              >
                <pre className="text-xs font-mono whitespace-pre-wrap line-clamp-4">
                  {cleanCode}
                </pre>
                <div className="absolute inset-0 bg-linear-to-b from-transparent via-muted/50 to-muted backdrop-blur-[1px] rounded-md flex items-end justify-center pb-2">
                  <span className="text-xs text-muted-foreground font-medium">
                    Click to expand
                  </span>
                </div>
              </div>
            )}
            {isExpanded && (
              <>
                <CodeBlock
                  defaultValue="python"
                  data={[
                    {
                      language: "python",
                      filename: "generated.py",
                      code: cleanCode,
                    },
                  ]}
                >
                  <CodeBlockHeader>
                    <CodeBlockCopyButton className="ml-auto" />
                  </CodeBlockHeader>
                  <CodeBlockBody>
                    {(item) => (
                      <CodeBlockItem key={item.language} value={item.language}>
                        <CodeBlockContent language="python">
                          {item.code}
                        </CodeBlockContent>
                      </CodeBlockItem>
                    )}
                  </CodeBlockBody>
                </CodeBlock>
                <button
                  onClick={() => setIsExpanded(false)}
                  className="text-xs text-primary hover:underline"
                >
                  Collapse
                </button>
              </>
            )}
          </div>
        )}

        {showEvaluation && (
          <div className="space-y-4 pt-4 border-t">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <h4 className="text-sm font-semibold text-green-700 flex items-center gap-1">
                  <svg
                    className="h-4 w-4"
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 20 20"
                    fill="currentColor"
                  >
                    <path
                      fillRule="evenodd"
                      d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                      clipRule="evenodd"
                    />
                  </svg>
                  Pros
                </h4>
                <ul className="space-y-1.5 pl-1">
                  {result.pros?.map((pro, idx) => (
                    <li
                      key={idx}
                      className="text-sm text-muted-foreground flex gap-2"
                    >
                      <span className="text-green-600 shrink-0">•</span>
                      <span>{pro}</span>
                    </li>
                  ))}
                </ul>
              </div>

              <div className="space-y-2">
                <h4 className="text-sm font-semibold text-red-700 flex items-center gap-1">
                  <svg
                    className="h-4 w-4"
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 20 20"
                    fill="currentColor"
                  >
                    <path
                      fillRule="evenodd"
                      d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                      clipRule="evenodd"
                    />
                  </svg>
                  Cons
                </h4>
                <ul className="space-y-1.5 pl-1">
                  {result.cons?.map((con, idx) => (
                    <li
                      key={idx}
                      className="text-sm text-muted-foreground flex gap-2"
                    >
                      <span className="text-red-600 shrink-0">•</span>
                      <span>{con}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>

            {result.metrics && (
              <div className="space-y-2 pt-2">
                <h4 className="text-sm font-semibold">Detailed Metrics:</h4>
                <div className="space-y-2">
                  {Object.entries(result.metrics).map(([key, value]) => (
                    <div
                      key={key}
                      className="flex items-start justify-between gap-4 text-sm"
                    >
                      <span className="text-muted-foreground capitalize">
                        {key.replace(/_/g, " ")}:
                      </span>
                      <div className="flex-1 text-right space-y-0.5">
                        <div className="font-medium">
                          Score: {value.score.toFixed(2)}
                        </div>
                        <div className="text-xs text-muted-foreground">
                          {value.notes}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </CardContent>
    </Card>
  );
}
