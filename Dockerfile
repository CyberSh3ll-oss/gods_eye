FROM kalilinux/kali-rolling

# Prevent interactive prompts during installation
ENV DEBIAN_FRONTEND=noninteractive

# Update and install requested tools
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    git \
    curl \
    sudo \
    # Bluetooth \
    spooftooph \
    # Host/OSINT \
    spiderfoot \
    amass \
    dmitry \
    legion \
    nmap \
    theharvester \
    unicornscan \
    zenmap-kbx \
    # Network DNS \
    dnsenum \
    dnsmap \
    dnsrecon \
    # Web Scanning \
    dirb \
    dirbuster \
    ffuf \
    gobuster \
    recon-ng \
    wfuzz \
    # Web Vuln Scanning \
    burpsuite \
    davtest \
    skipfish \
    wapiti \
    whatweb \
    wpscan \
    # Wireless \
    aircrack-ng \
    reaver \
    wifite \
    && rm -rf /var/lib/apt/lists/*

# Set up working directory
WORKDIR /opt/gods_eye

# Clone ZPhisher into the tools directory
RUN git clone https://github.com/htr-tech/zphisher.git /opt/zphisher

# Copy project files
COPY requirements.txt .
COPY gods_eye.py .

# Install Python requirements
RUN pip3 install --no-cache-dir -r requirements.txt --break-system-packages

# Set the wrapper script as the entry point
ENTRYPOINT ["python3", "gods_eye.py"]
