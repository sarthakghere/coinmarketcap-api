from .models import Coin
from .coinmarketcap import CoinMarketCap

# def start_scraping_job(job, coins):
#     for coin in coins:
#         cmc = CoinMarketCap(job=job,coin=coin)
#         coin_obj = cmc.scrape_data()
#         coin_obj.save()
import openpyxl
from openpyxl import Workbook

def start_scraping_job(job, coins):
    # Create a workbook and a sheet
    wb = Workbook()
    ws = wb.active
    ws.title = "Coin Data"

    # Add headers to the sheet
    headers = [
        "ID", "Job ID", "Name", "Price", "Price Change", "Market Cap", "Market Cap Rank",
        "Volume", "Volume Rank", "Volume Change", "Circulating Supply",
        "Total Supply", "Diluted Market Cap", "Contracts", "Official Links",
        "Socials"
    ]
    ws.append(headers)

    for coin in coins:
        cmc = CoinMarketCap(job=job, coin=coin)
        coin_obj = cmc.scrape_data()
        coin_obj.save()

        # Extract data from coin_obj
        data = [
            coin_obj.id,
            job.id,
            coin_obj.name,
            coin_obj.price,
            coin_obj.price_change,
            coin_obj.market_cap,
            coin_obj.market_cap_rank,
            coin_obj.volume,
            coin_obj.volume_rank,
            coin_obj.volume_change,
            coin_obj.circulating_supply,
            coin_obj.total_supply,
            coin_obj.diluted_market_cap,
            str(coin_obj.contracts),       # JSON fields as string
            str(coin_obj.official_links),  # JSON fields as string
            str(coin_obj.socials)          # JSON fields as string
        ]
        
        
        ws.append(data)

    # Save the workbook
    job.complete = True
    job.save()
    wb.save(f"./output/job_{job.id}_coin_data.xlsx")



