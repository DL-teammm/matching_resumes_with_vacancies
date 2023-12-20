import requests
import time
import os


class HHDownloader:
    """
    Downloads HTML pages witch contain links to resumes
    Automatically switch the pages by changing the page number in the link
    """
    def __init__(self, start_url_template: str, data_path: str, timeout=10):
        self.start_url_template = start_url_template
        self.headers = {'User-Agent':
                            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        self.timeout = timeout
        self.data_path = data_path

    def check_if_exists(self, page_num: int):
        """Check if the page was already downloaded"""
        return os.path.exists(os.path.join(self.data_path, 'resume_page_{0}.html'.format(page_num)))

    def download_pages(self, start_page: int, end_page: int):
        """"Starts the process of downloading pages in the specified range"""
        for page_num in range(start_page, end_page + 1):
            if self.check_if_exists(page_num):
                print(f"File {'resume_page_{0}.html'.format(page_num)} already exists. Skip")
                continue
            print(f"Start downloading {page_num} page")
            page_url = self.get_page_url(page_num)
            print(f"Downloaded {page_num} page")
            page = self.download_page(page_url)
            self.save_page(page, page_num)
            print(f"Saved {page_num} page")
            print("*" * 20)
            time.sleep(self.timeout)

    def get_page_url(self, page_num: int):
        """Changes the page number in the link"""
        return self.start_url_template.format(page_num)

    def download_page(self, url: str):
        page = requests.get(url, headers=self.headers)
        return page

    def save_page(self, page, page_num: int):
        """Save the HTML page with page number in title to chosen directory"""
        page_file_name = os.path.join(self.data_path, 'resume_page_{0}.html'.format(page_num))
        with open(page_file_name, 'w+', encoding="utf-8") as resume_request:
            resume_request.write(page.text)


if __name__ == "__main__":
    start_url = "https://spb.hh.ru/search/resume?text=&no_magic=true&ored_clusters=true&order_by=relevance&items_on_page=100&search_period=365&logic=normal&pos=full_text&exp_period=all_time&exp_company_size=any&hhtmFrom=account_login"
    hh_downloader = HHDownloader(start_url, "Y:/OpenCV/HH/HH_parcer-master/data/", timeout=20)
    hh_downloader.download_pages(0, 1000)
