import time
import serial

STAT_FOLDER = "/sys/class/net/{}/statistics"
RX_BYTES = STAT_FOLDER + "/rx_bytes"
TX_BYTES = STAT_FOLDER + "/tx_bytes"

DEV = "eth0"


def get_bytes(dev):
    rx = int(get_rx_bytes(dev))
    tx = int(get_tx_bytes(dev))

    return rx, tx


def bytes_to_mbit(bytes):
    return (bytes * 8) / 1024**2


def get_rx_bytes(dev):
    with open(RX_BYTES.format(dev)) as f:
        content = f.readline()
    return content


def get_tx_bytes(dev):
    with open(TX_BYTES.format(dev)) as f:
        content = f.readline()
    return content


def main():
    s = serial.Serial("/dev/ttyACM0", 9600)

    old_rx, old_tx = get_bytes(DEV)
    t = 5

    while True:
        time.sleep(t)

        rx, tx = get_bytes(DEV)

        tx_mbit = int(bytes_to_mbit(rx - old_rx) / t)
        rx_mbit = int(bytes_to_mbit(tx - old_tx) / t)

        print(tx_mbit)
        print(rx_mbit)

        s.write(str(tx_mbit))
        s.write("\n")
        s.write(str(rx_mbit))
        s.write("\n")

        old_rx, old_tx = rx, tx


if __name__ == "__main__":
    main()
