
msg = 'CMD|nick olos'

tipo, contenido = msg.split("|",1)
print(contenido)

cmd, arg = contenido.split(" ",1)

if cmd == 'exit':
    print(cmd)

if cmd  == 'nick':
    print(arg)