import requests
import time
from countries.country_provider import Country
from web_crawler.cache import Cache
from web_crawler.restaurant import Restaurant
from web_crawler.processors import MichelinPageProcessor, RestaurantProcessor


MICHELIN_BASE_URL = "https://guide.michelin.com"

class MichelinCrawler:

	def __init__(self, country: Country):
		self.country = country
		self.url = f"{MICHELIN_BASE_URL}/en/{country.shortcode}/restaurants"
		self.cache = Cache(country)
		self.page_processors = []


	def fetch_pages(self):
		page_number = 1
		url = self.url
		while True:
			page_file_name = f"page_{page_number}.html"
			page = self.cache.get_or_load(
				page_file_name, 
				lambda: self.make_request_and_get_content(url))
			page_processor = MichelinPageProcessor(page)
			self.page_processors.append(page_processor)

			uri = page_processor.get_next_page_uri()
			if uri is not None:
				url = f"{MICHELIN_BASE_URL}{uri}"
				page_number = page_number + 1
			else:
				break

	def fetch_cards(self):
		cards = []
		for page_processor in self.page_processors:
			cards.extend(page_processor.get_card_processors())
		self.card_processors = cards

	def get_restaurant_objects(self):
		restaurants = []
		skipped_count = 0
		for card_processor in self.card_processors:
			uri = card_processor.get_restaurant_uri()

			# Skip restaurants that don't belong to the target country
			# Check if the URI contains the country shortcode or expected region
			if not uri:
				continue

			# Filter out restaurants from other regions
			# Special handling for different countries
			if self.country.shortcode == "sg":
				# Singapore URLs should contain "singapore-region"
				if "singapore-region" not in uri and f"/{self.country.shortcode}/" not in uri:
					print(f"Skipping non-Singapore restaurant: {uri}")
					skipped_count += 1
					continue
			elif self.country.shortcode == "tw":
				# Taiwan has multiple regions: taipei-region, taichung-region, kaohsiung-region, tainan-region, northern-taiwan
				taiwan_regions = ["taipei-region", "taichung-region", "kaohsiung-region", "tainan-region", "northern-taiwan"]
				# Skip British Columbia restaurants that appear in Taiwan results
				if "british-columbia" in uri:
					print(f"Skipping non-Taiwan restaurant: {uri}")
					skipped_count += 1
					continue
				# Accept any Taiwan region
				if not any(region in uri for region in taiwan_regions):
					print(f"Skipping restaurant from different region: {uri}")
					skipped_count += 1
					continue
			elif f"/{self.country.shortcode}/" not in uri:
				# For other countries, check if the shortcode is in the URI
				print(f"Skipping restaurant from different region: {uri}")
				skipped_count += 1
				continue

			url = f"{MICHELIN_BASE_URL}{uri}"
			file_name = f"restaurants/{uri.split('/')[-1]}.html"
			restaurant_page = self.cache.get_or_load(
				file_name,
				lambda: self.make_request_and_get_content(url))
			restaurant_processor = RestaurantProcessor(restaurant_page)
			restaurants.append(Restaurant(card_processor, restaurant_processor))

		if skipped_count > 0:
			print(f"Skipped {skipped_count} restaurants from other regions")

		self.restaurants = restaurants
		return restaurants

	def make_request_and_get_content(self, url):
		# Too lazy to use a real rate limiter, but this will at least help with getting throttled.
		# If the data is cached, this wont matter anyway.
		print(f"Sleeping for 1 seconds to avoid throttling. Then fetching {url}")
		time.sleep(1)
		return requests.get(url).content
		