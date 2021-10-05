#!/usr/bin/env python3

import argparse
import sys
from requests import Request, Session
import requests
import re

def generic_request(url:str, as_json:bool=True, call='GET', data:{}=None, files:{}=None):

    s = Session()

    if as_json and data is not None:
        req = Request(call,  url, json=data, files=files)
    else:
        req = Request(call,  url, data=data, files=files)

    prepped = s.prepare_request(req)

    r = s.send(prepped)
    r.raise_for_status()


    if as_json and r.text:
        return json.loads( r.text )
    else:
        return r.text


def main():
    parser = argparse.ArgumentParser(description='get_cellranger: download cellranger as it is EULA protected!')
    parser.add_argument('-o', '--outfile', default=None, help="output file, default is what is provided by website")
    parser.add_argument('-v', '--version', default=None, help="default is latest")

    args = parser.parse_args()

    data = {'email': 'kim.brugger@uib.no',
            'first_name': 'Kim',
            'last_name': 'Brugger',
            'company': 'University of Bergen',
            'country': 'Norway',
            'agreed': True}


    r = generic_request("https://support.10xgenomics.com/single-cell-gene-expression/software/downloads/latest", call='POST', data=data, as_json=False)
    g = re.search(r'curl -o\</span\> (.*?)\</div', r, re.MULTILINE)

    if g is None:
        print("Cannot find URL!")
        sys.exit( 10 )

    download_link = g.groups( 1 )[0]
    if args.version is not None:
        print( f"diff version {args.version}")
        download_link = re.sub(r'-(.*?).tar.gz', f'-{args.version}.tar.gz', download_link)


#    print( download_link)

    filename, uri = download_link.split( " ")
    uri = uri.replace('"','')
    uri = uri.replace('&amp;','&')



    print( filename, uri)
    if args.outfile is not None:
        filename = args.outfile

    r = requests.get(uri)  
    with open(filename, 'wb') as f:
        f.write(r.content)
    f.close()



if __name__ == "__main__":
    main()

