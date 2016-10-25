```bash
(env) ➜  jira git:(master) ✗ ./jira-ctl.py
usage: jira-ctl.py [-h] [-lp] [-li LIST_PROJECT_ISSUES] [-ua UPDATE_ASSIGNEE]
                   [-ud UPDATE_DATE] [-usts UPDATE_STATUS]
                   [-usum UPDATE_SUMMARY]

optional arguments:
  -h, --help            show this help message and exit
  -lp, --list-projects  List all projects
  -li LIST_PROJECT_ISSUES, --list-issues LIST_PROJECT_ISSUES
                        List Issues for a specific project
  -ua UPDATE_ASSIGNEE, --update-assignee UPDATE_ASSIGNEE
                        Update an issues assignee format: <issue
                        number>,<first_last>
  -ud UPDATE_DATE, --update-date UPDATE_DATE
                        Update an issues due date format: <issue number
                        >,<yyyy-mm-dd>
  -usts UPDATE_STATUS, --update-status UPDATE_STATUS
                        Update an issues status format: <issue
                        number>,'<Open|In Progress|Resolved>'
  -usum UPDATE_SUMMARY, --update-summary UPDATE_SUMMARY
                        Update an issues summary format: <issue
                        number>,'<summary>'
(env) ➜  jira git:(master) ✗
```
