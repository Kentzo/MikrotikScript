"""Prepare a local dev extension without committing or publishing the project."""
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / '.zed-dev'
BASE.mkdir(exist_ok=True)
# Each run creates a separate snapshot; existing local files are preserved.
snapshot = Path(tempfile.mkdtemp(prefix='mikrotik-', dir=BASE))
grammar = snapshot / 'grammar'
extension = snapshot / 'extension'
grammar.mkdir()
extension.mkdir()
for name in ('grammar.js', 'tree-sitter.json', 'LICENSE'):
    shutil.copy2(ROOT / name, grammar / name)
shutil.copytree(ROOT / 'src', grammar / 'src')
shutil.copytree(ROOT / 'languages', grammar / 'languages')

def git(*args):
    return subprocess.check_output(
        ['git', '-c', 'core.hooksPath=/dev/null', '-C', str(grammar), *args],
        text=True, stderr=subprocess.STDOUT,
    ).strip()

git('init', '--quiet')
git('add', '.')
git('-c', 'user.name=MikroTik local development', '-c', 'user.email=dev@localhost',
    '-c', 'commit.gpgsign=false', 'commit', '--quiet', '-m', 'Local grammar snapshot')
revision = git('rev-parse', 'HEAD')
manifest = (ROOT / 'extension.toml').read_text()
before, _ = manifest.split('[grammars.mikrotik]', 1)
manifest = before + '[grammars.mikrotik]\n'
manifest += f'repository = {json.dumps(grammar.as_uri())}\nrev = {json.dumps(revision)}\n'
(extension / 'extension.toml').write_text(manifest)
shutil.copytree(ROOT / 'languages', extension / 'languages')
shutil.copy2(ROOT / 'LICENSE', extension / 'LICENSE')
print('In Zed, choose Extensions > Install Dev Extension and select:')
print(extension)
print('This snapshot uses a local Git grammar revision. Rerun after changes and reinstall the new snapshot.')
