#!/bin/bash

# Check if OPENAI_API_KEY environment variable is set
if [ -z "$OPENAI_API_KEY" ]; then
  echo "Error: OPENAI_API_KEY is not set."

else


# Perform the curl operation using the API key from the environment variable
curl -X POST https://text2pptx.onrender.com/llm/batch_pptx \
-H "Content-Type: application/json" \
-d '{
        "ai_type": "openai",
        "model": "gpt-3.5-turbo",
        "system_prompt": "You are an expert on tabletop role playing games",
        "user_prompt": "Generate a presentation on what Dungeons And Dragons is|||Generate a presentation on Dungeons And Dragons Adventurers League and how it contributed to the renewal of interest in the game|||Differences between Pathfinder and Dungeons and Dragons",
        "api_key": "'"$OPENAI_API_KEY"'",
        "template":"Bespoke",
        "schema":"{type:object,properties:{title:{type:string},subtitle:{type:string},slides:{type:array,items:{type:object,properties:{heading:{title:Heading,description:The_slide_Heading,type:string},bullet_points:{title:Bullet_Points,description:The_bullet_points,type:array,items:{type:string}}},required:[heading,bullet_points]}}},required:[title,slides]}"
    }' -o ./test/new_output.zip
fi

# new:      "schema":"{type:object,properties:{title:{type:string},subtitle:{type:string},slides:{type:array,items:{type:object,properties:{heading:{title:Heading,description:The_slide_Heading,type:string},bullet_points:{title:Bullet_Points,description:The_bullet_points,type:array,items:{type:string}}},required:[heading,bullet_points]}}},required:[title,slides]}"
# gpt4 :    "model": "gpt-4-turbo",
# curl -X POST https://text2pptx.onrender.com/llm/batch_infer \
# curl -X POST http://localhost:8501/llm/batch_pptx \
