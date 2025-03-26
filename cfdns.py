from cloudflare import Cloudflare
import argparse


def cloudflare_dns_record_edit(record_name, zone_name, token, ip):
    cf = Cloudflare(api_token=token)
    get_zone_info = cf.zones.list(extra_query={'name': zone_name})
    zone_info = get_zone_info.to_dict()
    zone_id = zone_info['result'][0]['id']
    if zone_id is None:
        exit("CLOUDFLARE_ZONE_ID is not defined")
    get_record_info = cf.dns.records.list(zone_id=zone_id, extra_query={'name': record_name})
    record_info = get_record_info.to_dict()
    record_id = record_info['result'][0]['id']
    if record_id is None:
        exit("DNS_RECORD_ID is not defined")
    cf.dns.records.update(
        zone_id=zone_id,
        type="A",
        dns_record_id=record_id,
        name=record_name,
        content=ip,
        proxied=True
    )
    
    
def cloudflare_dns_record_delete(record_name, zone_name, token):
    cf = Cloudflare(api_token=token)
    get_zone_info = cf.zones.list(extra_query={'name': zone_name})
    zone_info = get_zone_info.to_dict()
    zone_id = zone_info['result'][0]['id']
    if zone_id is None:
        exit("CLOUDFLARE_ZONE_ID is not defined")
    get_record_info = cf.dns.records.list(zone_id=zone_id, extra_query={'name': record_name})
    record_info = get_record_info.to_dict()
    record_id = record_info['result'][0]['id']
    if record_id is None:
        exit("DNS_RECORD_ID is not defined")

    cf.dns.records.delete(
        zone_id=zone_id,
        dns_record_id=record_id
    )


def cloudflare_dns_record_create(zone_name, record_name, ip, token):
    cf = Cloudflare(api_token=token)
    get_zone_info = cf.zones.list(extra_query={'name': zone_name})
    zone_info = get_zone_info.to_dict()
    zone_id = zone_info['result'][0]['id']
    if zone_id is None:
        exit("CLOUDFLARE_ZONE_ID is not defined")
    cf.dns.records.create(
        zone_id=zone_id,
        type="A",
        name=record_name,
        content=ip,
        proxied=True
    )


def parse_arguments():
    parser = argparse.ArgumentParser(description='Manage DNS records in CF')
    parser.add_argument('--action', type=str, help='create/delete/edit')
    parser.add_argument('--zone_name', type=str, help='domain name')
    parser.add_argument('--record_name', type=str, help='url')
    parser.add_argument('--ip', type=str, help='ip for the record')
    parser.add_argument('--token', type=str, help='credentials')

    return parser.parse_args()


def main():
    args = parse_arguments()
    action = args.action
    domain = args.zone_name
    url = args.record_name
    ip = args.ip
    credentials = args.token
    if action == 'create':
        print("Creating a record {s} ...".format(s=url))
        cloudflare_dns_record_create(domain, url, ip, credentials)
    elif action == 'delete':
        print("Deleting a record {s} ...".format(s=url))
        cloudflare_dns_record_delete(url, domain, credentials)
    elif action == 'edit':
        print("Editing a record...".format(s=url))
        cloudflare_dns_record_edit(url, domain, credentials, ip)
    else:
        print("FACK!")
        exit(1)
    
    print("Done!")
    exit(0)


if __name__ == '__main__':
    main()
    

