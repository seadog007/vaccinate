from typing import Tuple, List, Any
import requests
from bs4 import BeautifulSoup
from hospital_types import HospitalID, AppointmentAvailability


def parseTzuchiTaipei() -> Tuple[HospitalID, AppointmentAvailability]:
    r = requests.get(
        "https://reg-prod.tzuchi-healthcare.org.tw/tchw/HIS5OpdReg/OpdTimeShow?Pass=XD;0022",
        verify="../data/tzuchi-healthcare-org-tw-chain.pem",
        timeout=2,
    )
    soup = BeautifulSoup(r.text, "html.parser")
    table = soup.find("table", {"id": "MainContent_gvOpdList"})
    rows = table.find_all("tr", {"class": "OpdListD"})
    rows = filter(rowContainsAppointment, rows)
    # PEP8 Style: if list is not empty, then there are appointments
    return (
        8,
        AppointmentAvailability.AVAILABLE
        if bool(rows)
        else AppointmentAvailability.UNAVAILABLE,
    )


def rowContainsAppointment(row: List[Any]) -> bool:
    columns = row.find_all("td")
    column_two_has_appointment = bool(columns[1].find_all("a"))
    column_three_has_appointment = bool(columns[2].find_all("a"))
    return column_two_has_appointment or column_three_has_appointment
