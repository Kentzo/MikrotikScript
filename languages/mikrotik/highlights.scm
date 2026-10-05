(identifier) @variable
(comment) @comment
(string) @string
(escape_sequence) @string.escape
(variable) @variable
(keyword) @keyword
(builtin) @function
(boolean) @boolean
(number) @number
(duration) @number
(ipv4) @string.special
(ipv6) @string.special
(mac_address) @string.special
(internal_id) @constant
(path) @function
(operator) @operator

((identifier) @function
  (#any-of? @function "add" "set" "get" "print" "find" "remove" "enable" "disable"
    "export" "import" "reset" "run" "move" "monitor" "ping" "traceroute"))

; Property names followed by an assignment, e.g. address=192.0.2.1/24.
((identifier) @property . (operator) @_equals
  (#eq? @_equals "="))

["{" "}" "[" "]" "(" ")"] @punctuation.bracket
[";" ","] @punctuation.delimiter
