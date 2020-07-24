import os, json
from utils.clear import clear

def build(PROJECT_NAME, BASE_PATH, IDE_CHOICES) :
    os.mkdir(PROJECT_NAME)
    os.chdir(PROJECT_NAME)

    WEB_STARTER_DIR = os.path.join(BASE_PATH, 'Miscellaneous/Automate-Creating-Projects/web_starter')

    os.mkdir('js')
    os.mkdir('styles')

    html = open('index.html', 'w+')
    html_starter = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="styles/style.css">
    <title>Document</title>
</head>
<body>
    


    <script src="js/script.js"></script>

</body>
</html>
        '''
    html.write(html_starter)
    html.close()

    css_dir = os.path.join(os.getcwd(), 'styles')
    css = open(f'{css_dir}/style.css', 'w+')
    css_starter = '''* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}'''
    css.write(css_starter)
    css.close()

    js = open('js/script.js', 'w+')
    js.close()

    clear()

    return IDE_CHOICES[1], []