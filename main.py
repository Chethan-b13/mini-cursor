from langchain_core.messages import HumanMessage

from app.graph.agent import graph


while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    print("\nAssistant:\n")

    for event in graph.stream(
        {
            "messages": [
                HumanMessage(content=user_input)
            ]
        },
        stream_mode="updates"
    ):
        print("----------------------------------")
        for node_name, node_output in event.items():
            print(f"\n🔹 NODE: {node_name}")
            print(node_output)
        print("----------------------------------")
        print()

    print()