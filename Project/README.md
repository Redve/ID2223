# Project
This service will provide user to get an estimation of what the final price is going to be. This service is of now only limited to three types of property which is Apartements(Lägenheter), Row Houses(Par/Kedje/Radhus) and Villas(Villor). The data was trained with properties from Stockholm so this makes the model limited for predicting for Stockholm. The system consists of a Feature Pipeline which runs on Github actions once every week. The training pipeline runs every weeek after the feature pipeline.
 
## Project members 
* Adnane Acudad
* Redve Ahmed

## Data
The data was scraped from hemnet using Selenium. There is also a weekly scraper that runs in order to deliver continous data to the system. 

## Attempts
There was an attempt to use JSON data however, hemnets requests were very messy so this resulted in Selenium being used.


