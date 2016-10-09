FROM python:2.7-onbuild

RUN chown -R www-data:www-data ./static
RUN chown -R www-data:www-data ./media

COPY ./run_web
COPY ./run_celery

RUN chmod +x ./run_web
RUN chmod +x ./run_celery
