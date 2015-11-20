from binFunc import *
from datetime import datetime
import time

ent = 71

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

        print "Estou criando um novo sistema de arquivos", self.bitmap, self.raiz, self.dirs

        # Demora para criar um arquivo de 100MB
        makeEmptyBin(fileSystem, 100000)

        escreveIntBin(fileSystem, 0, self.bitmap)
        escreveIntBin(fileSystem, 2, self.raiz)
        escreveIntBin(fileSystem, 4, self.dirs)
        
        for i in xrange(7):
            switchBitmap(fileSystem, i)

        # Inicializa o diretorio raiz com 5 blocos
        
        self.escreveBloco(2, struct.pack("h", 3)+struct.pack("h", 0))
        self.escreveBloco(3, struct.pack("h", 4)+struct.pack("h", 0))
        self.escreveBloco(4, struct.pack("h", 5)+struct.pack("h", 0))
        self.escreveBloco(5, struct.pack("h", 6)+struct.pack("h", 0))
        self.escreveBloco(6, struct.pack("h", -1)+struct.pack("h", 0))


    def criaDiretorio(self, nome):
        self.criaArquivo(nome)
        
        ant = self.devolveBloco(nome)
        for i in xrange(3):
            novo = self.FirstFit()
            if novo:
                self.escreveBloco(ant, struct.pack("h", novo)+struct.pack("h", 0))
            else:
                print "Acabou o espaco em criaDiretorio"
                break

            ant = novo
        self.escreveBloco(ant, struct.pack("h", -1)+struct.pack("h", 0))

    def devolveBloco(self, nome):
        # Tamanho da entrada em bytes
        global ent
        # Verifica se o nome e a raiz
        if nome == "/":
            return self.raiz

        # Faz uma busca a partir da raiz
        else:
           
            caminho = nome.split("/")
            atual = [self.raiz]

            for i in xrange(1, len(caminho)):

                prox, cont, conteudo = self.leBloco(atual[0])
                
                for j in xrange(cont):
                    if conteudo[0+j*ent:(len(caminho[i]))+j*ent] == caminho[i]:
                        atual = struct.unpack("h", conteudo[12+j*ent:14+j*ent])
                        if i == len(caminho)-1:
                            return atual[0]
                        else:
                            break
                    
            return False 

    
    def devolveEntrada(self, bloco, nome):
        global ent
        prox, cont, conteudo = self.leBloco(bloco)
                
        for j in xrange(cont):
            novo = self.ajustaNome(conteudo[0+j*ent:12+j*ent])
            if novo == nome:
                return j*ent

        return False


    def find(self, diretorio, arquivo):
        global ent
        end = self.devolveBloco(diretorio)

        prox, cont, conteudo = self.leBloco(end)

        if cont == -1:
            return

        for j in xrange(cont):
            nome = self.ajustaNome(conteudo[0+j*ent:12+j*ent])
            if nome == arquivo:
                if diretorio == "/":
                    print diretorio+arquivo
                else:
                    print diretorio+"/"+arquivo
                return        
            else:
                if diretorio == "/":
                    self.find(diretorio+nome, arquivo)
                else:
                    self.find(diretorio+"/"+nome, arquivo)



    def ajustaNome(self, a):
        b = []
        for i in xrange(len(a)):
            if a[i] != "\0":
                b.append(a[i])

        b = "".join(b)
        return b


    def esticaNome(self, a):
        b = list(a)
        while len(b) < 12:
            b.append("\0")

        b = "".join(b)
        return b
        


    def getRaiz(self):
        return self.raiz


    #..............................
    # Le o bloco de numero "bloco"
    #..............................
    def leBloco(self, bloco):
        ini = bloco*self.tam
        data = leIntervalo(self.nome, ini, ini+self.tam)
        # Ponteiro para o proximo bloco
        prox = int(struct.unpack("h", data[0:2])[0])
        
        # Contador de conteudo
        cont = int(struct.unpack("h", data[2:4])[0])

        # Retorna o ponteiro para o proximo bloco, o contador, e o conteudo
        return prox, cont, data[4:]


    #.............................................................
    # Imprime o conteudo do arquivo que comeca no bloco "endereco"
    #.............................................................
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


    #......................................................
    # Retorna o primeiro endereco de bloco vazio encontrado
    #......................................................
    def FirstFit(self):
        # Atualizar para 25000 que eh a qtd de blocos disponiveis
        for i in xrange(25):
            if not getBitmap(self.nome, i):
                return i
        print "ACABOU O ESPACO"
        return False


    #..........................................
    # Devolve o momento atual em 16 caracteres
    #..........................................
    def getTimeNow(self):
        data = datetime.now()
        now = str(data.year)+"-"+str(data.month)+"-"+str(data.day)+" "+str(data.hour)+":"+str(data.minute)
        return now



    def atualizaAcesso(self, arquivo):
        caminho = arquivo.split("/")

        if len(caminho) == 2:
            pai = "/"
        else:
            pai = "/".join(caminho[:(len(caminho)-1)])

        blocoPai = self.devolveBloco(pai)

        prox, cont, conteudo = self.leBloco(blocoPai)
        
        entrada = self.devolveEntrada(blocoPai, caminho[(len(caminho)-1)])

        # Posicao da data de acesso no conteudo do diretorio
        conteudo = conteudo[:46]+self.getTimeNow()+conteudo[62:]
        
        self.escreveBloco(blocoPai, struct.pack("h", prox)+struct.pack("h", cont)+conteudo)


    def criaArquivo(self, arquivo):
        global ent
        caminho = arquivo.split("/")

        if arquivo == "/":
            return True

        if len(caminho) == 2:
            pai = "/"
        else:
            pai = "/".join(caminho[:(len(caminho)-1)])

        blocoPai = self.devolveBloco(pai)

        prox, cont, conteudo = self.leBloco(blocoPai)

        if cont == -1:
            print "O caminho digitado nao e valido,", caminho[(len(caminho)-2)], "nao eh um diretorio."
            return False

        ant = blocoPai
        while prox != -1 and cont == 56:
            ant = prox
            prox, cont, conteudo = self.leBloco(prox)

        espaco = self.FirstFit()
        if espaco:
            # Marco o espaco como ocupado
            switchBitmap(self.nome, espaco)
            # Adiciono entrada na pasta pai
            entrada = self.esticaNome(caminho[len(caminho)-1])+struct.pack("h", espaco)+self.getTimeNow()+self.getTimeNow()+self.getTimeNow()+"000000000"

            conteudo = conteudo[:cont*ent]+entrada+conteudo[(cont+1)*ent:]
            cont += 1
        
            self.escreveBloco(ant, struct.pack("h", prox)+struct.pack("h", cont)+conteudo)

            # Escrevo o conteudo do bloco espaco
            self.escreveBloco(espaco, struct.pack("h", -1)+struct.pack("h", -1))
            return True
        else:
            print "ACABOU O ESPACO em criaArquivo"
            return False


