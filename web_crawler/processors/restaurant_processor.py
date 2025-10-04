from bs4 import BeautifulSoup
import json
import re

class RestaurantProcessor:
	def __init__(self, html_content):
		self.soup = BeautifulSoup(html_content, "html.parser")
		self.json_ld_data = self._extract_json_ld()

	def get_restaurant_website(self):
		element = self.soup.find("a", attrs={"data-event": "CTA_website"})
		if element is not None:
			return element["href"]
		return None

	def get_restaurant_review(self):
		try:
			description_div = self.soup.find("div", class_="restaurant-details__description--text")
			if description_div:
				p_element = description_div.find("p")
				if p_element:
					# Get text content even if it's not a simple string
					return p_element.get_text(strip=True)
			return None
		except Exception as e:
			print(f"Failed to fetch review: {e}")
			return None

	def _extract_json_ld(self):
		"""Extract JSON-LD structured data from the page"""
		try:
			script_tag = self.soup.find("script", type="application/ld+json")
			if script_tag and script_tag.string:
				return json.loads(script_tag.string)
		except (json.JSONDecodeError, AttributeError) as e:
			print(f"Failed to extract JSON-LD data: {e}")
		return {}

	def get_full_address(self):
		"""Get the complete street address"""
		if self.json_ld_data and "address" in self.json_ld_data:
			address = self.json_ld_data["address"]
			if isinstance(address, dict):
				return address.get("streetAddress", "N/A")
		return "N/A"

	def get_postal_code(self):
		"""Get the postal/ZIP code"""
		if self.json_ld_data and "address" in self.json_ld_data:
			address = self.json_ld_data["address"]
			if isinstance(address, dict):
				return address.get("postalCode", "N/A")
		return "N/A"

	def get_city_locality(self):
		"""Get the city or locality name"""
		if self.json_ld_data and "address" in self.json_ld_data:
			address = self.json_ld_data["address"]
			if isinstance(address, dict):
				return address.get("addressLocality", "N/A")
		return "N/A"
