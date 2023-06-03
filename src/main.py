# from database import update_database
from util import add_manga_by_link, send_notificacion, get_notification_test, test_get_variables_env, send_mail

lista_mangas_temporal = ('https://lectortmo.com/library/manga/20201/houseki-no-kuni',
                         'https://lectortmo.com/library/manga/44034/blue-period',
                         'https://lectortmo.com/library/manga/218/yofukashi-no-uta',
                         'https://lectortmo.com/library/manga/38888/uzaki-chan-wa-asobitai',
                         'https://lectortmo.com/library/manga/145/vinland-saga',)

# update_database()
# url_test = 'https://lectortmo.com/library/manga/20201/houseki-no-kuni'
# add_manga_by_link(url_test)

# for x in lista_mangas_temporal:
#     add_manga_by_link(x)

# send_notificacion()
# test_get_variables_env()

# Ejemplo de uso
# destinatario = 'elias.or.dev@gmail.com'
# asunto = 'Prueba de correo con archivo HTML formateado'

# template_file = 'template_mail.html'

# data  = {
#         "notifications" : get_notification_test(),
#     }

# send_mail(destinatario, asunto, template_file, data)

# send_notificacion()