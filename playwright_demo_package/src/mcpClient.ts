import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";

export interface PlaywrightConnection {
  client: Client;
  transport: StdioClientTransport;
}

export async function connectPlaywrightMcp(): Promise<PlaywrightConnection> {
  const transport = new StdioClientTransport({
    command: "npx",
    args: ["@playwright/mcp@latest"],
    stderr: "inherit",
  });

  const client = new Client({ name: "playwright-agentic-cli", version: "0.1.0" });
  await client.connect(transport);

  return { client, transport };
}

