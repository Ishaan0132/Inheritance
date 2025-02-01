# Suricata IDS Integration with Wazuh

This guide will walk you through the process of installing Suricata (a high-performance Network Intrusion Detection System) on your local Linux machine and integrating it with Wazuh for enhanced security monitoring. This setup will allow you to detect and analyze network threats efficiently.

---

## Prerequisites

- **A Linux machine** (Ubuntu/Debian recommended)
- **Root (sudo) access** to your system
- **Internet access** for downloading packages

---

## 📌 Table of Contents

1. [Installing Suricata on Linux](#1-installing-suricata-on-linux)
2. [Installing Wazuh](#2-installing-wazuh)
3. [Integrating Suricata with Wazuh](#3-integrating-suricata-with-wazuh)
4. [Verifying the Installation](#4-verifying-the-installation)
5. [Optional: Configuring the Chatbot](#5-optional-configuring-the-chatbot)
6. [Troubleshooting](#6-troubleshooting)

---

## 1️⃣ Installing Suricata on Linux

### 🛠 Step 1: Update System

Ensure your system is up-to-date:

```bash
sudo apt update && sudo apt upgrade -y
```

### 📦 Step 2: Install Dependencies

Install the required dependencies:

```bash
sudo apt install -y build-essential libpcap-dev libnet1-dev libyaml-dev \
    zlib1g-dev liblzma-dev libpcre3-dev libcap-ng-dev libmagic-dev
```

### 🔧 Step 3: Install Suricata

#### Method 1: Install via Package Manager

```bash
sudo apt install -y suricata
```

#### Method 2: Install from Source

```bash
cd /tmp
git clone https://github.com/OISF/suricata.git
cd suricata
./autogen.sh
./configure
make
sudo make install-full
```

### ✅ Step 4: Verify Installation

```bash
suricata --build-info
```

---

## 2️⃣ Installing Wazuh

### 🔑 Step 1: Add Wazuh Repository

```bash
curl -s https://packages.wazuh.com/key/GPG-KEY-WAZUH | sudo apt-key add -
sudo sh -c 'echo "deb https://packages.wazuh.com/4.x/apt stable main" > /etc/apt/sources.list.d/wazuh.list'
```

### 📥 Step 2: Install Wazuh Manager

```bash
sudo apt update
sudo apt install -y wazuh-manager
```

### 🖥 Step 3: Install Wazuh Agent

```bash
sudo apt install -y wazuh-agent
```

### 🚀 Step 4: Start Wazuh Services

```bash
sudo systemctl start wazuh-manager
sudo systemctl start wazuh-agent
sudo systemctl enable wazuh-manager
sudo systemctl enable wazuh-agent
```

---

## 3️⃣ Integrating Suricata with Wazuh

### 🔌 Step 1: Install Wazuh Suricata Module

```bash
sudo apt install wazuh-modulesd
```

### 📝 Step 2: Configure Wazuh to Receive Suricata Alerts

Edit Wazuh configuration:

```bash
sudo nano /var/ossec/etc/ossec.conf
```

Add:

```xml
<localfile>
  <log_format>json</log_format>
  <location>/var/log/suricata/eve.json</location>
</localfile>
```

### 🖊 Step 3: Configure Suricata to Output JSON

Edit Suricata configuration:

```bash
sudo nano /etc/suricata/suricata.yaml
```

Ensure the `outputs` section includes:

```yaml
outputs:
  - eve-log:
      enabled: yes
      filetype: syslog
      filename: /var/log/suricata/eve.json
```

### 🔄 Step 4: Restart Services

```bash
sudo systemctl restart suricata
sudo systemctl restart wazuh-manager
sudo systemctl restart wazuh-agent
```

---

## 4️⃣ Verifying the Installation

### ⚡ Step 1: Generate Test Alerts

Run a network scan:

```bash
nmap -p 80,443 <your-local-ip>
```

Check Suricata logs:

```bash
tail -f /var/log/suricata/eve.json
```

### 🔎 Step 2: Check Wazuh Alerts

Check Wazuh dashboard or log monitoring interface.

---

## 5️⃣ Optional: Configuring the Chatbot

We have developed a chatbot using **Botpress**, which will be integrated into our website in the future. This chatbot will assist in monitoring Wazuh logs and Suricata alerts, providing real-time security insights.

### 🔗 Chatbot Integration Features:

- Retrieves security alerts from Wazuh logs and Suricata events.
- Provides automated responses for threat analysis and mitigation.
- Can be embedded into a website dashboard for easy access.

### 🚀 Steps to Integrate:

1. **Connect to Wazuh Logs**: Configure the chatbot to read from `/var/ossec/logs/ossec.log` and `/var/log/suricata/eve.json`.
2. **Process Security Events**: Use Botpress workflows to analyze alerts and provide recommendations.
3. **Deploy on Website**: Embed the chatbot widget for real-time interaction with security data.

### 💡 Example Queries:

- **"Show me the latest Suricata alerts."**
- **"What threats were detected in the last 24 hours?"**
- **"How do I resolve this Wazuh alert?"**

This chatbot will enhance security monitoring by providing instant, AI-driven responses to security-related queries.

---

## 6️⃣ Troubleshooting

🔹 **Suricata Logs Not Generated?** Ensure Suricata is running and `suricata.yaml` is correctly configured.
<br>

🔹 **Wazuh Not Receiving Alerts?** Verify log file path in `ossec.conf`.
<br>

🔹 **Network Configuration Issues?** Ensure Suricata is capturing relevant network traffic.

### 📂 Log Files

- **Suricata logs:** `/var/log/suricata/suricata.log`
- **Wazuh logs:** `/var/ossec/logs/ossec.log`

---

💡 **Need Help?** Refer to official documentation or community forums for support.

📢 **This guide covers the installation and initial configuration of Suricata IDS with Wazuh for security monitoring. Further tuning and rule management may be required for optimal performance.**
