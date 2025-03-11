# example RSS feed https://ooh.directory/feeds/cats/n8ypp8/rss/ai.xml

'''
Requirements: 
class for parsing RSS pages, input: https://ooh.directory/feeds/cats/n8ypp8/rss/ai.xml
'''
import requests
import xml.etree.ElementTree as ET

class RSSManager:
    def __init__(self, address):
        self.address = address
        self.tree = None
        self.root = None

    def fetch_feed(self):
        """Fetches the RSS feed from the given URL and parses it into an XML tree."""
        try:
            response = requests.get(self.address, timeout=10)
            response.raise_for_status()
            self.tree = ET.ElementTree(ET.fromstring(response.content))
            self.root = self.tree.getroot()
            return True
        except requests.RequestException as e:
            print(f"Error fetching feed: {e}")
            return False
        except ET.ParseError as e:
            print(f"Error parsing XML: {e}")
            return False

    def is_valid(self):
        """Validates if the fetched XML is an RSS feed."""
        if self.root is None:
            return False
        return self.root.tag == "rss" or "rss" in self.root.tag.lower()

    def parse_feed(self):
        """Parses the RSS feed and extracts articles."""
        if not self.is_valid():
            print("Invalid RSS feed")
            return []

        items = []
        for item in self.root.findall(".//item"):
            title = item.find("title").text if item.find("title") is not None else "No Title"
            description = item.find("description").text if item.find("description") is not None else "No Description"
            link = item.find("link").text if item.find("link") is not None else "No Link"

            items.append({
                "title": title,
                "description": description,
                "link": link
            })
        return items

    def display_feed(self):
        """Displays the parsed RSS feed in a readable format."""
        articles = self.parse_feed()
        if not articles:
            print("No articles found.")
            return

        for idx, article in enumerate(articles, start=1):
            print(f"\nArticle {idx}:")
            print(f"Title: {article['title']}")
            print(f"Description: {article['description']}")
            print(f"Link: {article['link']}\n")

# Example Usage
if __name__ == "__main__":
    rss_url = "https://ooh.directory/feeds/cats/n8ypp8/rss/ai.xml"
    parser = RSSManager(rss_url)

    if parser.fetch_feed():
        parser.display_feed()
