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
            try:
                nome = cmd[1]

                fileSystem = SistemaArquivos(nome)
                montado = True
                print "Sistema de arquivos", nome, "montado com sucesso"

            except IndexError:
                print "Voce precisa digitar o caminho do sistema de arquivos"

            
        elif cmd[0] == "cp" and montado:
            try:
                origem  = cmd[1]
                destino = cmd[2]

                try:
                    f = open(origem, "r")
                    f.close()

                    fileSystem.copiaArquivo(origem, destino)

                except IOError:
                    print "Arquivo origem nao existe"

            except IndexError:
                print "Voce precisa digitar origem e destino"

        elif cmd[0] == "mkdir" and montado:
             try:
                nome = cmd[1]

                fileSystem.criaDiretorio(nome)
 
             except IndexError:
                print "Digite o nome completo do diretorio"
            

        elif cmd[0] == "rmdir" and montado:
            try:
                nome = cmd[1]

                fileSystem.removeDiretorio(nome)
            except IndexError:
                print "Digite o nome completo do diretorio"

        elif cmd[0] == "cat" and montado:
            try:
                nome = cmd[1]

                bloco = fileSystem.devolveBloco(nome)
                fileSystem.leArquivo(bloco)

            except IndexError:
                print "Digite o caminho completo do arquivo"


        elif cmd[0] == "touch" and montado:
            try:
                nome = cmd[1]

                bloco = fileSystem.devolveBloco(nome)
                if bloco:
                    #"Ja existia, atualizei"
                    fileSystem.atualizaAcesso(nome)
                else:
                    #"Tive que criar pq nao existia"
                    fileSystem.criaArquivo(nome)
                    
            except IndexError:
                print "Voce precisa escrever o nome completo do arquivo"


        elif cmd[0] == "rm" and montado:
            try:
                nome = cmd[1]

                fileSystem.removeArquivo(nome)

            except IndexError:
                print "Digite o caminho completo para o arquivo"

        elif cmd[0] == "ls" and montado:
            try:
                nome = cmd[1]

                fileSystem.leArquivo(fileSystem.devolveBloco(nome))

            except IndexError:
                print "Digite o caminho completo do diretorio"
            

        elif cmd[0] == "find" and montado:
            try:
                diretorio = cmd[1]
                arquivo   = cmd[2]
                fileSystem.find(diretorio, arquivo)

            except IndexError:
                print "Voce precisa digitar diretorio e arquivo"


        elif cmd[0] == "df" and montado:
            fileSystem.df()


        elif cmd[0] == "umount" and montado:
            print "Sistema de arquivos", fileSystem.nome, "desmontado."
            fileSystem.FAT = [None for i in xrange(25000)]
            montado = False
            

        cmd = raw_input("[ep3]: ").split()


