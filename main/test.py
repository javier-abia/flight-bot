from flights import flight
from flights import flights_data
import json

f1 = flight('departure', 'IATA', 'destination', 'date', 'price', 'scales', 'duration')
f2 = flight('departure1', 'IATA1', 'destination1', 'date1', 'price1', 'scales1', 'duration1')
l = [f1,f2]

with open('test.json', 'w') as fl:
    json.dump([i.__dict__ for i in l], fl, indent=2)

with open('test.json', 'r') as fl:
    lnew = json.load(fl)

print(f'{lnew[0]}\n{lnew[1]}')