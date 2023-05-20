# www.rvusa.com Data Scraper

www.rvusa.com is an excellent repository of RV model info.  Unfortunately it is not offer an interface that allows advanced filtering/searching.

For example, say you wanted to find all 2016-2020 MY Class C motorhomes under 27' with Grey tanks larger than 45 gallons.  I decided to build a scraper to take all the rvusa.com model info and dump it into an panda dataframe and .xls so it is easily searchable/filterable.

The scraper works today, but there are some rough edges/workaround implemented for how rvusa organizes data.  Some to-do items:

* Move the current shell script wrappers to python
* Incorporate command line tools to enabl filtering what is scraped (e.g. scrapy by RV class, brand etc.)
* Perform some data cleanup

The resulting .xlsx is also in the git repo if you simply want to download it to filter / search the data.