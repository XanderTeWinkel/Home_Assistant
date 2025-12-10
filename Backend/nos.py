import requests
import xml.etree.ElementTree as ET

NOS_RSS_URL = "https://feeds.nos.nl/nosnieuwsalgemeen"

def fetch_nos_news():
    try:
        response = requests.get(NOS_RSS_URL)
        response.raise_for_status()
        root = ET.fromstring(response.content)
        news_items = []

        for item in root.findall(".//item"):
            title = item.find("title").text  # type: ignore
            link = item.find("link").text  # type: ignore
            pub_date = item.find("pubDate").text  # type: ignore
            
            # Attempt to get image
            image_url = None
            media_content = item.find("{http://search.yahoo.com/mrss/}content")
            if media_content is not None and 'url' in media_content.attrib:
                image_url = media_content.attrib['url']
            else:
                enclosure = item.find("enclosure")
                if enclosure is not None and 'url' in enclosure.attrib:
                    image_url = enclosure.attrib['url']

            news_items.append({
                "title": title,
                "link": link,
                "pub_date": pub_date,
                "image": image_url
            })
        
        return news_items

    except requests.RequestException as e:
        print(f"Error fetching NOS news: {e}")
        return []
