import os
from dotenv import load_dotenv
from groq import Groq

from prompts import SYSTEM_PROMPT
from memory import ConversationMemory
from rag import RAG
from actions import create_support_ticket

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def main():
    print("Customer Support Agent (type 'exit' to quit)\n")

    memory = ConversationMemory(SYSTEM_PROMPT)
    rag = RAG()

    while True:
        user_input = input("You: ")

        if user_input.lower() in {"exit", "quit"}:
            print("Goodbye")
            break

        # add user message to memory
        memory.add_user_message(user_input)

        # retrieve context from RAG
        context, is_relevant = rag.retrieve(user_input)

        # Gaudrails HARD STOP: out-of-scope question
        if not is_relevant:
            response = (
                "I can help with questions related to our company and services, "
                "but I don't have information on that topic."
            )
            print(f"\nAI: {response}\n")
            memory.add_assistant_message(response)
            continue

        # build messages ONLY for valid support questions
        messages = memory.get_messages().copy()

        messages.append({
            "role": "user",
            "content": f"Use the following company information to answer:\n{context}"
        })

        # call Groq LLM
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            temperature=0.3
        )

        answer = response.choices[0].message.content
        print(f"\nAI: {answer}\n")

        memory.add_assistant_message(answer)

        # simple escalation rule
        if "ticket" in user_input.lower() or "human" in user_input.lower():
            create_support_ticket(user_input)


if __name__ == "__main__":
    main()
