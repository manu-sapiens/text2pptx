curl -X POST \
  http://localhost:8501/generate_presentation \
  -H 'Content-Type: application/json' \
  -d '{"template":"Ion Boardroom", "title": "Understanding AI", "subtitle":"By Bespoke Intelligence", "slides": [{"heading": "Introduction","bullet_points": ["Brief overview of AI", "Importance of understanding AI"]}]}' \
  -o ./test/output.pptx