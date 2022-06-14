# We're Using NaytSeyd's Special Docker
FROM rioprojectx/riobot:j1xlte

# Working Directory
WORKDIR /RioProjectX/

# Clone Repo
RUN git clone -b seden https://github.com/RioProjectX/Pyogram-Userbot.git /RioProjectX/

# Run bot
CMD ["python3", "rio.py"]
