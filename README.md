# 🛡️ Malicious IP Intelligence System

A Python-based cybersecurity project that analyzes IP address reputation using the VirusTotal API and classifies IPs as **Safe, Suspicious, or Malicious** using a project-defined classification rule.

## 🎯 Project Objective

The objective of this project is to automate basic IP reputation analysis using threat intelligence data and generate a structured report of the findings.

## 🔍 Features

- Reads IP addresses from a text file
- Queries VirusTotal for IP reputation
- Extracts malicious, suspicious, harmless, and undetected results
- Applies a project-defined classification rule
- Generates a CSV report of the analysis
- Uses an environment variable to protect the API key

## 🛠️ Technologies Used

- Python
- VirusTotal API
- Requests
- Kali Linux
- CSV

## 📁 Project Structure

```text
malicious-ip-intelligence-system/
├── README.md
├── code/
│   └── ip_intelligence.py
├── data/
│   └── ip_list.txt
├── results/
│   └── ip_reputation.csv
└── screenshots/
    ├── execution.png
    └── results.png
