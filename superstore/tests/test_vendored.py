class TestVendored:
    def test_gettimeseries(self):
        from superstore import getTimeSeries

        df = getTimeSeries()
        assert len(df) == 30
        assert len(df.columns) == 4
        assert df.columns.tolist() == ["A", "B", "C", "D"]

    def test_gettimeseries_ncol_nper(self):
        from superstore import getTimeSeries

        df = getTimeSeries(nper=100, ncol=10)
        assert len(df) == 100
        assert len(df.columns) == 10
        assert df.columns.tolist() == list("ABCDEFGHIJ")
