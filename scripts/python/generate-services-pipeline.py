import yaml

with open('ci/services.yml') as f:
    data = yaml.safe_load(f)

services = data.get("services", [])

with open('.gitlab-ci.generated.yml', 'w') as out:
    out.write("stages:\n  - render\n  - commit\n\n")

    for s in services:
        out.write(f"render_{s['name']}:\n")
        out.write(f"  extends: .render_docker_service\n")
        out.write(f"  variables:\n")
        out.write(f"    SERVICE_NAME: {s['name']}\n")
        out.write(f"    SERVICE_CATEGORY: {s['category']}\n\n")

    out.write("commit_all:\n")
    out.write("  stage: commit\n")
    out.write("  image: alpine:latest\n")
    out.write("  tags: [docker]\n")
    out.write("  needs:\n")
    for s in services:
        out.write(f"    - job: render_{s['name']}\n")
        out.write("      artifacts: true\n")
    out.write("  before_script:\n")
    out.write("    - apk add --no-cache git\n")
    out.write("    - git config user.name \"CI Bot\"\n")
    out.write("    - git config user.email \"ci@example.com\"\n")
    out.write("  script:\n")
    out.write("    - git add */*/compose || echo \"No changes\"\n")
    out.write("    - git commit -m \"🚀 Auto-render all services [ci skip]\" || echo \"Nothing to commit\"\n")
    out.write("    - git push \"https://oauth2:${CI_GITLAB_TOKEN}@${CI_SERVER_HOST}/${CI_PROJECT_PATH}.git\" HEAD:main\n")
    out.write("  rules:\n")
    out.write("    - if: '$CI_COMMIT_BRANCH == \"main\"'\n")
    out.write("      when: on_success\n")
