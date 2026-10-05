# MikroTik RouterOS no Zed

Extensão de destaque de sintaxe para arquivos de configuração e scripts `.rsc`
no Zed, usando Tree-sitter. Inclui pareamento de delimitadores e indentação, sem
LSP ou código Rust próprio.

## Desenvolver e testar

Requisitos: Node.js/npm, Python 3.11+, Git e um compilador C para os testes nativos.
O Tree-sitter CLI está fixado no lockfile.

```sh
npm ci
npm run generate
npm test
npm run check
npm run prepare:zed
```

O último comando prepara uma cópia da extensão e uma revisão Git local da
gramática em `.zed-dev/`, sem criar commits no projeto ou publicar arquivos.
No Zed, abra **Extensions > Install Dev Extension**, selecione o diretório
`extension` impresso pelo comando e abra `examples/router.rsc`.
O Zed baixa automaticamente o wasi-sdk necessário para compilar a gramática.
Siga os requisitos de instalação de extensões da sua versão do Zed.
Após alterações, gere o parser novamente, execute os testes e prepare/reinstale
uma nova cópia local.

Em ambientes com cache de usuário somente leitura, configure um diretório gravável:

```sh
export npm_config_cache=/tmp/mikrotik-npm-cache
export XDG_CACHE_HOME=/tmp/mikrotik-tree-sitter-cache
```

## Cobertura

- Comentários `#`, continuação de linha, strings, escapes e interpolação.
- Variáveis simples e nomes entre aspas, palavras de controle e comandos `:`.
- Caminhos de menus, comandos comuns, parâmetros seguidos de `=` e operadores.
- IPv4/CIDR, IPv6, MAC, números e durações.
- Blocos, expressões e substituições de comandos, com pareamento e indentação.

Esta é uma gramática estrutural para destaque de sintaxe: não verifica a validade
de comandos, nomes de parâmetros ou intervalos de endereços no RouterOS.
A cobertura inicial não inclui todas as formas de data, IPv6 com zona/IPv4
embutido ou todas as combinações de escapes dentro de expressões interpoladas.
Os casos em `test/corpus/` e as capturas verificadas por `scripts/check.py`
documentam o comportamento testado. A aparência depende do tema do Zed e requer
verificação visual no editor.

## Publicação futura

O manifesto aponta para este repositório, na branch `master`.
Antes de distribuir a extensão, publique a gramática no repositório correto e
substitua `grammars.mikrotik.rev` pelo SHA do commit que a contém. Atualize as URLs
caso o destino seja outro fork. A instalação local acima funciona antes disso.
Nenhum push ou publicação é realizado pelos scripts.

Referências: [linguagens no Zed](https://zed.dev/docs/extensions/languages) e
[desenvolvimento de extensões](https://zed.dev/docs/extensions/developing-extensions).
