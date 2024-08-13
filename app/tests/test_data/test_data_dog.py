from faker import Faker


fake = Faker(locale="ru")

fake_dog_data = []


basic_response = {
    "page_number": 1,
    "size": 10,
    "total_pages": 0,
    "total_result": 0,
    "result": [],
}
fake_incorrect_dog_data = {
    "1": {
        "apartment": "apart",
        "name": fake.first_name(),
        "breed": fake.last_name(),
    },
    "2": {
        "apartment": 2,
        "name": True,
        "breed": fake.last_name(),
    },
    "3": {
        "apartment": 3,
        "name": fake.first_name(),
        "breed": 254,
    },
    "4": {
        "apartment": 3,
        "breed": 254,
    },
}

for num in range(1, 4):
    fake_dog_data.append(
        {
            "apartment": num,
            "name": fake.first_name(),
            "breed": fake.last_name(),
        },
    )
