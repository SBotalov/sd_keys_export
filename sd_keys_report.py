from jira import JIRA
import openpyxl
import os
import sd_uat_01_creds as creds

#connecting to Jira
jiraOptions = {'server' : creds.url
               }
jira = JIRA(server=jiraOptions, token_auth=creds.api_token)

os.chdir('C:\Botalov\Py\\approvals')
if os.path.isfile('approvals.xlsx'): #checking if the approvals.xlsx exists and deleting
    os.unlink('approvals.xlsx')

wb = openpyxl.Workbook() #creating Excel object
sheet = wb.get_sheet_by_name('Sheet') # sheet object
sheet['A1'] = 'Parent'
sheet['B1'] = 'Approval'
cell = 2

print('Searhing for issues..')
for singleIssue in jira.search_issues(jql_str='project = SD and issueFunction in parentsOf("issueType = Approval")', maxResults=0):
    parent_id = singleIssue.key    
    approval_ids = jira.search_issues(jql_str='parent = %s and issuetype = Approval' % parent_id)
    if len(approval_ids) > 0:
        for approval_issue in approval_ids:
            cell_id = 'B' + str(cell) #cell id for approval sub-task
            cell_index = 'A' + str(cell) # cell id for parent issue
            sheet[cell_index] = parent_id
            sheet[cell_id] = approval_issue.key
            cell += 1
print('Done')

wb.save('approvals.xlsx')
