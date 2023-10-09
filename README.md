# Chat via socket

## Configurando

Para rodar tanto cliente ou servidor, é necessário editar as configurações de IP e remover o comentário da linha que especifica qual o protocolo desejado.

## Rodando e utilizando o chat

Para rodar o chat, é necessário primeiro rodar o arquivo `src/server_main.py` e em seguida `src/client_main.py` (pode-se rodar quantos clientes quiser).

No terminal do pode-se utilizar os seguintes comandos no terminal do cliente<br/>

# Comandos de controle

```python
# Conecta e cadastra usuário
/connect <user_name>

# Desconecta e remove cadastro de usuário no servidor
/exit
```

# Comandos de controle

```python

# Mensagem privada
/privmsg <nome-destino> <mensagem>

# Mensagem broadcast
/msg <mensagem>

# Envia arquivo privado
/privfile <nome-destino> <filepath>

# Envia arquivo em broadcast
/file <filepath>
```
