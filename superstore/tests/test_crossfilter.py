from datetime import datetime
from random import randint
from unittest.mock import patch

from superstore.crossfilter import JOBS_SCHEMA, MACHINE_SCHEMA, STATUS_SCHEMA, USAGE_SCHEMA, _clip, _id, _randrange, jobs, machines, status, usage


class TestCrossfilters:
    def test_id(self):
        with patch("superstore.crossfilter.uuid4") as uuidmock:
            uuidmock.return_value = "1-2-3-abc"
            assert _id() == "abc"

    def test_clip(self):
        for _ in range(100):
            assert 10 <= _clip(randint(0, 100), 10, 20) <= 20

    def test_clip_inf(self):
        for _ in range(100):
            assert 10 <= _clip(randint(0, 100), 10, float("inf"))

    def test_randrange(self):
        for _ in range(100):
            assert 10 < _randrange(10, 20) < 20

    def test_schema_invariance(self):
        assert JOBS_SCHEMA == {
            "machine_id": str,
            "job_id": str,
            "name": str,
            "units": int,
            "start_time": datetime,
            "end_time": datetime,
        }
        assert MACHINE_SCHEMA == {
            "machine_id": str,
            "kind": str,
            "cores": int,
            "region": str,
            "zone": str,
        }
        assert STATUS_SCHEMA == {
            "machine_id": str,
            "kind": str,
            "cores": int,
            "region": str,
            "zone": str,
            "cpu": float,
            "mem": float,
            "free": float,
            "network": float,
            "disk": float,
            "status": str,
            "last_update": datetime,
        }
        assert USAGE_SCHEMA == {
            "machine_id": str,
            "kind": str,
            "cores": int,
            "region": str,
            "zone": str,
            "cpu": float,
            "mem": float,
            "free": float,
            "network": float,
            "disk": float,
        }

    def test_machines(self):
        some_machines = machines(100)
        assert isinstance(some_machines, list)
        assert len(some_machines) == 100
        for machine in some_machines:
            assert len(machine["machine_id"]) == 12
            assert machine["kind"] in ("core", "edge", "worker")
            assert machine["region"] in ("na", "eu", "ap")
            assert machine["zone"] in "ABCD"
            assert machine["cores"] in (4, 8, 16, 32, 64)

    def test_usage(self):
        machine = machines(1)[0]

        assert usage({}) == {"cpu": 0, "disk": 0, "free": 100, "mem": 0, "network": 0}

        expected = {"cpu": 0, "disk": 0, "free": 100, "mem": 0, "network": 0}
        expected.update(machine)

        assert usage(machine) == expected

    def test_status(self):
        with patch("superstore.crossfilter.datetime") as dt:
            dt.utcnow.return_value = datetime(2020, 1, 1)

            machine = machines(1)[0]
            m_usage = usage(machine)
            assert status({}) == {"last_update": datetime(2020, 1, 1, 0, 0), "status": "unknown"}

            expected = machine.copy()
            expected.update({"last_update": datetime(2020, 1, 1, 0, 0), "status": "unknown"})
            assert status(machine) == expected

            expected = m_usage.copy()
            expected["last_update"] = datetime(2020, 1, 1)
            m_usage["cpu"] = 0.0
            expected["cpu"] = 0.0
            expected["status"] = "idle"
            assert status(m_usage) == expected

            m_usage["cpu"] = 50.0
            expected["cpu"] = 50.0
            expected["status"] = "active"
            assert status(m_usage) == expected

            m_usage["cpu"] = 100.0
            expected["cpu"] = 100.0
            expected["status"] = "capacity"
            assert status(m_usage) == expected

    def test_jobs(self):
        with patch("superstore.crossfilter.datetime") as dt:
            dt.utcnow.return_value = datetime(2020, 1, 1)

            machine = machines(1)[0]
            assert jobs({}) is None

            for _ in range(100):
                job = jobs(machine)
                if job:
                    assert job["machine_id"] == machine["machine_id"]
                    assert len(job["job_id"]) == 12
                    assert job["start_time"] == datetime(2020, 1, 1)
                    assert len(job["name"].split("-")) == 2
