import pypdf
from pypdf import PdfReader
import re
from io import BytesIO

# def extractdata(pdf_file):
#     '''Extracts raw data from pdf file and processes the raw data to extract relavant information'''
#     reader = PdfReader(pdf_file)
#     num_pages = len(reader.pages)
#     raw_incidents_text = list()
#     for page_number in range(num_pages):
#         page = reader.pages[page_number]
#         text = page.extract_text()
#         raw_incidents_text.append(text)
#     # print("EXTRACTED ALL INCIDENTS TEXT!!\n")
#     all_incidents = process_incidents_by_page(raw_incidents_text)
#     # print('ALL INCIDENTS!')
#     # print(raw_incidents_text)
#     return all_incidents

def extractdata(pdf_file):
    '''Extracts raw data from pdf file and processes it page by page'''
    reader = PdfReader(pdf_file)
    incident_pattern = r"(Traffic Stop|Suspicious|Missing Person|Kidnapping|Assist EMS|Headache|Fire Fuel Spill|Fire Carbon Monoxide Alarm|COP Problem Solving|Officer in Danger|Assist Fire|Assault|Fire Transformer Blown|Fire Mutual Aid|Bar Check|Test Call|Animal Vicious|Back Pain|Fire Dumpster|Preg/Child Birth/Miscarriage|Welfare Check|Bomb/Threats/Package|Special Assignment|Prowler|Burns/Explosions|EMS Mutual Aid|Homicide|Stand By EMS|Loud Party|Molesting|Fire Residential|Cardiac Respritory Arrest|Body Reported|Animal Livestock|Traumatic Injury|Reckless Driving|Shooting Stabbing Penetrating|Carbon Mon/Inhalation/HazMat|Foot Patrol|Transfer/Interfacility|Animal Trapped|Choking|Burglary|COP Relationships|Unknown Problem/Man Down|Officer Needed Nature Unk|Barking Dog|Animal Bites/Attacks|Warrant Service|Contact a Subject|Disturbance/Domestic|Motorist Assist|Noise Complaint|Larceny|Trespassing|Unconscious/Fainting|Medical Call Pd Requested|Shots Heard|Alarm|Supplement Report|Convulsion/Seizure|MVA With Injuries|Overdose/Poisoning|Mutual Aid|Diabetic Problems|Heat/Cold Exposure|Breathing Problems|Public Assist|Runaway or Lost Child|Chest Pain|MVA Non Injury|Public Intoxication|Stroke|Open Door/Premises Check|Check Area|Vandalism|Animal Complaint|Animal Dead|Fire Alarm|Follow Up|Item Assignment|Animal Injured|Fraud|Pick Up Partner|Supplement Report|911 Call Nature Unknown|Falls|Escort/Transport|Animal at Large|Parking Problem|Abdominal Pains/Problems|Indecent Exposure|Animal Bite|Hit and Run|Stolen Vehicle|Sick Person|Harassment / Threats Report|Fire Grass|Assault EMS Needed|Alarm Holdup/Panic|Fight|Fire Smoke Investigation|Heart Problems/AICD|Fire Commercial|Fire Electrical Check|COP DDACTS|Fire Odor Investigation|Extra Patrol|Fire Controlled Burn|Civil Standby|Drunk Driver|Hemorrhage/Lacerations|Warrant Service|Debris in Roadway|Pick Up Items|Found Item|Stand By EMS|Stake Out|Unknown Problem/Man Down|Officer Needed Nature|Assist Police|Unk|Allergies/Envenomations|Road Rage|Fire Carbon Monoxide Alarm|Fire Water Rescue|Fire Down Power Line|Fire Gas Leak|Drowning/Diving/Scuba Accident|Cardiac Respiratory Arrest|Drug Violation|Loud Party)"
    ori_types = r"(OK0140200|14005|EMSSTAT|14009|COMMAND)"
    whole_string_pattern = rf"(\d{{1,2}}/\d{{1,2}}/\d{{4}} \d{{1,2}}:\d{{2}})\s+(\d{{4}}-\d{{8}})\s+(.*?)(?:(\n(?!\d{{1,2}}/\d{{1,2}}/\d{{4}}).*)+)?\s+({incident_pattern})\s+({ori_types})"
    page_text = ''

    for page in range(len(reader.pages)):
        page_text += reader.pages[page].extract_text() +"\n"
    lines = page_text.splitlines()

    final_list = []
    c_l = ''
    for line in lines:
        if "Daily Incident Summary (Public)" in line or line is None or "Date / Time Incident Number Location Nature Incident ORI" in line:
            continue
        # Check if the line starts a new incident
        if re.match(r'\d{1,2}/\d{1,2}/\d{4}', line):
            line = re.sub(r'(\d{4}-\d{8})([A-Z])', r'\1 \2', line)
            match = re.match(whole_string_pattern, line)
            if match:
                final_list.append([match.groups()[0], match.groups()[1], match.groups()[2], match.groups()[4], match.groups()[6]])  
            c_l = line 
        else:
            line = c_l + ' ' + line
            line = re.sub(rf'{incident_pattern}', r' \1', line)
            match = re.match(whole_string_pattern, line)
            if match:
                final_list.append([match.groups()[0], match.groups()[1], match.groups()[2], match.groups()[4], match.groups()[6]])  
    return final_list


