from colorama import Fore, init                                                   

init(convert=True)                                                                  
default_color = 0x4A86E8                                                            
error_color = 0xFF4040
warning_color = 0xEED202
admin_color = 0x00B054


def red(text: str):                                                                
    colored_text = Fore.LIGHTRED_EX + str(text) + Fore.RESET
    return colored_text


def blue(text: str):                                                                
    colored_text = Fore.LIGHTBLUE_EX + str(text) + Fore.RESET
    return colored_text


def green(text: str):                                                             
    colored_text = Fore.LIGHTGREEN_EX + str(text) + Fore.RESET
    return colored_text


def yellow(text: str):                                                             
    colored_text = Fore.LIGHTYELLOW_EX + str(text) + Fore.RESET
    return colored_text


def pink(text: str):                                                            
    colored_text = Fore.LIGHTMAGENTA_EX + str(text) + Fore.RESET
    return colored_text


def cyan(text: str):                                                               
    colored_text = Fore.LIGHTCYAN_EX + str(text) + Fore.RESET
    return colored_text