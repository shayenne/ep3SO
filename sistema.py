from binFunc import *
from datetime import datetime


class SistemaArquivos:

    nome = None
    raiz = None
    dirs = []
    bitmap = None
    FAT = []
    tam = 4000

    def __init__(self, nome):
        # se o sistema de arquivos nao existe, criar um novo
        self.nome = nome
        try:
            with open(self.nome, 'rb') as fileSystem:
                print "Sistema existe"
                self.bitmap = leIntBin(self.nome, 0)
                self.raiz = leIntBin(self.nome, 2)
                self.dirs = leIntBin(self.nome, 4)

                print self.bitmap, self.raiz, self.dirs
                
        except IOError:
            self.criaSistemaArquivos()

    def criaSistemaArquivos(self):
        fileSystem = self.nome
        # Endereco de blocos
        self.bitmap = 1
        self.raiz = 2
        self.dirs = 3

        print "Estou criando um novo arquivo ", self.bitmap, self.raiz, self.dirs

        # Demora para criar um arquivo de 100MB
        makeEmptyBin(fileSystem, 100000)

        escreveIntBin(fileSystem, 0, self.bitmap)
        escreveIntBin(fileSystem, 2, self.raiz)
        escreveIntBin(fileSystem, 4, self.dirs)
        
        for i in xrange(7):
            switchBitmap(fileSystem, i)


    def devolveBloco(self, nome):
        # Tamanho da entrada em bytes
        ent = 71
        # Verifica se o nome e a raiz
        if nome == "/":
            print "ESSE e o bloco ", self.raiz
            return self.raiz

        # Faz uma busca a partir da raiz
        else:
           
            caminho = nome.split("/")
            atual = [self.raiz]
            print "Entrei aqui"
            for i in xrange(1, len(caminho)):
                print "O atual e", atual
                prox, cont, conteudo = self.leBloco(atual[0])
                print conteudo[0:12], caminho[i] 
                for j in xrange(cont):
                    print "Esse e o valor de j", j,  conteudo[0+j*ent:(len(caminho[i]))+j*ent], caminho[i]
                    if conteudo[0+j*ent:(len(caminho[i]))+j*ent] == caminho[i]:
                        print "Entrei no if"
                        atual = struct.unpack("h", conteudo[12+j*ent:14+j*ent])
                        if i == len(caminho)-1:
                            print "Esse e o bloco ",atual[0]
                            return atual[0]
                        else:
                            print "Entrei no else"
                            break
                    
                        




    def find(self, diretorio, arquivo):
        #vazio
        return None

        
    def getRaiz(self):
        return self.raiz


    # Le o bloco de numero "bloco" e retorna o proximo apontado pelo bloco
    # lido
    def leBloco(self, bloco):
        ini = bloco*self.tam
        data = leIntervalo(self.nome, ini, ini+self.tam)
        # Ponteiro para o proximo bloco
        prox = int(struct.unpack("h", data[0:2])[0])
        print prox
        # Contador de conteudo
        cont = int(struct.unpack("h", data[2:4])[0])
        print cont

        return prox, cont, data[4:]

    def leArquivo(self, endereco):
        prox, cont, conteudo = self.leBloco(endereco)
        while prox != -1:
            print conteudo
            prox, cont, conteudo = self.leBloco(prox)
        print conteudo


    # OBS: Nunca recebe um conteudo maior que 4 kB
    # Recebe um conteudo e escreve no bloco apontado por endereco
    def escreveBloco(self, endereco, conteudo):
        ini = endereco*self.tam
        escreveIntervalo(self.nome, ini, ini+self.tam, conteudo)

    # Retorna o primeiro endereco de bloco vazio encontrado
    def FirstFit(self):
        for i in xrange(25000):
            if not getBitmap(self.nome, i):
                return i
        print "ACABOU O ESPACO"
        return False


    # Devolve o momento atual em 16 caracteres
    def getTimeNow(self):
        data = datetime.now()
        now = str(data.year)+"-"+str(data.month)+"-"+str(data.day)+" "+str(data.hour)+":"+str(data.minute)
        return now


if __name__=="__main__":
    teste = SistemaArquivos("primeiro")
    # Raiz
    teste.escreveBloco(2, struct.pack("h", 4)+struct.pack("h", 2)+"casa\0\0\0\0\0\0\0\0"+struct.pack("h", 5)+teste.getTimeNow()+teste.getTimeNow()+teste.getTimeNow()+"000000040"+"comida\0\0\0\0\0\0"+struct.pack("h", 6)+teste.getTimeNow()+teste.getTimeNow()+teste.getTimeNow()+"000000080")

    teste.escreveBloco(4, struct.pack("h", -1)+struct.pack("h", 0)+ "zczzijisdfj")
    # CASA
    teste.escreveBloco(5, struct.pack("h", -1)+struct.pack("h", 1)+"gato\0\0\0\0\0\0\0\0"+struct.pack("h", 7)+teste.getTimeNow()+teste.getTimeNow()+teste.getTimeNow()+"000000080")

    teste.escreveBloco(6, struct.pack("h", -1)+struct.pack("h", -1)+"AQUI ESTA O CONTEUDO DO ARQUIVO COMIDA")

    teste.escreveBloco(7, struct.pack("h", -1)+struct.pack("h", -1)+"AQUI ESTA O CONTEUDO DO ARQUIVO GATO")

    teste.leArquivo(2)
    teste.leArquivo(5)
    teste.devolveBloco("/casa/gato")
    teste.devolveBloco("/comida")
    teste.leArquivo(6)


    