#............................
# MAIN
#............................
if __name__=="__main__":
    teste = SistemaArquivos("primeiro")
    # Raiz
    #teste.escreveBloco(2, struct.pack("h", 4)+struct.pack("h", 2)+"casa\0\0\0\0\0\0\0\0"+struct.pack("h", 5)+teste.getTimeNow()+teste.getTimeNow()+teste.getTimeNow()+"000000040"+"comida\0\0\0\0\0\0"+struct.pack("h", 6)+teste.getTimeNow()+teste.getTimeNow()+teste.getTimeNow()+"000000080")

    #teste.escreveBloco(4, struct.pack("h", -1)+struct.pack("h", 0)+ "zczzijisdfj")
    # CASA
    #teste.escreveBloco(5, struct.pack("h", -1)+struct.pack("h", 1)+"gato\0\0\0\0\0\0\0\0"+struct.pack("h", 7)+teste.getTimeNow()+teste.getTimeNow()+teste.getTimeNow()+"000000080")

    #teste.escreveBloco(6, struct.pack("h", -1)+struct.pack("h", 1)+"racao\0\0\0\0\0\0\0"+struct.pack("h", 9)+teste.getTimeNow()+teste.getTimeNow()+teste.getTimeNow()+"000000080"+"AQUI ESTA O CONTEUDO DO ARQUIVO COMIDA")

    #teste.escreveBloco(7, struct.pack("h", -1)+struct.pack("h", -1)+"AQUI ESTA O CONTEUDO DO ARQUIVO GATO")

    #teste.escreveBloco(9, struct.pack("h", -1)+struct.pack("h", -1)+"AQUI ESTA O CONTEUDO DO ARQUIVO RACAO")

    #teste.leArquivo(2)
    #teste.leArquivo(5)
    #teste.devolveBloco("/casa/gato")
    #teste.devolveBloco("/comida/racao")
    #teste.leArquivo(6)
    #teste.leArquivo(teste.devolveBloco("/casa/gato"))

    #print teste.devolveBloco("/oi")

    #teste.find("/", "casa")

    #teste.leArquivo(5)
 
    #teste.atualizaAcesso("/casa/gato")
    #teste.leArquivo(5)

    #teste.leArquivo(teste.devolveBloco("/comida"))
    #teste.criaArquivo("/comida/agua")
    #teste.leArquivo(teste.devolveBloco("/comida"))
    #teste.leArquivo(teste.devolveBloco("/comida/agua"))

    teste.criaDiretorio("/roupa")
    teste.leArquivo(2)
    teste.criaDiretorio("/casa")
    teste.leArquivo(2)
