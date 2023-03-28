#!/usr/bin/env python
# coding: utf-8

from collections import defaultdict
from datetime import date
import smtplib
from smtplib import SMTP_SSL as SMTP
from email.message import EmailMessage
# import mimetypes
import sys
from argparse import ArgumentParser

def parse_user_email_map(map_file):
    # user email
    user_email = dict() # defaultdict("")
    
    with open(map_file) as m_p:
        m_p_list = list(m_p)
        user_email = {user: email for user, email in 
                      [pair.strip().split("\t") for pair in m_p_list]}
    return(user_email)

def parse_scan_results(scan_results, threshold=0):
    """
    user filename filesize
    """
    # supposedly you have filtered the scan results by size/file type: threshold = 0
    
    user_results = defaultdict(list)
    
    with open(scan_results) as s_r:
        s_r_list = list(s_r)
        for result in s_r_list:
            user, filename, filesize = result.strip().split("\t")
            # if int(filesize) > threshold:
            user_results[user].append(filename+"\t"+filesize)
       
    return(user_results)

def parse_header(header_file):
    header = "Please be reminded to compress/clean the data in the attached file at your earliest convenience."
    if header_file:
        with open(header_file) as h_f:
            header = "\n".join(h_f.readlines())
    return(header)

def write_the_log(email, all_results, log_file, today):
    with open(log_file, "a") as log_f:
        print("A reminder of cleaning up the data below has been sent to " + email + " on " + today + ".",
              file=log_f)
        print(all_results,
             file=log_f)
        
def get_key(key_file):
    key = ""
    with open(key_file) as k_f:
        key = k_f.readline().strip()
    return(key)


def send_email(SMTPserver, sender, USERNAME, PASSWORD, email, subject, message, all_results, attachment):
    
    # With reference to 
    # https://docs.python.org/3/library/email.examples.html and
    # https://stackoverflow.com/questions/64505/sending-mail-from-python-using-smtp
    
    # Create the container email message.
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join([email]) # may add user_email["admin"]
    msg.preamble = 'You will not see this in a MIME-aware mail reader.\n'
    
    msg.set_content(message)
    msg.add_attachment(all_results, # maintype='text', subtype='plain', 
                       filename=attachment)
    
    try:
        conn = SMTP(SMTPserver)
        conn.set_debuglevel(False)
        conn.login(USERNAME, PASSWORD)
        try:
            conn.send_message(msg)
        finally:
            conn.quit()
    
    except:
        sys.exit( "mail failed; %s" % "CUSTOM_ERROR" ) # give an error message
        
def main():
    parser = ArgumentParser(description="""\
Send reminders to users according to disk scanning results
""")
    
    # scan results
    parser.add_argument('-r', '--scan_results', required=True,
                        metavar='FILE',
                        dest='scan_results',
                        help="""Scan results containing filename and filesize.""")

    # user email map
    parser.add_argument('-m', '--map_file', required=False,
                        metavar='FILE',
                        default="user_email_map.txt",
                        dest='map_file',
                        help='A map of user-email pairs.')
    
    # log file
    parser.add_argument('-l', '--log_file', required=False,
                        # action='append', metavar='RECIPIENT',
                        default="log_file.txt", dest='log_file',
                        help='Log file name.')

    # sender config
    parser.add_argument('-sd', '--sender', required=False, default="emailPyTestG@gmail.com",
                        dest='sender',
                        help="""Sender of the email.""")
    parser.add_argument('-server', '--SMTPserver', required=False, default="smtp.gmail.com",
                        dest='SMTPserver',
                        help="""SMTP server.""")
    parser.add_argument('-usr', '--USERNAME', required=False, default="emailPyTestG",
                        dest='USERNAME',
                        help="""Username of the sender email.""")
    parser.add_argument('-pwd', '--PASSWORD', required=False, default=None,
                        dest='PASSWORD',
                        help="""Password for the sender email.""")
    
    # email contents
    parser.add_argument('-hd', '--header_file', required=False,
                        metavar='FILE',
                        dest='header_file',
                        help="""Header.""")
    parser.add_argument('-sj', '--subject', required=False,
                        dest='subject',
                        help="""Subject of the email.""")
    parser.add_argument('-a', '--attachment', required=False,
                        default = "file_list.txt",
                        dest='attachment',
                        help="""Name for the attachement.""")
    
    
    args = parser.parse_args()
    today = str(date.today())
    user_email = parse_user_email_map(args.map_file)
    user_results = parse_scan_results(args.scan_results)
    header = parse_header(args.header_file)
    if not args.subject:
        args.subject = "Reminder of data cleanup on " + today
        
    if not args.PASSWORD:
        args.PASSWORD = get_key("key_file.txt")
    elif args.PASSWORD[-3:]=="txt" or "key" in args.PASSWORD:
        args.PASSWORD = get_key(args.PASSWORD)
        
    for user, results in user_results.items():
        email = user_email[user]
        all_results = "\n".join(results)
                    
        message = header # feel free to customize this
        
        send_email(args.SMTPserver, args.sender, 
                   args.USERNAME, args.PASSWORD,
                   email, args.subject, message, all_results, args.attachment)
        write_the_log(email, all_results, args.log_file, today)
    
if __name__ == "__main__":
    main()

