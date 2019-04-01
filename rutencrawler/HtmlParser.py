from bs4 import BeautifulSoup
import re
import json
import datetime
class HtmlParser:
    def __init__(self, response):
        self._response = response
        self._response.encoding = "utf-8"
        self._parser = BeautifulSoup(self._response.text, "html.parser")
    def get_javascript_context(self, regex):
        scripts = self._parser.select("script")
        try:
            script_with_shipping_detail = [script.text for script in scripts if "RT.context" in script.text][0]
        except IndexError:
            error_message = "RT.context cannot be found in the html, data might have been moved by the website developer."
            raise ValueError(error_message)
        else:

            regex_matches = re.search(regex, script_with_shipping_detail)
            search_result = regex_matches.group(0)
            return search_result



class ProductListParser(HtmlParser):
    def __init__(self, product_list_response):
        super().__init__(product_list_response)

    def get_max_page(self):
        return self._get_number_of_products() / self._get_number_per_page() +1
    def _get_number_of_products(self):
        regex = '(?<="page":{"total":)(.*)(?=,"perPage)'
        max_page = self.get_javascript_context(regex)
        return int(max_page)
    def _get_number_per_page(self):
        regex = '(?<="perPage":)(.*)(?=,"current")'
        number_per_page = self.get_javascript_context(regex)
        return int(number_per_page)


    def get_product_list(self):
        """
        Return a list of product_url
        """
        product_urls = []
        product_a_tags = self._parser.select(".item-info h3 a")
        for product_a_tag in product_a_tags:
            product_urls.append(product_a_tag.get("href"))
        return product_urls


class ProductPageParser(HtmlParser):
    def __init__(self, product_page_response):
        super().__init__(product_page_response)

    def get_product(self):
        product = {
                    "title":self._get_title(),
                    "images":self._get_images(),
                    "shipping_fees":self._get_shipping_fees()
                    }
        return product
    def _get_title(self):
        return self._parser.select_one("meta[itemprop='description']").get("content")
    def _get_images(self):
        """
        Return a list of image urls
        """
        image_tags = self._parser.select(".item-image-wrap img")
        image_links = [image_tag.get("src") for image_tag in image_tags]
        return image_links

    def _get_shipping_fees(self):
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
            search_result = self.get_javascript_context(shipment_info_regex)
            shipment_list = json.loads(search_result)
            shipment_dict = {shipping_method['name']:shipping_method['cost'] for shipping_method in shipment_list}
            return shipment_dict
