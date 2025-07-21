# # from agents import Agent, Runner, function_tool
# # import httpx
# # from connection import config
# # import chainlit as cl
# # import json
# # from chainlit.element import Image

# # # --- Tool Function ---
# # @function_tool
# # async def get_cars(keyword: str = "") -> str:
# #     url = "https://67820232c51d092c3dcdf34f.mockapi.io/carrental/cars"

# #     try:
# #         async with httpx.AsyncClient() as client:
# #             response = await client.get(url)
# #             data = json.loads(response.text)

# #             cl.logger.info(f"Fetched cars: {data}")

# #             keyword = keyword.strip().lower()
# #             generic_terms = [
# #                 "cars", "show me cars", "list cars", "car",
# #                 "vehicles", "available cars", "all cars"
# #             ]

# #             if not keyword or any(term in keyword for term in generic_terms):
# #                 filtered = data
# #             else:
# #                 filtered = [car for car in data if keyword in car['name'].lower()]

# #             if not filtered:
# #                 await cl.Message(content="❌ No cars found with that keyword.").send()
# #                 return ""  # Avoid assistant fallback message

# #             for car in filtered:
# #                 await cl.Message(
# #                     content=f"""**🚗 {car['name']}**
# # 📊 **Type:** {car['type']} | 🛢️ Fuel: {car['fuel_capacity']} | ⚙️ Transmission: {car['transmission']}
# # 👥 **Seats:** {car['seating_capacity']} | 💰 **Price:** {car['price_per_day']}/day
# # 📝 {car['description']}
# # """,
# #                     elements=[
# #                         Image(name=car['name'], display="inline", url=car['image_url'])
# #                     ]
# #                 ).send()

# #             return ""  # Tool already sent messages, no need to return text

# #     except Exception as e:
# #         await cl.Message(content=f"❌ Error fetching car data: {e}").send()
# #         return ""  # Avoid assistant fallback


# # # --- Agent ---
# # shopping_agent = Agent(
# #     name="ShoppingAgent",
# #     instructions="You are a helpful car rental agent. Greet the customer and help find the best car. Use the 'get_cars' tool to search.",
# #     tools=[get_cars],
# # )

# # # --- Chat Start ---
# # @cl.on_chat_start
# # async def on_chat_start():
# #     cl.user_session.set("agent", shopping_agent)
# #     cl.user_session.set("config", config)
# #     cl.user_session.set("chat_history", [])
# #     await cl.Message(
# #         content="🚗 **Welcome to Car Rental Assistant!**\nType something like `BMW`, `SUV`, or `show me cars`."
# #     ).send()

# # # --- Message Handler ---
# # @cl.on_message
# # async def on_message(message: cl.Message):
# #     msg = cl.Message(content="🧠 Thinking... please wait 🚗")
# #     await msg.send()

# #     agent = cl.user_session.get("agent")
# #     run_config = cl.user_session.get("config")
# #     history = cl.user_session.get("chat_history") or []

# #     history.append({"role": "user", "content": message.content})

# #     try:
# #         result = await Runner.run(
# #             starting_agent=agent,
# #             input=history,
# #             run_config=run_config
# #         )

# #         response_content = result.final_output or ""
# #         if response_content.strip():
# #             msg.content = response_content
# #             await msg.update()
# #         else:
# #             await msg.remove()  # Prevent duplicate or fallback messages

# #         cl.user_session.set("chat_history", result.to_input_list())

# #     except Exception as e:
# #         msg.content = f"❌ Error: {str(e)}"
# #         await msg.update()


# # car_rental_bot.py

# from agents import Agent, Runner, function_tool
# import httpx
# import json
# import chainlit as cl
# from connection import config
# from chainlit.element import Image

# # --- Tool Function ---
# @function_tool
# async def get_cars(keyword: str = "") -> str:
#     url = "https://67820232c51d092c3dcdf34f.mockapi.io/carrental/cars"

#     try:
#         async with httpx.AsyncClient() as client:
#             response = await client.get(url)
#             data = json.loads(response.text)

#         cl.logger.info(f"Fetched cars: {data}")

#         keyword = keyword.strip().lower()
#         generic_terms = ["cars", "show me cars", "list cars", "car", "vehicles", "available cars", "all cars"]

#         if not keyword or any(term in keyword for term in generic_terms):
#             filtered = data
#         else:
#             filtered = [
#                 car for car in data
#                 if keyword in car['name'].lower()
#                 or keyword in car['type'].lower()
#                 or keyword in car['description'].lower()
#             ]

#         if not filtered:
#             await cl.Message(content=f"❌ Sorry, no cars found for '**{keyword}**'. Please try another keyword like `BMW`, `SUV`, or `Toyota`.").send()
#             return "No cars matched."

#         for car in filtered:
#             await cl.Message(
#                 content=f"""**🚗 {car['name']}**
# 📊 **Type:** {car['type']} | 🛢️ Fuel: {car['fuel_capacity']} | ⚙️ Transmission: {car['transmission']}
# 👥 **Seats:** {car['seating_capacity']} | 💰 **Price:** {car['price_per_day']}/day
# 📝 {car['description']}
# """,
#                 elements=[
#                     Image(name=car['name'], display="inline", url=car['image_url'])
#                 ]
#             ).send()

#         return "✅ Car listing completed."

#     except Exception as e:
#         await cl.Message(content=f"❌ Error fetching car data: {e}").send()
#         return "Car search failed due to error."

