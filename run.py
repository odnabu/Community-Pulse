# 10.06.2025
# Video: Python Advanced 4: Flask: Summary session 1 (Повторение, решение задач)    Müller Alexander
# link: https://player.vimeo.com/video/1092111490?h=02293fbf54

# 11.06.2025
# Python Advanced 4: Flask: Summary session 1 (Повторение, решение задач)
# link: https://player.vimeo.com/video/1092444197?h=4fc42a8cb4

# 11.06.2025
# Python Adv 8: Flask: Summary session 2 (Повторение, решение задач)
# link: https://player.vimeo.com/video/1092439106?h=1ae131892c

from app import create_app
import os

config_name = os.getenv('FLASK_ENV') or 'default'
app = create_app(config_name)

if __name__ == '__main__':
    app.run()



# flask db init
# flask db migrate
# flask db upgrade
# python run.py
