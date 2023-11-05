class TestSuperstore:
    def test_superstore(self):
        import pandas as pd

        from superstore import employees, superstore

        df = superstore()
        assert isinstance(df, pd.DataFrame)
        assert list(df.columns) == [
            "Row ID",
            "Order ID",
            "Order Date",
            "Ship Date",
            "Ship Mode",
            "Customer ID",
            "Segment",
            "Country",
            "City",
            "State",
            "Postal Code",
            "Region",
            "Product ID",
            "Category",
            "Sub-Category",
            "Sales",
            "Quantity",
            "Discount",
            "Profit",
        ]
        assert df.shape[0] == 1000
        df = employees()
        assert isinstance(df, pd.DataFrame)
        assert list(df.columns) == [
            "Row ID",
            "Employee ID",
            "First Name",
            "Surname",
            "Prefix",
            "Suffix",
            "Phone Number",
            "Email",
            "SSN",
            "Street",
            "City",
            "Postal Code",
            "Region",
            "State",
            "Country",
            "Start Date",
            "Date of Birth",
        ]
        assert df.shape[0] == 1000
