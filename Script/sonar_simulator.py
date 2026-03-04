import argparse
import datetime
import time

import serial


def generate_nmea_dpt(depth):
    return checksum(f"SDDPT,{depth:.1f},0.1,100")


def generate_nmea_dbt(depth):
    feet = depth * 3.28084
    fathoms = depth * 0.546806649
    return checksum(f"SDDBT,{feet:.1f},f,{depth:.1f},M,{fathoms:.1f},F")


def generate_nmea_sentence(depth, sentence_type):
    normalized_type = sentence_type.lower()
    if normalized_type == "dpt":
        return generate_nmea_dpt(depth)
    if normalized_type == "dbt":
        return generate_nmea_dbt(depth)
    raise ValueError(f"Unsupported sentence type: {sentence_type}")


def checksum(sentence):
    checksum_value = 0
    for char in sentence:
        checksum_value ^= ord(char)
    return f"${sentence}*{checksum_value:02X}"


def depth_from_now(now=None):
    if now is None:
        now = datetime.datetime.now()
    return 10 + now.second


def main(
    serial_port,
    baud_rate,
    sentence_type="dpt",
    iterations=None,
    interval=1.0,
    now_provider=None,
    sleep_func=time.sleep,
):
    if now_provider is None:
        now_provider = datetime.datetime.now

    ser = None
    try:
        ser = serial.Serial(serial_port, baud_rate, timeout=1)
        print(f"Connected to serial port {serial_port} at {baud_rate} baud.")

        sent_count = 0
        while iterations is None or sent_count < iterations:
            depth = depth_from_now(now_provider())
            nmea_sentence = generate_nmea_sentence(depth, sentence_type)
            ser.write((nmea_sentence + "\r\n").encode("ascii"))
            print(nmea_sentence)
            sent_count += 1

            if iterations is None or sent_count < iterations:
                sleep_func(interval)

    except KeyboardInterrupt:
        print("Script stopped by user.")
    except Exception as exc:
        print(f"An error occurred: {exc}")
    finally:
        if ser is not None and ser.is_open:
            ser.close()


def parse_args():
    parser = argparse.ArgumentParser(description="NMEA-0183 sonar simulator (DPT/DBT)")
    parser.add_argument("serial_port", help="Serial device path (example: /dev/ttyUSB0)")
    parser.add_argument("baud_rate", type=int, help="Serial baud rate (example: 9600)")
    parser.add_argument(
        "--sentence-type",
        choices=["dpt", "dbt"],
        default="dpt",
        help="NMEA sentence type to emit (default: dpt)",
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=1.0,
        help="Delay between sentences in seconds (default: 1.0)",
    )
    parser.add_argument(
        "--iterations",
        type=int,
        default=None,
        help="Number of sentences to send (default: infinite loop)",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    main(
        serial_port=args.serial_port,
        baud_rate=args.baud_rate,
        sentence_type=args.sentence_type,
        iterations=args.iterations,
        interval=args.interval,
    )
