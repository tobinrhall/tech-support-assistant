import os
from dotenv import load_dotenv
from openai import OpenAI
import glob

# Load .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY not found. Make sure it's set in your .env file.")

client = OpenAI(api_key=api_key)

NORMAL_MODE_PROMPT = """
You are a highly skilled IT support assistant who explains issues clearly, calmly, and professionally.

Your responses must ALWAYS follow this structured format:

SUMMARY:
<2–3 sentences explaining the situation>

LIKELY CAUSES:
- <cause 1>
- <cause 2>
- <cause 3>

RECOMMENDED STEPS:
1. <step 1>
2. <step 2>
3. <step 3>

OPTIONAL NOTES:
<any additional warnings, clarifications, follow-up questions>

STYLE RULES:
- Keep explanations clear and beginner-friendly.
- Use technical accuracy and best practices.
- You may include light Diablo references (small hints only).
"""

DIABLO_MODE_PROMPT = """
You are Deckard Cain — the wise, ancient Horadrim scholar — but with perfect modern IT expertise.
You speak in a wise, dramatic, slightly archaic tone — but your technical advice is always accurate.

Your responses must ALWAYS follow this structured format:

SUMMARY:
<A mystical but clear explanation of the issue>

LIKELY CAUSES:
- <cause 1 explained as "corrupted runes", "shadowed drivers", etc.>
- <cause 2>
- <cause 3>

RECOMMENDED STEPS:
1. <step 1>
2. <step 2>
3. <step 3 — optional ancient wisdom>

OPTIONAL NOTES:
<Final warning, blessing, or deeper insight>

STYLE RULES:
- Speak like Deckard Cain ("Stay awhile and listen", "hero", "the forces of darkness", etc.)
- BUT never sacrifice clarity, accuracy, or real IT best practices.
- No pure roleplay; you must STILL give correct troubleshooting.
"""

# Default mode is NORMAL
current_system_prompt = NORMAL_MODE_PROMPT
current_mode_name = "Normal"
current_level = "Normal"  # can be "Normal", "ELI5", "Advanced"

KNOWLEDGE_BASE_DIR = "knowledge_base"

def load_knowledge_base():
    """Load all .txt files from the knowledge_base directory."""
    docs = []
    if not os.path.isdir(KNOWLEDGE_BASE_DIR):
        return docs

    pattern = os.path.join(KNOWLEDGE_BASE_DIR, "*.txt")
    for path in glob.glob(pattern):
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            docs.append({
                "filename": os.path.basename(path),
                "content": content
            })
        except Exception as e:
            print(f"[Warning] Could not read {path}: {e}")
    return docs

def find_relevant_docs(query, docs, max_docs=2):
    """Naive relevance: count overlapping words between query and each doc."""
    if not docs:
        return []

    query_words = set(query.lower().split())
    scored = []

    for doc in docs:
        content_words = set(doc["content"].lower().split())
        overlap = len(query_words & content_words)
        if overlap > 0:
            scored.append((overlap, doc))

    # Sort by overlap descending and return top N
    scored.sort(key=lambda x: x[0], reverse=True)
    return [doc for _, doc in scored[:max_docs]]




def get_assistant_reply(user_message: str, docs) -> str:
    # Find relevant docs for this query
    relevant_docs = find_relevant_docs(user_message, docs)
    context_texts = []
    for doc in relevant_docs:
        context_texts.append(f"From {doc['filename']}:\n{doc['content']}\n")

    combined_context = "\n\n".join(context_texts) if context_texts else ""

    messages = [
        {"role": "system", "content": current_system_prompt},
    ]


    if combined_context:
        messages.append({
            "role": "system",
            "content": f"Here are some reference notes that may help:\n\n{combined_context}"
        })

    messages.append({"role": "user", "content": user_message})
    messages = [
        {"role": "system", "content": current_system_prompt},
    ]

    # Add difficulty/level hint
    if current_level == "ELI5":
        messages.append({
            "role": "system",
            "content": "Explain everything as if to a complete beginner with almost no technical knowledge. Avoid jargon or explain it very simply. Use analogies when helpful."
        })
    elif current_level == "Advanced":
        messages.append({
            "role": "system",
            "content": "Assume the user has solid IT knowledge. Use more technical detail, specific tools, commands, and deeper explanations where appropriate."
        })
    # Normal = no extra instruction

    if combined_context:
        messages.append({
            "role": "system",
            "content": f"Here are some reference notes that may help:\n\n{combined_context}"
        })

    messages.append({"role": "user", "content": user_message})


    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages,
        temperature=0.4,
    )

    return response.choices[0].message.content.strip()


