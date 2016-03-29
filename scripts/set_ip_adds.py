
def parse_nmap():
    with open("nmap.txt", 'r') as nmap_file:
        nmap_contents = nmap_file.readlines()

    start_index = nmap_contents.index("Nmap scan report for 192.168.42.1\n")

    iparr = []
    for line in nmap_contents[start_index+2:]:
        if 'Host is up' not in line and 'Nmap done' not in line:
            iparr.append(line.replace("Nmap scan report for ", "").replace("\n", ""))

    esp_arr = []
    for device_index in range(len(iparr)):
        print device_index
        if device_index < len(iparr) - 1:
            if "5C:CF:7F" in iparr[device_index+1]:
                esp_arr.append(iparr[device_index])
