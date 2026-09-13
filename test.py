from tools.tavily_tool import tavily_search
from tools.flight_tool import search_flights
from backend import run_travel_agent

# res = tavily_search("best hotels in hyderabad")
# print(res)

# res = search_flights("Give me a plan of 7 days trip from hyd to banglore")
# print(res)


user_input = input("Enter Travel request:")
response = run_travel_agent(
    user_input=user_input,
    thread_id="test_user"
)

print("\nFINAL_RESPONSE:\n")
print(response["answer"])