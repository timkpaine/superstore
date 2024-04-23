import pandas as pd
from faker import Faker
from random import choice, randint, random

from .utils import US_SECTORS, US_SECTORS_MAP

fake = Faker()

__all__ = (
    "superstore",
    "employees",
)


def superstore(count=1000):
    data = []
    for id in range(count):
        dat = {}
        dat["Row ID"] = id
        dat["Order ID"] = fake.ein()
        dat["Order Date"] = fake.date_this_year()
        dat["Ship Date"] = fake.date_between_dates(dat["Order Date"]).strftime("%Y-%m-%d")
        dat["Order Date"] = dat["Order Date"].strftime("%Y-%m-%d")
        dat["Ship Mode"] = choice(["First Class", "Standard Class", "Second Class"])
        dat["Customer ID"] = fake.license_plate()
        dat["Segment"] = choice(["A", "B", "C", "D"])
        dat["Country"] = "US"
        dat["City"] = fake.city()
        dat["State"] = fake.state()
        dat["Postal Code"] = fake.zipcode()
        dat["Region"] = choice(["Region %d" % i for i in range(5)])
        dat["Product ID"] = fake.bban()
        sector = choice(list(US_SECTORS))
        industry = choice(list(US_SECTORS_MAP[sector]))
        dat["Category"] = sector
        dat["Sub-Category"] = industry
        dat["Sales"] = randint(1, 100) * 100
        dat["Quantity"] = randint(1, 100) * 10
        dat["Discount"] = round(random() * 100, 2)
        dat["Profit"] = round(random() * 1000, 2)
        data.append(dat)
    return pd.DataFrame(data)


def employees(count=1000):
    data = []
    for id in range(count):
        dat = {}
        dat["Row ID"] = id
        dat["Employee ID"] = fake.unique.license_plate()
        dat["First Name"] = fake.first_name()
        dat["Surname"] = fake.last_name()
        dat["Prefix"] = fake.prefix()
        dat["Suffix"] = fake.suffix()
        dat["Phone Number"] = fake.unique.phone_number()
        dat["Email"] = fake.safe_email()
        dat["SSN"] = fake.ssn()
        dat["Street"] = fake.street_address()
        dat["City"] = fake.city()
        dat["Postal Code"] = fake.zipcode()
        dat["Region"] = choice(["Region %d" % i for i in range(5)])
        dat["State"] = fake.state()
        dat["Country"] = "US"
        dat["Start Date"] = fake.date_between()  # 30yrs ago to today
        dat["Date of Birth"] = fake.date_of_birth(minimum_age=18, maximum_age=70)
        data.append(dat)
    return pd.DataFrame(data)
