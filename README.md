## Basic Function Calling

- I attended a cloudflare openai meetup on Oct 2 where I learned about new openai feature for structured outputs (i'll put that code up later too - that's way cooler)

- That event made me want to practice basic function calling

- This is basic and doesn't use structured outputs that I can tell, I was just doing it to get a feel for how to do this procedure

- in a *plot twist*, chatgpt did not write very much of this code for me!! I really had to go through it myself (which is great for learning). Not for lack of trying though! It turns out that ChatGPT was actually not great at understanding open ai's documentation / features. So went old school with this one! 

- here's the link to the doc I followed [OpenAI function calling doc](https://platform.openai.com/docs/guides/function-calling)


## Demo 
[![Watch the video](img/thumbnail.png)](https://youtu.be/VLbNAaQn5zI?si=S4SxcPJ1pxAVL8JR)

## What this code does
- there's a basic function called `when_did_my_order_ship` that just returns a random ship date based on your order num 
- when the user asks the llm for their ship date, the llm calls `when_did_my_order_ship` and returns the output of the function 

## prerequisites
- just openai & requests
- make sure your openai api key set in os env variable

