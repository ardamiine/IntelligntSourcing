# Intelligent Sourcing v1.1 <img src="https://github.com/MR10A/-intellegnt-sourcing/blob/main/Readme/image.png" alt="Web Crawler" width="50"/>
## Advanced Data Extraction and Processing Toolkit

Efficient and modular tools for scraping, analyzing, and processing data from various online sources across multiple regions.



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
│   └── data_suplier.html
│── LastToken.txt
├── requirements.txt
├── rout_run.py
└── tools.py
```
## 1. Denmark
- **auktioner.py**: Scrapes the Statstidende site (Denmark court site).
- **opencorporates.py**: Extracts corporate information from Denmark's open corporate databases.
- **proff.py**: Data extraction from Proff.dk website.
- **statsidende.py**: Module for interacting with the Danish Statstidende (Official Gazette).
- **StatsidendeMessages.py**: Handles message extraction from the Statstidende.
- **statsidendeProffAuktioner.py**: A combined scraper for both Statstidende and Proff and Auktioner data.
- **tools.py**: Utility functions specific to the Denmark modules.

## 2. Germany
- **buster.crx**: A Chrome extension for bypassing captcha.
- **dealone.py**: Scraping DealOne website data.
- **insolvenzantraegungen.py**: Scraping data from the Insolvenzantraegungen website.
- **tools.py**: Utility functions specific to the Germany modules.
- **unternehmensregister.py**: Extracts data from the German Unternehmensregister.
- **versteigerungskalender.py**: Scraping data from the German Versteigerungskalender website.

## 3. United Kingdom
- **buster.crx**: A Chrome extension for bypassing captcha.
- **endole.py**: Scraping data from Endole, a UK business information provider.
- **gazetteuk.py**: Scraping data from the UK Gazette, focusing on official notices.
- **tes.py**: Captcha solver.
- **tools.py**: Utility functions specific to the UK modules.

## 4. Download
This directory stores downloaded data files and assets after processing.

## 5. Static
Contains static assets such as images and CSS files used in the project:
- **Images**: (ozcol.png, reportanalysis.png, web-crawler.png, etc.)
- **CSS**: (buttons.css, styles.css, reportanalysis.css, etc.)
- **JavaScript**: (clicked.js, menu.js, etc.)

## 6. Templates
HTML templates for rendering data in a web interface:
- **down.html**: Template for download pages.
- **index.html**: Main landing page template.
- **popup.html**: Template for popup dialogs.
- **error.html**: Error page template.

## 7. Other Files
- **requirements.txt**: Contains the used libraries.
- **rout_run.py**: Main script to run the project’s routers.
- **tools.py**: General utility functions for the project.
- **LastToken.txt**: Stores the last access token for authentication with Selligent.
* Installation
Clone the repository.
Install dependencies:
_ ```bash
pip install -r requirements.txt
python
  ```
_ ```
  import nltk
  nltk.download('punkt')
  ```
* Usage
Run the main routine script:

```bash
python rout_run.py
```








