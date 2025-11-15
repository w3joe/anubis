import { Recommendation } from "@/lib/types";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  CodeBlock,
  CodeBlockHeader,
  CodeBlockCopyButton,
  CodeBlockBody,
  CodeBlockItem,
  CodeBlockContent,
  CodeBlockFiles,
  CodeBlockFilename,
} from "@/components/ui/shadcn-io/code-block";

// Helper function to clean code fences from code
function cleanCodeFences(code: string): string {
  // Remove markdown code fences like ```python or ```
  return code
    .replace(/^```[\w]*\n?/gm, "") // Remove opening fence with optional language
    .replace(/\n?```$/gm, "") // Remove closing fence
    .trim();
}

interface RecommendationSectionProps {
  recommendation: Recommendation | null;
}

export function RecommendationSection({
  recommendation,
}: RecommendationSectionProps) {
  if (!recommendation) {
    return null;
  }

  const cleanCode = cleanCodeFences(recommendation.code);

  return (
    <Card className="border-green-300 bg-green-50">
      <CardHeader>
        <CardTitle className="text-xl flex items-center gap-2 text-green-900">
          <svg
            className="h-5 w-5"
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
          Recommendation:{" "}
          <span className="font-bold text-green-700">
            {recommendation.bestModel}
          </span>
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="space-y-2">
          <p className="text-sm text-green-900 font-medium">Overall Score:</p>
          <p className="text-2xl font-bold text-green-700">
            {recommendation.bestScore.toFixed(2)} / 10
          </p>
        </div>

        {recommendation.potentialIssues && (
          <div className="space-y-2">
            <p className="text-sm text-green-900 font-medium">Analysis:</p>
            <p className="text-sm text-green-800 whitespace-pre-wrap">
              {recommendation.potentialIssues}
            </p>
          </div>
        )}

        <div className="space-y-2">
          <p className="text-sm text-green-900 font-medium">
            Recommended Code:
          </p>
          <CodeBlock
            className="bg-white/75"
            defaultValue="python"
            data={[
              {
                language: "python",
                filename: `${recommendation.bestModel}.py`,
                code: cleanCode,
              },
            ]}
          >
            <CodeBlockHeader>
              <CodeBlockFiles>
                {(item) => (
                  <CodeBlockFilename key={item.language} value={item.language}>
                    {item.filename}
                  </CodeBlockFilename>
                )}
              </CodeBlockFiles>
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
        </div>
      </CardContent>
    </Card>
  );
}
