import requests


# TODO: check proxy validation
# TODO: proxy replacement.
class Proxies:
    PROXIES = list()
    BASE_URL = "https://proxy.webshare.io/api/proxy/list/"
    API_KEY = "Token ea8b78668c8943edf40839b4941b85281ca8c043"

    class Proxy:
        def __init__(self, item):
            self.USERNAME = item['username']
            self.PASSWORD = item['password']
            self.IP_ADDRESS = item['proxy_address']
            self.HTTP_PORT = item['ports']['http']
            self.SOCKS_PORT = item['ports']['socks5']
            self.VALID = item['valid']
            self.COUNTRY = item['country_code']
            self.CITY = item['city_name']
            self.HTTP_URL = 'http://%s:%s@%s:%s' % (self.USERNAME, self.PASSWORD, self.IP_ADDRESS, self.HTTP_PORT)
            self.SOCKS_URL = 'socks5://%s:%s@%s:%s' % (self.USERNAME, self.PASSWORD, self.IP_ADDRESS, self.HTTP_PORT)

    @classmethod
    def set_proxies(cls):
        """
        set proxies from web-share api

        :return: fill the PROXIES list.
        """
        while True:
            try:
                response = requests.get(cls.BASE_URL, headers={"Authorization": cls.API_KEY})
                if response.status_code == 200:
                    for item in response.json()['results']:
                        proxy = Proxies.Proxy(item)
                        if proxy.COUNTRY != "US":
                            cls.PROXIES.append(proxy)
                    break
                else:
                    raise Exception("%s-%s" % (response.status_code, response.text))
            except Exception as ex:
                print("There is a problem in set_proxies method : %s" % ex)
                continue

    @classmethod
    def get_proxies(cls, start_count, end_count):
        """
        return the desired proxies from PROXIES list
        :param start_count: starting number of proxy in the PROXIES list
        :param end_count: finishing number of proxy in the PROXIES list
        :return: list of proxies
        """
        cls.set_proxies()
        if cls.PROXIES:
            return cls.PROXIES[start_count:end_count]
