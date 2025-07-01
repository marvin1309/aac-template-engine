# .gitlab-ci/scripts/python/render-services.py

import.yml
import subprocess
from pathlib import Path

with open('.gitlab-ci/services.yml') as f:
    services =.yml.safe_load(f)["services"]

for svc in services:
    name = svc["name"]
    category = svc["category"]
    vars_file = svc["vars_file"]
    service_dir = f"{category}/{name}"
    template_dir = f"{service_dir}/templates"
    compose_dir = f"{service_dir}/compose"
    internal_net = f"{name}_internal"

    Path(compose_dir).mkdir(parents=True, exist_ok=True)

    extra_args = [
        "-D", "SERVICE_NAME", name,
        "-D", "INTERNAL_NETWORK", internal_net,
        "-D", "USE_TRAEFIK", str(svc.get("default_secured_with_traefik", True)).lower()
    ]

    subprocess.run([
        "jinja", "-d", vars_file, "-f", .yml", *extra_args,
        "-o", f"{compose_dir}/docker-compose.yml",
        f"{template_dir}/docker-compose.yml.j2"
    ], check=True)

    subprocess.run([
        "jinja", "-d", vars_file, "-f", .yml", *extra_args,
        "-o", f"{compose_dir}/stack.env",
        f"{template_dir}/stack.env.j2"
    ], check=True)
