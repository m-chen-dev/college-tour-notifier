from check_availability import AvailabilityStatus
from custom_logging import log, format_message, format_toast_title, format_message_for_university
from notifier import send_message
from playwright.sync_api import Page

UNIVERSITY = "Princeton"
PRINCETON_CAMPUS_TOUR_URL = "https://apply.princeton.edu/portal/orange_key_tour"
month = "N/A"
year = "N/A"
has_parsed_month_and_year = False

def load_page(page : Page):
    try:
        page.wait_for_selector(".ui-datepicker-calendar", timeout=5000)
    except TimeoutError:
        log("Page waited too long to load and find available openings")
        return AvailabilityStatus(False, None)

def parse_month_and_year(page : Page):
    global month, year, has_parsed_month_and_year
    page.reload()
    
    load_page(page)
    
    date_picker_title = page.query_selector("#register_datepicker > div > div > div")
    
    if not date_picker_title:
        return
    
    month_label = date_picker_title.query_selector(".ui-datepicker-month")
    year_label = date_picker_title.query_selector(".ui-datepicker-year")
    month = month_label.text_content() if month_label else "N/A"
    year = year_label.text_content() if year_label else "N/A"
    has_parsed_month_and_year = True

def get_availability_status_princeton(page : Page):
    for row in page.query_selector_all("tr"):
        for day in row.query_selector_all("td"):
            is_available = day.evaluate("el => el.classList.contains('available')")
            
            if not is_available:
                continue
            
            text_element = day.query_selector("a") 
            date_available = f"{month} {text_element.text_content()} {year}" if text_element else ""
            return AvailabilityStatus(True, format_message(UNIVERSITY, date_available))
        
    return AvailabilityStatus(False, None)

def check_for_availability_princeton(page : Page):
    page.goto(PRINCETON_CAMPUS_TOUR_URL)
    
    if not has_parsed_month_and_year:
        parse_month_and_year(page)
    
    availability_status = get_availability_status_princeton(page)
    if availability_status.success:
        send_message(availability_status.message, format_toast_title(UNIVERSITY), PRINCETON_CAMPUS_TOUR_URL)
    else:
        log(format_message_for_university(UNIVERSITY))
        