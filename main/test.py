from flights import flight
from flights import flights_data
import pickle




with open('./docs/show/old_flights.txt', 'rb') as f:
    data = pickle.load(f)

fd = flights_data('asd', 'asd')
fd.show_flights(data)
