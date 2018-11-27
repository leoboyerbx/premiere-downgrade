#!/bin/bash -l
#$ -S /bin/bash

version=$1
if test "$2" = "-of"; then
	onefile="--onefile"
	isof="Yes"
else
	onefile=""
	isof="No"
fi

cat << END
Building with pytinstaller
Parameters:
Version: $version
Build only one file: $isof

Program will be compiled to dist/ folder.
END
pyinstaller converter.py --noconsole -n PremiereDowngrade-v${version} ${onefile} --icon=icon.ico
