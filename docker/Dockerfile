FROM python:3.12-alpine

ARG USERNAME=user
ARG ENV=prod

RUN if [ "$ENV" = "dev" ]; then \
  addgroup $USERNAME && adduser -D -G $USERNAME -h /home/$USERNAME $USERNAME; \
  else \
  addgroup -S $USERNAME && adduser -S -G $USERNAME -h /home/$USERNAME $USERNAME; \
  fi

WORKDIR /home/$USERNAME/workspace

RUN pip install --upgrade pip setuptools --no-cache-dir

COPY --chown=$USERNAME:$USERNAME . .

RUN pip install -r requirements.txt --no-cache-dir \
  && find /home/$USERNAME -type d -name '__pycache__' -exec rm -r {} + \
  && rm -rf /root/.cache/pip

RUN mkdir -p db \
  && chown -R $USERNAME:$USERNAME db

RUN chmod 700 entrypoint.sh

USER $USERNAME

ENTRYPOINT ["./entrypoint.sh"]
