# AI Hunt Game Backend

This backend generates balanced AI survival items for the Roblox AI hunt game.

## Setup

1. Connect repository to Render.
2. Add environment variable:

OPENAI_API_KEY = your_api_key

## Endpoint

POST /generate_item

Request JSON:
{
  "prompt": "Generate a strange horror survival item"
}

Returns JSON item data.

## Hosting

Deploy using Render Web Service with Python environment.