def process_incidents_by_page(raw_incidents_text:list):
    '''Processes the whole incidents data page-by-page, then line-by-line in each page 
        to extract relavant keys and values'''
    final_incidents_list = list()
    incident_type_pattern = r"(Traffic Stop|Suspicious|Missing Person|Kidnapping|Assist EMS|Headache|Fire Fuel Spill|Fire Carbon Monoxide Alarm|COP Problem Solving|Officer in Danger|Assist Fire|Assault|Fire Transformer Blown|Fire Mutual Aid|Bar Check|Test Call|Animal Vicious|Back Pain|Fire Dumpster|Preg/Child Birth/Miscarriage|Welfare Check|Bomb/Threats/Package|Special Assignment|Prowler|Burns/Explosions|EMS Mutual Aid|Homicide|Stand By EMS|Loud Party|Molesting|Fire Residential|Cardiac Respritory Arrest|Body Reported|Animal Livestock|Traumatic Injury|Reckless Driving|Shooting Stabbing Penetrating|Carbon Mon/Inhalation/HazMat|Foot Patrol|Transfer/Interfacility|Animal Trapped|Choking|Burglary|COP Relationships|Unknown Problem/Man Down|Officer Needed Nature Unk|Barking Dog|Animal Bites/Attacks|Warrant Service|Contact a Subject|Disturbance/Domestic|Motorist Assist|Noise Complaint|Larceny|Trespassing|Unconscious/Fainting|Medical Call Pd Requested|Shots Heard|Alarm|Supplement Report|Convulsion/Seizure|MVA With Injuries|Overdose/Poisoning|Mutual Aid|Diabetic Problems|Heat/Cold Exposure|Breathing Problems|Public Assist|Runaway or Lost Child|Chest Pain|MVA Non Injury|Public Intoxication|Stroke|Open Door/Premises Check|Check Area|Vandalism|Animal Complaint|Animal Dead|Fire Alarm|Follow Up|Item Assignment|Animal Injured|Fraud|Pick Up Partner|Supplement Report|911 Call Nature Unknown|Falls|Escort/Transport|Animal at Large|Parking Problem|Abdominal Pains/Problems|Indecent Exposure|Animal Bite|Hit and Run|Stolen Vehicle|Sick Person|Harassment / Threats Report|Fire Grass|Assault EMS Needed|Alarm Holdup/Panic|Fight|Fire Smoke Investigation|Heart Problems/AICD|Fire Commercial|Fire Electrical Check|COP DDACTS|Fire Odor Investigation|Extra Patrol|Fire Controlled Burn|Civil Standby|Drunk Driver|Hemorrhage/Lacerations|Warrant Service|Debris in Roadway|Pick Up Items|Found Item|Stand By EMS|Stake Out|Unknown Problem/Man Down|Officer Needed Nature|Assist Police|Unk|Allergies/Envenomations|Road Rage|Fire Carbon Monoxide Alarm|Fire Water Rescue|Fire Down Power Line|Fire Gas Leak|Drowning/Diving/Scuba Accident|Cardiac Respiratory Arrest|Drug Violation|Loud Party)"
    
    c=0
    for page_text in raw_incidents_text:
        c+=1
        incidents_by_page = page_text.split('\n')
        count = 0
        for incident_string in incidents_by_page:
            count+=1
            if "Daily Incident Summary (Public)" in incident_string or incident_string is None or "Date / Time Incident Number Location Nature Incident ORI" in incident_string:
                continue
            incident_time, incident_ori, incident_number = None, None, None
            incident_address, incident_nature = None, None
            incident_time = extract_time(incident_string)
            if not incident_time:
                continue
            incident_number = extract_number(incident_string)
            incident_address = extract_address(incident_string)
            incident_nature, incident_ori = extract_nature_and_ori(incident_string)
            final_incidents_list.append((incident_time, incident_number, incident_address, incident_nature, incident_ori))
    # print(count)
    # print(c)
    # print('PROCESSED ALL INCIDENTS!!')
    # print('Total rows count in extracted incidents list = ', count)
    # print('Total actual incidents count = ', len(final_incidents_list))
    return final_incidents_list

