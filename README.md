# FastAPI Nuxt3 template

## **Pre setup**

- [Install `Python 3.12`](https://www.python.org/),
- [Install `poetry`](https://python-poetry.org/),
- [Install `node 20+ LTS`](https://nodejs.org/en), or use nvm (node virtual manager) to install node
- [Install `Docker`, `docker-compose`](https://docs.docker.com/get-docker/)
- Install `make` command. [Windows](https://stackoverflow.com/questions/32127524/how-to-install-and-use-make-in-windows), [Linux](https://askubuntu.com/questions/161104/how-do-i-install-make) and [Mac](https://stackoverflow.com/questions/10265742/how-to-install-make-and-gcc-on-a-mac)

## **Setup on Local**

1. Configure `.env` file.

    ```sh
    cp secret/.env.example secret/.env
    ```

2. Create python virtual environment.

    - required to install python3.11 and poetry

    ```sh
    python3 -m venv .venv
    source .venv/bin/activate
    pip install --upgrade pip
    cd back
    poetry install --no-root
    ```

3. pre-commit.

    - required to activate `.venv` virtual environment.

    ```sh
    source .venv/bin/activate
    pre-commit install
    ```

4. Install and start. See [Makefile](./Makefile) for more detailed commands.

    - enjoy

    ```sh
    make install
    ```

    - frontend: <http://localhost:3000>
    - backend: <http://localhost:8000/docs>
