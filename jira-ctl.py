#!/usr/bin/env python

from jira.client import JIRA
import os, sys
import prettytable
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-lp', '--list-projects', action="store_true", dest="list_projects", required=False, help="List all projects")
parser.add_argument('-li', '--list-issues', action="store", dest="list_project_issues", required=False, help="List Issues for a specific project")
parser.add_argument('-ua', '--update-assignee', action="store", dest="update_assignee", required=False, help="Update an issues assignee format: <issue number>,<first_last>")
parser.add_argument('-ud', '--update-date', action="store", dest="update_date", required=False, help="Update an issues due date format: <issue number>,<yyyy-mm-dd>")
parser.add_argument('-usts', '--update-status', action="store", dest="update_status", required=False, help="Update an issues status format: <issue number>,'<Open|In Progress|Resolved>'")
parser.add_argument('-usum', '--update-summary', action="store", dest="update_summary", required=False, help="Update an issues summary format: <issue number>,'<summary>'")
args = parser.parse_args()

def get_pass():
    if os.environ.get('JIRA_PASS') == None:
        print "you must first export your JIRA_PASS in the shell by running: source getpass.sh"
        print 'or "export JIRA_PASS=<corp_ad_pass>'
        sys.exit()
    jira_password = str(os.environ['JIRA_PASS'])

    return jira_password

def connect_jira(jira_server, jira_user, jira_password):
    '''
    Connect to JIRA. Return None on error
    '''
    try:
        #print "Connecting to JIRA: %s" % jira_server
        jira_options = {'server': jira_server}
        jira = JIRA(options=jira_options,
                    # Note the tuple
                    basic_auth=(jira_user,
                                jira_password))
        return jira
    except Exception,e:
        print "Failed to connect to JIRA: %s" % e
        return None

def list_projects():
    projects = jira.projects()
    header = ["Projects"]
    table = prettytable.PrettyTable(header)
    for project in projects:
        row = [str(project)]
        table.add_row(row)
    print table

def list_project_issues(project):
    query = 'project = %s and status != Resolved order by due asc' % (project)
    #query = 'project = %s and status != Resolved order by due desc' % (project)
    #query = 'project = %s order by due desc' % (project)
    issues = jira.search_issues(query, maxResults=100)

    if issues:
        header = ["Ticket", "Summary", "Assignee", "Status", "Due Date"]
        table = prettytable.PrettyTable(header)

        for issue in issues:
                summary = issue.fields.summary
                st = str(issue.fields.status)
                dd = issue.fields.duedate
                assignee = issue.fields.assignee
                row = [issue, summary, assignee, st, dd]
                table.add_row(row)
        print table

def update_issue_assignee(issue_number, assignee):
    issue = jira.issue(issue_number)
    issue.update(assignee=assignee)
    print "updated %s with new Assignee: %s" % (issue_number, assignee)

def update_issue_duedate(issue_number, dd):
    issue = jira.issue(issue_number)
    issue.update(duedate=dd)
    print "updated %s with new Due Date: %s" % (issue_number, dd)

def update_issue_summary(issue_number, summary):
    issue = jira.issue(issue_number)
    issue.update(summary=summary)
    print "updated %s with new Summary: %s" % (issue_number, summary)

def update_issue_status(issue_number, status):
    # To figure out transitions view the following URL
    # https://jira.yourcompany.com/rest/api/2/issue/XXXXXX-22/transitions?expand=transitions.fields

    transitions = {
                    'Resolved': 11,
                    'Open': 41,
                    'In Progress': 21,
                    'Testing': 71,
                    'Transition': 81,
                    'Closed': 91,
    }

    issue = jira.issue(issue_number)
    jira.transition_issue(issue, transitions[status])
    print "updated %s with new Status: %s" % (issue_number, status)

if __name__ == "__main__":
    if not args:
        parser.print_help()
    else:
        jira_user = '<your_login>'
        jira_password = get_pass()
        jira_server = 'https://jira.yourcompany.com'

        jira = connect_jira(jira_server, jira_user, jira_password)

        if args.list_projects:
            list_projects()
        elif args.list_project_issues:
            project = args.list_project_issues
            list_project_issues(project)
        elif args.update_assignee:
            (issue_number, assignee) = args.update_assignee.split(',')
            update_issue_assignee(issue_number, assignee)
        elif args.update_date:
            (issue_number, dd) = args.update_date.split(',')
            update_issue_duedate(issue_number, dd)
        elif args.update_status:
            (issue_number, status) = args.update_status.split(',')
            update_issue_status(issue_number, status)
        elif args.update_summary:
            (issue_number, summary) = args.update_summary.split(',')
            update_issue_summary(issue_number, summary)
        else:
            parser.print_help()
