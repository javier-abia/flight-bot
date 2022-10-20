from flights import flight
from flights import flights_data
import json

f1 = flight('departure', 'IATA', 'destination', 'date', 'price', 'scales', 'duration')
f2 = flight('departure1', 'IATA1', 'destination1', 'date1', 'price1', 'scales1', 'duration1')
l = [f1,f2]

with open('test.json', 'w') as fl:
    for flight in l:
        json.dump(flight.__dict__, fl, indent=2)

        
