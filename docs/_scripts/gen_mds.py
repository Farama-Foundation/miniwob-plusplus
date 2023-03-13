# Generate markdown files for the environments.

import os
import shutil

import gymnasium as gym
from utils import trim

import miniwob  # noqa: F401

LAYOUT = "env"

gym.logger.set_level(gym.logger.DISABLED)

all_envs = list(gym.envs.registry.values())
filtered_envs = []


# Copy MiniWoB-plusplus/html to /docs/demos/
source_path = os.path.join(
    os.path.dirname(__file__),
    "..",
    "..",
    "html",
)
# Sphinx copies everything inside the first demos/ directory to the root
# So to ensure that the final path is /demos/** we need another demos folder
destination_path = os.path.join(os.path.dirname(__file__), "..", "demos", "demos")
shutil.copytree(source_path, destination_path)


# Obtain filtered list
for env_spec in all_envs:
    if env_spec.namespace != "miniwob":
        continue
    filtered_envs.append(env_spec)
filtered_envs.sort(key=lambda x: x.name)

# Update Docs
for i, env_spec in enumerate(filtered_envs):
    print("ID:", env_spec.id)
    try:
        env_spec = gym.spec(env_spec.id)

        split = env_spec.entry_point.split(":")
        mod = __import__(split[0], fromlist=[split[1]])
        env_class = getattr(mod, split[1])
        docstring = trim(env_class.__doc__)

        if not docstring:
            docstring = env_class.__class__.__doc__

        docstring = trim(docstring)

        env_type = "miniwob"
        env_name = env_spec.name
        title_env_name = env_name.replace("-", " ").title()

        # path for saving the markdown file
        md_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "environments",
            env_name + ".md",
        )
        os.makedirs(os.path.dirname(md_path), exist_ok=True)

        front_matter = f"""---
autogenerated:
title: {title_env_name}
---
"""
        title = f"# {title_env_name}"
        gif = ""
        info = f"""
<center>
    <a href="../../demos/miniwob/{env_name}.html"><button>Go To Demo</button></a>
</center>
"""
        if docstring is None:
            docstring = "No information provided"
        all_text = f"""{front_matter}
{title}

{gif}

{info}

{docstring}
"""
        file = open(md_path, "w", encoding="utf-8")
        file.write(all_text)
        file.close()
    except Exception as e:
        print(e)
