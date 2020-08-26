import csv
import json
import os
import time
from random import choice
from typing import Union, Generator, Any

import requests

VERSION = "0.0.1"
AUTHOR = "Parash Upreti"


class UCWage:
    """
    This class is used to scrape UC employee salary data
    from https://ucannualwage.ucop.edu/wage
    If the optional parameter `output` is True,
    a csv file will be create in `data` directory

    >> Example:
    >> from ucwage import UCWage
    >> wage = UCWage()
    >> campus = "Merced"
    >> year = 2018
    >> merced_2018 = wage(campus, year, output=True)
    """

    URL = 'https://ucannualwage.ucop.edu/wage/search.action'
    HEADERS = {'User-Agent': 'github.com/upretip/ucwage', 'DNT': '1'}
    PAYLOAD = {
        # '_search':'false',
        # 'nd':'1588809589891',
        # 'rows': '3000',
        'page': '1',
        'sidx': 'EAW_LST_NAM',
        'startSal': '0',
        'endSal': '9999999'
    }
    # DANR only exists before 2013, Hastings and ASUCLA added after 2017
    LOCATIONS = {'Hastings', 'UCOP', 'ASUCLA', 'Merced', 'Los Angeles', 'DANR',
                 'Santa Barbara', 'Santa Cruz', 'San Diego',
                 'Davis', 'Riverside',
                 'San Francisco', 'Irvine', 'Berkeley'}
    YEARS = list(range(2010, 2020))

    def __init__(self):
        pass

    def total_records(self, location: str, year: Union[str, int]) -> str:
        """
        Accepts the given location and the year and
        returns total records for that query
        :rparam:
        location: UC location as typed on the ucannual site
        year: the year the data is available for
        returns:
            records int

        """
        data = self.PAYLOAD.copy()

        if location in self.LOCATIONS and year in self.YEARS:
            data['location'] = location
            data['year'] = str(year)
        response = requests.post(self.URL, headers=self.HEADERS, data=data)
        response = json.loads(response.text.replace("'", "\""))
        return str(response["records"])

    def salaries(self, location: str, year: Union[str, int], output: bool = False, **kwargs: Any) -> Union[Exception, Generator[Any, Any, None]]:
        """
        Returns the full result from the query
        :rparam:
        location: UC location as typed on the ucannual site
        year: the year the data is available for
        output: if True
        returns:
            response['rows'] dict of all entries

        """
        data = self.PAYLOAD.copy()
        data['location'] = location
        data['year'] = year
        if (kwargs is None) or (kwargs is not None and 'rows' not in kwargs):
            data['rows'] = self.total_records(location, year)
        # update function with more kwargs here
        if kwargs is not None:
            for key, value in kwargs:
                if key in {'rows', 'page', 'sord', 'firstname', 'lastname'}:
                    data[key] = str(value)
        if int(data['rows']) > 0:
            try:
                response = requests.post(self.URL, headers=self.HEADERS, data=data)
                response = json.loads(response.text.replace("'", "\""), strict=False)
                salary = (person['cell'] for person in response['rows'])

            except Exception as e:
                return e

            if output:
                if 'data' not in os.listdir():
                    os.mkdir('data')
                with open(f'data/{location}_{year}.csv', 'w') as writefile:
                    writer = csv.writer(writefile)
                    writer.writerow(['Id', 'Year', 'Location', 'FirstName',
                                     'LastName', 'Title', 'GrossPay',
                                     'RegularPay', 'OvertimePay', 'OtherPay'])
                    writer.writerows(salary)
            # if data was written to csv, then the return will be empty
            return salary


def main():
    """Running this file as a script
    """
    wage = UCWage()
    campus = choice(list(wage.LOCATIONS))
    if campus == "DANR":
        year = choice(range(2010,2013))
    elif campus in ("Hastings", "ASUCLA"):
        year = choice(range(2018, 2020))
    else:
        year = choice(wage.YEARS)
    return wage.salaries(campus, year)


if __name__ == "__main__":
    random_scrape = main()
    for row in list(random_scrape)[:20]:
        print(row)
