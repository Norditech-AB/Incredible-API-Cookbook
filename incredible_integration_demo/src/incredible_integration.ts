import http from "node:http";
import readline from "node:readline/promises";
import { stdin as input, stdout as output } from "node:process";
import { URL } from "node:url";
import type {
  MessageParam,
  Tool,
  ToolUseBlock,
  MessageResponse,
} from "@anthropic-ai/sdk";

const API_KEY = "ik_your_incredible_api_key";
const USER_ID = "integration-demo-user";
const INTEGRATION_ID = "googlesheets";
const CALLBACK_BASE = "https://e93943c48233.ngrok-free.app";
const CALLBACK_PATH = "/oauth/google-sheets/callback";
const CALLBACK_PORT = 3001;
const MODEL = "small-1";
const MAX_TOKENS = 1024;

import { IncredibleClient } from "@incredible-ai/sdk";

type RegisteredTool = {
  definition: Tool;
  run: (args: Record<string, unknown>) => Promise<unknown>;
};

async function main() {
  const client = new IncredibleClient({ apiKey: API_KEY });
  const callbackUrl = buildCallbackUrl();
  const sheetTitle = generateSheetTitle();

  // Phase 1 — Discover integrations and share context
  const integrations = await client.integrations.list();
  logIntegrationSummary(integrations);

  // Phase 2 — Ensure Google Sheets OAuth is complete for this user
  await ensureOAuthAuthorized(client, callbackUrl);

  // Phase 3 — Build toolkit for the LLM and seed the conversation
  const tools = buildGoogleSheetsTools(client);
  const messages = createInitialMessages(sheetTitle);

  // Phase 4 — Let the agent orchestrate via tool-calling
  await runAgentConversation(client, tools, messages);

  // Phase 5 — Emit a transcript for debugging/troubleshooting
  logConversation(messages);
}

// ---------------------------------------------------------------------------
// Conversation Orchestration
// ---------------------------------------------------------------------------

async function runAgentConversation(
  client: IncredibleClient,
  tools: RegisteredTool[],
  messages: MessageParam[],
) {
  for (;;) {
    const response = await client.messages.create({
      model: MODEL,
      max_tokens: MAX_TOKENS,
      messages,
      tools: tools.map((tool) => tool.definition),
    });

    console.dir({ turn: response }, { depth: 3, colors: true });
    messages.push({ role: response.role, content: response.content });

    if (response.stop_reason !== "tool_use") {
      return;
    }

    const toolUses = extractToolUses(response);
    if (toolUses.length === 0) {
      console.warn("Tool stop requested but no tool_use blocks were returned.");
      return;
    }

    for (const toolUse of toolUses) {
      await invokeTool(tools, toolUse, messages);
    }
  }
}

async function invokeTool(tools: RegisteredTool[], toolUse: ToolUseBlock, messages: MessageParam[]) {
  const handler = tools.find((tool) => tool.definition.name === toolUse.name);
  if (!handler) {
    console.warn(`No handler registered for tool ${toolUse.name}`);
    messages.push({
      role: "user",
      content: [
        {
          type: "tool_result",
          tool_use_id: toolUse.id,
          is_error: true,
          content: `Tool ${toolUse.name} is unavailable.`,
        },
      ],
    });
    return;
  }

  try {
    const result = await handler.run(toolUse.input ?? {});
    messages.push({
      role: "user",
      content: [
        {
          type: "tool_result",
          tool_use_id: toolUse.id,
          content: typeof result === "string" ? result : JSON.stringify(result, null, 2),
        },
      ],
    });
  } catch (error) {
    messages.push({
      role: "user",
      content: [
        {
          type: "tool_result",
          tool_use_id: toolUse.id,
          is_error: true,
          content: `Tool invocation failed: ${error instanceof Error ? error.message : String(error)}`,
        },
      ],
    });
  }
}

// ---------------------------------------------------------------------------
// Initialization Helpers
// ---------------------------------------------------------------------------

