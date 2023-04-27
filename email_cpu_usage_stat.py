from collections import defaultdict
from datetime import date, datetime
import smtplib
from smtplib import SMTP_SSL as SMTP
from email.message import EmailMessage
# import mimetypes
import sys
from argparse import ArgumentParser
import os, fnmatch
import subprocess
import time

def parse_emails(emails):
    email_list = emails.split(",")
    return(email_list)

def get_key(key_file):
    key = ""
    with open(key_file) as k_f:
        key = k_f.readline().strip()
    return(key)


def send_email(SMTPserver, sender, USERNAME, PASSWORD, email, subject, message):

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
    #msg.add_attachment(all_results, # maintype='text', subtype='plain',
    #                   filename=attachment)

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
    parser.add_argument('-r', '--scan_results', required=False,
                        metavar='FILE',
                        dest='scan_results',
                        help="""Scan results containing filename and filesize.""")

    # user email map
    parser.add_argument('-m', '--map_file', required=False,
                        metavar='FILE',
                        default="user_email_map.txt",
                        dest='map_file',
                        help='A map of user-email pairs.')
    parser.add_argument('-e', '--emails', required=True,
                        dest='emails',
                        help="""List of recipinet email(s separated by comma).""")

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
    parser.add_argument('-hdf', '--header_file', required=False,
                        metavar='FILE',
                        dest='header_file',
                        help="""Header file.""")
    parser.add_argument('-hd', '--header', required=False,
                         metavar='FILE',
                        default='',
                         dest='header',
                         help="""Header.""")
    parser.add_argument('-sj', '--subject', required=False,
                        dest='subject',
                        help="""Subject of the email.""")
    parser.add_argument('-a', '--attachment', required=False,
                        default = "file_list.txt",
                        dest='attachment',
                        help="""Name for the attachement.""")
    parser.add_argument('-sig', '--signature', required=False,
                        default = "\n\nData Core Admin",
                        dest='signature',
                        help="""Signature.""")
    parser.add_argument('-p', '--program', required=False,
        default='avg_cpu_usage_once.sh',
        dest='program', help="""Path to the program.""")

    parser.add_argument('-i', '--interval', required=False,
        default='30',
        dest='interval', help="""Time interval.""")

    parser.add_argument('-t', '--times', required=False,
        default='10',
        dest='times', help="""How many time points for the stat.""")

    parser.add_argument('-s', '--sleep', required=False,
         default=0,
         dest='sleep', help="""Wait for how long (seconds).""")

    parser.add_argument('-th', '--threshold', required=False,
          default=100,
                        dest='threshold', help="""Threshold for sending notification (default: 100).""")


    args = parser.parse_args()

    if not args.PASSWORD:
        args.PASSWORD = get_key(".key_file.txt")
    elif args.PASSWORD[-3:]=="txt" or "key" in args.PASSWORD:
        args.PASSWORD = get_key(args.PASSWORD)

    email_list = parse_emails(args.emails)

    while True:
        result = subprocess.run([args.program, args.interval, args.times], stdout=subprocess.PIPE)
        stats = result.stdout.decode('utf-8')

        usage = float(stats.strip().split(" ")[-1])
        if usage <= float(args.threshold):
            now = str(datetime.now())
            if not args.subject:
                args.subject = "Average CPU usage, " + now

            for email in email_list:
                message = args.header + stats + args.signature
                # feel free to customize this
                send_email(args.SMTPserver, args.sender,
                           args.USERNAME, args.PASSWORD,
                           email, args.subject, message)
                # write_the_log(email, all_results, args.log_file, today)

        time.sleep(int(args.sleep))

if __name__ == "__main__":
    main()
