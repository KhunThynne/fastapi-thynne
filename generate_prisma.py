import os
import subprocess
from pathlib import Path

root_schema = Path("../../prisma/schema.prisma").read_text(encoding="utf-8")

# Inject Python generator and URL
py_generator = """
generator py {
  provider = "prisma-client-py"
  interface = "asyncio"
  recursive_type_depth = 5
}
"""

lines = root_schema.splitlines()
new_lines = []

in_db_block = False
for line in lines:
    if line.startswith('datasource db {'):
        in_db_block = True
    elif in_db_block and line.strip() == '}':
        new_lines.append('  url = env("DATABASE_URL")')
        in_db_block = False
    new_lines.append(line)

new_schema = py_generator + "\n" + "\n".join(new_lines)
Path("schema.prisma").write_text(new_schema, encoding="utf-8")

print("Running prisma generate...")
res = subprocess.run(["python", "-m", "prisma", "generate", "--schema", "schema.prisma"], capture_output=True, text=True)
print(res.stdout)
print(res.stderr)
if res.returncode != 0:
    print("Generation failed!")
    exit(1)

Path("schema.prisma").unlink()
print("Generation successful and temp schema cleaned up.")
