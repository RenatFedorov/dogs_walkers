from faker import Faker

fake = Faker(locale="ru")

fake_walker_data = []


basic_response = {
    "page_number": 1,
    "size": 10,
    "total_pages": 0,
    "total_result": 0,
    "result": [],
}
fake_incorrect_walker_data = {
    "1": {
        "name": 254,
        "surname": fake.last_name(),
        "active": True,
    },
    "2": {
        "name": fake.first_name(),
        "surname": 221,
        "active": True,
    },
    "3": {
        "surname": fake.last_name(),
        "active": 254,
    },
}

for _ in range(1, 4):
    fake_walker_data.append(
        {
            "name": fake.first_name(),
            "surname": fake.last_name(),
            "active": True,
        },
    )
