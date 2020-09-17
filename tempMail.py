#!/usr/bin/env python3

import requests
import argparse
import string
import random
import os
import re
import colorama

isEmpty = True
version = "0.0.1"
colorama.init(autoreset=True)
attach = False
response = None
email = None
f = None
PATH = "./.cache/"
if not os.path.isdir(PATH):
    os.mkdir(PATH)
f = open(PATH+"tempmail.txt", 'r+')


class Tmpmail():

    def getRandom(self, value, input, output=[]):
        for _ in range(1, value):
            output.append(random.choice(input))

        return ''.join(output)

    def register(self, username, domain):
        res = requests.get(
            f"https://www.1secmail.com/api/v1/?action=getMessages&login={username}&domain={domain}")
        response = res.json()

    def checkInbox(self, username, domain):
        res = requests.get(
            f"https://www.1secmail.com/api/v1/?action=getMessages&login={username}&domain={domain}")
        global response
        response = res.json()
        if res.json() == []:
            print(colorama.Fore.YELLOW + "inbox empty")
            return False
        elif res.json() != []:
            for i in range(len(res.json())):
                print(
                    colorama.Fore.YELLOW +
                    f"{+ res.json()[i]['id']}\t{res.json()[i]['from']}\t{res.json()[i]['date'].split()[0]}\t{res.json()[i]['date'].split()[1]}")

    def htmlToText(self, body):
        return re.sub(r"<.*?>", "", body)

    def readMail(self, username, domain, ID):
        # if not self.checkInbox(username, domain):
        #     return
        # else:
        global attach
        res = requests.get(
            f"https://www.1secmail.com/api/v1/?action=readMessage&login={username}&domain={domain}&id={ID}").json()
        if res['attachments']:
            attach = True
        # print(res.json())
        print(f"id: {res['id']}\nfrom: {res['from']}\nsubject: {res['subject']}\nattachments: {res['attachments']}\nbody: {self.htmlToText(res['body'])}\ndate: {res['date'].split()[0]}\ntime: {res['date'].split()[1]} ")


letters = [i for i in string.ascii_letters]
digits = [i for i in string.digits]
randWord = letters + digits
domains = ["com", "org", "net"]
tmpmail = Tmpmail()


def generateRandom(username=False):
    if not username:
        username = tmpmail.getRandom(10, randWord)
    else:
        username = username
    domain = "@1secmail." + random.choice(domains)
    print(colorama.Fore.YELLOW + "your temp mail " + colorama.Fore.BLUE+"=> " +
          colorama.Fore.GREEN + f"{username+domain}")
    global email, f
    email = username + domain
    f = open(PATH+"tempmail.txt", 'w+')
    f.seek(0)
    f.truncate(0)
    f.write(email)


def checkInbox():
    email = open("./.cache/tempmail.txt", "r").read()
    sep = email.split('@')
    username = sep[0]
    domain = sep[1]
    tmpmail.checkInbox(username, domain)


def readMail(ID):
    email = open("./.cache/tempmail.txt", "r").read()
    sep = email.split('@')
    username = sep[0]
    domain = sep[1]
    tmpmail.readMail(username, domain, ID)


parser = argparse.ArgumentParser()
parser.add_argument("--version",
                    help="print version and exit", action='store_true')
parser.add_argument("-g", "--generate",
                    help="generate a new random mail", action='store_true')
parser.add_argument("-c", "--check",
                    help="check for messages in inbox", action='store_true')
parser.add_argument("-R", "--recent",
                    help="print the most recent mail address", action='store_true')
parser.add_argument("--clean",
                    help="clear all cache", action='store_true')
parser.add_argument("-r", "--read",
                    help="read email", metavar="ID", type=int)
parser.add_argument("-u", "--custom",
                    help="use a custom username", metavar="Username", type=str)
args = parser.parse_args()


if args.generate:
    generateRandom()
    isEmpty = False

if args.clean:
    size = os.path.getsize("./.cache/tempmail.txt")
    f.truncate(0)
    print(colorama.Fore.GREEN + f"cleaned {size} bytes cache")
    isEmpty = False

if args.check:
    checkInbox()
    isEmpty = False

if args.read:
    readMail(args.read)
    isEmpty = False

if args.recent:
    print(colorama.Fore.BLUE + open("./.cache/tempmail.txt", "r").read())
    isEmpty = False

if args.custom:
    generateRandom(username=args.custom)
    isEmpty = False

if args.version:
    print(colorama.Fore.GREEN + version)
    isEmpty = False

if isEmpty:
    print(colorama.Fore.RED +
          f"run ./{__file__.split('/')[-1]} -h for help")