function buildCallbackUrl() {
  return `${CALLBACK_BASE.replace(/\/$/, "")}${CALLBACK_PATH}`;
}

function generateSheetTitle() {
  return `Incredible Integrations Catalog ${new Date().toISOString().slice(0, 10)}`;
}

function createInitialMessages(sheetTitle: string): MessageParam[] {
  return [
    {
      role: "system",
      content:
        "You are an Incredible integrations orchestrator. Use only the provided tools to list integrations, inspect their feature schemas, create a new spreadsheet, and then populate that spreadsheet. Always call create_google_sheet before attempting to write data. When calling write_google_sheets_from_json ensure you supply the sheet title/name plus a JSON array of row objects containing the expected columns. Summarize results at the end and include the direct Google Sheets URL if any tool returned it.",
    },
    {
      role: "user",
      content:
        `Create a spreadsheet titled '${sheetTitle}' with columns [Integration Name, Feature Name, Logo URL, Feature Description, Auth Method]. Work with the first ten integrations returned from list_incredible_integrations. Inspect the integration details so you understand feature inputs, call create_google_sheet once to provision the spreadsheet, gather the data, then invoke write_google_sheets_from_json using the JSON array of rows you assembled. Conclude by reporting the spreadsheet URL so I can open it immediately.`,
    },
  ];
}

function logIntegrationSummary(integrations: any[]) {
  console.log("Fetched integrations:");
  integrations.forEach((integration, index) => {
    console.log(`${index + 1}. id=${integration.id} name=${integration.name}`);
  });
}

function logConversation(messages: MessageParam[]) {
  console.log("\nFinal conversation:");
  messages.forEach((message) => {
    console.log(`${message.role.toUpperCase()}:`, message.content);
  });
}

// ---------------------------------------------------------------------------
// OAuth Flow
// ---------------------------------------------------------------------------

async function ensureOAuthAuthorized(client: IncredibleClient, callbackUrl: string) {
  const callbackNotification = waitForOAuthCallback();

  const connectResponse = await client.integrations.connect(INTEGRATION_ID, {
    callback_url: callbackUrl,
    user_id: USER_ID,
  });

  console.log("Google Sheets connect response:", JSON.stringify(connectResponse, null, 2));

  if (connectResponse?.redirect_url) {
    const rl = readline.createInterface({ input, output });
    await rl.question(
      `Visit this URL to authorize Google Sheets access:\n${connectResponse.redirect_url}\n\nPress Enter once authorization is complete...`,
    );
    rl.close();
  }

  const callbackResult = await callbackNotification;
  if ((callbackResult.status ?? "").toLowerCase() !== "success") {
    throw new Error("OAuth flow did not report success; aborting execution.");
  }
}

function waitForOAuthCallback() {
  return new Promise<Record<string, string>>((resolve) => {
    const server = http.createServer((req, res) => {
      if (!req.url) {
        res.writeHead(400).end("Missing URL");
        return;
      }

      const url = new URL(req.url, `http://localhost:${CALLBACK_PORT}`);

      if (url.pathname === CALLBACK_PATH) {
        const params = Object.fromEntries(url.searchParams.entries());
        console.log("\n[Callback] Received query:", params);

        res.writeHead(200, { "Content-Type": "text/plain" });
        res.end("Google Sheets authorization complete. You can close this tab.");

        resolve(params);
        server.close();
      } else {
        res.writeHead(404, { "Content-Type": "text/plain" });
        res.end("Not Found");
      }
    });

    server.listen(CALLBACK_PORT, () => {
      console.log(`Callback server listening on http://localhost:${CALLBACK_PORT}${CALLBACK_PATH}`);
    });
  });
}

// ---------------------------------------------------------------------------
// Tool Definitions
// ---------------------------------------------------------------------------

