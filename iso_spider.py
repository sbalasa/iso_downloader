import scrapy
import webbrowser


from pprint import pprint


class McAfeeSpider(scrapy.Spider):
    name = "contentsecurity"
    start_urls = ["https://contentsecurity.mcafee.com/"]

    def parse(self, response):
        return scrapy.http.FormRequest.from_response(
            response,
            formdata={"username": "Santee", "password": "passwrd"},
            callback=self.after_login,
        )

    def after_login(self, response):
        if b"Error while logging in" in response.body:
            self.logger.error("Login failed!")
        else:
            self.logger.info("Login succeeded!")
            iso_urls = []
            print("Downloading ISO files")
            for link in response.css("a[href*=iso]::attr(href)").getall():
                iso_urls.append(response.urljoin(link))
                webbrowser.open_new_tab(response.urljoin(link))
        pprint(iso_urls)
