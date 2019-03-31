from bs4 import BeautifulSoup
import re
import json
import datetime
class HtmlParser:
    def __init__(self, response):
        self._response = response
        self._response.encoding = "utf-8"
        self._parser = BeautifulSoup(self._response.text, "lxml")



class ProductListParser(HtmlParser):
    def __init__(self, product_list_response):
        super().__init__(product_list_response)
        

    def get_product_list(self):
        """
        Return a dict of product_title_to_url,
        key: product title
        value: product url
        """
        product_title_to_url = {}
        product_a_tags = self._parser.select(".item-info h3 a")
        for product_a_tag in product_a_tags:
            product_title_to_url[product_a_tag.text] = product_a_tag.get("href")
        return product_title_to_url


class ProductPageParser(HtmlParser):
    def __init__(self, product_page_response):
        super().__init__(product_page_response)

    def get_images(self):
        """
        Return a list of image urls
        """
        image_tags = self._parser.select(".item-image-wrap img")
        image_links = [image_tag.get("src") for image_tag in image_tags]
        return image_links

    def get_shipping_fees(self):
        """
        Return a dict of shipment_dict
        key: shipment type
        value: shipment cost

        shipment type:
        'SEVEN_COD' -> pay & collect @ 7-11
        'CVS_COD' -> pay & collect @ FamilyMart, OK, Hi-Life
        'MAPLE' -> 便利帶
        'SEVEN  -> collect @ 7-11
        'POST' -> shipping via post office
        'HOUSE' -> delivery to home
        'ISLAND' -> outer island
        """
        scripts = self._parser.select("script")
        try:
            script_with_shipping_detail = [script.text for script in scripts if "RT.context" in script.text][0]
        except IndexError:
            error_message = "Shipping Info has been moved by the website developer, please review ProductPageParser:get_shipping_fees()"
            raise ValueError(error_message)
        else:
            shipment_info_regex = '(?<=shipment":)(.*)(?=,"payment)'
            regex_matches = re.search(shipment_info_regex, script_with_shipping_detail)
            search_result = regex_matches.group(0)
            shipment_list = json.loads(search_result)
            shipment_dict = {shipping_method['name']:shipping_method['cost'] for shipping_method in shipment_list}
            return shipment_dict
