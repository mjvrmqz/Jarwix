import sys
import json

# Read the entire input from stdin
quiz_text = sys.stdin.read()

# Split by empty lines to get each question block
blocks = [b.strip() for b in quiz_text.split('\n\n') if b.strip()]

quiz_objects = []

for block in blocks:
    lines = [line.strip() for line in block.splitlines() if line.strip()]
    if len(lines) >= 3:
        question = lines[0]
        answers = lines[1:]  # This will keep "A..." and "B..." as separate strings
        quiz_objects.append({
            "question": question,
            "answers": answers
        })

# Output as JSON for Shortcuts to parse easily
print(json.dumps(quiz_objects))