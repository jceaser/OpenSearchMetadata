#!/bin/bash

# a simple script to post test data to the servlet

MVN=$(which mvn)
CURL=$(which curl)
if [ -a /home-nfs/bin/curl ]; then
    CURL=/home-nfs/bin/curl
fi

XML="application/xml"
CSV="text/plain"
JSON="application/json"
PDF="application/pdf"
BASIC="text/xml;charset=UTF-8"

portal="cwic"
format="${XML}"        #"text/plain" # "application/pdf"
client="GCMD-Client"

URL_OSD="http://gcmd.nasa.gov/KeywordSearch/default/openSearch.jsp" #?Portal=foo&clientId=foo

#mark - defaults
host=${URL_OSD}

function help()
{
    printf "Conduct an OpenSearch query on the GCMD web site"
    printf "Usage: cmd -V -P -h <host> -p <port> -r <rules> file\n"
    printf "%12s : %s\n" "-h" "host name, defaults to ${host}"
    printf "%12s : %s\n" "-p" "port, defaults to \"${port}\""
    printf "%12s : %s\n" "-f" "sets format: '${PDF}', '${CSV}', '${JSON}', '${PDF}'"
    printf "%12s : %s\n" "-r" "sets rules to run"
    printf "%12s : %s\n" "-s" "service name - defaults to ${service}"
    printf "%12s : %s\n" "-u" "user name - no default"
    printf "%12s : %s\n" "file" "file to POST"
    
    exit -1
}

if [ "$#" -eq 0 ]; then
    help
fi

while getopts "e:h:v?adcg" opt ; do
    case ${opt} in
        h) host=${OPTARG} ;;
        p) portal=${OPTARG} ;;
        v) verbose="echo -e" ;;
        g) ;;
        \?) manual ; exit ;;
        *) manual ; exit
    esac
done

#mark - Get OSD

${verbose} ${CURL} \
    --user-agent "${client}" \
    -H "Accept: ${format}" \
    "${host}?portal=${portal}&clientId=${client}" > /tmp/osd.xml

#mark - parse OSD

url=$(cat /tmp/osd.xml \
    | xmllint --xpath \
    "string(/*[name()='OpenSearchDescription']/*[name()='Url'][@type='application/atom+xml']/@template)" \
    -)

echo
echo ${url}
echo

#cat /tmp/list.txt | python2.7 open.py
ret=$(cat /tmp/osd.xml | python2.7 open.py)

type=$(echo "${ret}" | awk '{print $1}')
url=$(echo "${ret}" | awk '{print $2}')

${CURL} --user-agent "${client}" \
    -H "Content-Type: ${type}" \
    "${url}" > /tmp/open.xml

export TCLLIBPATH=/System/Library/Tcl/8.5/tdom0.8.3/
wish display2.wish /tmp/open.xml

#less /tmp/open.xml

echo end