
class CardProcessor:
	"""The card object should be a Beautiful Soup object."""
	def __init__(self, card):
		self.card = card

	def get_title_element(self):
		if not hasattr(self, "title_element"):
			title_h3 = self.card.find("h3", class_="card__menu-content--title")
			if title_h3:
				self.title_element = title_h3.find("a")
			else:
				self.title_element = None
		return self.title_element

	def get_name(self):
		elem = self.get_title_element()
		if elem and elem.string:
			return elem.string.strip()
		return "Unknown Restaurant"

	def get_restaurant_uri(self):
		elem = self.get_title_element()
		if elem and "href" in elem.attrs:
			return elem["href"]
		return ""

	def get_lat(self):
		if "data-lat" in self.card.attrs:
			return self.card["data-lat"]
		return "0"

	def get_lng(self):
		if "data-lng" in self.card.attrs:
			return self.card["data-lng"]
		return "0"

	def get_location(self):
		location_elem = self.card.find("div", class_="card__menu-footer--location")
		if location_elem and location_elem.string:
			return location_elem.string.strip()
		# Fallback: try to get from first card__menu-footer--score
		score_elems = self.card.find_all("div", class_="card__menu-footer--score")
		if score_elems and score_elems[0].string:
			return score_elems[0].string.strip()
		return "Unknown"

	def get_price_element(self):
		if not hasattr(self, "price_element"):
			# First try the old structure
			self.price_element = self.card.find("div", class_="card__menu-footer--price")
			# If not found, try the new structure (second card__menu-footer--score)
			if not self.price_element:
				score_elements = self.card.find_all("div", class_="card__menu-footer--score")
				# The second score element typically contains price and type
				if len(score_elements) >= 2:
					self.price_element = score_elements[1]
				else:
					self.price_element = None
		return self.price_element

	def get_price(self):
		element = self.get_price_element()
		if not element:
			return "N/A"

		# Get text and clean it up
		text = element.get_text(strip=True)
		if not text:
			return "N/A"

		# Split by the middle dot (·) or whitespace
		parts = text.replace('·', ' ').split()
		if parts:
			# First part should be the price (e.g., $, $$, $$$)
			price = parts[0].strip()
			if '$' in price:
				return price
		return "N/A"

	def get_type(self):
		element = self.get_price_element()
		if not element:
			return "Unknown"

		# Get text and clean it up
		text = element.get_text(strip=True)
		if not text:
			return "Unknown"

		# Split by the middle dot (·)
		if '·' in text:
			parts = text.split('·')
			if len(parts) >= 2:
				# Everything after the dot is the cuisine type
				return parts[1].strip()
		else:
			# Fallback to old logic - last word
			parts = text.split()
			if len(parts) > 1:
				return parts[-1].strip()
		return "Unknown"

	def get_rating(self):
		rating_images = self.card.find_all("img", class_="michelin-award", src=self.is_bib_or_star)
		count = len(rating_images)
		if count == 0:
			return "Unrated"
		elif count == 1 and "bib-gourmand" in rating_images[0]["src"]:
			return "Bib Gourmand"
		else:
			return f"{count} star"

	def is_bib_or_star(self, src):
		value = "bib-gourmand" in src or "1star" in src
		return value

	def get_google_link(self):
		name = self.get_name()
		location = self.get_location()
		if name and name != "Unknown Restaurant" and location and location != "Unknown":
			query = f"{name}+{location}".replace(" ", "+")
			return f"https://www.google.com/search?q={query}"
		return ""