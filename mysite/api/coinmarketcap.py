from bs4 import BeautifulSoup
from selenium import webdriver
from .models import Coin



class CoinMarketCap:
    def __init__(self, job, coin):
        self.job = job
        self.coin = coin
        self.base_url = f"https://coinmarketcap.com/currencies/{coin}/"

    def fetch_page(self):
        driver = webdriver.Chrome()
        driver.get(self.base_url)
        html = driver.page_source
        return html
    
    def extract_data(self, html):
        try:
            soup = BeautifulSoup(html, "html.parser")
            price = 0.0
            change = 0.0
            market_cap = 0.0
            cap_rank = 0
            volume = 0.0
            vol_rank = 0
            vol_change = 0.0
            circulating_supply = 0.0
            total_supply = 0.0
            diluted_market_cap = 0.0
            contracts = []
            official_links = []
            socials = []

            # Price
            price_str = soup.select_one(".fsQm").contents[0]
            price = float(price_str.replace("$", "").replace(",", ""))
            print(price)

            # Change
            change_element = (soup.select_one(".kzFEmO > div:nth-child(1) > p:nth-child(1)"))
            change_str = str(change_element.contents[1])
            change = float(change_str.split("%")[0])
            if change_element["color"] == "red":
                change = -change
            print(change)

            # Market Cap
            market_cap_str = str(soup.select_one("dl.sc-d1ede7e3-0 > div:nth-child(1) > div:nth-child(1) > dd:nth-child(2)").contents[1])
            market_cap_str = market_cap_str.replace("$", "").replace(",", "")
            market_cap = self.convert_suffix_to_number(market_cap_str)
            print(market_cap)

            # Cap Rank
            cap_rank_str = str(soup.select_one("dl.sc-d1ede7e3-0 > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > span:nth-child(2)").contents[0])
            cap_rank = int(cap_rank_str.replace("#", ""))
            print(f"Cap Rank: {cap_rank}")

            # Volume
            volume_str = str(soup.select_one("dl.sc-d1ede7e3-0 > div:nth-child(2) > div:nth-child(1) > dd:nth-child(2)").contents[1])
            volume_str = volume_str.replace("$", "").replace(",", "")
            volume = self.convert_suffix_to_number(volume_str)
            print(f"Volume: {volume}")

            # Volume Rank
            vol_rank_str = str(soup.select_one("dl.sc-d1ede7e3-0 > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > span:nth-child(2)").contents[0])
            vol_rank = int(vol_rank_str.replace("#", ""))
            print(f"Vol Rank: {vol_rank}")

            # Vol Change
            vol_change_str = str(soup.select_one("dl.sc-d1ede7e3-0 > div:nth-child(3) > div:nth-child(1) > dd:nth-child(2)").contents[0])
            vol_change = float(vol_change_str.replace("%", ""))
            print(f"Vol Change: {vol_change}")

            # Circulating Supply
            circulating_supply_element = soup.select_one("dl.sc-d1ede7e3-0 > div:nth-child(4) > div:nth-child(1) > dd:nth-child(2)").contents[0]
            circulating_supply_str = str(circulating_supply_element).split(" ")[0]
            circulating_supply_str = (circulating_supply_str.replace("," , ""))
            circulating_supply = self.convert_suffix_to_number(circulating_supply_str)
            print(f"Circulating Supply: {circulating_supply}")

            # Total Supply
            total_supply_element = soup.select_one("dl.sc-d1ede7e3-0 > div:nth-child(5) > div:nth-child(1) > dd:nth-child(2)").contents[0]
            total_supply_str = str(total_supply_element).split(" ")[0]
            total_supply_str = (total_supply_str.replace("," , ""))
            total_supply = self.convert_suffix_to_number(total_supply_str)
            print(f"Total Supply: {total_supply}")

            # Diluted Market Cap
            diluted_market_cap_str = str(soup.select_one("div.bwRagp:nth-child(7) > div:nth-child(1) > dd:nth-child(2)").contents[0])
            diluted_market_cap_str = diluted_market_cap_str.replace("$", "").replace(",", "")
            diluted_market_cap = self.convert_suffix_to_number(diluted_market_cap_str)
            print(f"Diluted MC: {diluted_market_cap}")


            # Contracts
            contracts = []
            try:
                contract_element = soup.select_one(".chain-name")
                contract_url = contract_element["href"]
                
            except Exception as e:
                pass
            else:
                parts = contract_url.split("/")
                domain_name = parts[2].split(".")[0]
                address = parts[4]
                data = {
                    "name": domain_name,
                    "address": address
                }
                contracts.append(data)

            print(contracts)

            # Official and Social Links
            try:
                official_links = []
                socials = []
                links_elements = soup.select("div.jTYLCR > div:nth-child(2) > div:nth-child(1) > div > a:nth-child(1)")
                for links in links_elements:

                    link = {
                        "name" : str(links.contents[1]),
                        "url" : str(links["href"])
                    }
                    if link.get("name").lower() == "website":
                        official_links.append(link)
                    else:
                        socials.append(link)

                print(f"official Links: {official_links}")
                print(f"Social Links: {socials}")
            except Exception:
                pass

        except (IndexError, ValueError, AttributeError) as e:
            print(f"Error parsing data for {self.coin}: {e}")


        return self.create_coin(price=price,
                                    change=change,
                                    market_cap=market_cap,
                                    cap_rank=cap_rank,
                                    volume=volume,
                                    vol_rank=vol_rank,
                                    vol_change=vol_change,
                                    circulating_supply=circulating_supply,
                                    total_supply=total_supply,
                                    diluted_market_cap=diluted_market_cap,
                                    contracts=contracts,
                                    official_links=official_links,
                                    socials=socials)
        

    def convert_suffix_to_number(self, value):
        multipliers = {'K': 1e3, 'M': 1e6, 'B': 1e9, 'T': 1e12}
        if value[-1] in multipliers:
            return float(value[:-1]) * multipliers[value[-1]]
        else:
            return float(value)

    def create_coin(self, price, change, market_cap, cap_rank, volume, vol_rank, vol_change, circulating_supply, total_supply, diluted_market_cap, contracts,official_links, socials):
        return Coin(
            name = self.coin,
            job = self.job,
            price = price,
            price_change = change,
            market_cap = market_cap,
            market_cap_rank = cap_rank,
            volume = volume,
            volume_rank = vol_rank,
            volume_change = vol_change,
            circulating_supply = circulating_supply,
            total_supply = total_supply,
            diluted_market_cap = diluted_market_cap,
            contracts = contracts,
            official_links = official_links,
            socials = socials
        )

    def scrape_data(self):
        html = self.fetch_page()
        coin = self.extract_data(html)
        return coin


