import sys, re, optparse as opt, subprocess as sub

try:
    assert ('linux' in sys.platform), "This code runs on Linux only."
except AssertionError as error:
    print(error)
    print("\nProgram exiting ...")
    sys.exit()

def get_arguments():
    arg_parser = opt.OptionParser()
    arg_parser.add_option("-i", "--interface", dest = "interface", help = "The network interface name")
    arg_parser.add_option("-m", "--mac", dest = "newmac", help = "The new Mac Address")
    (opts, args) = arg_parser.parse_args()
    if not opts.interface:
        arg_parser.error("Please specify a network interface use --help for the module help")
    elif not opts.newmac:
        arg_parser.error("Please specify a Mac Address use --help for the module help")
    if not re.match(r"(\w\w:){5}\w\w", opts.newmac):
        arg_parser.error("Please enter a valid Mac address")
    return opts

def change_mac(interface, newmac):
    sub.call(["ifconfig", "{0}".format(interface), "down"])
    sub.call(["ifconfig", "{0}".format(interface), "hw", "ether", "{0}".format(newmac)])
    sub.call(["ifconfig", "{0}".format(interface), "up"])

def get_current_mac(interface):
    mac_address_match_object = re.search(r"(\w\w:){5}\w\w", sub.check_output(["ifconfig", interface]))
    if  not mac_address_match_object:
        return None
    else:    
        return mac_address_match_object.group(0)

options = get_arguments()
sub.call(["ifconfig", "{}".format(options.interface), "up"])
current_mac = get_current_mac(options.interface)
print("Current Mac Address for {0} is {1}".format(options.interface, current_mac))
change_mac(options.interface,options.newmac)
current_mac = get_current_mac(options.interface)

if current_mac == options.newmac:
    print("Mac Address changed to {}".format(current_mac))
else:
    print("Interface does not have a Mac Address")