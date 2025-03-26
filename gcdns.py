import os
from googleapiclient import discovery
from googleapiclient import http
import argparse


def dns_record_create(project_id, managed_zone, ip, dns_name, record_type, ttl):
    service = discovery.build('dns', 'v1')
    dns_record_body = {
        'kind': 'dns#resourceRecordSet',
        'name': f'{dns_name}.',
        'rrdatas': [f'{ip}'],
        'ttl': f'{ttl}',
        'type': f'{record_type}'
    }
    request = service.resourceRecordSets().create(project=project_id,
                                                  managedZone=managed_zone,
                                                  body=dns_record_body)
    try:
        response = request.execute()
    except http.HttpError as e:
        print('Error response status code : {0}, reason : {1}'.format(e.status_code, e.error_details))
        exit(1)


def dns_record_delete(project_id, managed_zone, dns_name, record_type):
    service = discovery.build('dns', 'v1')
    request = service.resourceRecordSets().delete(project=project_id,
                                                  managedZone=managed_zone,
                                                  name=f'{dns_name}.',
                                                  type=f'{record_type}')
    try:
        response = request.execute()
    except http.HttpError as e:
        print('Error response status code : {0}, reason : {1}'.format(e.status_code, e.error_details))
        exit(1)


def dns_record_edit(project_id, managed_zone, ip, dns_name):

    ttl = 300
    record_type = "A"
    service = discovery.build('dns', 'v1')
    dns_record_body = {
        'kind': 'dns#resourceRecordSet',
        'name': f'{dns_name}',
        'rrdatas': [f'{ip}'],
        'ttl': f'{ttl}',
        'type': f'{record_type}'
    }
    request = service.resourceRecordSets().patch(project=project_id,
                                                 managedZone=managed_zone,
                                                 name=dns_name,
                                                 type=record_type,
                                                 body=dns_record_body)
    try:
        response = request.execute()
        print("The record was updated!")
    except http.HttpError as e:
        if e.status_code == 409:
            print('The DNS record {0}!'.format(e.error_details[0]['reason']))
        else:
            print('Error response status code : {0}, reason : {1}'.format(e.status_code, e.error_details))
            exit(1)


def parse_arguments():
    parser = argparse.ArgumentParser(description='Manage DNS records in Google Cloud DNS')
    parser.add_argument('--action', type=str, help='Action to perform: create, delete or edit')
    parser.add_argument('--project_id', type=str, help='Google Cloud project ID')
    parser.add_argument('--zone', type=str, help='DNS zone name')
    parser.add_argument('--dns_name', type=str, help='The name of the DNS record do not forget . at the end of the url!')
    parser.add_argument('--r_type', type=str, help='Type of DNS record (e.g., A, CNAME)')
    parser.add_argument('--ttl', type=int, default=300, help='TTL for the DNS record')
    parser.add_argument('--ip', type=str, help='Data for the DNS record')
    parser.add_argument('--key', type=str, help='json key file path')

    return parser.parse_args()


def main():
    args = parse_arguments()
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = args.key
    project = args.project_id
    zone = args.zone
    action = args.action
    if action == 'create':
        print("Creating a record...")
        dns_record_create(project, zone, args.ip, args.dns_name, args.r_type, args.ttl)
    elif action == 'delete':
        print("Deleting a record...")
        dns_record_delete(project, zone, args.dns_name, args.r_type)
    elif action == 'edit':
        print("Editing a record...")
        dns_record_edit(project, zone, args.ip, args.dns_name)

    print("Done!")
    exit(0)


if __name__ == '__main__':
    main()

