import sqlite3
from infra.comic import SqliteComicRepository
from infra.link import SqliteLinkRepository

DB_PATH = './hoge.db'

def update_check():
    connection = sqlite3.connect(DB_PATH)
    comic_repository = SqliteComicRepository(connection)
    link_repository = SqliteLinkRepository(connection)

    result = []
    comics = comic_repository.get_all()
    for comic in comics:
        new_links = comic.check(link_repository)
        if new_links:
            result.append((comic, new_links))
    if result:
        notify(result)
    connection.commit()


def notify(result):
    import os
    from sendgrid import SendGridAPIClient
    from sendgrid.helpers.mail import Mail
    body = _to_mail_body(result)
    message = Mail(from_email='uhiaha888@gmail.com',
                   to_emails='uhiaha888@gmail.com',
                   subject='更新があったよ',
                   plain_text_content=body)
    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    response = sg.send(message)

def _to_mail_body(result):
    body = ''
    for comic, links in result:
        body += f'{comic.title}: {comic.url}\n\n'
        for link in links:
            body += f'    {link.url}\n'
        body += '\n'
    return body


if __name__ == '__main__':
    update_check()
