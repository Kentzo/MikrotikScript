"""Validate the Zed manifest, actual parser output, and highlight captures."""
import os
from pathlib import Path
import re
import subprocess
import tempfile
import tomllib

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / 'node_modules' / '.bin' / 'tree-sitter'
os.chdir(ROOT)
os.environ.setdefault('XDG_CACHE_HOME', str(Path(tempfile.gettempdir()) / 'mikrotik-tree-sitter-cache'))

def run(*args):
    result = subprocess.run([str(CLI), *args], text=True, capture_output=True)
    if result.returncode:
        raise SystemExit(result.stdout + result.stderr)
    return result.stdout

manifest = tomllib.loads((ROOT / 'extension.toml').read_text())
config = tomllib.loads((ROOT / 'languages/mikrotik/config.toml').read_text())
assert config['grammar'] in manifest['grammars']
assert 'rsc' in config['path_suffixes']
run('test')
tree = run('parse', 'examples/router.rsc')
# Some CLI releases return success on recoverable syntax errors, so inspect the tree too.
assert not re.search(r'\b(ERROR|MISSING)\b', tree), tree
for query in ('highlights', 'brackets', 'indents'):
    output = run('query', f'languages/mikrotik/{query}.scm', 'examples/router.rsc')
    assert 'capture:' in output, f'{query}: no captures'
    if query == 'highlights':
        expected = {
            'comment': '# Representative RouterOS export and scripting constructs; documentation IPs only.',
            'property': 'interface',
            'function': ':put',
            'keyword': ':if',
            'boolean': 'yes',
            'variable': '$retryCount',
            'string.special': '2001:db8::1/64',
            'string.escape': '\\n',
            'number': '1h30m',
        }
        for capture, text in expected.items():
            pattern = rf' - {re.escape(capture)},[^\n]*text: `{re.escape(text)}`'
            assert re.search(pattern, output), f'missing {capture} capture for {text!r}'
print('PASS: 6 corpus cases, example parsed without errors, 3 Zed queries, 9 representative highlight captures, TOML configuration.')