# # --- Agent ---
# shopping_agent = Agent(
#     name="CarRentalAgent",
#     instructions="""
# You are a warm, helpful, and polite car rental assistant. 
# - Greet users nicely when they start the chat.
# - Help them find cars by using the `get_cars` tool.
# - Always respond clearly and professionally.
# - If they type something like `BMW`, `SUV`, `Toyota`, or `show me cars`, use the tool to return matching cars.
# - If no matches are found, gently suggest other options.
# """,
#     tools=[get_cars],
# )

# # --- Chat Start ---
# @cl.on_chat_start
# async def on_chat_start():
#     cl.user_session.set("agent", shopping_agent)
#     cl.user_session.set("config", config)
#     cl.user_session.set("chat_history", [])

#     await cl.Message(
#         content="""
# 👋 **Hello and welcome to Car Rental Assistant!**
# I'm here to help you find the perfect car for your needs.

# Just type something like:
# - `Show me cars`
# - `BMW`
# - `SUV`
# - `Electric` or `Diesel`

# Let's find your ride! 🚗
# """
#     ).send()

# # --- Message Handler ---
# @cl.on_message
# async def on_message(message: cl.Message):
#     thinking_msg = cl.Message(content="🧠 Thinking... please wait 🚗")
#     await thinking_msg.send()

#     agent = cl.user_session.get("agent")
#     run_config = cl.user_session.get("config")
#     history = cl.user_session.get("chat_history") or []

#     history.append({"role": "user", "content": message.content})

#     try:
#         result = await Runner.run(
#             starting_agent=agent,
#             input=history,
#             run_config=run_config
#         )

#         response_content = result.final_output or ""
#         if response_content.strip() and "car listing completed" not in response_content.lower():
#             thinking_msg.content = response_content
#             await thinking_msg.update()
#         else:
#             await thinking_msg.remove()

#         cl.user_session.set("chat_history", result.to_input_list())

#     except Exception as e:
#         thinking_msg.content = f"❌ Error: {str(e)}"
#         await thinking_msg.update()



# car_rental_bot.py

from agents import Agent, Runner, function_tool
import httpx
import json
import chainlit as cl
from connection import config
from chainlit.element import Image

# --- Tool Function ---
@function_tool
async def get_cars(keyword: str = "") -> str:
    url = "https://67820232c51d092c3dcdf34f.mockapi.io/carrental/cars"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            data = json.loads(response.text)

        cl.logger.info(f"Fetched cars: {data}")

        keyword = keyword.strip().lower()
        generic_terms = ["cars", "show me cars", "list cars", "car", "vehicles", "available cars", "all cars"]

        if not keyword or any(term in keyword for term in generic_terms):
            filtered = data
        else:
            filtered = [
                car for car in data
                if keyword in car['name'].lower()
                or keyword in car['type'].lower()
                or keyword in car['description'].lower()
            ]

        if not filtered:
            await cl.Message(content=f"❌ Sorry, no cars found for '**{keyword}**'. Please try another keyword like `BMW`, `SUV`, or `Toyota`.").send()
            return "__tool_already_replied__"

        for car in filtered:
            await cl.Message(
                content=f"""**🚗 {car['name']}**
📊 **Type:** {car['type']} | 🛢️ Fuel: {car['fuel_capacity']} | ⚙️ Transmission: {car['transmission']}
👥 **Seats:** {car['seating_capacity']} | 💰 **Price:** {car['price_per_day']}/day
📝 {car['description']}
""",
                elements=[
                    Image(name=car['name'], display="inline", url=car['image_url'])
                ]
            ).send()

        return "__tool_already_replied__"

    except Exception as e:
        await cl.Message(content=f"❌ Error fetching car data: {e}").send()
        return "__tool_already_replied__"

# --- Agent ---
shopping_agent = Agent(
    name="CarRentalAgent",
    instructions="""
You are a warm, helpful, and polite car rental assistant. 
- Greet users nicely when they start the chat.
- Help them find cars by using the `get_cars` tool.
- Always respond clearly and professionally.
- If they type something like `BMW`, `SUV`, `Toyota`, or `show me cars`, use the tool to return matching cars.
- If no matches are found, gently suggest other options.
- If the tool already replied with messages, do not send anything else.
""",
    tools=[get_cars],
)

# --- Chat Start ---
@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set("agent", shopping_agent)
    cl.user_session.set("config", config)
    cl.user_session.set("chat_history", [])

    await cl.Message(
        content="""
👋 **Hello and welcome to Car Rental Assistant!**
I'm here to help you find the perfect car for your needs.

Just type something like:
- `Show me cars`
- `BMW`
- `SUV`
- `Electric` or `Diesel`

Let’s get you on the road! 🚗
"""
    ).send()

# --- Message Handler ---
@cl.on_message
async def on_message(message: cl.Message):
    thinking_msg = cl.Message(content="🧠 Thinking... please wait 🚗")
    await thinking_msg.send()

    agent = cl.user_session.get("agent")
    run_config = cl.user_session.get("config")
    history = cl.user_session.get("chat_history") or []

    history.append({"role": "user", "content": message.content})

    try:
        result = await Runner.run(
            starting_agent=agent,
            input=history,
            run_config=run_config
        )

        response_content = result.final_output or ""

        if response_content.strip() and response_content.strip() != "__tool_already_replied__":
            thinking_msg.content = response_content
            await thinking_msg.update()
        else:
            await thinking_msg.remove()

        cl.user_session.set("chat_history", result.to_input_list())

    except Exception as e:
        thinking_msg.content = f"❌ Error: {str(e)}"
        await thinking_msg.update()
