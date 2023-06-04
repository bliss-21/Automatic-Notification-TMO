from database import create_session, update_database
from models import Manga, Notification
from dotenv import load_dotenv
import os 

""" import webscraping """
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime

""" import mail """
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader

# database init
update_database()

# Cargar variables de entorno desde el archivo .env
load_dotenv()

DESTINATION_MAIL = os.getenv('DESTINATION_MAIL')
SMTP_HOST  = os.getenv('SMTP_HOST')
SMTP_PORT  = os.getenv('SMTP_PORT')
SENDER_MAIL  = os.getenv('SENDER_MAIL')
SENDER_PASS_APP  = os.getenv('SENDER_PASS_APP')


def extract_name_from_link(link: str):
    """
    extrae el nombre del manga desde el link
    """
    resultado = re.search(r'[^/]+$', link)

    if resultado:
        texto_extraido = resultado.group(0)
        texto_extraido = texto_extraido.replace('-', ' ')
        return texto_extraido
    
    return "titulo no extraido"

def send_mail(destinatario, asunto, template_file, datos = []):
    # Configuración del servidor SMTP de Gmail
    smtp_host = SMTP_HOST
    smtp_port = SMTP_PORT
    correo_emisor = SENDER_MAIL
    contraseña_emisor = SENDER_PASS_APP

    # Cargar la plantilla HTML
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template(template_file)
    contenido_html = template.render(datos)

    # Crear objeto de mensaje
    msg = MIMEMultipart()
    msg['From'] = correo_emisor
    msg['To'] = destinatario
    msg['Subject'] = asunto

    # Agregar el cuerpo del mensaje como HTML
    msg.attach(MIMEText(contenido_html, 'html'))

    try:
        # Establecer conexión con el servidor SMTP de Gmail
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()
        # Iniciar sesión en la cuenta de Gmail
        server.login(correo_emisor, contraseña_emisor)
        # Enviar el correo electrónico
        server.send_message(msg)
        # Cerrar la conexión
        server.quit()
        print("Correo enviado exitosamente")
    except Exception as e:
        raise e

def download_manga_info(url:str):
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
        'Referer': 'https://www.google.com/'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    elemento = soup.find('li', class_='list-group-item')

    ultimo_nombre_capitulo = elemento.find('a', class_='btn-collapse')
    link_ultimo_capitulo = elemento.find('a', class_='btn btn-default btn-sm')
    titulo_manga = extract_name_from_link(url)

    manga = Manga(
        titulo_manga = titulo_manga,
        link_manga = url,
        ultimo_capitulo = ultimo_nombre_capitulo.text,
        link_ultimo_capitulo = link_ultimo_capitulo['href'],
        fecha_agregado = datetime.now(),
        fecha_actualizado = datetime.now(),
        activo = True
    )

    return manga

def add_manga_by_link(url:str):
    
    session = create_session()

    #validamos si el manga ya esta registrado mediante el titulo del mismo
    titulo_manga = extract_name_from_link(url)

    registro = session.query(Manga).filter(Manga.titulo_manga == titulo_manga).first()

    if registro is not None:
        return

    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
    #     'Referer': 'https://www.google.com/'
    # }
    # response = requests.get(url, headers=headers)
    # soup = BeautifulSoup(response.text, 'html.parser')

    # elemento = soup.find('li', class_='list-group-item')

    # ultimo_nombre_capitulo = elemento.find('a', class_='btn-collapse')
    # link_ultimo_capitulo = elemento.find('a', class_='btn btn-default btn-sm')

    # manga = Manga(
    #     titulo_manga = titulo_manga,
    #     link_manga = url,
    #     ultimo_capitulo = ultimo_nombre_capitulo.text,
    #     link_ultimo_capitulo = link_ultimo_capitulo,
    #     fecha_agregado = datetime.now(),
    #     fecha_actualizado = datetime.now(),
    #     activo = True
    # )

    manga = download_manga_info(url)

    # notificacion = Notification(#
    #     link_capitulo = manga.link_ultimo_capitulo,
    #     titulo_manga = manga.titulo_manga,
    #     nombre_capitulo = manga.ultimo_capitulo,
    #     fecha_creado = datetime.now(),
    #     #fk
    #     manga = manga
    # )

    session.add(manga)
    # session.add(notificacion)#
    session.commit()
    session.close()

def get_all_mangas(activo=None):
    session = create_session()
    query = session.query(Manga)

    if activo:
        query = query.filter(Manga.activo == activo)

    mangas = query.all()
    session.close()
    return mangas

def create_notification():

    session = create_session()

    # traer los mangas que tienen activo como true
    mangas =  get_all_mangas(True)

    for manga in mangas:
        
        # traemos el htmo de tmo y validamos si salio otro capitulo
        url = manga.link_manga
        current_manga = download_manga_info(url)

        if manga.ultimo_capitulo != current_manga.ultimo_capitulo:

            # actualizmos el manga
            manga.ultimo_capitulo = current_manga.ultimo_capitulo
            manga.link_ultimo_capitulo = current_manga.link_ultimo_capitulo
            manga.fecha_agregado = current_manga.fecha_agregado
            manga.fecha_actualizado = current_manga.fecha_actualizado

            # creamos la notificacion
            notificacion = Notification(
                link_capitulo = current_manga.link_ultimo_capitulo,
                titulo_manga = current_manga.titulo_manga,
                nombre_capitulo = current_manga.ultimo_capitulo,
                fecha_creado = datetime.now(),
                #fk
                manga = manga
            )

            session.add(notificacion)
            session.commit()
    
    session.close()

def send_notificacion():

    session = create_session()

    # traemos las notificaciones que no han sido notificadas, si no existen se detiene la funcion
    notifications = session.query(Notification).filter(Notification.notificado == False).all()

    data  = {
        "notifications" : notifications,
    }

    destinatario = DESTINATION_MAIL
    asunto = f'Mangas Actualizados esta semana en TMO'
    template_file = 'template_mail.html'


    try:
        send_mail(destinatario, asunto, template_file, data)

        notification_ids = [notification.id for notification in notifications]

        session.query(Notification).filter(Notification.id.in_(notification_ids)).update(
            {
                Notification.notificado: True,
                Notification.fecha_notificado: datetime.now()
            }
            , synchronize_session=False
        )

        session.commit()

    except Exception as e:
        print("Ocurrió un error al enviar el correo:", str(e))

    session.close()