Name: Vandana Cendrollu Nagesh

# Project Description
1. FEATURES
This Python package processes an incidents file from the Norman Police Department website using the provided file URL as input. It performs the following actions:

1. Takes the url of the pdf file as input or the user can upload the file.
2. Shows 3 unique visualizations on the webpage giving users better understanding about the incidents on that day.  

2. PROJECT STRUCTURE
The project is organized with a main file that initiates the process, which then utilizes three distinct modules: fetchincidents, extractdata, and dbmanager to perform the outlined tasks. All files are located in the assignment0 folder in the root directory, and the modules are imported into main.py to execute the necessary functions.

The downloaded PDF is saved in the resources/tmp/ directory and is later accessed using the pypdf package to extract the required data. The SQLite database file is also stored in the resources folder. During testing, the PDF file is stored in the test_files directory.

3. TESTING
The project is divided into three key phases: data download, data extraction, and data storage. Separate test files are provided for each phase:

1. test_download.py verifies the data download process.
2. test_extraction.py evaluates the extraction functions responsible for pulling specific information from the raw text.
3. test_dbmanager.py ensures proper functionality related to creating and managing the SQLite database.


# How to install
pipenv install

## How to run
pipenv run python3 project00/main.py --incidents <url>

## How to test
pipenv run python3 -m pytest <test_file>

[![Watch the video](https://img.youtube.com/vi/775e0nLt4gs/0.jpg)](https://youtu.be/fG2KjTSSwas)

## Functions
#### main.py \
main(): This function accepts a URL as a parameter. It orchestrates the data download, extraction of incident information, and saving the data in an SQLite database. It also prints the status of incidents and returns nothing.

#### fetchincidents.py \
fetchincidents(): Accepts a URL and retrieves the binary data from it, returning the data.

#### extractdata.py \
extractdata(): Takes a PDF file path as input, extracts raw data, and processes it to extract relevant incident information. Returns the extracted incident data as a list.

process_incidents_by_page(): Processes the incident data page-by-page, line-by-line, and returns a list of tuples containing parsed information.

extract_time(): Parses and returns the time of occurrence from the raw incident string.

extract_number(): Extracts and returns the incident number from the raw incident string.

extract_address(): Extracts and returns the location of the incident and the last index used to parse the nature of the incident.

extract_nature_and_ori(): Takes the raw incident string , parsing and returning the nature of the incident and the ORI code.

#### dbmanager.py \
createdb(): Accepts the database file path, creates an SQLite database (if it doesn't already exist), establishes a connection, and returns the connection object.

populatedb(): Accepts a database connection object and a list of incident tuples, inserting the data into the database.

status(): Takes the database connection object and prints a list of the types of incidents and the number of occurrences. It does not return any value.

## Database Development
The SQLite database contains a single table that stores all the incident information. The table has five columns:

incident_time: Stores the time the incident occurred.
incident_number: Stores the unique incident number.
incident_location: Stores the address where the incident took place.
nature: Stores the nature of the incident.
incident_ori: Stores the ORI code of the incident.

Sample data - 
0:01|2024-00000001|3603 N FLOOD AVE|Traffic Stop|OK0140200
0:03|2024-00000001|226 CINDY AVE|Chest Pain|14005
0:03|2024-00000001|226 CINDY AVE|Sick Person|EMSSTAT
0:04|2024-00000002|E MAIN ST / N JONES AVE|Traffic Stop|OK0140200

Database Connection and Commit - 
The database connection is established when createdb() is called in main.py. Data is committed to the database when the connection is made and when data is inserted via the populatedb() function. The connection is closed after the status() function is executed.


## Bugs and Assumptions
1. The ORI code can only be one of the following: ['OK0140200', 'EMSSTAT', '14005', '14009']. The code does not handle other ORI values.
2. The address is assumed to be a street address. Global addresses or addresses that include country or state details are not supported.
3. The code is limited to parsing U.S. street addresses only.
