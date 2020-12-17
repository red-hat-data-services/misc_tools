#!/usr/bin/python3
import json
import argparse
import sys
import posixpath
import koji
import requests
from requests import Session

DESCRIPTION = """
Report the upstream repository and commit for a container build.
"""

def get_koji_pathinfo(profile):
    """
    Return a Koji PathInfo object for our profile.

    :param str profile: profile name, like "koji" or "cbs"
    :returns: koji.PathInfo
    """
    conf = koji.read_config(profile)
    top = conf['topurl']
    pathinfo = koji.PathInfo(topdir=top)
    return pathinfo

def get_resources_url(profile, build):
    """
    Return the URL to the remote-source.json and remote-source.tar.gz for this build.

    :param str profile: profile name, like "koji" or "cbs"
    :param dict build: Koji build information
    """
    pathinfo = get_koji_pathinfo(profile)
    builddir = pathinfo.build(build)
    return posixpath.join(builddir, 'files/remote-sources/remote-source.json')

def parse_args():
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('--profile', default='brew',
                        help="Koji profile (default 'brew'). Your Koji client profile"
                             " definitions are stored in /etc/koji.conf.d/*.conf.")
    parser.add_argument('nvrs', nargs='+',
                        help='Container build NVR(s) to report.')
    parser.add_argument('-q', default=False, action='store_true',
                        help='Do not print headers')
    args = parser.parse_args()

    return args

def display_title(nvr):
    """
    Print a title for this container NVR.

    :param dict nvr: Name-Version-Release data for this container.
    """
    title = '%(name)s-%(version)s-%(release)s' % nvr
    underline = '=' * len(title)
    print(title)
    print(underline)

def main():
    args = parse_args()
    nvrs = [koji.parse_NVR(nvr) for nvr in args.nvrs]
    rsession = Session()

    exit_code = 0
    
    for nvr in nvrs:
        if not args.q:
            display_title(nvr)
        rsjson = get_resources_url(args.profile, nvr)
        r = requests.get(rsjson)
        if r.status_code == 200:
            js = json.loads(r.content)
            print(js['repo'])
            print(js['ref'])
        elif args.q:
            print(r.status_code)
        else:
            print('Response code: %s, reason: %s' % (r.status_code, r.reason))

if __name__ == '__main__':
    main()
