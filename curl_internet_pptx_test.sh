curl -X POST \
  https://text2pptx.onrender.com/generate_presentation \
  -H 'Content-Type: application/json' \
  -d '{"template":"Bespoke", "filename":"test.pptx", "title": "Understanding AI?", "subtitle":"Created by Capital Blueprint", "slides": [{"heading": "Introduction","bullet_points": ["Brief overview of AI", "Importance of understanding AI"]}]}' \
  -o ./test/output.pptx