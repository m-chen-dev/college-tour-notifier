from check_availability import AvailabilityStatus
from custom_logging import log, format_message, format_toast_title, format_message_for_university
from notifier import send_message
from playwright.sync_api import Page

UNIVERSITY = "Princeton"
PRINCETON_CAMPUS_TOUR_URL = "https://apply.princeton.edu/portal/orange_key_tour"
MONTH = "August"
YEAR = "2026"

def get_availability_status_princeton(page : Page):
    page.reload()
        
    try:
        page.wait_for_selector(".ui-datepicker-calendar", timeout=5000)
    except TimeoutError:
        log("Page waited too long to load and find available openings")
        return AvailabilityStatus(False, None)
    
    for row in page.query_selector_all("tr"):
        for day in row.query_selector_all("td"):
            is_available = day.evaluate("el => el.classList.contains('available')")
            
            if not is_available:
                continue
            
            text_element = day.query_selector("a") 
            date_available = f"{MONTH} {text_element.text_content()} {YEAR}" if text_element else ""
            return AvailabilityStatus(True, format_message(UNIVERSITY, date_available))
        
    return AvailabilityStatus(False, None)

def check_for_availability_princeton(page : Page):
    page.goto(PRINCETON_CAMPUS_TOUR_URL)
    
    availability_status = get_availability_status_princeton(page)
    if availability_status.success:
        send_message(availability_status.message, format_toast_title(UNIVERSITY), PRINCETON_CAMPUS_TOUR_URL)
    else:
        log(format_message_for_university(UNIVERSITY))
        