import readline



if __name__ == "__main__":
    cmd = raw_input("[ep3]: ").split()
    
    while cmd[0] != "sai":
       
        if   cmd[0] == "mount":
            print "Quero montar o sistema de arquivos"

        elif cmd[0] == "cp":
            print "Quero copiar"

        elif cmd[0] == "mkdir":
            print "Cria diretorio"

        elif cmd[0] == "rmdir":
            print "Apaga diretorio, se nao vazio, avisa o que apagou"

        elif cmd[0] == "cat":
            print "Mostra conteudo de arquivo"

        elif cmd[0] == "touch":
            print "Atualiza ultimo acesso ou cria novo arquivo"

        elif cmd[0] == "rm":
            print "Quero remover o arquivo"

        elif cmd[0] == "ls":
            print "Listar nome, tamanho em bytes e ultima modificacao"
            
        elif cmd[0] == "find":
            print "Quero buscar um arquivo a partir de um diretorio"

        elif cmd[0] == "df":
            print "Imprime informacoes"

        elif cmd[0] == "umount":
            print "Devo desmontar o sistema de arquivos"
            
        cmd = raw_input("[ep3]: ").split()
