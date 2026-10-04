<div align="center">

# ransomware-adversary-emulation

**Ransomware Adversary Emulation for Authorized Security Research and Education**

![License](https://img.shields.io/github/license/01xJB/ransomware-adversary-emulation?color=blue&style=for-the-badge)
![Version](https://img.shields.io/badge/version-3.1.0-success?style=for-the-badge)
![Python](https://img.shields.io/badge/python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Status](https://img.shields.io/badge/status-active-brightgreen?style=for-the-badge)

</div>

---

## Overview

`ransomware-adversary-emulation` is an **educational security research tool designed to simulate ransomware-style activity within controlled and authorized environments**.

The project was created to provide hands-on experience with the techniques, network behavior, authentication mechanisms, file discovery, and attack paths that defenders may encounter during a ransomware incident.

Rather than treating ransomware solely as a theoretical threat, this project provides a way to study how ransomware-style activity can interact with an **Active Directory environment, Windows hosts, SMB infrastructure, and network shares**.

The project can be used for:

- Security research and experimentation
- Red team and adversary-emulation exercises
- Blue team detection engineering
- SIEM and EDR validation
- Incident-response training
- Active Directory security testing
- Network segmentation testing
- Ransomware preparedness assessments
- Cybersecurity education and lab environments

> ## Authorized Use Only
>
> This project is intended **exclusively for authorized security research, education, and controlled laboratory environments**.
>
> Do not deploy this project against systems, networks, accounts, files, or data that you do not own or have explicit authorization to test.
>
> The author assumes no responsibility for damage, data loss, unauthorized access, or other consequences resulting from misuse of this software.

---

## Educational Purpose

Ransomware incidents are not limited to encrypting files.

A realistic ransomware intrusion can involve multiple stages, including:

1. Initial access
2. Authentication
3. Network and host discovery
4. Active Directory enumeration
5. Credential usage
6. SMB and network-share discovery
7. Lateral movement
8. File discovery
9. Data encryption
10. Detection and incident response

This project focuses on helping security practitioners understand **what these activities can look like from both the attacker and defender perspectives**.

A controlled lab can be used to observe questions such as:

- What systems are discoverable from a compromised workstation?
- Which network shares are accessible to a compromised identity?
- What authentication mechanisms are being used?
- What activity would appear in Windows security logs?
- What network traffic would an EDR or NDR solution observe?
- Can network segmentation limit lateral movement?
- Can an organization detect unusual SMB activity?
- What happens when a highly privileged account is compromised?
- Which defensive controls prevent or limit ransomware-style behavior?

The goal is to turn these questions into **repeatable security experiments**.

---

## Adversary Emulation

The project is designed around the concept of **adversary emulation**.

Instead of attempting to reproduce a specific real-world ransomware family, the tool reproduces selected behaviors associated with ransomware operations in order to evaluate defensive controls.

This allows defenders to build controlled scenarios such as:

```text
Compromised Host
      |
      v
Authentication
      |
      v
Network Discovery
      |
      v
Host / SMB Discovery
      |
      v
Network Share Discovery
      |
      v
File Discovery
      |
      v
Controlled Encryption Simulation
      |
      v
Detection / Response
```

Each stage can be observed through security telemetry and used to evaluate defensive capabilities.

---

## Features

| | |
|---|---|
| 🎯 **Network Discovery** | Identifies interconnected network ranges and discovers accessible Windows hosts and network shares within the authorized environment. |
| 🔐 **Authentication** | Supports authenticated interaction with Windows environments using supplied domain credentials or the current Windows authentication context. |
| 🧭 **SMB Discovery** | Discovers accessible SMB resources and network shares that are visible to the authenticated identity. |
| 📂 **File Discovery** | Identifies files available through discovered systems and network shares for controlled testing. |
| 🔒 **Encryption Simulation** | Provides an optional encryption mode for controlled laboratory environments to reproduce the impact associated with ransomware-style file encryption. |
| 🔑 **Decryption** | Supports restoration of files using the generated/provided decryption key. |
| 🧪 **Lab Research** | Can be incorporated into isolated Active Directory environments for repeatable security experiments. |

---

## Defensive Research Use Cases

This project can be particularly useful when paired with defensive security tooling.

For example, a controlled Active Directory lab could contain:

```text
             Active Directory
                    |
             +------+------+
             |             |
          DC01           FILE01
             |             |
             +------+------+
                    |
              WORKSTATION01
```

A security team could then monitor the workstation while performing an authorized emulation and evaluate:

- Windows Event Logs
- Sysmon telemetry
- EDR detections
- SIEM alerts
- SMB activity
- Authentication events
- Network connections
- File-system activity
- Suspicious process behavior
- Lateral-movement indicators

This makes the project useful not only for offensive security training, but also for **detection engineering and incident-response validation**.

---

## Research and Learning Goals

The project can be used to gain practical experience with:

### Active Directory

- Domain authentication
- Windows security principals
- Kerberos authentication
- SMB
- Network shares
- Domain-host relationships
- Privilege boundaries

### Network Security

- Network discovery
- Subnet identification
- Host discovery
- SMB enumeration
- Network segmentation
- Lateral movement concepts

### Defensive Security

- Detection engineering
- SIEM telemetry
- EDR telemetry
- Windows logging
- Incident response
- Ransomware preparedness
- Security-control validation

### Adversary Emulation

- Modeling attacker behavior
- Reproducing attack stages
- Building repeatable security exercises
- Measuring defensive visibility
- Validating security controls

---

## Requirements

- Python 3.7+
- Windows/Active Directory laboratory environment for AD-related testing
- Dependencies in [`requirements.txt`](requirements.txt)

Dependencies include:

- `impacket`
- `psutil`
- `pycryptodome`
- `smbprotocol`

---

## Installation

```bash
git clone https://github.com/01xJB/ransomware-adversary-emulation.git
cd ransomware-adversary-emulation
pip install -r requirements.txt
```

---

## Usage

```text
usage: main.py [-h] [-d DOMAIN] [-u USERNAME] [-p PASSWORD] [-dc DECRYPTION_KEY] [-en] [-ptt]

SMB network share scanner.

options:
  -h, --help
                        show this help message and exit

  -d DOMAIN, --domain DOMAIN
                        Windows domain name.

  -u USERNAME, --username USERNAME
                        Username to authenticate with.

  -p PASSWORD, --password PASSWORD
                        Password to authenticate with.

  -dc DECRYPTION_KEY, --decryption-key DECRYPTION_KEY
                        Provide a decryption key to decrypt all files.

  -en, --encrypt
                        Encrypt all files discovered on systems and network shares.

  -ptt
                        Use the current Windows authentication context.
```

### Authentication

A username and password can be supplied when testing an authorized Active Directory environment.

Alternatively, `-ptt` can be used to operate using the current Windows authentication context.

Example:

```bash
python emulate.py -d UNDERWRLD -u baphomet -p password
```

Using the current Windows authentication context:

```bash
python emulate.py -ptt
```

### Encryption Simulation

Encryption functionality should only be used inside an **isolated, disposable laboratory environment containing test data**.

```bash
python emulate.py -ptt -en
```

The encryption functionality is intended to reproduce the **defensive impact and telemetry associated with ransomware-style encryption**, allowing security teams to evaluate their detection and response capabilities.

---

## Command-Line Options

| Flag | Description |
|---|---|
| `-h`, `--help` | Prints the help menu |
| `-u`, `--username` | Username used for authentication |
| `-p`, `--password` | Password used for authentication |
| `-d`, `--domain` | Windows domain name |
| `-dc`, `--decryption-key` | Provides a decryption key for restoring encrypted test files |
| `-en`, `--encrypt` | Enables controlled encryption testing |
| `-ptt`, `--ptt` | Uses the current Windows authentication context |

---

## Recommended Lab Environment

For safe experimentation, use an isolated environment containing disposable systems and test data.

A basic environment could consist of:

```text
                Isolated Lab Network
                        |
              +---------+---------+
              |                   |
           DC01                FILE01
      Active Directory       SMB Shares
              |
              |
         WORKSTATION01
              |
              |
      Adversary Emulation
```

Recommended defensive tooling includes:

- Windows Event Logging
- Sysmon
- Microsoft Defender
- EDR/XDR platforms
- SIEM platforms
- Network monitoring
- Centralized log collection

The lab should be isolated from production systems and contain **no sensitive or irreplaceable data**.

---

## Detection Engineering

One of the primary educational goals of this project is to help defenders understand the telemetry generated by ransomware-style behavior.

A security team can use the project to develop and validate detections for:

- Unusual authentication activity
- Abnormal SMB connections
- Large-scale file access
- Suspicious file modifications
- Rapid file encryption
- Unexpected access to network shares
- Lateral movement
- Abnormal activity from compromised accounts

The resulting telemetry can then be investigated through a SIEM or EDR platform to determine whether the organization's controls provide sufficient visibility.

---

## What This Project Is

This project is:

- An adversary-emulation exercise
- A cybersecurity research project
- An Active Directory security laboratory tool
- A defensive detection-testing utility
- An educational resource
- A controlled ransomware-behavior simulation

## What This Project Is Not

This project is **not intended to be deployed against production environments or systems without explicit authorization**.

It should not be used to:

- Destroy or disrupt systems
- Encrypt unauthorized data
- Access networks without permission
- Obtain unauthorized credentials
- Impact third-party systems
- Deploy against real organizations without authorization

---

## Disclaimer

This software is provided for **educational and authorized security-testing purposes only**.

Ransomware and related attack techniques can cause significant data loss and operational disruption when used outside of a controlled environment.

Always use disposable test systems, test accounts, and non-sensitive data when performing experiments involving encryption or destructive behavior.

You are responsible for ensuring that your use of this project complies with all applicable laws, regulations, contracts, and organizational policies.

---

## License

Released under the [Apache-2.0 License](LICENSE).

---

<div align="center">

Built by [**01xJB**](https://github.com/01xJB)

</div>
