# Call perl script and execute it.
import subprocess, sys

perl = "/usr/bin/perl"
perl_script = "geo.pl";
params = "--mount-doom-hot"
pl_script = subprocess.Popen([perl, perl_script, params], stdout=sys.stdout)
pl_script.communicate()

# Use the perl output as input. 

import re

# Delete
del_list = ['>','title', 'taxon','PDAT','<','Type="String"','Item Name=','/Item','"','</Item>','<DocSum>','<Item Name=','DocSum','Accession']
# Lines with
words = ['"Accession" Type="String">GSE','<Item Name="title" Type="String">','taxon','<Item Name="PDAT" Type="String">']

rep = re.compile(r'|'.join(del_list))
keep = re.compile(r"|".join(words))
r3 = re.compile("GSE(?=\d)")

with open("geo.txt") as f, open("email_data.txt","w") as out:
    for line in f:
         # if line contains match from words
        if keep.search(line):
            # replace all unwanted substrings
            line = rep.sub("", line.lstrip())
            line = r3.sub("\n"'http://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE', line)  # Change Accesion number to Accession hyperlink.
            out.write(line)

# Email
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

fromaddr = "geo.weekly.analysis@gmail.com" # sender email
toaddr = ""           # receiver email
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "GEO Data Sets - Supported platforms"

# To send send txt file in email body.
f1 = (open("email_data.txt",'rU'))
geo = MIMEText(f1.read(),'plain') 
f1.close()
msg.attach(geo)

# Convert to string.
import smtplib
server = smtplib.SMTP('smtp.gmail.com', 587)
server.ehlo()
server.starttls()
server.ehlo()
server.login("geo.weekly.analysis", "password")
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
