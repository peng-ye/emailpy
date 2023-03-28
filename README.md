# emailpy
usage: emailpy.py [-h] -r FILE -m FILE [-l LOG_FILE] [-sd SENDER]
                  [-server SMTPSERVER] [-usr USERNAME] [-pwd PASSWORD]
                  [-hd FILE] [-sj SUBJECT] [-a ATTACHMENT]

Send reminders to users according to disk scanning results

optional arguments:
  -h, --help            show this help message and exit
  -r FILE, --scan_results FILE
                        Scan results containing filename and filesize.
  -m FILE, --map_file FILE
                        A map of user-email pairs.
  -l LOG_FILE, --log_file LOG_FILE
                        Log file name.
  -sd SENDER, --sender SENDER
                        Sender of the email.
  -server SMTPSERVER, --SMTPserver SMTPSERVER
                        SMTP server.
  -usr USERNAME, --USERNAME USERNAME
                        Username of the sender email.
  -pwd PASSWORD, --PASSWORD PASSWORD
                        Password for the sender email.
  -hd FILE, --header_file FILE
                        Header.
  -sj SUBJECT, --subject SUBJECT
                        Subject of the email.
  -a ATTACHMENT, --attachment ATTACHMENT
                        Name for the attachement.
# Example
python emailpy.py --scan_results ./scan_results.txt --map_file ./user_email_map.txt