def main():
    global current_system_prompt, current_mode_name, current_level

    print("=== Tech Support Assistant of Sanctuary ===")
    print("Type your issue (or 'quit' to exit).")
    print("-------------------------------------------")
    print("Current mode: Normal")

    # Load your tomes of knowledge at startup
    docs = load_knowledge_base()
    if docs:
        print(f"Loaded {len(docs)} knowledge base file(s) from '{KNOWLEDGE_BASE_DIR}'.")
    else:
        print(f"No knowledge base files found in '{KNOWLEDGE_BASE_DIR}'. You can add .txt files there anytime.")

    while True:
        user_input = input("\nYou: ").strip()

        if user_input.lower() in {"quit", "exit", "q"}:
            print("Assistant: Farewell, hero. May your system stay ever stable.")
            break

        if not user_input:
            continue

        # Mode switching commands
        lower = user_input.lower()

        # Level / difficulty commands
        if lower in {"eli5", "level basic", "level beginner"}:
            current_level = "ELI5"
            print("\nAssistant: Explanation level set to ELI5 — fear not, I shall speak plainly, hero.")
            print(f"Current mode: {current_mode_name}, Level: {current_level}")
            continue

        if lower in {"level normal", "normal level"}:
            current_level = "Normal"
            print("\nAssistant: Returning to normal explanation level.")
            print(f"Current mode: {current_mode_name}, Level: {current_level}")
            continue

        if lower in {"level advanced", "advanced", "expert mode"}:
            current_level = "Advanced"
            print("\nAssistant: Very well. I shall speak as to a fellow scholar of the arcane arts of IT.")
            print(f"Current mode: {current_mode_name}, Level: {current_level}")
            continue

        if lower in {"mode diablo", "diablo mode", "diablo on"}:
            current_system_prompt = DIABLO_MODE_PROMPT
            current_mode_name = "Diablo"
            print("\nAssistant: Diablo Mode activated. Darkness stirs, hero…")
            print(f"Current mode: {current_mode_name}")
            continue

        if lower in {"mode normal", "normal mode", "diablo off"}:
            current_system_prompt = NORMAL_MODE_PROMPT
            current_mode_name = "Normal"
            print("\nAssistant: Returning to Normal Mode. Clarity restored.")
            print(f"Current mode: {current_mode_name}")
            continue

# Help command
        if lower in {"help", "?", "commands"}:
            print("\n=== Available Commands ===")
            print("Type your issue normally to get help, e.g.:")
            print("  My PC is freezing on start-up\n")
            print("Special commands:")
            print("  mode diablo    - Switch to Diablo Mode (Deckard Cain flavor)")
            print("  mode normal    - Switch back to Normal Mode")
            print("  eli5           - Beginner-friendly explanations")
            print("  level normal   - Normal explanation level")
            print("  level advanced - More technical, detailed steps")
            print("  help or ?      - Show this help message")
            print("  quit           - Exit the assistant")
            print(f"\nCurrent mode: {current_mode_name}, Level: {current_level}")
            continue



        try:
            reply = get_assistant_reply(user_input, docs)
            print("\nAssistant:", reply)
        except Exception as e:
            print("\n[An error emerges from the burning depths of the network]:", e)


if __name__ == "__main__":
    main()
