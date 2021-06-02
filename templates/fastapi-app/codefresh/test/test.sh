#!/bin/bash

# Run some tests. This script is intended to be run from a Geodesic environment-specific tool Docker image
# with this repo code mounted as a volume. Therefore, you cannot use absolute file paths to reference files here.


# Use set -x to echo the commands as they are executed. Very helpful for understanding
# what is causing a failure.
set -x

# If you want to fail fast, or if the failure of an early part of the script could
# cause a false positive due to the success of a later part of the script,
# then you can use
# set -e
# to cause the script to exit immediately if a command exits with an error.
# However, this can backfire by causing the script to fail due to
# transient errors that can happen while the environment is initializing.


# If you are using a Unix pipe, you probably want to set pipefail
# or else the failure of the first part of the pipe would be masked by the
# success of the second part, even with `set -e`. For example,
#   curl -f foo | grep bar
# will always succeed without "pipefail".
# However, in this test, early failures are OK.
#
# set -o pipefail

# Simple sanity check that we loaded our environment properly
#echo EXAMPLE_ENV is "\"$EXAMPLE_ENV\""

#######
### If you are running a test harness that has the right version of python and
### all the libraries you need, then you could try waiting for the database
### to start. Our example test harness does not have the necessary requirements
### to run this.
## Wait for the database to start. Not strictly necessary, but
## useful for distinguishing failure of the environment from
## failure of the app. Use a distinctive exit code for easier diagnosis.
#python wait_for_postgres.py || exit 111
#######

# Athough curl has a built-in retry mechanism, it gives up on serious errors
# like not being able to find the host or hostname, so we loop anyway.

# From here on, we are explicitly echoing enough information that the automatic echo is unhelpful
set +x

for i in {1..12}; do
  sleep 5
  echo "$(date -u --rfc-3339=seconds): Starting health check attempt #$i:"
  curl -sf  http://<REPO_NAME>/health-check/
  curl_exit=$?
  echo "$(date -u --rfc-3339=seconds): Health check attempt #$i: status $curl_exit"
  (($curl_exit == 0)) && echo "Success!" && exit 0
done

exit 101
