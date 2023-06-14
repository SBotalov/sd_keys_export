from jira import JIRA
import openpyxl
import os
import sd_uat_01_creds as creds
import time

#connecting to Jira
jiraOptions = {'server' : creds.url
               }
jira = JIRA(server=jiraOptions, token_auth=creds.api_token)

os.chdir('C:\Botalov\Py\\approvals')
if os.path.isfile('approvals.xlsx'): #checking if the approvals.xlsx exists 
    os.unlink('approvals.xlsx') # delete the file
    print('The old one approvals.xlsx is deleted.')

wb = openpyxl.Workbook() #creating Excel object
sheet = wb.get_sheet_by_name('Sheet') # sheet object
sheet['A1'] = 'Parent'
sheet['B1'] = 'Approval'
cell = 2

print('Searhing for issues..')
start_time = time.time() # loop start time
for singleIssue in jira.search_issues(jql_str='project = SD and issueFunction in parentsOf("issueType = Approval")', maxResults=10000): #searching for parent tasks
    parent_id = singleIssue.key    
    approval_ids = jira.search_issues(jql_str='parent = %s and issuetype = Approval' % parent_id) #searching for approval sub-tasks
    for approval_issue in approval_ids:
        cell_id = 'B' + str(cell) #cell id for approval sub-task
        cell_index = 'A' + str(cell) # cell id for parent issue
        sheet[cell_index] = parent_id
        sheet[cell_id] = approval_issue.key
        cell += 1

end_time = time.time() # loop end time
print('Done')
elapsed_time = end_time - start_time # loop elapsed time
print('Elapsed time: ', elapsed_time)

wb.save('approvals.xlsx') # save .xlsx
