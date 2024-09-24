# Set a base image for python
FROM python:3.12.2-slim

# Set the working directory
WORKDIR /app

# Install CyberGhost - OpenVPN
# RUN apt-get update && apt-get install -y openvpn unzip wget

# Install Chrome
RUN apt-get update && apt-get install -y wget gnupg2 \
  && apt-get install -y unzip \
  && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
  && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' \
  && apt-get update \
  && apt-get install -y google-chrome-stable

# Install ChromeDriver
RUN wget -q "https://chromedriver.storage.googleapis.com/2.41/chromedriver_linux64.zip" \
  && unzip chromedriver_linux64.zip -d /usr/local/bin/ \
  && rm chromedriver_linux64.zip

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code
COPY . /app/

# Run the command
CMD ["python", "main.py"]
