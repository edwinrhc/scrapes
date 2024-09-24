import subprocess

# Scrape the data
print("Scraping the data...")
subprocess.run(["python", "scrape_data.py"])

# Process the data
print("Processing the data...")
subprocess.run(["python", "process_data.py"])
