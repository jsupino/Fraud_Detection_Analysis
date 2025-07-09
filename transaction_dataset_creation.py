from faker import Faker
import random
import csv
import os

fake = Faker('en_US')
num_records = 1000

us_cities = [
    "New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia",
    "San Antonio", "San Diego", "Dallas", "San Jose", "Austin", "Jacksonville",
    "Fort Worth", "Columbus", "Charlotte", "San Francisco", "Indianapolis",
    "Seattle", "Denver", "Washington", "Boston", "El Paso", "Nashville",
    "Detroit", "Oklahoma City", "Portland", "Las Vegas", "Memphis", "Louisville",
    "Baltimore", "Milwaukee", "Albuquerque", "Tucson", "Fresno", "Sacramento",
    "Kansas City", "Mesa", "Atlanta", "Omaha", "Colorado Springs", "Raleigh",
    "Long Beach", "Virginia Beach", "Miami", "Oakland", "Minneapolis", "Tulsa",
    "Wichita", "New Orleans", "Arlington"
]

try:
    print(f"Current working directory: {os.getcwd()}")

    with open('updatedtransactions.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['transaction_id', 'user_id', 'date', 'amount', 'category', 'location'])

        for i in range(num_records):
            transaction_id = i + 1
            user_id = random.randint(1,300)
            date = fake.date_time_between(start_date='-1y', end_date='now')
            amount = round(random.uniform(5.0, 20000.0), 2)
            category = random.choice(['clothing', 'electronics', 'groceries', 'restaurant', 'other'])
            location = random.choice(us_cities)
            
            writer.writerow([transaction_id, user_id, date, amount, category, location])
    print("File saved successfully!")
except Exception as e:
    print(f"Error occurred: {e}")