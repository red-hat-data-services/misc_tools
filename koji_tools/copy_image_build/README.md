# Copy images from lastest koji container build by tag and package

This script will lookup the lastest build for a particular package associated with a particular
tag in a koji build system (which can be specified with the 'profile' option).

If the build is a container build, it will copy all of the image tags reported by OSBS to
the designated image repository. Either skopeo or buildah can be used for the transfer.

# Links

https://koji.fedoraproject.org/koji/api

https://docs.pagure.org/koji/writing_koji_code/


# Special thanks

Thanks to Ken Dreyer at Red Hat for providing examples on how to do this!
