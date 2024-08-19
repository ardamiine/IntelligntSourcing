from bs4 import BeautifulSoup

# Read the XML content from the file
with open('data_suplier.xml', 'r', encoding='utf-8') as file:
    xml_content = file.read()

# Parse the XML content
soup = BeautifulSoup(xml_content, 'xml')

# Find the relevant part containing the table
table_content = soup.find('ExecuteServerScriptResult').string

# Decode the HTML entities
decoded_table_content = BeautifulSoup(table_content, 'html.parser').prettify()

# Print the decoded table content
with open('data_suplier.html', 'w', encoding='utf-8') as file:
    file.write(decoded_table_content)
    print("file saved")
print(decoded_table_content)
