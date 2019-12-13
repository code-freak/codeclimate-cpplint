FROM python:3.7-alpine

# use custom cpplint version
ARG CPPLINT_SOURCE=https://github.com/code-freak/cpplint/archive/189afcb278d3c0b986b3e6c3e21cc969a97a3186.tar.gz

COPY engine.json /engine.json
COPY codeclimate-cpplint.py /opt/codeclimate-cpplint/bin/
RUN pip install $CPPLINT_SOURCE \
    && addgroup -g 9000 app \
    && adduser -Su 9000 -G app app \
    && chmod +x /opt/codeclimate-cpplint/bin/codeclimate-cpplint.py \
    && ln -s /opt/codeclimate-cpplint/bin/codeclimate-cpplint.py /usr/bin/codeclimate-cpplint

USER app
VOLUME /code
WORKDIR /code
CMD ["/usr/bin/codeclimate-cpplint"]