function buildGoogleSheetsTools(client: IncredibleClient): RegisteredTool[] {
  return [
    {
      definition: {
        name: "list_incredible_integrations",
        description:
          "Return the first ten Incredible integrations with id, name, logo_url, auth_method, and available features.",
        input_schema: { type: "object", properties: {}, additionalProperties: false },
      },
      run: async () => {
        const all = await client.integrations.list();
        return all.slice(0, 10);
      },
    },
    {
      definition: {
        name: "retrieve_integration_details",
        description:
          "Retrieve a specific integration’s full details, including feature metadata and descriptions.",
        input_schema: {
          type: "object",
          properties: {
            integration_id: { type: "string" },
          },
          required: ["integration_id"],
          additionalProperties: false,
        },
      },
      run: async (args) => {
        const integrationId = String(args.integration_id ?? INTEGRATION_ID);
        return client.integrations.retrieve(integrationId);
      },
    },
    {
      definition: {
        name: "create_google_sheet",
        description:
          "Create a fresh Google Sheet using GOOGLESHEETS_CREATE_GOOGLE_SHEET1. Provide title and optional sheet_name.",
        input_schema: {
          type: "object",
          properties: {
            title: { type: "string" },
            sheet_name: { type: "string" },
          },
          required: ["title"],
          additionalProperties: false,
        },
      },
      run: async (args) => {
        const title = String(args.title);
        const sheet_name = args.sheet_name ? String(args.sheet_name) : undefined;

        return client.integrations.execute(INTEGRATION_ID, {
          user_id: USER_ID,
          feature_name: "GOOGLESHEETS_CREATE_GOOGLE_SHEET1",
          inputs: sheet_name ? { title, sheet_name } : { title },
        });
      },
    },
    {
      definition: {
        name: "write_google_sheets_from_json",
        description:
          "Use GOOGLESHEETS_SHEET_FROM_JSON to replace/create a sheet from a JSON array of row objects. Provide spreadsheet_title (aka title), sheet_title (aka sheet_name), and rows_json (array of row objects with the columns Integration Name, Feature Name, Logo URL, Feature Description, Auth Method).",
        input_schema: {
          type: "object",
          properties: {
            spreadsheet_title: { type: "string" },
            sheet_title: { type: "string" },
            rows_json: { type: "string" },
          },
          required: ["spreadsheet_title", "sheet_title", "rows_json"],
          additionalProperties: false,
        },
      },
      run: async (args) => {
        const spreadsheetTitle = args.spreadsheet_title ?? args.title;
        const sheetTitle = args.sheet_title ?? args.sheet_name;
        const rowsPayload = args.rows_json ?? args.sheet_json;

        if (!spreadsheetTitle || !sheetTitle || rowsPayload == null) {
          throw new Error(
            "write_google_sheets_from_json requires spreadsheet_title, sheet_title, and rows_json inputs.",
          );
        }

        const title = String(spreadsheetTitle);
        const sheet_name = String(sheetTitle);

        let rowsValue: unknown;
        if (typeof rowsPayload === "string") {
          if (!rowsPayload.trim()) {
            throw new Error("rows_json must not be empty.");
          }
          try {
            rowsValue = JSON.parse(rowsPayload);
          } catch (error) {
            throw new Error(`rows_json must be valid JSON: ${error instanceof Error ? error.message : String(error)}`);
          }
        } else {
          rowsValue = rowsPayload;
        }

        if (!Array.isArray(rowsValue)) {
          throw new Error("rows_json must parse to an array of row objects.");
        }

        return client.integrations.execute(INTEGRATION_ID, {
          user_id: USER_ID,
          feature_name: "GOOGLESHEETS_SHEET_FROM_JSON",
          inputs: {
            title,
            sheet_name,
            sheet_json: rowsValue,
          },
        });
      },
    },
  ];
}

// ---------------------------------------------------------------------------
// Utilities
// ---------------------------------------------------------------------------

function extractToolUses(response: MessageResponse) {
  return (response.content ?? []).filter(
    (block): block is ToolUseBlock => block.type === "tool_use",
  );
}

main().catch((error) => {
  console.error("[incredible-integrations-demo] failed", error);
  process.exitCode = 1;
});
