#!/usr/bin/env bash

# bind pip to Python 3
alias pip=pip3

#  installation options
# a) default
# pip install .
#
# b) development mode
# pip install -e .
#
# c) from VCS
# pip install -e git+https://github.com/micutio/ComplexAutomatonBase.git
#
# uninstallation
# pip uninstall ComplexAutomatonBase

print_options() {
    echo usage: $0 [-h, --help, -dev, -rm, -vcs]
    echo -e "\t -h or --help - print options to standard output and exit"
    echo -e "\t -dev         - install CAB in development mode"
    echo -e "\t -vcs         - install CAB directly from github"
    echo -e "\t -rm          - uninstall CAB"
}

# true => install, false => uninstall
INSTALL=true
OPT_DEV=""
TARGET="."

for i in $*
do
    case $i in
        "-rm")
            INSTALL=false
            ;;
        "-dev")
            OPT_DEV="-e"
            ;;
        "-vcs")
            TARGET="git+https://github.com/micutio/ComplexAutomatonBase.git"
            ;;
        "-h")
            print_options
            exit 0
            ;;
    esac
done

if [ "$INSTALL" = "true" ]
then
    pip install -r requirements.txt
    pip install $OPT_DEV $TARGET
else
    pip uninstall -r requirements.txt
    pip uninstall ComplexAutomatonBase
fi