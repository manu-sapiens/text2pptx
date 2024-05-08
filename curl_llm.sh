#!/bin/bash

# Check if OPENAI_API_KEY environment variable is set
if [ -z "$OPENAI_API_KEY" ]; then
  echo "Error: OPENAI_API_KEY is not set."

else


# Perform the curl operation using the API key from the environment variable
curl -X POST http://localhost:8501/llm/infer \
-H "Content-Type: application/json" \
-d '{
        "ai_type": "openai",
        "model": "gpt-4-turbo",
        "system_prompt": "Please generate a JSON with the following structure.",
        "user_prompt": "Generate details for a presentation on the success of Dungeons And Dragons.",
        "api_key": "'"$OPENAI_API_KEY"'",
        "schema":"{~type~:~object~,~properties~:{~title~:{~type~:~string~},~subtitle~:{~type~:~string~},~slides~:{~type~:~array~,~items~:{~type~:~object~,~properties~:{~heading~:{~type~:~string~,~description~:~the heading of this slide~},~bullet_points~:{~type~:~array~,~items~:{~type~:~string~}}}}}},~required~:[~title~,~slides~]}"
    }' -o ./test/output.bin
fi