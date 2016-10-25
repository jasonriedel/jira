#!/bin/bash 

echo -n "Jira Password: "
read -s JIRA_PASSWORD
echo ""
export JIRA_PASS=$JIRA_PASSWORD
