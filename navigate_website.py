from playwright.async_api import async_playwright
from playwright.async_api import TimeoutError
import asyncio
import time


#Helper function that retries any new page load in if there is a network error
async def retry_operation(operation, exceptions_to_retry, max_retries=3, delay=5):
    for attempt in range(max_retries):
        try:
            return await operation()
        except exceptions_to_retry as e:
            if attempt < max_retries - 1:
                print(f"Attempt {attempt + 1} failed with error: {e}. Retrying in {delay} seconds...")
                await asyncio.sleep(delay)
            else:
                print(f"Operation failed after {max_retries} attempts.")
                raise e
        except Exception as unexpected_error:
            print(f"Unexpected error occurred: {unexpected_error}")
            raise unexpected_error
        
#Helper function to determine last day of each month
def month_end_helper(month, year):
    if month == 1:
        return 31
    elif month == 2:
        if year % 4 == 0:
            return 29
        else:
            return 28
    elif month == 3:
        return 31
    elif month == 4:
        return 30
    elif month == 5:
        return 31
    elif month == 6:
        return 30
    elif month == 7:
        return 31
    elif month == 8:
        return 30
    elif month == 9:
        return 30
    elif month == 10:
        return 31
    elif month == 11:
        return 30
    elif month == 12:
        return 31


# Navigates the website and shows custom data until the end of the month inputted
async def show_month_data(month, day, year, page):
    async with async_playwright() as pw:
        
        # wrap the prone-to-fail operations with the retry mechanism:
        await retry_operation(page.get_by_role('button', name=' Dates').click, (TimeoutError))
        await retry_operation(page.get_by_role('menuitem', name= '✏ Custom' ).click, (TimeoutError))
        
        await page.locator('#startDate').press('Meta+a')
        await page.locator('#startDate').fill(str(year) + '-' + str(month) + '-' + str(day))
        await page.locator('#endDate').click()
        await page.locator('#endDate').press('Meta+a')
        await page.locator('#endDate').fill(str(year) + '-' + str(month) + '-' + str(month_end_helper(month, year)))

        async with page.expect_navigation():
            await retry_operation(page.get_by_role('button', name= 'Submit').click, (TimeoutError))