# def extract_nature_and_ori(input_string, start_index):
#     '''Parses the nature of the incident and the ori number from the raw incident string'''
#     standard_oris = ['OK0140200', 'EMSSTAT', '14005', '14009']
#     ori_match = re.search(r'(\w+)$', input_string)
#     ori_number = None
#     incident_nature = None
#     end_index = -1
#     if ori_match:
#         for s in standard_oris:
#             if s in input_string:
#                 ori_number = s
#                 end_index = input_string.find(ori_number)
#                 break
#     if not ori_number:
#         # print('ORI NUMBER IS NONE FOR THIS INPUT STRING')
#         # print(input_string)
#         return None, None
#     incident_nature = input_string[start_index+1:end_index].strip(' ')
#     return incident_nature, ori_number
def extract_nature_and_ori(input_string):
    ori = ''
    nature = ''
    ori_pattern = r"(OK0140200|14005|EMSSTAT|14009|COMMAND)"
    incident_types = r"(Traffic Stop|Suspicious|Missing Person|Kidnapping|Assist EMS|Headache|Fire Fuel Spill|Fire Carbon Monoxide Alarm|COP Problem Solving|Officer in Danger|Assist Fire|Assault|Fire Transformer Blown|Fire Mutual Aid|Bar Check|Test Call|Animal Vicious|Back Pain|Fire Dumpster|Preg/Child Birth/Miscarriage|Welfare Check|Bomb/Threats/Package|Special Assignment|Prowler|Burns/Explosions|EMS Mutual Aid|Homicide|Stand By EMS|Loud Party|Molesting|Fire Residential|Cardiac Respritory Arrest|Body Reported|Animal Livestock|Traumatic Injury|Reckless Driving|Shooting Stabbing Penetrating|Carbon Mon/Inhalation/HazMat|Foot Patrol|Transfer/Interfacility|Animal Trapped|Choking|Burglary|COP Relationships|Unknown Problem/Man Down|Officer Needed Nature Unk|Barking Dog|Animal Bites/Attacks|Warrant Service|Contact a Subject|Disturbance/Domestic|Motorist Assist|Noise Complaint|Larceny|Trespassing|Unconscious/Fainting|Medical Call Pd Requested|Shots Heard|Alarm|Supplement Report|Convulsion/Seizure|MVA With Injuries|Overdose/Poisoning|Mutual Aid|Diabetic Problems|Heat/Cold Exposure|Breathing Problems|Public Assist|Runaway or Lost Child|Chest Pain|MVA Non Injury|Public Intoxication|Stroke|Open Door/Premises Check|Check Area|Vandalism|Animal Complaint|Animal Dead|Fire Alarm|Follow Up|Item Assignment|Animal Injured|Fraud|Pick Up Partner|Supplement Report|911 Call Nature Unknown|Falls|Escort/Transport|Animal at Large|Parking Problem|Abdominal Pains/Problems|Indecent Exposure|Animal Bite|Hit and Run|Stolen Vehicle|Sick Person|Harassment / Threats Report|Fire Grass|Assault EMS Needed|Alarm Holdup/Panic|Fight|Fire Smoke Investigation|Heart Problems/AICD|Fire Commercial|Fire Electrical Check|COP DDACTS|Fire Odor Investigation|Extra Patrol|Fire Controlled Burn|Civil Standby|Drunk Driver|Hemorrhage/Lacerations|Warrant Service|Debris in Roadway|Pick Up Items|Found Item|Stand By EMS|Stake Out|Unknown Problem/Man Down|Officer Needed Nature|Assist Police|Unk|Allergies/Envenomations|Road Rage|Fire Carbon Monoxide Alarm|Fire Water Rescue|Fire Down Power Line|Fire Gas Leak|Drowning/Diving/Scuba Accident|Cardiac Respiratory Arrest|Drug Violation|Loud Party)"
    ori_match = re.search(ori_pattern, input_string)
    if ori_match:
        ori = ori_match.group(1)
    nature_match = re.search(incident_types, input_string)
    if nature_match:
        nature = nature_match.group(1)
    return nature, ori

