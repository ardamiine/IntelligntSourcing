import os 
#from googletrans import Translator
from deep_translator import GoogleTranslator
import pandas as pd 
import openpyxl
from collections import defaultdict
from nltk.tokenize import word_tokenize
import nltk
import requests
from xml.etree import ElementTree

# Function to save DataFrame to Excel
def save_to_excel(df, base_filename):
    directory = "download"
    if not os.path.exists(directory):
        os.makedirs(directory)

    filename = os.path.join(directory, base_filename)
    counter = 1
    while os.path.exists(filename):
        filename = os.path.join(directory, f"{os.path.splitext(base_filename)[0]}_{counter}.xlsx")
        counter += 1

    df.to_excel(filename, index=False)
    print(f"Data saved to {filename}")
    
    return filename
#function to reverse date

def reverse_date_format(date_str):
    parts = date_str.split('-')
    reversed_date_str = f"{parts[2]}-{parts[1]}-{parts[0]}"
    return reversed_date_str


#function to transalte de to en 


def translate_to_en(text):
    translator = GoogleTranslator(source='auto', target="en")
    translation = translator.translate(text)
    return translation


# Function to convert list of dictionaries to DataFrame
def convert_to_df(info_list):
    return pd.DataFrame(info_list)

def analyse_rapport(rapport_text):
    # Ensure you download the necessary resources
    nltk.download('punkt')

    # Define phases and keywords
    phases = {
        "Préliminaire": [
            "vorläufigen", "insolvenzverwalter", "vorläufiger", "gesetzlicher", "vertreter",
            "überwachung", "prüfung", "sicherstellung", "gläubigerschutz", "risikobewertung"
        ],
        "procedure de faillite": [
            "insolvenz", "verfahren", "zahlungsunfähig", "klage", "verfahren",
            "gläubiger", "rettungsversuch", "antrag", "entscheidung", "schulden"
        ],
        "Traitement": [
            "abwicklungsphase", "gläubiger", "versammeln", "gläubigerversammlungen", "verkauf",
            "abschluss", "liquidation", "abwicklung", "vermögensverteilung", "einladung"
        ],
        "liquidation": [
            "liquidation", "liquidator", "vermögenswerte", "schlussbilanz", "zahlungen",
            "abschreibung", "restverbindlichkeiten", "schlussbericht", "verteilung",
            "schließung"
        ]
    }

    # Tokenize the rapport text
    tokens = word_tokenize(rapport_text.lower())

    # Analyze the text for phases
    phase_analysis = defaultdict(int)

    for token in tokens:
        for phase, keywords in phases.items():
            if token in keywords:
                phase_analysis[phase] += 1

    # Total keywords found
    total_keywords_found = sum(phase_analysis.values())

    # Determine conclusion based on the phases detected
    max_phase = max(phase_analysis, key=phase_analysis.get, default=None)
    
    # Calculate percentages
    phase_percentages = {
        phase: round((count / total_keywords_found * 100)) if total_keywords_found > 0 else 0
        for phase, count in phase_analysis.items()
    }
    
    # Return conclusion and percentages
    conclusion = max_phase if max_phase else "none"
    return conclusion, phase_percentages

def auth(db, user, password, domain):
    # URL of the server to send the POST request to
    url = "https://srvcrmv9dev.najnah.tn/cdmwebservices/sessionservices.asmx"
    
    # XML data to be sent in the POST request
    xml_data = f"""<?xml version="1.0" encoding="utf-8"?>
    <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
      <soap:Body>
        <Login xmlns="http://selligent.com/webservices/">
          <database>{db}</database>
          <user>{user}</user>
          <password>{password}</password>
          <domain>{domain}</domain>
        </Login>
      </soap:Body>
    </soap:Envelope>"""
    
    # Headers
    headers = {
        "Content-Type": "text/xml"
    }
    
    # Sending the POST request
    response = requests.post(url, data=xml_data, headers=headers, verify=False)
    
    # Checking the response
    if response.status_code == 200:
        print("auth say: Request was successful")
        
        return extract_login_result(response.content)
    else:
        print(f"auth say: Failed to send request. Status code: {response.status_code}")

        return None

