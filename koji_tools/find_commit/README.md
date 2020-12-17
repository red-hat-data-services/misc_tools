# Report the source url and commit for container build(s) by nvr 

This script will lookup a container build by nvr and report the
remote source url and commit that was used for the build. It
does this by downloading the remote-source.json from the build
system and displaying the 'repo' and 'ref' fields.

This is a quick way to link a container build to upstream sources
to aid debugging, traceability, etc.

# Links

https://koji.fedoraproject.org/koji/api

https://docs.pagure.org/koji/writing_koji_code/

# Based on

https://pagure.io/fork/ktdreyer/koji-tools
