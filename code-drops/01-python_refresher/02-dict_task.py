# Dictionary Asignment

my_vehicle = {
    "model": "K5",
    "make": "KIA",
    "year": 2013,
    "mileage": 60000
}

for keys, values in zip(my_vehicle.keys(), my_vehicle.values()):
    print(f"{keys}: {values}")

vehicle2 = my_vehicle.copy()
vehicle2["number_of_tires"] = 4
vehicle2.pop("mileage")
print(vehicle2)