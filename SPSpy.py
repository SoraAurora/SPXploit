import pyshark
import json
from print_color import print

def capture_packets(interface, display_filter):
    # Use pyshark to capture packets on the specified interface with the given display filter
    cap = pyshark.LiveCapture(interface=interface, display_filter=display_filter , include_raw=True,use_json=True)

    for packet in cap:
        field_names = packet.tcp._all_fields
        field_values = packet.tcp._all_fields.values()
        for field_name in field_names:
            for field_value in field_values:
                #find tcp payload
                if field_name == 'tcp.payload':
                    try:
                        # converts array contain hex to ascii and prints them out
                        byte_string = bytes.fromhex(field_value[0])
                        ascii_string = byte_string.decode("ASCII")
                        print(f'{field_name} -- {ascii_string}' ,tag="DATA",tag_color="green",color='yellow' )
                    except:
                        continue

def ascii_logo():  
    print("\n")                                                                                                                                                                                                               
    print("            SSSSSSSSSSSSSSS PPPPPPPPPPPPPPPPP           SSSSSSSSSSSSSSS                                               ",color='purple')
    print("            SS:::::::::::::::SP::::::::::::::::P        SS:::::::::::::::S                                         ",color='purple')
    print("            S:::::SSSSSS::::::SP::::::PPPPPP:::::P      S:::::SSSSSS::::::S                                         ",color='purple')
    print("            S:::::S     SSSSSSSPP:::::P     P:::::P     S:::::S     SSSSSSS                                         ",color='purple')
    print("            S:::::S              P::::P     P:::::P     S:::::S           ppppp   pppppppppyyyyyyy           yyyyyyy",color='purple')
    print("            S:::::S              P::::P     P:::::P     S:::::S           p::::ppp:::::::::py:::::y         y:::::y ",color='purple')
    print("            S::::SSSS           P::::PPPPPP:::::P       S::::SSSS        p:::::::::::::::::py:::::y       y:::::y  ",color='purple')
    print("            SS::::::SSSSS      P:::::::::::::PP         SS::::::SSSSS   pp::::::ppppp::::::py:::::y     y:::::y   ",color='purple')
    print("                SSS::::::::SS    P::::PPPPPPPPP             SSS::::::::SS  p:::::p     p:::::p y:::::y   y:::::y    ",color='purple')
    print("                SSSSSS::::S   P::::P                        SSSSSS::::S p:::::p     p:::::p  y:::::y y:::::y     ",color='purple')
    print("                        S:::::S  P::::P                             S:::::Sp:::::p     p:::::p   y:::::y:::::y      ",color='purple')
    print("                        S:::::S  P::::P                             S:::::Sp:::::p    p::::::p    y:::::::::y       ",color='purple')
    print("            SSSSSSS     S:::::SPP::::::PP               SSSSSSS     S:::::Sp:::::ppppp:::::::p     y:::::::y        ",color='purple')
    print("            S::::::SSSSSS:::::SP::::::::P               S::::::SSSSSS:::::Sp::::::::::::::::p       y:::::y         ",color='purple')
    print("            S:::::::::::::::SS P::::::::P               S:::::::::::::::SS p::::::::::::::pp       y:::::y          ",color='purple')
    print("            SSSSSSSSSSSSSSS   PPPPPPPPPP                SSSSSSSSSSSSSSS   p::::::pppppppp        y:::::y           ",color='purple')
    print("                                                                        p:::::p               y:::::y            ",color='purple')
    print("                                                                        p:::::p              y:::::y             ",color='purple')
    print("                                                                        p:::::::p            y:::::y              ",color='purple')
    print("                                                                        p:::::::p           y:::::y               ",color='purple')
    print("                                                                        p:::::::p          yyyyyyy                ",color='purple')
    print("                                                                        ppppppppp                                 ",color='purple')
    print("\n")                                                                                          


if __name__ == "__main__":
    ascii_logo()
    print("Capturing..." , tag="Info",tag_color="cyan",color='white')
    # Specify the loopback interface and display filter
    interface = "Adapter for loopback traffic capture"
    display_filter = "json"

    # Start capturing packets and processing JSON data
    capture_packets(interface, display_filter)
