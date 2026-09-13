from tools.tavily_tool import tavily_search
from tools.flight_tool import search_flights

# res = tavily_search("best hotels in hyderabad")
# print(res)

res = search_flights("Give me a plan of 7 days trip from hyd to banglore")
print(res)