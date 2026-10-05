// A structural highlighting grammar, not a RouterOS configuration validator.
module.exports = grammar({
  name: 'mikrotik',

  extras: $ => [/\s/, $.comment, $.line_continuation],
  word: $ => $.identifier,

  rules: {
    source_file: $ => repeat($._item),
    _item: $ => choice(
      $.block, $.command_substitution, $.parenthesized_expression,
      $.string, $.variable, $.keyword, $.builtin, $.boolean,
      $.ipv4, $.ipv6, $.mac_address, $.duration, $.number,
      $.path, $.identifier, $.internal_id, $.operator, ';', ',',
    ),
    block: $ => seq('{', repeat($._item), '}'),
    command_substitution: $ => seq('[', repeat($._item), ']'),
    parenthesized_expression: $ => seq('(', repeat($._item), ')'),
    comment: _ => token(seq('#', /[^\r\n]*/)),
    line_continuation: _ => token(seq('\\', /\r?\n/)),
    string: $ => seq('"', repeat(choice(
      $.string_content, $.escape_sequence, $.variable,
      $.string_expression,
    )), '"'),
    string_content: _ => token(prec(-1, /[^"\\$]+/)),
    escape_sequence: _ => token(seq('\\', choice(/[0-9a-fA-F]{2}/, /[^\r\n]/, /\r?\n/))),
    variable: $ => seq('$', choice($.identifier, $.number, $.quoted_variable)),
    quoted_variable: _ => token(seq('"', repeat(choice(/[^"\\\r\n]/, /\\[^\r\n]/)), '"')),
    string_expression: $ => seq('$', choice($.parenthesized_expression, $.command_substitution)),
    keyword: _ => choice(
      ':local', ':global', ':if', ':else', ':for', ':foreach', ':while',
      ':do', ':onerror', ':on-error', ':return', ':break', ':continue',
      'do', 'else', 'from', 'to', 'step', 'in', 'where', 'and', 'or', 'not',
    ),
    builtin: _ => token(/:[a-zA-Z][a-zA-Z0-9_-]*/),
    boolean: _ => choice('true', 'false', 'yes', 'no'),
    ipv4: _ => token(prec(2, /[0-9]{1,3}(\.[0-9]{1,3}){3}(\/[0-9]{1,2})?/)),
    mac_address: _ => token(prec(3, /[0-9a-fA-F]{2}(:[0-9a-fA-F]{2}){5}/)),
    ipv6: _ => token(prec(2, choice(
      /[0-9a-fA-F]{1,4}(:[0-9a-fA-F]{1,4}){2,7}(\/[0-9]{1,3})?/,
      /([0-9a-fA-F]{1,4}(:[0-9a-fA-F]{1,4})*)?::([0-9a-fA-F]{1,4}(:[0-9a-fA-F]{1,4})*)?(\/[0-9]{1,3})?/,
    ))),
    duration: _ => token(prec(3, choice(
      /([0-9]+(ms|us|ns|s|m|h|d|w))+/, /[0-9]+:[0-9]{2}:[0-9]{2}(\.[0-9]+)?/,
    ))),
    number: _ => token(choice(/0[xX][0-9a-fA-F]+/, /[0-9]+(\.[0-9]+)?/)),
    path: _ => token(prec(1, /\/[a-zA-Z][a-zA-Z0-9_-]*(\/[a-zA-Z][a-zA-Z0-9_-]*)*/)),
    identifier: _ => /[a-zA-Z_][a-zA-Z0-9_.-]*/,
    internal_id: _ => token(/\*[0-9a-fA-F]+/),
    operator: _ => choice('=', '!=', '<', '>', '<=', '>=', '+', '-', '*', '/', '%',
      '!', '&&', '||', '~', '|', '^', '&', '<<', '>>', '.', '->', ':'),
  },
});
