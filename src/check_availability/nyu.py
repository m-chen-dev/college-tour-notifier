from check_availability import AvailabilityStatus
from custom_logging import log, format_message, format_toast_title, format_message_for_university
from notifier import send_message
from playwright.sync_api import Page

UNIVERSITY = "NYU Tandon"
NYU_CAMUS_TOUR_URL = "https://connect.nyu.edu/portal/bk_campus_tour"

def get_availability_status_nyu(page : Page):
    page.reload()
        
    try:
        page.wait_for_selector(".item", timeout=5000)
    except TimeoutError:
        log("Page waited too long to load and find available openings")
        return AvailabilityStatus(False, None)
    
    for date_item in page.query_selector_all(".item"):
        legend = date_item.query_selector(".calendar_legend")
        if not legend:
            log("Legend element not found")
            continue
        
        is_available = legend.evaluate("el => el.classList.contains('available')")
        
        if not is_available:
            continue
        
        event = date_item.query_selector(".event")
        text_element = event.query_selector("p") if event else None
        text = text_element.text_content() if text_element else ""
        lines = text.splitlines() if text else []
        date_available = lines[1] if len(lines) >= 2 else ""
        
        return AvailabilityStatus(True, format_message(UNIVERSITY, date_available))
        
    return AvailabilityStatus(False, None)

def check_for_availability_nyu(page : Page):
    page.goto(NYU_CAMUS_TOUR_URL)
    
    availability_status = get_availability_status_nyu(page)
    if availability_status.success:
        send_message(availability_status.message, format_toast_title(UNIVERSITY), NYU_CAMUS_TOUR_URL)
    else:
        log(format_message_for_university(UNIVERSITY))