# def extract_address(input_string):
#     '''Parses the location of the incident from the raw incident string'''
#     street_type_list = ['RD/156', 'LAMB TOWING', '201 W GRAY', '1919 W BOYD'
#         , 'BNSF RR', '1100 N PORTER', 'BRIARCLIFF', 'CHESTNUT', 'H4 AL', 'HWY 9',
#         'Allee', 'Alley', 'Ally', 'Aly', 'Anex', 'Annex',
#         'Annx', 'Anx', 'Arc', 'Arcade', 'Av', 'Ave', 'APT',
#         'Aven', 'Avenu', 'Avenue', 'Avn', 'Avnue', 'Base', 'Bayoo',
#         'Bayou', 'Bch', 'Beach', 'Bend', 'Bg', 'Bgs',
#         'Blf', 'Blfs', 'Bluf', 'Bluff', 'Bluffs', 'Blvd',
#         'Bnd', 'Bot', 'Bottm', 'Bottom', 'Boul', 'Boulevard',
#         'Boulv', 'Br', 'Branch', 'Brdge', 'Brg', 'Bridge',
#         'Brk', 'Brks', 'Brnch', 'Broadway', 'Brook', 'Brooks',
#         'Btm', 'Burg', 'Burgs', 'Byp', 'Bypa', 'Bypas',
#         'Bypass', 'Byps', 'Byu', 'Camp', 'Canyn', 'Canyon',
#         'Cape', 'Causeway', 'Causwa', 'Cen', 'Cent', 'Center',
#         'Centers', 'Centr', 'Centre', 'Cir', 'Circ', 'Circl',
#         'Circle', 'Circles', 'Cirs', 'Clb', 'Clf', 'Clfs',
#         'Cliff', 'Cliffs', 'Club', 'Cmn', 'Cmns', 'Cmp',
#         'Cnter', 'Cntr', 'Cnyn', 'Common', 'Commons', 'Cor',
#         'Corner', 'Corners', 'Cors', 'Course', 'Court', 'Courts',
#         'Cove', 'Coves', 'Cp', 'Cpe', 'Crcl', 'Crcle',
#         'Creek', 'Cres', 'Crescent', 'Crest', 'Crk', 'Crossing',
#         'Crossroad', 'Crossroads', 'Crse', 'Crsent', 'Crsnt', 'Crssng',
#         'Crst', 'Cswy', 'Ct', 'Ctr', 'Ctrs', 'Cts',
#         'Curv', 'Curve', 'Cv', 'Cvs', 'Cyn', 'Dale',
#         'Dam', 'Div', 'Divide', 'Dl', 'Dm', 'Dr',
#         'Driv', 'Drive', 'Drives', 'Drs', 'Drv', 'Dv',
#         'Dvd', 'Est', 'Estate', 'Estates', 'Ests', 'Exp',
#         'Expr', 'Express', 'Expressway', 'Expw', 'Expy', 'Ext',
#         'Extension', 'Extensions', 'Extn', 'Extnsn', 'Exts', 'Fall'
#         , 'Ferry', 'Field', 'Fields', 'Flat', 'Flats',
#         'Fld', 'Flds', 'Fls', 'Flt', 'Flts', 'Ford',
#         'Fords', 'Forest', 'Forests', 'Forg', 'Forge', 'Forges',
#         'Fork', 'Forks', 'Fort', 'Frd', 'Frds', 'Freeway',
#         'Freewy', 'Frg', 'Frgs', 'Frk', 'Frks', 'Frry',
#         'Frst', 'Frt', 'Frway', 'Frwy', 'Fry', 'Ft',
#         'Fwy', 'Garden', 'Gardens', 'Gardn', 'Gateway', 'Gatewy',
#         'Gatway', 'Gdn', 'Gdns', 'Glen', 'Glens', 'Gln',
#         'Glns', 'Grden', 'Grdn', 'Grdns', 'Green', 'Greens',
#         'Grn', 'Grns', 'Grov', 'Grove', 'Groves', 'Grv',
#         'Grvs', 'Gtway', 'Gtwy', 'Harb', 'Harbor', 'Harbors',
#         'Harbr', 'Haven', 'Hbr', 'Hbrs', 'Heights', 'Highway',
#         'Highwy', 'Hill', 'Hills', 'Hiway', 'Hiwy', 'Hl',
#         'Hllw', 'Hls', 'Hollow', 'Hollows', 'Holw', 'Holws',
#         'Hrbor', 'Ht', 'Hts', 'Hvn', 'Hway', 'Hwy',
#         'Inlet', 'Inlt', 'Is', 'Island', 'Islands', 'Isle',
#         'Isles', 'Islnd', 'Islnds', 'Iss', 'Jct', 'Jction',
#         'Jctn', 'Jctns', 'Jcts', 'Junction', 'Junctions', 'Junctn',
#         'Juncton', 'Key', 'Keys', 'Knl', 'Knls', 'Knol',
#         'Knoll', 'Knolls', 'Ky', 'Kys', 'Lake', 'Lakes',
#         'Land', 'Landing', 'Lane', 'Lck', 'Lcks', 'Ldg',
#         'Ldge', 'Lf', 'Lgt', 'Lgts', 'Light', 'Lights',
#         'Lk', 'Lks', 'Ln', 'Lndg', 'Lndng', 'Loaf',
#         'Lock', 'Locks', 'Lodg', 'Lodge', 'Loop', 'Loops',
#         'Lp', 'Mall', 'Manor', 'Manors', 'Mdw', 'Mdws',
#         'Meadow', 'Meadows', 'Medows', 'Mews', 'Mill', 'Mills',
#         'Mission', 'Missn', 'Ml', 'Mls', 'Mnr', 'Mnrs',
#         'Mnt', 'Mntain', 'Mntn', 'Mntns', 'Motorway', 'Mount',
#         'Mountain', 'Mountains', 'Mountin', 'Msn', 'Mssn', 'Mt',
#         'Mtin', 'Mtn', 'Mtns', 'Mtwy', 'Nck','Ne' , 'Neck', 'Nw','Norman', 'OK-9', 'OK', ','
#         'Opas', 'Orch', 'Orchard', 'Orchrd', 'Oval', 'Overpass',
#         'Ovl', 'Park', 'Parks', 'Parkway', 'Parkways', 'Parkwy',
#         'Pass', 'Passage', 'Path', 'Paths', 'Pike', 'Pikes',
#         'Pine', 'Pines', 'Pkway', 'Pkwy', 'Pkwys', 'Pky',
#         'Pl', 'Place', 'Plain', 'Plains', 'Plaza', 'Pln',
#         'Plns', 'Plz', 'Plza', 'Pne', 'Pnes', 'Point',
#         'Points', 'Port', 'Ports', 'Pr', 'Prairie', 'Prk',
#         'Prr', 'Prt', 'Prts', 'Psge', 'Pt', 'Pts',
#         'Rad', 'Radial', 'Radiel', 'Radl', 'Ramp', 'Ranch',
#         'Ranches', 'Rapid', 'Rapids', 'Rd', 'Rdg', 'Rdge',
#         'Rdgs', 'Rds', 'Rest', 'Ridge', 'Ridges', 'Riv',
#         'River', 'Rivr', 'Rnch', 'Rnchs', 'Road', 'Roads',
#         'Route', 'Row', 'Rpd', 'Rpds', 'Rst', 'Rte',
#         'Rue', 'Run', 'Rvr','Se' , 'Shl', 'Shls', 'Shoal',
#         'Shoals', 'Shoar', 'Shoars', 'Shore', 'Shores', 'Shr',
#         'Shrs', 'Skwy', 'Skyway', 'Smt', 'Spg', 'Spgs',
#         'Spng', 'Spngs', 'Spring', 'Springs', 'Sprng', 'Sprngs',
#         'Spur', 'Spurs', 'Sq', 'Sqr', 'Sqre', 'Sqrs',
#         'Sqs', 'Squ', 'Square', 'Squares', 'St', 'Sta',
#         'Station', 'Statn', 'Stn', 'Str', 'Stra', 'Strav',
#         'Straven', 'Stravenue', 'Stravn', 'Stream', 'Street', 'Streets',
#         'Streme', 'Strm', 'Strt', 'Strvn', 'Strvnue', 'Sts',
#         'Sumit', 'Sumitt', 'Summit', 'Sw', 'Ter', 'Terr', 'Terrace',
#         'Throughway', 'Tpke', 'Trace', 'Traces', 'Track', 'Tracks',
#         'Trafficway', 'Trail', 'Trailer', 'Trails', 'Trak', 'Trce',
#         'Trfy', 'Trk', 'Trks', 'Trl', 'Trlr', 'Trlrs',
#         'Trls', 'Trnpk', 'Trwy', 'Tunel', 'Tunl', 'Tunls',
#         'Tunnel', 'Tunnels', 'Tunnl', 'Turnpike', 'Turnpk', 'Un',
#         'Underpass', 'Union', 'Unions', 'Uns', 'Upas', 'Valley',
#         'Valleys', 'Vally', 'Vdct', 'Via', 'Viadct', 'Viaduct',
#         'View', 'Views', 'Vill', 'Villag', 'Village', 'Villages',
#         'Ville', 'Villg', 'Villiage', 'Vis', 'Vist', 'Vista',
#         'Vl', 'Vlg', 'Vlgs', 'Vlly', 'Vly', 'Vlys',
#         'Vst', 'Vsta', 'Vw', 'Vws', 'Walk', 'Walks',
#         'Wall', 'Way', 'Ways', 'Well', 'Wells', 'Wl',
#         'Wls', 'Wy', 'Xing', 'Xrd', 'Xrds', 'NPD RANGE', 'PD', 'I', 'UNKNOWN', 'O-358', 'NE', 'SW', 'SE', 'TOP TIER TACTICAL, DEL CITY', 'UNIT 1201', '3550 W', '363 N', 'GOLDSBY']
#     street_type_pattern = r'\b(?:' + '|'.join(map(re.escape, street_type_list)) + r')\b'
#     start_pattern = r'\d{4}-\d{8}'
#     start_match = re.search(start_pattern, input_string)
#     street_address = ''
#     last_index = -1
#     if start_match:
#         start_index = start_match.end()
#         last_index = start_index
#         matches = list(re.finditer(rf'({street_type_pattern})', input_string[start_index:], flags=re.IGNORECASE))
#         # Check for special cases like <UNKNOWN>
#         special_pattern = r'<[^>]+>'
#         special_match = re.search(special_pattern, input_string[start_index:])
#         if special_match:
#             parsed_text = special_match.group()
#             street_address = parsed_text
#             last_index = start_index + special_match.end()
#         elif matches:
#             # Filter matches where all matched strings are in uppercase
#             uppercase_matches = [match for match in matches if match.group(1).isupper()]
#             # #finding the longest matched street address
#             # longest_match = max(matches, key=lambda m: m.end() - start_index)
#             # # Extract the substring from the starting pattern until the longest matched street type
#             # street_address = input_string[start_index:start_index + longest_match.start() + len(longest_match.group(1))].strip()
#             # last_index = longest_match.end() + start_index - 1
#             if uppercase_matches:
#                 # Find the longest matched street type among uppercase matches
#                 longest_match = max(uppercase_matches, key=lambda m: m.end() - start_index)

