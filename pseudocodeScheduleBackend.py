
import pandas as pd
from bs4 import BeautifulSoup
import requests


# part that sends a request to html file
url = "https://www.studyMap.com/schedule" # something like that
response = requests.get(url)
response.text[:100]  # Access the HTML with the text property


class HTMLTableParser:

    def parse_url(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        return [(table['id'], self.parse_html_table(table)) \
                for table in soup.find_all('table')]

    def parse_html_table(self, table):
        n_columns = 0
        n_rows = 0
        column_names = []

        # Find number of rows and columns
        # we also find the column titles if we can
        for row in table.find_all('tr'):

            # Determine the number of rows in the table
            td_tags = row.find_all('td')
            if len(td_tags) > 0:
                n_rows += 1
                if n_columns == 0:
                    # Set the number of columns for our table
                    n_columns = len(td_tags)

            # Handle column names if we find them
            th_tags = row.find_all('th')
            if len(th_tags) > 0 and len(column_names) == 0:
                for th in th_tags:
                    column_names.append(th.get_text())






        # since we're going through all the table here we can add id's of all the checkboxes (if they're unique)
        # we can add them to the lisr