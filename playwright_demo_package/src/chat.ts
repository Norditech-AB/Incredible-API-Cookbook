import type { Message, MessageParam, ToolUseBlock } from "@anthropic-ai/sdk/resources/messages.mjs";

import { mkdir, writeFile } from "node:fs/promises";
import { join } from "node:path";

import { anthropic } from "./incredibleClient.js";
import { connectPlaywrightMcp } from "./mcpClient.js";
import type { McpTool } from "./tools.js";
import { toAnthropicTools } from "./tools.js";

export type ChatInput = {
  role: "user" | "assistant";
  content: string;
};

export async function chat(messages: ChatInput[]): Promise<Message> {
  const { client: mcp, transport } = await connectPlaywrightMcp();

  try {
    const toolListing = await mcp.listTools();
    const tools = toAnthropicTools(toolListing.tools as McpTool[]);

    let response = await anthropic.messages.create({
      model: process.env.ANTHROPIC_MODEL ?? "claude-3-7-sonnet-20250219",
      max_tokens: 1024,
      tools,
      messages: messages as MessageParam[],
    });

    const toolUses = response.content.filter(
      (block): block is ToolUseBlock => block.type === "tool_use",
    );

    if (!toolUses.length) {
      return response;
    }

    const toolResults: MessageParam[] = [];

    for (const call of toolUses) {
      const args = (call.input ?? {}) as Record<string, unknown>;
      const result = await mcp.callTool({ name: call.name, arguments: args });
      await logMcpResult(call.name, result);
      const entries = Array.isArray(result.content) ? result.content : [];
      const text = entries
        .map((entry) =>
          entry && typeof entry === "object" && "text" in entry && typeof entry.text === "string"
            ? entry.text
            : JSON.stringify(entry),
        )
        .join("\n");

      toolResults.push({
        role: "user",
        content: [
          {
            type: "tool_result",
            tool_use_id: call.id,
            content: text,
          },
        ],
      });
    }

    response = await anthropic.messages.create({
      model: process.env.ANTHROPIC_MODEL ?? "claude-3-7-sonnet-20250219",
      max_tokens: 1024,
      tools,
      messages: [
        ...messages,
        { role: "assistant", content: response.content } as MessageParam,
        ...toolResults,
      ],
    });

    return response;
  } finally {
    await transport.close();
  }
}

async function logMcpResult(name: string, payload: unknown) {
  const logsDir = join(process.cwd(), "mcp_logs");
  await mkdir(logsDir, { recursive: true });
  const filename = `${name}-${Date.now()}.json`;
  const filePath = join(logsDir, filename);
  await writeFile(filePath, JSON.stringify(payload, null, 2), "utf8");
}

