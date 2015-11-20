import readline
import binFunc
from sistema import *
import time
#import arquivo
#import diretorio



if __name__ == "__main__":
    montado = False

    cmd = raw_input("[ep3]: ").split()
    
    while cmd[0] != "sai":
       
        if   cmd[0] == "mount":
            #print "Quero montar o sistema de arquivos"
            try:
                nome = cmd[1]

                # Teste de tempo de criacao do arquivo
                #ini = time.time()
                fileSystem = SistemaArquivos(nome)
                #fim = time.time()
            
                #print "Demorou exatamente ", fim - ini
                montado = True
                print "Sistema de arquivos", nome, "montado com sucesso"
            except IndexError:
                print "Voce precisa digitar o caminho do sistema de arquivos"

            
        elif cmd[0] == "cp" and montado:
            print "Quero copiar"

            try:
                origem  = cmd[1]
                destino = cmd[2]

                try:
                    f = open(origem, "r")
                    f.close()

                    #arquivo = Arquivo(destino)
                    #arquivo.cp(origem)

                except IOError:
                    print "Arquivo origem nao existe"

            except IndexError:
                print "Voce precisa digitar origem e destino"

        elif cmd[0] == "mkdir" and montado:
            print "Cria diretorio"
            pasta = Diretorio(fileSystem.getRaiz())
            pasta.mkdir(cmd[1])

        elif cmd[0] == "rmdir" and montado:
            print "Apaga diretorio, se nao vazio, avisa o que apagou"

        elif cmd[0] == "cat" and montado:
            print "Mostra conteudo de arquivo"
            try:
                nome = cmd[1]

                bloco = fileSystem.devolveBloco(nome)
                fileSystem.leArquivo(bloco)

            except IndexError:
                print "Digite o caminho completo do arquivo"

        elif cmd[0] == "touch" and montado:
            #print "Atualiza ultimo acesso ou cria novo arquivo"
            try:
                nome = cmd[1]

                bloco = fileSystem.devolveBloco(nome)
                if bloco:
                    print "Ja existia, atualizei"
                    fileSystem.atualizaAcesso(nome)
                else:

                    print "Tive que criar pq nao existia"
                    fileSystem.criaArquivo(nome)
                        
                        
                    
                    
            except IndexError:
                print "Voce precisa escrever o nome completo do arquivo"

        elif cmd[0] == "rm" and montado:
            print "Quero remover o arquivo"

        elif cmd[0] == "ls" and montado:
            print "Listar nome, tamanho em bytes e ultima modificacao"
            
        elif cmd[0] == "find" and montado:
            #print "Quero buscar um arquivo a partir de um diretorio"
            try:
                diretorio = cmd[1]
                arquivo   = cmd[2]
                fileSystem.find(diretorio, arquivo)

            except IndexError:
                print "Voce precisa digitar diretorio e arquivo"

        elif cmd[0] == "df" and montado:
            print "Imprime informacoes"

        elif cmd[0] == "umount" and montado:
            print "Devo desmontar o sistema de arquivos"
            montado = False
            
        cmd = raw_input("[ep3]: ").split()


