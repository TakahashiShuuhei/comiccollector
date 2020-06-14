

def update_check():
    result = []
    comics = _load_comics()
    for comic in comics:
        new_links = comic.check()
        if new_links:
            result.append((comic, new_links))
    if result:
        notify(result)


def notify(result):
    import os
    from sendgrid import SendGridAPIClient
    from sendgrid.helpers.mail import Mail
    body = _to_mail_body(result)
    message = Mail(from_email='uhiaha888@gmail.com',
                   to_email='uhiaha888@gmail.com',
                   subject='更新があったよ',
                   text_content=text)
    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    response = sg.send(message)

def _to_mail_body(result):
    body = ''
    for comic, links in result:
        body += f'{comic.title}: {comic.url}\n\n'
        for link in links:
            body += f'    {link}\n'
        body += '\n'
    return body


if __name__ == '__main__':
    update_check()
