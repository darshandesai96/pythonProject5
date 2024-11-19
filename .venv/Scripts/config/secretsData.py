from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

username = 'ashutoshshinde59@gmail.com'

SCOPES = [
        "https://www.googleapis.com/auth/gmail.send"
    ]
path_cred = 'C:/Users/darsh/PycharmProjects/pythonProject5/.venv/Scripts/config/credentials.json'

flow = InstalledAppFlow.from_client_secrets_file(
            path_cred, SCOPES)

path_for_resume = 'C:/Users/darsh/PycharmProjects/pythonProject5/.venv/Scripts/resume/Resume_of_Darshan_Desai_SDE_updated.pdf'
path_for_excel = 'C:/Users/darsh/PycharmProjects/pythonProject5/.venv/Scripts/jobList/jobmaillist.csv'
path_for_mailed = 'C:/Users/darsh/PycharmProjects/pythonProject5/.venv/Scripts/jobList/mailedList.csv'
path_for_log = 'C:/Users/darsh/PycharmProjects/pythonProject5/.venv/Scripts/jobList/'

startDate = ''
endDate = ''
fileCheck = True
dateCheck = True

linkedIn = 'https://www.linkedin.com/in/darshan-desai07/'
github = 'https://github.com/darshandesai96'

body = """
Hi {recruiter_name},

I hope this email finds you well. I’m reaching out to express my interest in potential software development opportunities at {company_name}. With over four years of experience in designing and implementing scalable software solutions, I am confident in my ability to contribute to your team and help drive innovative projects.

In my career, I have developed expertise in Java, Python, full-stack development, and advanced database management. I’ve successfully crafted RESTful APIs, optimized application performance using multithreading, and implemented Redis-backed caching systems, achieving up to a 40% reduction in latency. Additionally, I have hands-on experience with frameworks like Spring Boot, Angular, Django, and Kubernetes, which has helped me deliver robust, high-performing applications.

I came across the recent job posting for a {job_id} position at {company_name}. The role aligns perfectly with my skills and career aspirations, and I’m eager to contribute my expertise to {company_name}'s innovative projects.

I’ve attached my resume for your review. I would appreciate the opportunity to discuss how my background can add value to your team. Thank you for your time, and I look forward to hearing from you.

Best regards,  
Darshan Desai  
{linkedin} | {github}
"""