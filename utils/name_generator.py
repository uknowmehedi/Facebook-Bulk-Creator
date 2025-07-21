import random

names = {
    "male": ["John", "David", "Alex", "Mark"],
    "female": ["Sophia", "Lily", "Emily", "Ava"]
}

def get_random_name():
    gender = random.choice(["male", "female"])
    return random.choice(names[gender]), random.choice(names[gender])

def get_random_dob():
    return random.randint(1, 28), str(random.randint(1, 12)), random.randint(1988, 1998)