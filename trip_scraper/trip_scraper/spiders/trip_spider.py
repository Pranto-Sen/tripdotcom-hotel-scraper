import scrapy
from trip_scraper.items import HotelItem
import re
import json
import random
import os
from urllib.parse import urlparse
import requests

class TripSpider(scrapy.Spider):
    name = 'trip_spider'
    start_urls = ['https://uk.trip.com/hotels/?locale=en-GB&curr=GBP']

    def __init__(self, *args, **kwargs):
        super(TripSpider, self).__init__(*args, **kwargs)
        self.image_folder = 'hotel_images'
        if not os.path.exists(self.image_folder):
            os.makedirs(self.image_folder)

    def download_image(self, image_url, hotel_name):
        try:
            response = requests.get(image_url, stream=True)
            if response.status_code == 200:
                file_extension = os.path.splitext(urlparse(image_url).path)[1]
                safe_hotel_name = "".join([c for c in hotel_name if c.isalpha() or c.isdigit() or c==' ']).rstrip()
                filename = f"{safe_hotel_name}{file_extension}"
                filepath = os.path.join(self.image_folder, filename)
                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
                return filepath
        except Exception as e:
            self.logger.error(f"Failed to download image: {e}")
        return None

    def parse(self, response):
        script_content = response.xpath('//script[contains(text(), "window.IBU_HOTEL")]/text()').get()
        if script_content:
            json_data_match = re.search(r'window\.IBU_HOTEL\s*=\s*({.*?});', script_content, re.DOTALL)
            if json_data_match:
                json_data_str = json_data_match.group(1)
                try:
                    json_data = json.loads(json_data_str)
                    htlsData = json_data.get('initData', {}).get('htlsData', {})
                    
                    inbound_cities = htlsData.get('inboundCities', [])
                    outbound_cities = htlsData.get('outboundCities', [])
                    
                    all_cities = inbound_cities + outbound_cities
                    
                    valid_cities = [city for city in all_cities if city.get('recommendHotels')]
                    
                    selected_cities = random.sample(valid_cities, min(3, len(valid_cities)))
                    
                    for city in selected_cities:
                        city_info = {
                            'city_name': city.get('name')
                        }
                        
                        hotels = city.get('recommendHotels', [])
                        
                        for hotel in hotels:
                            district_name = hotel.get('districtName') or hotel.get('fullAddress', '')
                            hotel_name = hotel.get('hotelName')
                            image_url = 'https://ak-d.tripcdn.com/images' + hotel.get('imgUrl', '')
                            local_image_path = self.download_image(image_url, hotel_name)
                            
                            item = HotelItem(
                                Title = hotel_name,
                                Rating = hotel.get('rating'),
                                Country = city_info['city_name'],
                                Location = district_name,
                                latitude = hotel.get('lat'),
                                longitude = hotel.get('lon'),
                                Price = hotel.get('prices', {}).get('priceInfos', [{}])[0].get('price'),
                                Hotel_img = local_image_path
                            )
                            
                            yield item

                except json.JSONDecodeError as e:
                    self.logger.error(f"Failed to decode JSON: {e}")