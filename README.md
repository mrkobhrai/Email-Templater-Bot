# Email Templater #

This python script runs to generate individual emails based on a HTML template provided. This is especially useful when needing to send out lots of emails with slight variations such as distributing usernames and passwords.

## Templates ## 
Templates should be done in Jinja templating as per: https://jinja.palletsprojects.com/en/3.0.x/

## Data ##
Data should be CSV files and by the bare minimum need the field 'email'. Any other template fields should also be specified

# Setup # 
Set the environment (using OS environ or .env file in the root) with `EMAIL_SENDER` (the email address you want to send emails from) and `EMAIL_PASSWORD` (the email password you want to use) and optionally the `EMAIL_SERVER`, the SMTP server you're logging into e.g. by default this is smtp.office365.com for sending office 365 outlook emails

# Running The Program # 
To run this program, run 'run.py'. First select the .jinja template file, then select the data CSV. It will then ask you for an email subject. Then a sample email will be sent to your sender email. Check this email, if it looks good, then write Y in the console to send all emails