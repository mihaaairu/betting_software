## Build and run the container

```shell
docker-compose up --build
```

## [Open swagger](http://localhost:8000/docs) for testing

---
## Testing session

1. Setup project environment variables (in stock .env configured to work in Docker).
2. Mark `./app/src/` folder as a source folder.
3. Install poetry dependencies inside `./app/src/` folder:
    ```shell
    poetry install
    ```
4.  Add testing packages:
    ```shell
    poetry add pytest httpx asgi-lifespan 
    ```
5. Run (non-cli) `./tests/tests.py` file.