import dotenv from "dotenv";
import { IncredibleClient } from "@incredible-ai/sdk";

dotenv.config();

export const anthropic = new IncredibleClient({streamThinkingMode: 'default', apiKey: "ik_your_incredible_api_key"});

