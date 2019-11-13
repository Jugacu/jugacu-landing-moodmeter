#!C:/Users/Jugacu/AppData/Local/Programs/Python/Python38-32/python.exe

from dotenv import load_dotenv
import cssutils
from ftplib import FTP
from pathlib import Path
import os

load_dotenv()

default_color = '#212121'
dirname = os.path.dirname(__file__)
css_path_file = os.path.join(dirname, './css/main.css')

colors = [
    '#080808',  # black
    '#621919',  # redish
    '#ab653a',  # brownish
    '#ab9e3a',  # yellow
    '#3aab44',  # green -- middle
    '#eeeeee',  # white
    '#8c8caa',  # white/blue
    '#3a8bab',  # blue
    '#4c3aab',  # purple
    '#a03aab',  # love
]


def init():
    selected_value = showMenu()

    print('reading css...')
    css = readCss()

    print('generating hexadecimal...')
    color = genColor(selected_value)

    css['.triangle svg']['stroke'] = color

    print(f'picked color: {color[:-1]}')

    print('writting to file...')
    writeCss(css)

    print('uploading...')
    upload()
    print('done')


def showMenu():
    print('Jugacu\'s mood meter')
    print('----------------')

    while True:
        input_data = input('please enter a value [1-' + str(len(colors)) + '] (0 to default): ')
        if input_data.isdigit() and (0 <= int(input_data) <= len(colors)):
            break

    return int(input_data)


def readCss():
    with open(css_path_file, 'r') as file:
        data = file.read()
        css = cssutils.parseString(data, validate=False)
        file.close()

    dct = {}
    for rule in css:
        selector = rule.selectorText
        styles = rule.style.cssText

        styles_dic = {}
        for s in styles.split('\n'):
            pair = s.split(':')
            styles_dic[pair[0]] = pair[1]

        dct[selector] = styles_dic

    return dct


def genColor(selected_value):
    return colors[selected_value - 1] + ';' if selected_value != 0 else default_color + ';'


def writeCss(css):
    text = ''
    for stl in css:
        text += stl + ' {\n'
        for p in css[stl]:
            text += '\t' + p + ':' + css[stl][p] + '\n'
        text += '}\n'

    with open(css_path_file, 'w') as file:
        file.write(text)
        file.close()


def upload():
    file_path = Path(css_path_file)
    with FTP(os.getenv('FTP_HOST')) as ftp, open(file_path, 'rb') as file:
        try:
            ftp.login(os.getenv('FTP_USER'), os.getenv('FTP_PASSWORD'))
            ftp.cwd(os.getenv('FTP_DIR'))
            ftp.storbinary(f'STOR {file_path.name}', file)
        except Exception as e:
            print(e)
            print('[ERR] error during FTP conexion')
        finally:
            ftp.close()


init()
