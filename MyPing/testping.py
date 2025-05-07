import csv

from ping3 import ping


def myping(addr):
    return ping(addr, unit='ms')


addresses = ['google.com', 'ya.ru', 'nsu.ru', 'pinterest.com', 'ozon.ru',
             'behance.net', 'hanbook.com', 'songsterr.com', 'muzton.com', 'doctorhouse.su']

with open("ping_info.csv", mode="w+") as out_file:
    file_writer = csv.writer(out_file, delimiter=",", lineterminator="\r")
    file_writer.writerow(["Addresses", "RTT, ms"])
    for address in addresses:
        ping_ms = myping(address)
        file_writer.writerow([address, int(ping_ms) if ping_ms is not None else "No connection"])