def extract_login_result(response_content):
    #Parse the XML response to get the LoginResult
    tree = ElementTree.fromstring(response_content)
    # Find the LoginResult element
    login_result_element = tree.find('.//{http://selligent.com/webservices/}LoginResult')
    
    if login_result_element is not None:
        return login_result_element.text
    else:
        raise Exception("LoginResult not found in the response")




def isInSelligent(nrFrn="undefined",Email="undefined",WebFrn="undefined",AddrFrn="undefined",Mobile="undefined",SiretFrn="undefined",tel="undefined"):
    token = LastToken("LastToken.txt")
    url = "https://srvcrmv9dev.najnah.tn/cdmwebservices/ScriptServices.asmx"
    
    
    xml_data = f"""<?xml version="1.0" encoding="utf-8"?>
        <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
        <soap:Body>
        <ExecuteServerScript xmlns="http://selligent.com/webservices/">
        <sessionParams>{token}</sessionParams>
        <scriptNrid>41688058318854</scriptNrid>
        <paramsValue>
        {nrFrn};{Email};{WebFrn};{AddrFrn};{Mobile};{SiretFrn};{tel}
        </paramsValue>
    </ExecuteServerScript>
  </soap:Body>
</soap:Envelope>"""
    

    headers = {
        "Content-Type": "text/xml"
    }
    
    #POST 
    if checkToken(token):
        print("isINSelligent say: Token is exist")

        response = requests.post(url, data=xml_data, headers=headers, verify=False)
    
        #Checking 
        if response.status_code == 200:
            print("isINSelligent say: Request was successful")
            print(response.content) 
            print("isINSelligent say: len request",len(response.content))
            """with open("data_suplier.html", 'w') as f:
                f.write(response.text)
                print(f"Data  saved")"""
            return False if len(response.content)<=914 else True
        else:
            print(f"isINSelligent say: Failed to send request. Status code: {response.status_code}")
            return False
    else :
        print("isINSelligent say; Generate Tooken.......")
        token = auth("SELL_DEV", "$WS", "", "najnah")
        with open("LastToken.txt", 'w') as f:
            f.write(token)
        print(f"Token saved")
        isInSelligent(nrFrn,Email,WebFrn,AddrFrn,Mobile,SiretFrn,Mobile)

#test
def checkToken(token):
    url = "https://srvcrmv9dev.najnah.tn/cdmwebservices/ScriptServices.asmx"
    
    
    xml_data = f"""<?xml version="1.0" encoding="utf-8"?>
        <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
        <soap:Body>
        <ExecuteServerScript xmlns="http://selligent.com/webservices/">
        <sessionParams>{token}</sessionParams>
        <scriptNrid>41688058318854</scriptNrid>
        <paramsValue>
        ;undefined;undefined;undefined;undefined;undefined;undefined
        </paramsValue>
    </ExecuteServerScript>
  </soap:Body>
</soap:Envelope>"""
    headers = {
        "Content-Type": "text/xml"
    }
    response  = requests.post(url=url,data=xml_data,headers=headers,verify=False)
    if response.status_code == 200:
        print("checkToken say: Token checked ")
        print("checkToken say:",len(response.content))
        return True if len(response.content)>765 else False
    else:
        
        print("checkToken say: Error in requets")
        return False
    
# Usage 
def LastToken(file):
    with open(file, 'r') as f:
            lines = f.readlines()
            if lines:
                return lines[-1].strip() 
            else :
                return None
#ifVide for webservices
def IfVide(text):
    return text if text else "undefined"
        
if __name__ == "__main__":
    save_to_excel()
    reverse_date_format()
    translate_to_en()
    analyse_rapport()
   # sup = "707 ArjytjPPAREL"
    #print(isInSelligent(nrFrn=IfVide(sup)))
    #print(translate_to_en(""))'''
    
   
    