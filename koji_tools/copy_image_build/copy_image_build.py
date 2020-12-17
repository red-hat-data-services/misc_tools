#!/usr/bin/python3

import argparse
import koji
from subprocess import check_call
import sys

def check_build(build):
    try:
        build['extra']['image']
    except:
        return False
    return True

def get_source_image(build):
    # Find the sha256 pullspec and return that as our source image
    pullspecs = build['extra']['image']['index']['pull']
    for pullspec in pullspecs:
        if '@sha256' in pullspec:
            return pullspec

def get_latest_build(session, tag, package):
    latestBuilds = session.getLatestBuilds(tag=tag, package=package)
    assert len(latestBuilds), "No builds found for package %s in tag %s" % (package, tag)

    # There should be only 1 build since we asked for a specific package in a latest build
    # Use the NVR to get detailed information
    return session.getBuild(latestBuilds[0]["nvr"])
        
def get_koji_session(profile):
    mykoji = koji.get_profile_module(profile)
    opts = mykoji.grab_session_options(mykoji.config)
    return mykoji.ClientSession(mykoji.config.server, opts)

def get_tag_list(build):
    # Return all the tags that OSBS produces
    # If the specified tag lists are empty just return the NVR
    tags = []
    for tag_list in ['unique_tags', 'floating_tags', 'tags']:
        if tag_list in build['extra']['image']['index']:
            tags += build['extra']['image']['index'][tag_list]
    if not tags:
        print("Expected tags not found in the build, using the nvr instead")
        tags = [build["nvr"]]
    return tags

def push_with_buildah(source_image, registry, user, package, tags):
    # Pull the source image
    cmd = ['buildah', 'pull', source_image]
    check_call(cmd)

    # Tag the source image and push for all known tags
    buildah_dest = '{registry}/{reg_user}/{package}:{tag}'    
    for tag in tags:
        destination = buildah_dest.format(registry=registry, reg_user=user, package=package, tag=tag)
        cmd = ['buildah', 'tag', source_image, destination]
        check_call(cmd)

        cmd = ['buildah', 'push', destination]
        print(cmd)
        check_call(cmd)

def copy_with_skopeo(source_image, registry, user, package, tags):        
    # TODO: authenticate skopeo to the destination registry for copying.
    # Run "skopeo login ... " see https://bugzilla.redhat.com/1800815
    skopeo_dest = 'docker://{registry}/{reg_user}/{package}:{tag}'
    for tag in tags:
        destination = skopeo_dest.format(registry=registry, reg_user=user, package=package, tag=tag)
        source = 'docker://' + source_image
        cmd = ['skopeo', 'copy', source, destination]
        print(cmd)
        check_call(cmd)
        
def main(tag, package, user, profile='brew', registry='quay.io', buildah=False):
    session = get_koji_session(profile)
    build = get_latest_build(session, tag, package)
    assert check_build(build), "This build does not appear to be an image build"
    
    source_image = get_source_image(build)
    assert source_image, "Failed to find sha256 pullspec in the build to use as a source"
 
    tags = get_tag_list(build)
    if args.buildah:
        push_with_buildah(source_image, registry, user, package, tags)
    else:
        copy_with_skopeo(source_image, registry, user, package, tags)
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Copy images from the latest koji container build of a given package in a given tag to an image registry")
    parser.add_argument('tag',
                        help="the buildsystem tag that includes the desired package")
    parser.add_argument('package',
                        help="the name of the desired package")
    parser.add_argument('reg_user', metavar='registry_user',
                        help="the registry user account which will hold the images. The repository name will match the package name.")
    parser.add_argument('-p', '--profile', dest='profile', default='brew',
                        help="the koji profile to use for connecting to the build system (default: 'brew')")
    parser.add_argument('-r', '--registry', dest='registry', default='quay.io',
                        help="the name of the image registry to use (default: 'quay.io')")
    parser.add_argument('-b', '--buildah', dest='buildah', default=False, action='store_true',
                        help="use buildah to pull images and push them instead of skopeo copy (the default)")
    args = parser.parse_args()
    main(args.tag, args.package, args.reg_user, args.profile, args.registry, args.buildah)
