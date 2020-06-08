import imaplib
import email
from pymongo import MongoClient


def mail_to_mongo(login, password, search='ALL'):
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(login, password)
    mail.select("INBOX")
    list_id = mail.search(None, search)[1][0].split()
    mail_list = []
    for id in list_id:
        mail_dict = {}
        status, data = mail.fetch(id, '(RFC822)')
        message = email.message_from_bytes(data[0][1])
        from_list = message["From"].split()
        address = from_list[1][1:-1]
        name = email.header.decode_header(from_list[0])[0][0]
        if isinstance(name, bytes):
            name = email.header.decode_header(from_list[0])[0][0].decode('utf-8')
        title = email.header.decode_header(message['Subject'])[0][0]
        if isinstance(title, bytes):
            title = title.decode('utf-8')
        payload = message.get_payload()[0]
        body = payload.get_payload(decode=True)
        if isinstance(body, bytes):
            body = body.decode('utf-8')
        mail_dict['from'] = [name, address]
        mail_dict['title'] = title
        mail_dict['body'] = body
        mail_dict['date'] = message['Date']
        mail_list.append(mail_dict)
    client = MongoClient('localhost', 27017)
    db = client['mail']
    collection = db['test']
    collection.insert_many(mail_list)
    mail.logout()


if __name__ == '__main__':
    login = input('Set your login: ')
    password = input('Set your password: ')
    mail_to_mongo(login, password)

