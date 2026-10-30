grammar Lang;

@header {package hello;}

// Parser
lang_program : PROGRAM EOF;

// Lexer
PROGRAM : 'hello';
