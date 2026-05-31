import sys
import json

quiz_text = sys.stdin.read()

blocks = [b.strip() for b in quiz_text.split('\n\n') if b.strip()]

quiz_objects = []

for block in blocks:
    lines = [line.strip() for line in block.splitlines() if line.strip()]
    if len(lines) >= 3:
        question = lines[0]
        answers = lines[1:]
        quiz_objects.append({
            "question": question,
            "answers": answers
        })

print(json.dumps(quiz_objects))
