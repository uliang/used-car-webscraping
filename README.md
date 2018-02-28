# used-car-webscraping

Scrape used car listings from [Sg Car Mart](http://www.sgcarmart.com/used_cars/listing.php) to a .csv file. We then can analyse the data and build a model for car prices from several relevant factors. 

The great thing is that these are actual and up-to-date car prices. This script can be programmed to run periodically to get most updated listings. Evolution of prices over time can be analysed. 

# Requirements
Most of the visual and statistical analysis can be found in the accompanying Jupyter Notebook. Required packages are given in the requirements.txt file. To install them, create a conda environment (if using [Anaconda](https://www.anaconda.com)) and then install the required packages listed in the requirements.txt file. 

Type
`conda create -n env_name python=3.6`
`pip install-r requirements.txt`

from the terminal. 

Scraping script will output a .csv file in your working directory. To run type 
`python scrape.py`
from the terminal. 
