
# PySysKit 🛠️

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)]()
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**PySysKit** is a powerful, modular, and lightweight Python toolkit designed for system administration, performance monitoring, process management, security auditing, and log analysis. It brings together low-level system utilities into a clean, intuitive Python API as well as a Command Line Interface (CLI).

---

## 📌 Table of Contents

- [Features](#-features)
- [Project Architecture](#-project-architecture)
- [Installation](#-installation)
- [Quick Start & API Usage](#-quick-start--api-usage)
  - [System Information & Monitoring](#1-system-information--monitoring)
  - [Process Management](#2-process-management)
  - [Network Utilities](#3-network-utilities)
  - [Filesystem Operations](#4-filesystem-operations)
  - [Security Auditing](#5-security-auditing)
  - [Log Analysis](#6-log-analysis)
- [Command Line Interface (CLI)](#-command-line-interface-cli)
- [Running Tests](#-running-tests)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

- 💻 **System Monitoring**: Retrieve detailed metrics on CPU, RAM, Disk usage, and system runtime info.
- ⚙️ **Process Management**: Inspect running processes, monitor resource consumption, and manage process states.
- 🌐 **Network Diagnostics**: Interface inspection, socket connectivity checks, IP lookup, and port scanning.
- 📁 **Filesystem Operations**: Fast directory scanning, file hash verification, integrity tracking, and disk metrics.
- 🛡️ **Security Auditing**: Auditing file permissions, checking suspicious activity, and security posture inspection.
- 📜 **Log Management**: Parse, filter, and extract insights from system and application log files.
- 🖥️ **Built-in CLI**: Access key toolkit features directly from your terminal.

---

## 📁 Project Architecture

```text
PySysKit/
├── src/
│   └── pysyskit/
│       ├── __init__.py         # Package initialization
│       ├── cli.py              # Command Line Interface (CLI) entrypoint
│       ├── exceptions.py       # Custom exception handlers
│       ├── core/               # Core engine & logging infrastructure
│       │   ├── __init__.py
│       │   └── logger.py
│       └── modules/            # Functional system modules
│           ├── __init__.py
│           ├── system.py       # Hardware and OS metrics
│           ├── process.py      # Process lifecycle management
│           ├── network.py      # Network diagnostics & scanning
│           ├── filesystem.py   # File integrity & disk utilities
│           ├── security.py     # Security audit & hashing
│           └── logs.py         # Log parser and analyzer
├── tests/                      # Automated unit test suite
│   ├── test_logs.py
│   └── test_security.py
├── pyproject.toml              # Build & project configuration
├── requirements.txt            # Package dependencies
├── .gitignore
└── README.md
```

---

## 🚀 Installation

### Option 1: Install from Source (Recommended for Development)

```bash
# Clone the repository
git clone https://github.com/Mostafaabdow2/PySysKit.git
cd PySysKit

# Create a virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies and package in editable mode
pip install -e .
```

### Option 2: Install via Requirements

```bash
pip install -r requirements.txt
```

---

## 💡 Quick Start & API Usage

### 1. System Information & Monitoring
Get instant insights into host hardware and operating system status:

```python
from pysyskit.modules.system import SystemInfo

sys_info = SystemInfo()

# Fetch general system information
print("OS:", sys_info.get_os_info())
print("CPU Usage:", sys_info.get_cpu_usage())
print("Memory Usage:", sys_info.get_memory_usage())
```

### 2. Process Management
Inspect and filter running processes across your system:

```python
from pysyskit.modules.process import ProcessManager

proc_mgr = ProcessManager()

# List active processes
processes = proc_mgr.list_processes()
for proc in processes[:5]:
    print(f"PID: {proc['pid']} | Name: {proc['name']} | CPU: {proc['cpu_percent']}%")
```

### 3. Network Utilities
Check port statuses, network interfaces, and connectivity:

```python
from pysyskit.modules.network import NetworkUtils

net = NetworkUtils()

# Check open ports on localhost
open_ports = net.scan_ports("127.0.0.1", ports=[22, 80, 443, 8080])
print("Open Ports:", open_ports)
```

### 4. Filesystem Operations
Monitor disk usage and inspect file properties:

```python
from pysyskit.modules.filesystem import FileSystemManager

fs = FileSystemManager()

# Check disk usage
usage = fs.get_disk_usage("/")
print(f"Disk Total: {usage['total']} GB | Free: {usage['free']} GB")
```

### 5. Security Auditing
Compute file cryptographic hashes and inspect security parameters:

```python
from pysyskit.modules.security import SecurityAuditor

auditor = SecurityAuditor()

# Calculate file hash for integrity check
file_hash = auditor.compute_hash("pyproject.toml", algorithm="sha256")
print(f"SHA256 Hash: {file_hash}")
```

### 6. Log Analysis
Parse and search log files for specific keywords or error levels:

```python
from pysyskit.modules.logs import LogAnalyzer

analyzer = LogAnalyzer()

# Scan log file for errors
errors = analyzer.search_logs(log_file_path="app.log", level="ERROR")
print("Found errors:", errors)
```

---

## 🖥️ Command Line Interface (CLI)

`PySysKit` comes with a CLI tool to execute operations directly from the terminal.

```bash
# Display CLI help menu
pysyskit --help

# Get current system status overview
pysyskit system status

# List top running processes
pysyskit process list

# Audit file security hash
pysyskit security hash --file pyproject.toml
```

---

## 🧪 Running Tests

PySysKit uses `pytest` for automated unit testing. To run the test suite:

```bash
# Run all tests
pytest

# Run tests with detailed verbosity
pytest -vv

# Run coverage report
pytest --cov=src/pysyskit
```

---

## 🤝 Contributing

Contributions are welcome! Follow these steps to contribute:

1. **Fork** the repository.
2. Create a new branch: `git checkout -b feature/your-feature-name`.
3. Make your changes and commit them: `git commit -m 'Add new feature'`.
4. Push to your branch: `git push origin feature/your-feature-name`.
5. Open a **Pull Request**.

Please ensure all tests pass and your code complies with PEP 8 standards.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

👨‍💻 Created & Maintained by **[Mostafa Abdow](https://github.com/Mostafaabdow2)**
