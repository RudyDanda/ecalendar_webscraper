from playwright.async_api import async_playwright
import navigate_website
import asyncio
import re
import pandas as pd

###############Helper Functions###############

# data wrangling helper
def number_cleaner(s):
    # remove non-numeric characters
    cleaned = re.sub(r'[^0-9.-]', '', s)
    
    # Split by decimal and rejoin with only the first decimal
    parts = cleaned.split('.')
    return parts[0] + '.' + ''.join(parts[1:]) if len(parts) > 1 else parts[0]

# Returns the 
async def get_header_rows(index, page):
        
        header_rows = await page.query_selector_all('//*[starts-with(@id, "ctl00_ContentPlaceHolder1_ctl02_Repeater1_ctl") and contains(@id, "_th1")]//tr/th[1]')
        header_ele = await header_rows[index].inner_text()

        return header_ele


async def get_all_days(month, year, page):

    last_day = navigate_website.month_end_helper(month, year)


    days = await page.query_selector_all('#calendar > tbody')

    return days

#######################################################################
############# CSS/XPath selector code on website   ####################
#######################################################################

async def collect_data(day, date, page):
    async with async_playwright() as pw:

        data = [] #pandas data list
        
        # All rows for a given day
        rows = await day.query_selector_all('//tr[@data-url]') 
        
        
        for row in rows:

            #dictionary to hold each row
            row_data = {} 

            ##########Time##########
            time_element = await row.query_selector('td:nth-child(1)')
            if await time_element.inner_text() != None:
                time_inner = await time_element.inner_text()
                time_text = time_inner.strip()
                row_data['Time'] = time_text
            else:
                row_data['Time'] = ''

            ########Country#########
            country_element = await row.query_selector('td:nth-child(2)')
            if await country_element.inner_text() != None:
                country_inner = await country_element.inner_text()
                country_text = country_inner.strip()
                row_data['Country'] = country_text
            else:
                row_data['Country'] = ''

            ##########Event#############
            event_element = await row.query_selector('td:nth-child(3)')
            if await event_element.inner_text() != None:
                event_inner = await event_element.inner_text()
                event_text = event_inner.strip()
                row_data['Event'] = event_text
            else:
                row_data['Event'] = ''

            ###########Actual########
            actual_element = await row.query_selector('td:nth-child(4)')

            if await actual_element.inner_text() != None:
                actual_inner = await actual_element.inner_text()
                actual_text = actual_inner.strip()
                row_data['Actual'] = actual_text
            else:
                row_data['Actual'] = ''

            ############Consensus########
            consensus_element = await row.query_selector('td:nth-child(6)')

            if await consensus_element.inner_text() != None:
                consensus_inner = await consensus_element.inner_text()
                consensus_text = consensus_inner.strip()
                row_data['Consensus'] = consensus_text
            else:
                row_data['Consensus'] = ''

            ###########Forecast#########
            forecast_element = await row.query_selector('td:nth-child(7)')

            if await forecast_element.inner_text() != None:
                forecast_inner = await forecast_element.inner_text()
                forecast_text = forecast_inner.strip()
                row_data['Forecast'] = forecast_text
            else:
                row_data['Forecast'] = ''

            ###########Beat/Inline/Miss#########
            #     
            bim_number = ''

            #Calculate difference between Actual and Forecast
            if await forecast_element.inner_text() != '' and await actual_element.inner_text() != '':
                bim_number = float(number_cleaner(actual_text)) - float(number_cleaner(forecast_text))

            #Assign category
            result = ''
            if bim_number != '':
                if bim_number > 0:
                    result = 'Beat'
                elif bim_number < 0:
                    result = 'Miss'
                else:
                    result = 'In-Line'

            row_data['BIM'] = result

            # add the dictionary row data to the pandas dataframe
            data.append(row_data)

        
#######################################################################
#############  Pandas data exporting to Excel sheet  ##################
#######################################################################
        try:

            #
            df_old = pd.read_excel('2022.xlsx', index_col=[0,1])
            df_new = pd.DataFrame(data)

            df_new.reset_index(inplace=True)
            # Then set a MultiIndex with 'date' as the first level and the original index as the second level
            df_new.set_index([pd.Index([date]*len(df_new), name='Date'), 'index'], inplace=True)

            pieces = [df_old, df_new]
            df_combined = pd.concat(pieces, ignore_index=False)
            
            
            df_combined.to_excel('2022.xlsx', header=True)

        except:
            

            df = pd.DataFrame(data)

            
            df.reset_index(inplace=True)

            # Then set a MultiIndex with 'date' as the first level and the original index as the second level
            df.set_index([pd.Index([date]*len(df), name='Date'), 'index'], inplace=True)
            

            df.to_excel('2022.xlsx', header=True)
            

        