"""
    NMAP search script - runs nmap when quiz view is started, collects
    all mats within subnet

    Author: Jake Poirier
    Date: 5/5/2016
"""

import subprocess


def run_nmap():
    subprocess.call(["sh", "/home/pi/HoppoRoo/HoppoRoo/scripts/search_nmap.sh"])


def parse_nmap():
    """
    Script to parse output of nmap and find ip addresses
    of mats that are connected
    :return: list of ip addresses connected
    """
    dir = "/home/pi/HoppoRoo/HoppoRoo/scripts/iplist.txt"
    #dir = 'C:\\Users\\Jake\\git3\\HoppoRoo\\scripts\\iplist.txt'
    with open(dir, 'r') as nmap_file:
        nmap_contents = nmap_file.readlines()

    start_index = nmap_contents.index("Nmap scan report for 192.168.42.1\n")

    iparr = []
    for line in nmap_contents[start_index+2:]:
        if 'Host is up' not in line and 'Nmap done' not in line:
            iparr.append(line.replace("Nmap scan report for ", "").replace("\n", ""))

    esp_arr = []
    for device_index in range(len(iparr)):
        if device_index < len(iparr) - 1:
            if "5C:CF:7F" in iparr[device_index+1]:
                esp_arr.append(iparr[device_index])

    return esp_arr

if __name__ == '__main__':
    parse_nmap()