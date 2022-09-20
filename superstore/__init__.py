# *****************************************************************************
#
# Copyright (c) 2021, the superstore authors.
#
# This file is part of the superstore library, distributed under the terms of
# the Apache License 2.0.  The full license can be found in the LICENSE file.
#

__version__ = "0.1.0"

import pandas as pd
import finance_enums
from faker import Faker
from random import random, randint, choice

fake = Faker()


def superstore(count=1000):
    data = []
    for id in range(count):
        dat = {}
        dat["Row ID"] = id
        dat["Order ID"] = fake.ein()
        dat["Order Date"] = fake.date_this_year()
        dat["Ship Date"] = fake.date_between_dates(dat["Order Date"]).strftime(
            "%Y-%m-%d"
        )
        dat["Order Date"] = dat["Order Date"].strftime("%Y-%m-%d")
        dat["Ship Mode"] = choice(["First Class", "Standard Class", "Second Class"])
        dat["Ship Mode"] = choice(["First Class", "Standard Class", "Second Class"])
        dat["Customer ID"] = fake.license_plate()
        dat["Segment"] = choice(["A", "B", "C", "D"])
        dat["Country"] = "US"
        dat["City"] = fake.city()
        dat["State"] = fake.state()
        dat["Postal Code"] = fake.zipcode()
        dat["Region"] = choice(["Region %d" % i for i in range(5)])
        dat["Product ID"] = fake.bban()
        sector = choice(list(finance_enums.US_SECTORS))
        industry = choice(list(finance_enums.US_SECTORS_MAP[sector]))
        dat["Category"] = sector
        dat["Sub-Category"] = industry
        dat["Sales"] = randint(1, 100) * 100
        dat["Quantity"] = randint(1, 100) * 10
        dat["Discount"] = round(random() * 100, 2)
        dat["Profit"] = round(random() * 1000, 2)
        data.append(dat)
    return pd.DataFrame(data)
