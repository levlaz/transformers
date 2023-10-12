import sys

import anyio
import dagger


async def main():
    config = dagger.Config(log_output=sys.stdout)

    # initialize Dagger client
    async with dagger.Connection(config) as client:
        # use a python:3.11-slim container
        # get version
        python = (
            client.container()
            .from_("cimg/python:3.8.12")
            .with_exec(["python", "-V"])
            .with_env_variable("RUN_CUSTOM_TOKENIZERS", "True")
            .with_exec(["sh", "-c", "sudo apt-get -y update && sudo apt-get install -y cmake"])
            .pipeline("install jumanpp")
            .with_exec(["sh", "-c", "wget https://github.com/ku-nlp/jumanpp/releases/download/v2.0.0-rc3/jumanpp-2.0.0-rc3.tar.xz"])
            .with_exec(["sh", "-c", "tar xvf jumanpp-2.0.0-rc3.tar.xz"])
            .with_exec(["sh", "-c", "mkdir jumanpp-2.0.0-rc3/bld"])
            .with_workdir("jumanpp-2.0.0-rc3/bld")
            .with_exec(["sh", "-c", "sudo cmake .. -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/usr/local"])
            .with_exec(["sh", "-c", "sudo make install"])
        )

        # execute
        version = await python.stdout()

    # print output
    print(f"Hello from Dagger and {version}")


anyio.run(main)
