# Intelligent Sourcing

<img src="https://raw.githubusercontent.com/MR10A/-intellegnt-sourcing/main/Readme/image.png?token=GHSAT0AAAAAACWKUL75LMTJGZI3NWM4JWUOZWRRSPA" alt="Web Crawler" width="100"/>

Directory Structure:
```
├── Denmark
│   ├── __pycache__/
│   ├── allRapport.py
│   ├── auktioner.py
│   ├── opencorporates.py
│   ├── proff.py
│   ├── statsidende.py
│   ├── StatsidendeMessages.py
│   ├── statsidendeProffAuktioner.py
│   └── tools.py
├── download/
├── Germany
│   ├── __pycache__/
│   ├── buster.crx
│   ├── dealone.py
│   ├── insolvenzantraegungen.py
│   ├── tools.py
│   ├── unternehmensregister.py
│   └── versteigerungskalender.py
├── img/
│   ├── static/
│   ├── templates/
│   ├── buttons.css
│   ├── clicked.js
│   ├── country.svg
│   ├── Germany.svg
│   ├── login.png
│   ├── ozcol.png
│   ├── reportanalysis.css
│   ├── reportanalysis.png
│   ├── script.js
│   ├── styles.css
│   └── web-crawler.png
├── UnitedKingdom
│   ├── __pycache__/
│   ├── buster.crx
│   ├── endole.py
│   ├── gazetteuk.py
│   ├── tes.py
│   ├── tools.py
│   └── __init__.py
├── templates/
│   ├── web.svg
│   ├── down.html
│   ├── error.html
│   ├── index.html
│   ├── popup.html
│   └── test.html
├── download/
│   ├── data_suplier.html
│   ├── LastToken.txt
├── requirements.txt
├── rout_run.py
└── tools.py
```
1. Denmark
allRapport.py: Module for generating comprehensive reports from Danish data.
auktioner.py: Scrapes auction-related data from Danish websites.
opencorporates.py: Extracts corporate information from Denmark's open corporate databases.
proff.py: Data extraction from Denmark's Proff.dk website.
statsidende.py: Module for interacting with the Danish Statstidende (Official Gazette).
StatsidendeMessages.py: Handles message extraction from the Statstidende.
statsidendeProffAuktioner.py: A combined scraper for both Statstidende and Proff auction data.
tools.py: Utility functions specific to the Denmark modules.
2. Germany
buster.crx: A Chrome extension for overcoming scraper blockages.
dealone.py: Scraper module for DealOne data.
insolvenzantraegungen.py: Handles insolvency-related data scraping in Germany.
tools.py: Utility functions specific to the Germany modules.
unternehmensregister.py: Extracts data from the German Unternehmensregister (Company Register).
versteigerungskalender.py: Scraper for German auction calendars.
3. United Kingdom
buster.crx: A Chrome extension for bypassing web scraper restrictions.
endole.py: Data extraction from Endole, a UK business information provider.
gazetteuk.py: Scraper for the UK Gazette, focusing on official notices.
tes.py: A scraper for The Education Service data.
tools.py: Utility functions specific to the UK modules.
4. Download
This directory stores downloaded data files and assets after processing.

5. Static
Contains static assets such as images and CSS files used in the project:

Images: (ozcol.png, reportanalysis.png, web-crawler.png, etc.)
CSS: (buttons.css, styles.css, reportanalysis.css, etc.)
JavaScript: (clicked.js, menu.js, etc.)
6. Templates
HTML templates for rendering data in a web interface:

down.html: Template for download pages.
index.html: Main landing page template.
popup.html: Template for popup dialogs.
error.html: Error page template.
7. Other Files
requirements.txt: Lists Python dependencies needed for the project.
rout_run.py: Main script to run the project’s routines.
tools.py: General utility functions for the project.
data_suplier.html: Web template for data suppliers.
LastToken.txt: Stores the last access token for authentication.
Getting Started
Prerequisites
Ensure you have Python 3.x installed and the required libraries as listed in requirements.txt.

Installation
Clone the repository.
Install dependencies:
bash
Copier le code
pip install -r requirements.txt
Usage
Run the main routine script:

bash
Copier le code
python rout_run.py
Modules can also be run individually for targeted data extraction.

Contributing
Contributions are welcome! Please submit a pull request with a detailed description of the changes.

License
This project is licensed under the MIT License - see the LICENSE.md file for details.

Acknowledgments
Thanks to all contributors and the open-source community for the tools and libraries used in this project.

Feel free to adjust the text to better match the specifics of your project!







