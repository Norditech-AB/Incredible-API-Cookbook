import dotenv from "dotenv";

import { chat } from "./chat.js";

dotenv.config();

async function runDemo() {
  const response = await chat([
    {
      role: "user",
      content: "Visit https://example.com, report the page title and capture the first paragraph text.",
    },
  ]);

  console.log(JSON.stringify(response.content, null, 2));
}

runDemo().catch((error) => {
  console.error("Demo failed", error);
  process.exit(1);
});
