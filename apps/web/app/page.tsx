"use client";
import { MultiSelect } from "@/components/multiselect";
import { Textarea } from "@/components/ui/textarea";
import { OrderedCheckboxGroup } from "@/components/ordered-checkbox-group";
import { useState } from "react";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { Metric, Model } from "@/lib/types";
import { METRICS, MODELS } from "@/lib/consts";
import { evaluateRequest } from "@/lib/api";
import { sendEvaluateRequest } from "@/app/actions/api";

export default function Home() {
  const [selectedModels, setSelectedModels] = useState<Model[]>([]);
  const [orderedMetrics, setOrderedMetrics] = useState<Metric[]>([]);
  const [input, setInput] = useState<string>("");
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [isLoading, setIsLoading] = useState(false);

  const handleSelect = (value: Model) => {
    setSelectedModels((prev) =>
      prev.includes(value)
        ? prev.filter((item) => item !== value)
        : [...prev, value]
    );
  };

  const handleRemove = (value: Model) => {
    setSelectedModels((prev) => prev.filter((item) => item !== value));
  };

  const handleSubmit = async () => {
    setErrors({});
    setIsLoading(true);

    // Validate the input using the zod schema
    const result = evaluateRequest.safeParse({
      prompt: input.trim(),
      models: selectedModels,
      metrics: orderedMetrics,
    });

    if (!result.success) {
      // Handle validation errors
      const fieldErrors: Record<string, string> = {};
      result.error.issues.forEach((err) => {
        const path = err.path.join(".");
        fieldErrors[path] = err.message;
      });
      setErrors(fieldErrors);
      setIsLoading(false);
      return;
    }

    try {
      // Call the API function with validated data
      const response = await sendEvaluateRequest(result.data);

      if (!response.ok) {
        throw new Error(`API request failed: ${response.statusText}`);
      }

      // Handle successful response
      console.log("Request sent successfully");
      // TODO: Handle the response (e.g., display results)
    } catch (error) {
      console.error("Error submitting request:", error);
      setErrors({
        general: "An error occurred while submitting the request",
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="flex min-h-screen w-full flex-col items-center gap-10 py-20 px-16 max-w-4xl mx-auto">
      <h1 className="text-8xl font-serif">Anubis</h1>
      <div className="w-full flex flex-col gap-2">
        <Textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          id="input"
          className="bg-white/75 h-32 relative text-md"
          placeholder="e.g., Write a function to sort an array using merge sort..."
        />
        {errors.prompt && (
          <p className="text-sm text-red-500">{errors.prompt}</p>
        )}
      </div>
      <div className="w-full flex flex-col gap-2">
        <MultiSelect
          options={MODELS}
          selectedValues={selectedModels}
          handleSelect={handleSelect}
          handleRemove={handleRemove}
          placeholder="Select models..."
        />
        {errors.models && (
          <p className="text-sm text-red-500">{errors.models}</p>
        )}
      </div>

      <div className="w-full flex flex-col gap-2">
        <Label className="text-sm font-medium" htmlFor="checkboxes">
          Rank your priorities (click in order of importance):
        </Label>
        <OrderedCheckboxGroup
          options={METRICS}
          selectedValues={orderedMetrics}
          onChange={setOrderedMetrics}
        />
        {errors.metrics && (
          <p className="text-sm text-red-500">{errors.metrics}</p>
        )}
      </div>

      {errors.general && (
        <p className="text-sm text-red-500">{errors.general}</p>
      )}

      <Button
        className="w-full"
        type="submit"
        aria-label="submit"
        onClick={handleSubmit}
        disabled={isLoading}
      >
        {isLoading ? "Submitting..." : "Compare Models"}
      </Button>
    </main>
  );
}
