Containerized sandbox example

This folder contains a minimal Dockerfile that shows how you could run plugin
subprocesses inside an isolated container. This is an example only — for
real isolation use full VM images and strict network rules.

Build:

```bash
docker build -t mercury-sandbox:latest .
```

Run an interactive shell inside the container (bind the repo if desired):

```bash
docker run --rm -it -v "$(pwd):/app" mercury-sandbox:latest /bin/bash
```

From inside the container you can run plugin subprocesses with `MERCURY_SAFE=1`.
