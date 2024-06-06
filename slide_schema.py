GPT_TOOL_SLIDE_SCHEMA = {
  "type": "function",
  "function": {
    "name": "json_answer",
    "description": "Generate output using the specified schema",
    "parameters": {
        "type": "object",
        "properties": {
          "slides": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "heading": {"type": "string"},
                "bullet_points": {
                  "type": ["array", "null"],
                  "items": {
                    "type": "object",
                    "properties": {
                      "bullet_type": {
                        "type": "string",
                        "enum": ["none", "bullet", "number", "letter"]
                      },
                      "bullet_level": {
                        "type": "string",
                        "enum": ["0", "1", "2", "3"]
                      },
                      "bullet_text": {"type": "string"}
                    },
                    "required": ["bullet_type", "bullet_level", "bullet_text"]
                  }
                }
              },
              "required": ["heading"]
            }
          }
        }
      }
  }
}