#                 # Extract the substring from the starting pattern until the longest matched street type
#                 parsed_text = input_string[start_index:start_index + longest_match.start() + len(longest_match.group(1))].strip()
#                 street_address = parsed_text
#                 # print("Parsed Text:", parsed_text)
#                 # print("Ending Index:", start_index + longest_match.start() + len(longest_match.group(1)))
#                 last_index = longest_match.end() + start_index - 1
#         else:
#             # Check for latitude and longitude coordinates
#             lat_lon_pattern = r'([-+]?\d*\.?\d+);([-+]?\d*\.?\d+)'
#             lat_lon_match = re.search(lat_lon_pattern, input_string[start_index:])
            
#             if lat_lon_match:
#                 parsed_text = lat_lon_match.group()
#                 street_address = parsed_text
#                 last_index = lat_lon_match.end()+start_index
#             else:
#                 # Check for special cases like <UNKNOWN>
#                 special_pattern = r'<[^>]+>'
#                 special_match = re.search(special_pattern, input_string[start_index:])
                
#                 if special_match:
#                     parsed_text = special_match.group()
#                     street_address = parsed_text
#                     last_index = start_index + special_match.end()
#     #             else:
#     #                 print("No street type, coordinates, or special cases found after the starting pattern.")
#     #                 print(input_string)
#     # if street_address=='' or last_index==-1:
#     #     print(input_string)
#     #     print('street address', street_address)
#     #     print('last index', last_index)
#     return street_address, last_index
    
