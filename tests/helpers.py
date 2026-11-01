from faker import Faker

fake = Faker()


def generate_user_data():
    return {
        "email": f"{fake.user_name()}{fake.random_number(digits=6)}@example.com",
        "password": fake.password(length=10),
        "name": fake.first_name(),  # случайное имя, например Anna
    }
