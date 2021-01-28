FROM python:3

WORKDIR /usr/src/seu-bot

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./seu-bot.py" ]