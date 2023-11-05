class TestVendored:
    def test_gettimeseries(self):
        from superstore import getTimeSeries

        df = getTimeSeries()
        assert len(df) == 30
        assert len(df.columns) == 4
        assert df.columns.tolist() == ["A", "B", "C", "D"]
