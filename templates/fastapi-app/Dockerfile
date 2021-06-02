FROM segment/chamber:2 AS chamber

FROM python:3.9-slim

# Installs `chamber` for secure access to AWS SSM Parameter Store
COPY --from=chamber /chamber /bin/chamber

ARG BUILD_COMMIT_SHA
ENV BUILD_COMMIT_SHA ${BUILD_COMMIT_SHA:-}

# Arg to permit installing different requirements (default to app only)
ARG REQUIREMENTS="requirements/requirements.txt"

RUN apt-get update
RUN apt-get install -y --no-install-recommends build-essential gcc libpq-dev dumb-init

# install requirements
RUN pip install --upgrade pip && pip install pip-tools
COPY requirements/ requirements/
RUN pip-sync ${REQUIREMENTS}

# Create a non-root user and use it
RUN useradd worker
USER worker

WORKDIR /code/

COPY . /code/

ENV PYTHONPATH "${PYTHONPATH}/code"

ENTRYPOINT [ "./docker-entrypoint.sh" ]
CMD [ "ddtrace-run", "uvicorn", "app.main:app", "--port", "80", "--host", "0.0.0.0", "--loop", "uvloop" ]
