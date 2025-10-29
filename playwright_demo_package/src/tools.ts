export type McpTool = {
  name: string;
  description?: string | null;
  title?: string | null;
  inputSchema?: unknown;
};

import type { Tool as AnthropicTool } from "@anthropic-ai/sdk/resources/messages.mjs";

export function toAnthropicTools(tools: McpTool[]): AnthropicTool[] {
  return tools.map((tool) => ({
    name: tool.name,
    description: tool.description ?? tool.title ?? "",
    input_schema:
      (tool.inputSchema as AnthropicTool["input_schema"]) ?? {
        type: "object",
        properties: {},
        additionalProperties: true,
      },
  }));
}
