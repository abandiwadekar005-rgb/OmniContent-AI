
import anthropic

client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from environment

def call_claude(prompt):
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text