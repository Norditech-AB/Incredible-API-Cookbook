# Incredible Google Sheets Integration Demo

This self-contained TypeScript demo shows how to orchestrate Incredible's integrations API with Google Sheets using tool-calling. It walks through OAuth setup, lists integrations, retrieves feature metadata, provisions a sheet, and writes the catalog via `GOOGLESHEETS_SHEET_FROM_JSON`.

## Prerequisites
- Node.js 18+
- An Incredible API key
- ngrok (or another HTTPS tunnel) pointing to your local machine
- Google account with access to Sheets

## Setup
1. `npm install`
2. Copy `.env.example` to `.env` and fill in:
   - `INCREDIBLE_API_KEY` (required)
   - `INCREDIBLE_BASE_URL` (optional override)
   - `PLAYWRIGHT_MCP_*` values are not used here, can be removed
3. Start ngrok: `ngrok http 3001` (or the port of your choice)
4. Update `.env` with the HTTPS URL returned by ngrok for the callback base, or edit the constants in `src/incredible_integration.ts`.

## Run
```
npx tsx src/incredible_integration.ts
```
Follow the prompts:
- Authorize Google Sheets when the URL is displayed
- Wait while the agent lists integrations, gathers metadata, creates the sheet, and writes the data
- The final assistant response includes a direct Google Sheets URL you can open

## Packaging
To zip this demo for distribution:
```
zip -r incredible_integration_demo.zip incredible_integration_demo
```
