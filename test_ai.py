"""
====================================
AI Test File

This file checks whether Python
can communicate with Ollama.

Author : SK
====================================
"""

# Import AI function
from utils.ai_engine import ask_ai


print("=" * 50)
print("Testing AI Engine...")
print("=" * 50)

question = """
What is Artificial Intelligence?

Explain in simple words.
"""

answer = ask_ai(question)

print("\nAI Response:\n")
print(answer)
