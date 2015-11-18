from binFunc import *

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

        makeEmptyBin(fileSystem, 28000)

        escreveIntBin(fileSystem, 0, self.bitmap)
        switchBitmap(fileSystem, 0)
        switchBitmap(fileSystem, 1)
        switchBitmap(fileSystem, 2)
        switchBitmap(fileSystem, 3)
        switchBitmap(fileSystem, 4)
        switchBitmap(fileSystem, 5)
        switchBitmap(fileSystem, 6)
        #switchBitmap(fileSystem, 3)
        if not getBitmap(fileSystem, 8):
            print "Encontrei espaco vazio"
        else:
            print "Sai daqui"
        escreveIntBin(fileSystem, 2, self.raiz)
        escreveIntBin(fileSystem, 4, self.dirs)

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

        return prox, data[4:]

    def leArquivo(self, endereco):
        prox, conteudo = self.leBloco(endereco)
        while prox != -1:
            print conteudo
            prox, conteudo = self.leBloco(prox)
        print conteudo


    # OBS: Nunca recebe um conteudo maior que 4 kB
    def escreveBloco(self, endereco, conteudo):
        ini = endereco*self.tam
        escreveIntervalo(self.nome, ini, ini+self.tam, conteudo)

    # Retorna o primeiro endereco de bloco vazio encontrado
    def FirstFit(self):
        for i in xrange(25000):
            if not getBitmap(self.nome, i):
                return i
        return "ACABOU O ESPACO"

if __name__=="__main__":
    teste = SistemaArquivos("primeiro")
    teste.escreveBloco(3, struct.pack("h", 4)+struct.pack("h", 0)+"aiudhaisudiausdiaushdiuashd")
    teste.escreveBloco(4, struct.pack("h", -1)+struct.pack("h", 0)+ "zczzijisdfj")
    teste.leArquivo(3)
    print "Encontrei o espaco ", teste.FirstFit()

    
