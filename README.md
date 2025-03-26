# simple_dns_tools
This repository contains tools written on Python to manage DNS records in Cloud Flare or Google Cloud. 
The basic options are create, delete, or edit of A type records.

Do not forget to install the correct Python libraries from the requirements file

Example for cfdns:
some/python cfdns.py --action create --zone_name my_domain.tld --record_name example.my_domain.tld --ip 1.2.3.4 --token my_token 
some/python cfdns.py --action delete --zone_name my_domain.tld --record_name example.my_domain.tld --token my_token 
some/python cfdns.py --action edit --zone_name my_domain.tld --record_name example.my_domain.tld --ip 1.2.3.5 --token my_token 

Example for gcdns:
some/python gcdns.py --action create --project_id my_project_id --zone zone-name --dns_name example.my_domain.tld. --r_type A --ttl 300 --ip 1.2.3.4 --key some/path/google_key.json
some/python gcdns.py --action delete --project_id my_project_id --zone zone-name --dns_name example.my_domain.tld. --key some/path/google_key.json
some/python gcdns.py --action edit --project_id my_project_id --zone zone-name --dns_name example.my_domain.tld. --r_type A --ttl 300 --ip 1.2.3.5 --key some/path/google_key.json
