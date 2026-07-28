from dataclasses import dataclass
from enum import Enum
from playwright.sync_api import Page

@dataclass
class AvailabilityStatus:
    success : bool
    message : str | None

class University(Enum):
    PRINCETON = 1,
    NYU_TANDON = 2

from .princeton import check_for_availability_princeton
from .nyu import check_for_availability_nyu

university_checking = {
    University.PRINCETON: check_for_availability_princeton,
    University.NYU_TANDON: check_for_availability_nyu
}

def check_for_availability(page : Page, university : University):
    if university not in university_checking:
        return
    
    university_checking[university](page)

def check_all_for_availability(page : Page):
    for university in University:
        check_for_availability(page, university)
