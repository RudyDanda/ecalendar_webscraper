from playwright.async_api import async_playwright
import string
import re
import asyncio
import CSS_selectors
import navigate_website


async def main():
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)

        page = await browser.new_page()

        await page.goto("https://tradingeconomics.com/calendar")

        # Select time frame to collect data
        for year in range(2022, 2023):
            for month in range(1, 13):

                await navigate_website.show_month_data(month,1,year,page)
                days = await CSS_selectors.get_all_days(month, year, page)
                
                i = 0
                for day in days:
                    date = await CSS_selectors.get_header_rows(i, page)

                    await CSS_selectors.collect_data(day, date, page)

                    i = i + 1
                    if i == 100:
                        break
                
                


if __name__ == "__main__":
    asyncio.run(main())