import csv
import os
import time

import requests

API_URL = "https://www.virustotal.com/api/v3/ip_addresses/{}"
INPUT_FILE = "data/ip_list.txt"
OUTPUT_FILE = "results/ip_reputation.csv"


def classify_ip(malicious, suspicious):
    if malicious >= 3:
        return "Malicious"
    if malicious >= 1 or suspicious >= 1:
        return "Suspicious"
    return "Safe"


def check_ip(ip, api_key):
    headers = {"x-apikey": api_key}

    response = requests.get(
        API_URL.format(ip),
        headers=headers,
        timeout=30
    )

    response.raise_for_status()

    data = response.json().get("data", {})
    attributes = data.get("attributes", {})
    stats = attributes.get("last_analysis_stats", {})

    malicious = int(stats.get("malicious", 0))
    suspicious = int(stats.get("suspicious", 0))
    harmless = int(stats.get("harmless", 0))
    undetected = int(stats.get("undetected", 0))
    reputation = attributes.get("reputation", 0)

    return {
        "IP": ip,
        "Reputation": reputation,
        "Malicious": malicious,
        "Suspicious": suspicious,
        "Harmless": harmless,
        "Undetected": undetected,
        "Classification": classify_ip(malicious, suspicious)
    }


def main():
    api_key = os.getenv("VT_API_KEY")

    if not api_key:
        raise RuntimeError(
            "VT_API_KEY is not set. "
            "Export your VirusTotal API key before running the script."
        )

    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        ips = [line.strip() for line in file if line.strip()]

    results = []

    print("=" * 55)
    print("           MALICIOUS IP INTELLIGENCE SYSTEM")
    print("=" * 55)

    for index, ip in enumerate(ips, start=1):
        print(f"\nChecking {index}/{len(ips)}: {ip}")

        try:
            result = check_ip(ip, api_key)
            results.append(result)

            print(f"Reputation: {result['Reputation']}")
            print(f"Malicious: {result['Malicious']}")
            print(f"Suspicious: {result['Suspicious']}")
            print(f"Classification: {result['Classification']}")

        except requests.RequestException as error:
            print(f"Request failed for {ip}: {error}")

        if index < len(ips):
            print("Waiting before next request ...")
            time.sleep(20)

    fieldnames = [
        "IP",
        "Reputation",
        "Malicious",
        "Suspicious",
        "Harmless",
        "Undetected",
        "Classification"
    ]

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    with open(
        OUTPUT_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(results)

    print("\n" + "=" * 55)
    print("Scan completed successfully!")
    print(f"Results saved to: {OUTPUT_FILE}")
    print("=" * 55)


if __name__ == "__main__":
    main()
