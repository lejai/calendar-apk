FROM kivy/buildozer:latest
WORKDIR /app
COPY build.sh /app/build.sh
RUN chmod +x /app/build.sh
ENTRYPOINT ["/bin/bash", "/app/build.sh"]