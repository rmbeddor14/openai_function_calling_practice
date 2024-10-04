## to practice function calling
## I am still unclear if this uses structured outputs but I don't think it does
## i feel like i'm two steps from the punchline here like maybe it's too hard coded it's not taking full advantage of ai and needs to be rethought
import os
import requests
import random
from datetime import datetime, timedelta
from openai import OpenAI
import json

def when_did_my_order_ship(order_id): 
    ## for demo purposes, print that the function was called
    print("function called!")
    ## if the order is under 1000 then give it a random day in the last week
    ## otherwise just say it's not been shipped 
    if order_id < 1000:
        return (datetime.now()-timedelta(days=random.randint(0, 6))).strftime('%Y-%m-%d')
    else:
        return "Not yet shipped"

def chatbot(chat_input,order_id=None):

    # Initialize the OpenAI client
    client = OpenAI()
    
    tools = [
    {
        "type": "function",
        "function": {
            "name": "when_did_my_order_ship",
            "description": "Get the delivery date for a customer's order. Call this whenever you need to know the delivery date, for example when a customer asks 'Where is my package'",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "The customer's order ID.",
                    },
                },
                "required": ["order_id"],
                "additionalProperties": False,
            }
        }
    }
    ]

    messages = [
        {"role": "system", "content": "You are a helpful customer support assistant. Use the supplied tools to assist the user."},
        {"role": "user", "content": f"here is the input {chat_input}"}
    ]

    # Add order_id as a context if it's provided
    ## Here again we're kind of hardcoding? 
    if order_id:
        messages.append({"role": "user", "content": f"My order ID is {order_id}"})


    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=tools,
    )

    ### typically you would print the response
    ### but this is function calling so we're going to actually just process the response

    # response_message = response.choices[0].message
    # print(response_message)
    
    # Check if the model requested a function call
    if response.choices[0].message.tool_calls:
        tool_call = response.choices[0].message.tool_calls[0] #isolate tool_call from the response


        ## here's an example of what this looks like if you print "tool_call"
        ### ChatCompletionMessageToolCall(id='call_SHJVFhkhz0qMygrZImcmWNKA', function=Function(arguments='{"order_id":"10000"}', name='when_did_my_order_ship'), type='function')

        ## print for demo 
        print(f"\n\n tool call result message {tool_call} \n\n")


        function_name = tool_call.function.name # identify the name of the function from the response 
        order_id = json.loads(tool_call.function.arguments)["order_id"] # identify the order_id

        ## if the function name is defined in your code, then call it 
        ## there is prob a more elegant way to do this 
        if function_name in globals():
            fxn_return = globals()[function_name](int(order_id))  

        # Create a message with the function result
        function_call_result_message = {
            "role": "tool",
            "content": json.dumps({
                "order_id": order_id,
                "order_date": fxn_return
            }),
            "tool_call_id": tool_call.id
        }

        ## here's an example of the function_call_result_message
        ##{'role': 'tool', 'content': '{"order_id": "10000", "order_date": "Not yet shipped"}', 'tool_call_id': 'call_XqbVQ1fYccIT7EaBVWSZdAkh'}

        print("\n\n function_call_result_message \n after you run the function then you send this message to the llm")
        print(f"{function_call_result_message}\n\n")

        # Send the result back to the model to get the final response
        completion_payload = {
            "model": "gpt-4o",
            "messages": messages + [response.choices[0].message, function_call_result_message]
        }

        # Call the API with the function result
        final_response = client.chat.completions.create(
            model=completion_payload["model"],
            messages=completion_payload["messages"]
        )

        print(final_response.choices[0].message.content)
        print("\n\n")
        return final_response
    else:
        # If no function call was generated, return the normal assistant message
        # If no order ID is provided, ask for it
        if "order_id" not in chat_input.lower():
            print("I couldn't find your order ID. Could you please provide it?")
            return False  # Indicates we still need the order ID
        
        return response.choices[0].message
    



def main():

    ## put your own input
    print("\n\nWhat can I help you with today? I really only know how to do one thing - look up your order ship date in a system so I hope you need help with that!")
    user_input = input("\n\nTell me how I can help: ")

    ## samples (so you don't have to type so much)
    #user_input = "when did my order ship my order number is 10000"
    #user_input = "when did my order ship? my order num is 13"
    #user_input = "when did my order ship?"

    order_id = None  # Start without an order ID

    while True:
        # Call chatbot and if it returns False, ask for order_id
        response = chatbot(user_input, order_id)

        if response is False:
            order_id = input("Please enter your order ID: ")
        else:
            break  # Exit the loop once we have handled the order ID

if __name__ == "__main__":
    main()