def extract_address(input_string):
    address = ''
    incident_types = r"(Traffic Stop|Suspicious|Missing Person|Kidnapping|Assist EMS|Headache|Fire Fuel Spill|Fire Carbon Monoxide Alarm|COP Problem Solving|Officer in Danger|Assist Fire|Assault|Fire Transformer Blown|Fire Mutual Aid|Bar Check|Test Call|Animal Vicious|Back Pain|Fire Dumpster|Preg/Child Birth/Miscarriage|Welfare Check|Bomb/Threats/Package|Special Assignment|Prowler|Burns/Explosions|EMS Mutual Aid|Homicide|Stand By EMS|Loud Party|Molesting|Fire Residential|Cardiac Respritory Arrest|Body Reported|Animal Livestock|Traumatic Injury|Reckless Driving|Shooting Stabbing Penetrating|Carbon Mon/Inhalation/HazMat|Foot Patrol|Transfer/Interfacility|Animal Trapped|Choking|Burglary|COP Relationships|Unknown Problem/Man Down|Officer Needed Nature Unk|Barking Dog|Animal Bites/Attacks|Warrant Service|Contact a Subject|Disturbance/Domestic|Motorist Assist|Noise Complaint|Larceny|Trespassing|Unconscious/Fainting|Medical Call Pd Requested|Shots Heard|Alarm|Supplement Report|Convulsion/Seizure|MVA With Injuries|Overdose/Poisoning|Mutual Aid|Diabetic Problems|Heat/Cold Exposure|Breathing Problems|Public Assist|Runaway or Lost Child|Chest Pain|MVA Non Injury|Public Intoxication|Stroke|Open Door/Premises Check|Check Area|Vandalism|Animal Complaint|Animal Dead|Fire Alarm|Follow Up|Item Assignment|Animal Injured|Fraud|Pick Up Partner|Supplement Report|911 Call Nature Unknown|Falls|Escort/Transport|Animal at Large|Parking Problem|Abdominal Pains/Problems|Indecent Exposure|Animal Bite|Hit and Run|Stolen Vehicle|Sick Person|Harassment / Threats Report|Fire Grass|Assault EMS Needed|Alarm Holdup/Panic|Fight|Fire Smoke Investigation|Heart Problems/AICD|Fire Commercial|Fire Electrical Check|COP DDACTS|Fire Odor Investigation|Extra Patrol|Fire Controlled Burn|Civil Standby|Drunk Driver|Hemorrhage/Lacerations|Warrant Service|Debris in Roadway|Pick Up Items|Found Item|Stand By EMS|Stake Out|Unknown Problem/Man Down|Officer Needed Nature|Assist Police|Unk|Allergies/Envenomations|Road Rage|Fire Carbon Monoxide Alarm|Fire Water Rescue|Fire Down Power Line|Fire Gas Leak|Drowning/Diving/Scuba Accident|Cardiac Respiratory Arrest|Drug Violation|Loud Party)"
    pattern = rf"\d{{4}}-\d{{8}}\s+(.*?)\s+{incident_types}"
    match = re.search(pattern, input_string)
    if match:
        address = str(match.group(1))
        return address

def extract_number(input_string):
    '''Parses the incident number from the raw incident string'''
    incident_number_pattern = re.compile(r'(\d{4}-\d{8}\s)')
    match = re.search(incident_number_pattern, input_string)
    if match:
        incident_number = match.group(1).strip(' ')
    else:
        incident_number = None
    return incident_number

def extract_time(input_string):
    '''Parses the time when incident occurred from the raw incident string'''
    time_pattern = re.compile(r'\b(\d{1,2}:\d{2})\b')
    match = re.search(time_pattern, input_string)
    if match:
        incident_time = match.group(1)
    else:
        incident_time = None
    return incident_time