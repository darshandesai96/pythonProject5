import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders
import os
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.base import MIMEBase
from Scripts.config.jobListRead import *
from Scripts.config.secretsData import *
from Scripts.config.secretsData import *
from datetime import datetime,date
import base64

def readFile():
    df = readFromPandas()
    dateFromLookFor = ''
    dateEndLookFor = ''
    date_format = "%Y-%m-%d"
    if startDate != '':
        dateFromLookFor = datetime.strptime(startDate,date_format)
    else:
        dateFromLookFor = date.today().strftime(date_format)
    
    if endDate != '':
        dateEndLookFor = datetime.strptime(endDate,date_format)
    else:
        dateEndLookFor = date.today().strftime(date_format)
    
    if dateCheck:
        filteredDf = df.loc[(df['Date'] >= dateFromLookFor) & (df['Date'] <= dateEndLookFor)]
    else:
        filteredDf = df.copy()

    return filteredDf

def formatIncludedFile():
    df = readFile()
    dfAlreadyMailed = readFromPandasMailed()
    col = ['JobId','Mail']

    df['COMBO'] = df[col].apply(lambda row: '@'.join(row.values.astype(str)), axis=1)
    dfAlreadyMailed['COMBO'] = dfAlreadyMailed[col].apply(lambda row: '@'.join(row.values.astype(str)), axis=1)
    dfAlreadyMailedDetails = df[~df['COMBO'].isin(dfAlreadyMailed[dfAlreadyMailed['isMailed'] == 'Y']['COMBO'])]
    return dfAlreadyMailedDetails

def main():
    finalDataFram = formatIncludedFile()

    for _, row in finalDataFram.iterrows():
        send_email(row['FirstName'], row['Company'], row['JobId'], linkedIn, github,
                   row['Mail'])



def send_email(firstName,company,jobId,linkedInId, gitId,mailId):
    message = MIMEMultipart()
    message['From'] = username
    message['To'] = mailId
    message['Subject'] = f"Interest in {jobId} at {company}"

    emailBody = body.format(
        recruiter_name=firstName,
        company_name=company,
        job_id=jobId,
        linkedin=linkedInId,
        github=gitId
    )

    message.attach(MIMEText(emailBody, 'plain'))
    creds = flow.run_local_server(port=0)
    service = build('gmail', 'v1', credentials=creds)

    try:
        with open(path_for_resume, "rb") as pdf_file:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(pdf_file.read())
            encoders.encode_base64(part)  # Encode the file in base64
            part.add_header(
                'Content-Disposition',
                f'attachment; filename={os.path.basename(path_for_resume)}'
            )
            message.attach(part)
    except Exception as e:
        print(f"Failed to attach file: {path_for_resume}. Error: {e}")

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    try:
        # with smtplib.SMTP_SSL('smtp.gmail.com', 587) as server:
        #     server.login(username, password)
        message = service.users().messages().send(userId="me", body={"raw": raw_message}).execute()
        # server.sendmail(username, mailId, message.as_string())
        print(f"Email sent to {mailId} {jobId}")
        # Log the success in the file
        log_email_status(firstName,company, mailId, "Success",jobId)
    except Exception as e:
        print(f"Failed to send email to {mailId}  {jobId}: {e}")
        # Log the failure in the file
        log_email_status(firstName, company, mailId, "Failed", jobId,str(e))


def log_email_status(recruiter_name, company_name, recipient_email, status, jobId,error_message=""):

    log_file = path_for_mailed
    date_format = "%Y-%m-%d"

    timestamp = date.today().strftime(date_format)

    if status != "Failed":
        status = "Y"
    else:
        status = "N"

    # Prepare log data
    log_data = {
        'Date': timestamp,
        'Company': company_name,
        'Mail': recipient_email,
        'JobId':jobId,
        'isMailed': status,
        'error_message': error_message
    }

    # If the log file doesn't exist, create it with headers
    if not os.path.exists(log_file):
        log_df = pd.DataFrame(columns=log_data.keys())
        log_df.to_csv(log_file, index=False)

    # Append the log data to the file
    log_df = pd.DataFrame([log_data])
    log_df.to_csv(log_file, mode='a', header=False, index=False)

if __name__ == "__main__":
    main()
