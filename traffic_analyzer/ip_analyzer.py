import requests
import csv
import time

existing_locations = set()
def get_ip_locations():
        try:
            with open('external_ips.csv') as f:
                ips = [line.strip() for line in f if line.strip()]
            for ip in ips:
                try:
                    r = requests.get(f'http://ip-api.com/json/{ip}')
                    
                    if r.status_code == 200:
                        data = r.json()
                        query = data.get('query', 'Unknown')
                        country = data.get('country', 'Unknown')
                        city = data.get('city', 'Unknown')
                        isp = data.get('isp', 'Unknown')
                        location = (country, city)
                        if (location, isp) not in existing_locations:
                            with open('ip_geolocation.csv', 'a', newline='', encoding='utf-8') as csvfile:
                                writer = csv.writer(csvfile)
                                writer.writerow([query, location, isp])
                                existing_locations.add((location, isp))
                    if r.status_code != 200:
                        print(f"Failed to retrieve IP{ip}: Status code {r.status_code}")
                except Exception as e:
                    print(f"Error processing IP {ip}: {e}")
                    
        except Exception as e:
            print(f"Error in processing the IP list: {e}")



