# AUTOGENERATED! DO NOT EDIT! File to edit: 00_roster.ipynb (unless otherwise specified).

__all__ = ['ShiftProperties', 'Shift', 'Roster']

# Cell
from dataclasses import dataclass
from datetime import datetime, timedelta, date, time
from ics import Calendar, Event
import re
from typing import Optional
from zoneinfo import ZoneInfo


@dataclass
class ShiftProperties:
    name: str
    starting_hour: timedelta
    duration: timedelta


@dataclass
class Shift:
    properties: ShiftProperties
    date: datetime

    def __post_init__(self):
        self.beginning: datetime = self.date + self.properties.starting_hour


# Cell
@dataclass
class Roster:
    shifts: list[Shift]
    name: str = "Jane Doe"
    _year: int = 2022
    _month: int = 1  # TODO: Read from Excel
    _dayp = re.compile(r"MO|DI|MI|DO|FR|SA|SO")
    _datep = re.compile(r"\d{2}")

    @classmethod
    def from_dict(
        cls, input: dict[str, str], mapper: Optional[dict] = None
    ) -> "Roster":
        shifts = []
        for date_str, abbr in input.items():
            props = mapper[abbr]
            if props is None:
                continue
            date = datetime(
                year=cls._year,
                month=cls._month,
                day=int(cls._datep.search(date_str).group()),
                tzinfo=ZoneInfo("Europe/Berlin"),
            )
            shift = Shift(props, date=date)
            shifts.append(shift)
        return cls(shifts=shifts)

    def to_ics(self):
        c = Calendar()
        for shift in self.shifts:
            e = Event()
            e.name = shift.properties.name
            e.begin = shift.beginning
            e.duration = shift.properties.duration
            c.events.add(e)
        return c
