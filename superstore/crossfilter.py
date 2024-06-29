from coolname import generate as generateName
from datetime import datetime, timedelta
from random import choice, randint, random
from uuid import uuid4

_MACHINE_TYPES = ("edge", "core", "worker")
_REGIONS = ("na", "eu", "ap")
_ZONES = ("A", "B", "C", "D")

__all__ = (
    "machines",
    "MACHINE_SCHEMA",
    "usage",
    "USAGE_SCHEMA",
    "status",
    "STATUS_SCHEMA",
    "jobs",
    "JOBS_SCHEMA",
)


def _id():
    return str(uuid4()).rsplit("-", 1)[-1]


MACHINE_SCHEMA = {
    "machine_id": str,
    # "name": common name
    "kind": str,
    "cores": int,
    "region": str,
    "zone": str,
}


def machines(count: int = 100):
    """Generate data representing different kinds of machines.

    Machines have the following fields:

      machine_id: uuid
      name: common name
      kind: kind of machine
      capacity: number in 4,8,16,32,64
      region:
      zone:
    """
    ret = []
    for _ in range(count):
        rand = random()
        if rand < 0.2:
            kind = "core"
            cores = choice((8, 16, 32))
        elif rand < 0.7:
            kind = "edge"
            cores = choice((4, 8))
        else:
            kind = "worker"
            cores = choice((32, 64))

        machine = {
            "machine_id": _id(),
            # "name": "-".join(generateName(2)),
            "kind": kind,
            "cores": cores,
            "region": choice(_REGIONS),
            "zone": choice(_ZONES),
        }
        ret.append(machine)

    return ret


USAGE_SCHEMA = {
    "cpu": float,
    "mem": float,
    "free": float,
    "network": float,
    "disk": float,
}
USAGE_SCHEMA.update(MACHINE_SCHEMA)


def _clip(value, value_min, value_max):
    return round(max(min(value, value_max), value_min), 2)


def _randrange(low, high):
    return (random() * (high - low)) + low


def usage(machine):
    """Generate usage information based on type of machine

    Fields:
      machine_id
      cpu in 0-100
      mem in 0-100
      free in 100-0
      network in 0-100,
      disk in 0-100
    """
    ret = machine.copy()

    if ret.get("cpu", None) is None or random() < 0.1:
        ret.update(
            {
                "cpu": 0,
                "mem": 0,
                "free": 100,
                "network": 0,
                "disk": 0,
            }
        )
        return ret

    if machine["kind"] == "core":
        # bursty cpu/mem/network/disk
        ret["cpu"] = _randrange((ret.get("cpu") or 15) - 15, (ret.get("cpu") or 35) + 15)
        ret["mem"] = _randrange((ret.get("mem") or 35) - 15, (ret.get("mem") or 55) + 15)
        ret["network"] = _randrange((ret.get("network") or 35) - 15, (ret.get("network") or 55) + 15)
        ret["disk"] = _randrange((ret.get("disk") or 35) - 15, (ret.get("disk") or 55) + 15)
    elif machine["kind"] == "edge":
        # low cpu, medium mem, high network/disk
        ret["cpu"] = _randrange((ret.get("cpu") or 15) - 5, (ret.get("cpu") or 35) + 5)
        ret["mem"] = _randrange((ret.get("mem") or 35) - 5, (ret.get("mem") or 55) + 5)
        ret["network"] = _randrange((ret.get("network") or 65) - 5, (ret.get("network") or 75) + 5)
        ret["disk"] = _randrange((ret.get("disk") or 65) - 5, (ret.get("disk") or 75) + 5)
    else:
        # high cpu, high mem, high network/disk
        ret["cpu"] = _randrange((ret.get("cpu") or 75) - 5, (ret.get("cpu") or 85) + 5)
        ret["mem"] = _randrange((ret.get("mem") or 75) - 5, (ret.get("mem") or 85) + 5)
        ret["network"] = _randrange((ret.get("network") or 75) - 5, (ret.get("network") or 85) + 5)
        ret["disk"] = _randrange((ret.get("disk") or 75) - 5, (ret.get("disk") or 85) + 5)

    # clip everything
    ret["cpu"] = _clip(ret["cpu"], 0, 100)
    ret["mem"] = _clip(ret["mem"], 0, 100)
    ret["free"] = 100 - ret["mem"]
    ret["network"] = _clip(ret["network"], 0, float("inf"))
    ret["disk"] = _clip(ret["disk"], 0, float("inf"))
    return ret


STATUS_SCHEMA = {
    "status": str,
    "last_update": datetime,
}
STATUS_SCHEMA.update(USAGE_SCHEMA)


def status(machine):
    """Generate status information based on type of machine

    Fields:
      machine_id
      status: idle, active, capacity, unknown
      last_update: datetime
    """
    ret = machine.copy()
    ret["last_update"] = datetime.utcnow()

    if machine.get("cpu", None) is None:
        ret["status"] = "unknown"
        return ret

    if machine.get("cpu", 0) < 20:
        ret["status"] = "idle"
    elif machine.get("cpu", 0) > 80:
        ret["status"] = "capacity"
    else:
        ret["status"] = "active"
    return ret


JOBS_SCHEMA = {
    "machine_id": str,
    "job_id": str,
    "name": str,
    "units": int,
    "start_time": datetime,
    "end_time": datetime,
}


def jobs(machine):
    """Generate job information based on type of machine
    Fields:
      machine_id
      name:
      units:
      start_time: datetime
      end_time: datetime
    """
    if machine.get("kind", "") != "worker":
        return

    if random() < 0.5:
        return

    ret = {
        "machine_id": machine["machine_id"],
        "job_id": _id(),
        "name": "-".join(generateName(2)),
        "units": choice((1, 2, 4, 8)),
        "start_time": datetime.utcnow(),
        "end_time": datetime.utcnow() + timedelta(seconds=randint(0, 400)),
    }
    return ret
