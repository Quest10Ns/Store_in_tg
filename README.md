# 🤝 Welcome, there is an online store implemented here in the form of a telegram bot

To work with this project, you need to have Python 3.12 installed. All the necessary libraries and frameworks can be
found in the `requirements.txt` file. To install them, follow these steps:

1. First, create a virtual environment:

   ```
   python -m venv .venv
   ```

2. Activate the virtual environment

   ```
   .venv/Scripts/activate
   ```

3. Upgrade your pip version:

   ```
   python.exe -m pip install --upgrade pip
   ```

4. Install the required libraries and frameworks:

   ```
   pip install -r requirements.txt
   ```

5. Check that the installation was successful:

   ```
   pip list
   ```

   You should see something like this:

   ```
   Package            Version
   ------------------ --------
   aiofiles           23.2.1
   aiogram            3.10.0
   aiohttp            3.9.5
   aiosignal          1.3.1
   annotated-types    0.7.0
   APScheduler        3.10.4
   asyncio            3.4.3
   asyncpg            0.29.0
   attrs              24.2.0
   certifi            2024.7.4
   charset-normalizer 3.3.2
   Deprecated         1.2.14
   distro             1.9.0
   frozenlist         1.4.1
   greenlet           3.0.3
   idna               3.7
   magic-filter       1.0.12
   multidict          6.0.5
   netaddr            1.3.0
   pip                24.2
   psycopg2           2.9.9
   pydantic           2.8.2
   pydantic_core      2.20.1
   python-dotenv      1.0.1
   pytz               2024.1
   requests           2.32.3
   six                1.16.0
   SQLAlchemy         2.0.32
   typing_extensions  4.12.2
   tzdata             2024.1
   tzlocal            5.2
   urllib3            2.2.2
   wrapt              1.16.0
   yarl               1.9.4
   yookassa           3.3.0
   ```

6. Create a `.env` file.

7. Add the following to the `.env` file:

   ```
   TOKEN = 6866916052:AAHQCfrFywwFizgEv1FyO9jHGP1bdaLlPoA
   TOKEN2 = 7436017578:AAG82bQRSxEWvjtSvVCz4pbh_f11wcEDFtg
   SQLALCHEMY_URL = postgresql+asyncpg://postgres:3720@localhost/kletkidb
   ADMIN_LOGIN = admlog
   ADMIN_PASSWORD = admpas
   ACCOUNT_ID = from yookassa
   SECRET_KEY = from yookassa
   ```

8. Run the code from ```main.py``` and check that everything is working as expected.
