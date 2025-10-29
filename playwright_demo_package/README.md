# Playwright MCP Demo

This package contains the minimal files needed to run `src/demo.ts`, which bridges Anthropic's Messages API with the Playwright MCP server.

## Prerequisites
- Node.js 18+
- Anthropic API key in `.env`
- Playwright MCP server launched via `npx @playwright/mcp@latest`
- Optional: ngrok tunnel if Anthropic must reach your local MCP server

## Setup
1. `npm install`
2. Copy `.env.example` to `.env` and fill in:
   - `ANTHROPIC_API_KEY`
   - `ANTHROPIC_MODEL` (optional)
   - `PLAYWRIGHT_MCP_SSE_URL` (if using SSE/ngrok)
   - `PLAYWRIGHT_MCP_TOKEN` (if your MCP server requires a token)
3. Ensure Playwright MCP is reachable. You can run:
   ```
   npx @playwright/mcp@latest --port 3001 --host 0.0.0.0 --allowed-hosts "*"
   ```

## Run
```
npx tsx src/demo.ts
```
The script will prompt Anthropic to open https://example.com via the MCP server and log the captured output. MCP tool invocations are logged in `mcp_logs/`.

## Packaging
To zip this demo directory for distribution:
```
zip -r playwright_demo_package.zip playwright_demo_package
```
