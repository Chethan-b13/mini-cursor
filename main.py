from langchain_core.messages import HumanMessage

from app.graph.agent import graph


while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    result = graph.invoke({
        "messages": [
            HumanMessage(content=user_input)
        ]
    })

    print("\nAssistant:")
    print(result["messages"][-1].content)
    print()