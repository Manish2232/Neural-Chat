from langchain_mistralai import ChatMistralAI
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage

load_dotenv()

model = ChatMistralAI(
    model = "mistral-small-2506",
    temperature = 0.7
)
print("------Welcome type 0 to exit the Application------")
print("1 : Happy\n2 : Sad\nfor other press anything")
mood = input("Please chhose AI mood : ")

if mood == "1" :
    messages = [
    SystemMessage(content = "You are a funny AI agent")
    ]

elif mood == "2":
    messages = [
    SystemMessage(content = "You are a sad AI agent")
    ]

else:
    messages = [
    SystemMessage(content = "You are a neutral AI agent")
    ] 





while True:

    

    prompt = input("You : ")

    if prompt == "0":
        print("Good By!")
        break

    messages.append(HumanMessage(content = prompt))

    
    
    response = model.invoke(messages)
    messages.append(response)
    print("Bot : ", response.content)
