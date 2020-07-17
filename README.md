# UCWage: Salary information for University of California Employees

Every summer, University of California system releases the salary information on their public website [ucannualwage.ucop.edu](https://ucannualwage.ucop.edu/wage) for the previous calendar year. 
This information is available for all employees.  Names for those whose primary role was student (graudate or undergraduate) if they received any paycheck that year are masked.

This library provides an easy and pythonic way to get the salary data for a given campus and year. 

```
from ucwage import UCWage

campus = "UCOP"
year = 2015
wage = UCWage()

# if output (False by default) then function yields salaries
data = wage.salaries(campus, year, output=True)

```

Please be respectful of the University of California technology and property when running this code. 
While this data is availble to public for free, excessive requests will put a burden on their system.
If you are not familiar with ethical scraping, there are plenty of blog posts out there.

Motivated by [ralieghlittles](https://github.com/raleighlittles)