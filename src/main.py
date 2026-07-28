from resource_manager import PlayWrightResourceManager
from check_availability import check_all_for_availability
from custom_logging import log
from time import sleep

def main(): 
    try:
        with PlayWrightResourceManager() as resource_manager:
            while True:
                check_all_for_availability(resource_manager.page)
                sleep(60)
                
    except KeyboardInterrupt:
        log("Program cancelled abruptly")

if __name__ == "__main__":
    main()
