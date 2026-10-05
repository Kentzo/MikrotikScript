(block "{" @open "}" @close)
(command_substitution "[" @open "]" @close)
(parenthesized_expression "(" @open ")" @close)
((string "\"" @open "\"" @close) (#set! rainbow.exclude))
