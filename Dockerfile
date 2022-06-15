FROM naytseyd/sedenbot:j1xlte

# Working Directory
WORKDIR /riouserbot/

# Clone Repo
RUN git clone -b rio https://github.com/rioprojectx/pyogram-userbot.git /riouserbot/

# Run bot
CMD ["python3", "rio.py"]
