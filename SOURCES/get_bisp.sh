#!/bin/bash

#
# Simple script that downloads the BISP tar archive from bankid.com
#

function print_usage() {
	echo "Usage: `basename $0` [<version>]"
	echo ""
	echo "Download bisp from bankid.com. If <version> is specified, download"
	echo "the specific version. Otherwise download the latest."
	echo ""
	echo "The file will be downloaded to the current directory."
	echo ""
}

if [ $# -eq 1 ] && [ "$1" == "--help" -o "$1" == "-h" -o "$1" == "-?" ] ; then
	print_usage
	exit 1
fi


if [ $# -gt 0 ] ; then
	VERSION="$1"
	echo "Downloading BISP version ${VERSION}..."
	wget -nc --content-disposition https://install.bankid.com/Repository/BISP-${VERSION}.tar.gz
	RET=$?
else
	VERSION=""
	echo "Downloading the latest version of BISP..."
	wget -nc --content-disposition https://install.bankid.com/Download?defaultFileId=Linux
	RET=$?
fi

if [ ${RET} -eq 0 ] ; then
	echo "Download succeeded."
	exit 0
else
	echo "Download failed."
	exit 1
fi

