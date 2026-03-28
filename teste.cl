class Main inherits IO {
    -- Este é um teste com arquivo externo
    
    numero : Int <- 42;
    texto : String <- "Estou lendo de um arquivo!";
    
    (* Comentário de bloco
       para testar se o lexer pula as linhas certinho.
    *)
    
    main() : Object {
        out_string(texto)
    };
    
    # ? -- Dois caracteres inválidos para forçar nossa função t_error
};