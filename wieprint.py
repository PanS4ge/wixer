import datetime
from colorama import *

Time = Style.BRIGHT
Warning = Fore.YELLOW
Error = Fore.LIGHTRED_EX
Critical = Fore.RED
Debug = Fore.LIGHTMAGENTA_EX
Info = Fore.LIGHTBLUE_EX
Ok = Fore.GREEN
Success = Fore.LIGHTGREEN_EX
RESET = Style.RESET_ALL

allow_debug = True

def info(text: str = None) -> str:
    print(Time + f"[ {datetime.datetime.now().strftime('%H:%M:%S')} ]" + " " + Info + "[ INFO ]" + " " + f"{text}" + RESET)
    #return text

def warning(text: str = None) -> None:
    print(Time + f"[ {datetime.datetime.now().strftime('%H:%M:%S')} ]" + " " + Warning + "[ WARNING ]" + " " + f"{text}" + RESET)

def debug(text: str = None) -> None:
    if(allow_debug):
        print(Time + f"[ {datetime.datetime.now().strftime('%H:%M:%S')} ]" + " " + Debug + "[ DEBUG ]" + " " + f"{text}" + RESET)

def critical(text: str = None) -> None:
    print(Time + f"[ {datetime.datetime.now().strftime('%H:%M:%S')} ]" + " " + Critical + "[ CRITICAL ]" + " " + f"{text}" + RESET)

def ok(text: str = None) -> None:
    print(Time + f"[ {datetime.datetime.now().strftime('%H:%M:%S')} ]" + " " + Ok + "[ OK ]" + " " + f"{text}" + RESET)

def success(text: str = None) -> None:
    print(Time + f"[ {datetime.datetime.now().strftime('%H:%M:%S')} ]" + " " + Success + "[ SUCCESS ]" + " " + f"{text}" + RESET)

def ttToReturn(info: str = None, text: str = None) -> None:
    return (f"[ {datetime.datetime.now().strftime('%H:%M:%S')} ]" + " " + "[ " + info + " ]" + " " + f"{text}{RESET}\n")