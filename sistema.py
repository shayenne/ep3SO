from binFunc import *
from datetime import datetime
import time
from termcolor import colored, cprint


ent = 70

class SistemaArquivos:

    nome = None
    raiz = None
    dirs = []
    bitmap = None
    FAT = [None for i in xrange(25000)]
    tam = 4000

    #..................................................
    def __init__(self, nome):
        # se o sistema de arquivos nao existe, criar um novo
        self.nome = nome
    
        self.inicializaFAT()
        #print self.FAT
        try:
            with open(self.nome, 'rb') as fileSystem:
                print "Sistema existe"
                self.bitmap = leIntBin(self.nome, 0)
                self.raiz = leIntBin(self.nome, 2)
                self.dirs = leIntBin(self.nome, 4)

                print self.bitmap, self.raiz, self.dirs
                
        except IOError:
            self.criaSistemaArquivos()


    #......................................................
    def criaSistemaArquivos(self):
        fileSystem = self.nome
        # Endereco de blocos
        self.bitmap = 1
        self.raiz = 2
        self.dirs = 3

        print "Estou criando um novo sistema de arquivos", self.bitmap, self.raiz, self.dirs

        # Demora para criar um arquivo de 100MB
        makeEmptyBin(fileSystem, 100000000)

        escreveIntBin(fileSystem, 0, self.bitmap)
        escreveIntBin(fileSystem, 2, self.raiz)
        escreveIntBin(fileSystem, 4, self.dirs)
        
        # Inicializa o diretorio raiz com 5 blocos
        startMM(self.nome)
        for i in xrange(7):
            switchBitmap(fileSystem, i)

        
        self.escreveBloco(2, struct.pack("h", 3)+struct.pack("h", 0))
        self.escreveBloco(3, struct.pack("h", 4)+struct.pack("h", 0))
        self.escreveBloco(4, struct.pack("h", 5)+struct.pack("h", 0))
        self.escreveBloco(5, struct.pack("h", 6)+struct.pack("h", 0))
        self.escreveBloco(6, struct.pack("h", -1)+struct.pack("h", 0))
        endMM()

    #..................................................................
    def inicializaFAT(self):
       
        startMM(self.nome)
        i = 2
        while i < 25000:
            if self.FAT[i] == None and usedBitmap(self.nome, i):
                ant = i
                prox, c, cont = self.leBloco(ant)
                while prox != -1 and prox != 0:
                    self.FAT[ant] = prox
                    print "Mudei a entrada", ant, " da FAT para", prox
                    ant = prox
                    prox, c, cont = self.leBloco(ant)
                    print "Esse e o proximo", prox
                if prox != 0:
                    self.FAT[ant] = prox
                    print "Mudei a entrada", ant, " da FAT para", prox
            i += 1

        endMM()

    #................................................................
    def criaDiretorio(self, nome):
        self.criaArquivo(nome)
        
        ant = self.devolveBloco(nome)
        
        self.FAT[ant] = None
        # Diminui a qtd de bitmaps
        startMM(self.nome)
        for i in xrange(4):
            novo = self.FirstFit()
            print "FirstFit devolveu", novo, "em criaDiretorio"
            if novo:
                self.escreveBloco(ant, struct.pack("h", novo)+struct.pack("h", 0))
                switchBitmap(self.nome, novo)
            else:
                print "Acabou o espaco em criaDiretorio"
                break

            ant = novo
        
        self.escreveBloco(ant, struct.pack("h", -1)+struct.pack("h", 0))
        # Finaliza o bitmap
        endMM()
        self.inicializaFAT()

    #..................................................................
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
                startMM(self.nome)
                prox, cont, conteudo = self.leBloco(atual[0])
                endMM()
                for j in xrange(cont):
                    if conteudo[0+j*ent:(len(caminho[i]))+j*ent] == caminho[i]:
                        atual = struct.unpack("h", conteudo[12+j*ent:14+j*ent])
                        if i == len(caminho)-1:
                            return atual[0]
                        else:
                            break
                    
            return False 

    
    #..................................................................
    def devolveEntrada(self, bloco, nome):
        global ent
        startMM(self.nome)
        prox, cont, conteudo = self.leBloco(bloco)
                
        for j in xrange(cont):
            novo = self.ajustaNome(conteudo[0+j*ent:12+j*ent])
            if novo == nome:
                return j*ent

        return False

    #................................................................
    def find(self, diretorio, arquivo):
        global ent
        end = self.devolveBloco(diretorio)
        startMM(self.nome)
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


    #.....................................................................
    def ajustaNome(self, a):
        b = []
        for i in xrange(len(a)):
            if a[i] != "\0":
                b.append(a[i])

        b = "".join(b)
        return b

    #......................................................................
    def esticaNome(self, a):
        b = list(a)
        while len(b) < 12:
            b.append("\0")

        b = "".join(b)
        return b
        

    #......................................................................
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
        global ent
        startMM(self.nome)
        prox, cont, conteudo = self.leBloco(endereco)

        
        while prox != -1:
            if cont != -1:# Eh um diretorio
                for i in xrange(cont):
                    nome = self.ajustaNome(conteudo[0+i*ent:12+i*ent])
                    bl = struct.unpack("h", conteudo[12+i*ent:14+i*ent])

                    p, c, ctd = self.leBloco(bl[0])
                    #print "O contador e", c
                    if c == -1:
                        #tam  = int(str(conteudo[62+i*ent:71+i*ent]))
                        tam  = struct.unpack("q", conteudo[62+i*ent:70+i*ent])[0] 
                        mod  = conteudo[30+i*ent:46+i*ent]
                        print nome, tam, mod
                    else:
                        print colored(nome, 'blue', attrs=['bold'])
            else:
                print conteudo

            prox, cont, conteudo = self.leBloco(prox)

        # Ultimo bloco
        if cont != -1: # Eh um diretorio
            for i in xrange(cont):
                nome = self.ajustaNome(conteudo[0+i*ent:12+i*ent])
                bl = struct.unpack("h", conteudo[12+i*ent:14+i*ent])
                
                p, c, ctd = self.leBloco(bl[0])
                if c == -1:
                    #tam  = int(str(conteudo[62+i*ent:71+i*ent]))
                    tam  = struct.unpack("h", conteudo[62+i*ent:64+i*ent])[0]
                    mod  = conteudo[30+i*ent:46+i*ent]
                    print nome, tam, mod
                else:
                    print "[{}]".format(nome)
        else:
            print conteudo
            
        endMM()

    #.............................................................
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
        x = getBitmap(self.nome, 25000)
        while x >= 0 and x <= 6:
            switchBitmap(self.nome, x)
            x = getBitmap(self.nome, 25000)
    
        return x
        print "ACABOU O ESPACO"
        return False


    #..........................................
    # Devolve o momento atual em 16 caracteres
    #..........................................
    def getTimeNow(self):
        data = datetime.now()
        mes = data.month
        if mes < 10:
            mes = str("0"+str(mes))
        dia = data.day
        if dia < 10:
            dia = str("0"+str(dia))
        hora = data.hour
        if hora < 10:
            hora = str("0"+str(hora))
        minuto = data.minute
        if minuto < 10:
            minuto = str("0"+str(minuto))
        now = str(data.year)+"-"+str(mes)+"-"+str(dia)+" "+str(hora)+":"+str(minuto)
        return now


    #.............................................
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
        conteudo = conteudo[:46+entrada]+self.getTimeNow()+conteudo[62+entrada:]
        startMM(self.nome)
        self.escreveBloco(blocoPai, struct.pack("h", prox)+struct.pack("h", cont)+conteudo)
        endMM()

    #.............................................
    def atualizaTamanho(self, arquivo, tamanho):
        caminho = arquivo.split("/")

        if len(caminho) == 2:
            pai = "/"
        else:
            pai = "/".join(caminho[:(len(caminho)-1)])
        startMM(self.nome)
        blocoPai = self.devolveBloco(pai)

        startMM(self.nome)
        prox, cont, conteudo = self.leBloco(blocoPai)
        
        entrada = self.devolveEntrada(blocoPai, caminho[(len(caminho)-1)])

        # Posicao da data de acesso no conteudo do diretorio
        conteudo = conteudo[:62+entrada]+struct.pack("q", tamanho)
        
        self.escreveBloco(blocoPai, struct.pack("h", prox)+struct.pack("h", cont)+conteudo)
        endMM()

    #..................................................
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
        # Diminui a qtd de bitmaps
        startMM(self.nome)
        prox, cont, conteudo = self.leBloco(blocoPai)

        if cont == -1:
            print "O caminho digitado nao e valido,", caminho[(len(caminho)-2)], "nao eh um diretorio."
            return False
        
        ant = blocoPai
        while prox != -1 and cont == 57:
            ant = prox
            prox, cont, conteudo = self.leBloco(ant)
        
        espaco = self.FirstFit()
        endMM()
        print "FirstFit devolveu", espaco, "em criaArquivo"
        if espaco:
            startMM(self.nome)
            # Marco o espaco como ocupado
            #if not usedBitmap(self.nome, espaco):
            switchBitmap(self.nome, espaco)
            # Adiciono entrada na pasta pai
            entrada = self.esticaNome(caminho[len(caminho)-1])+struct.pack("h", espaco)+self.getTimeNow()+self.getTimeNow()+self.getTimeNow()+struct.pack("q", 0)

            conteudo = conteudo[:cont*ent]+entrada+conteudo[(cont+1)*ent:]
            cont += 1
            
            self.escreveBloco(ant, struct.pack("h", prox)+struct.pack("h", cont)+conteudo)

            # Escrevo o conteudo do bloco espaco
            self.escreveBloco(espaco, struct.pack("h", -1)+struct.pack("h", -1))
            self.FAT[espaco] = -1
            endMM()
            self.inicializaFAT()
            return True
        else:
            print "ACABOU O ESPACO em criaArquivo"
            return False



    #...................................................................
    def copiaArquivo(self, origem, destino):
        self.criaArquivo(destino)

        arquivo = open(origem, "r")
        
        arquivo.seek(0, 2)
        tamanho = arquivo.tell()
        
        arquivo.seek(0)
        buf = arquivo.read(tamanho)
        arquivo.close()
        qtd = (tamanho / 3996) + 1

        bls = [self.devolveBloco(destino)]
        # Diminuir a criacao de bitmaps
        startMM(self.nome)
        for i in xrange(qtd-1):
            novo = self.FirstFit()
            print "FirstFit devolveu ", novo, "em copiaArquivo"
            if novo:
                bls.append(novo)
                switchBitmap(self.nome, novo)
                
            else:
                print "Nao foi possivel copiar o arquivo"
                for j in xrange(len(bls)):
                    switchBitmap(self.nome, bls[j])
                endMM()
                return
        endMM()
            
        startMM(self.nome)
        for i in xrange(qtd - 1):
            self.escreveBloco(bls[i], struct.pack("h", bls[i+1])+ struct.pack("h", -1)+buf[0+i*3996:(i+1)*3996])
            self.FAT[bls[i]] = bls[i+1]
            
        self.escreveBloco(bls[qtd-1], struct.pack("h", -1)+struct.pack("h", -1)+buf[(qtd-1)*3996:(qtd)*3996])
        self.FAT[bls[qtd-1]] = -1

        # Finaliza o bitmap usado no FirstFit
        endMM()

        print "Estou mandando escrever um tamanho de ", tamanho
        self.atualizaTamanho(destino, tamanho)
        self.inicializaFAT()


    #..................................................
    # REMOCAO
    #..................................................
    def removeArquivo(self, arquivo):
        global ent

        bl = self.devolveBloco(arquivo)
        
        startMM(self.nome)
        caminho = arquivo.split("/")

        if arquivo == "/":
            return True

        if len(caminho) == 2:
            pai = "/"
        else:
            pai = "/".join(caminho[:(len(caminho)-1)])

        blocoPai = self.devolveBloco(pai)
        startMM(self.nome)
        prox, cont, conteudo = self.leBloco(blocoPai)
        
        if cont == -1:
            print "O caminho digitado nao e valido"
            return False

        ant = blocoPai
        entrada = self.devolveEntrada(ant, caminho[len(caminho)-1])
        #print "Esse e o conteudo do arquivo pai e a entrada e", entrada, conteudo

        
        if entrada != 0:
            while not entrada and prox != -1:
                ant = prox
                prox, cont, conteudo = self.leBloco(ant)
                entrada = self.devolveEntrada(ant, caminho[len(caminho)-1])
            

        if entrada is not False:
            print "Achei", arquivo
            
            #print "Contador antes", cont
            cont -= 1
            #print "Contador depois", cont
            #print "Diretorio antes"
            #self.leArquivo(ant)
            if entrada / ent == cont:
                #print "Ultima"
                conteudo = conteudo[:(cont)*ent]+conteudo[(cont+1)*ent:]
                #print "Agora so tem ", cont, "arquivos"
                
            else:
                #print "Meio"
                ultima = conteudo[(cont)*ent:(cont+1)*ent]
                conteudo = conteudo[:entrada]+ultima+conteudo[entrada+ent:cont*ent]+conteudo[(cont+1)*ent:]
                #print "Preciso pegar a ultima entrada e por aqui!"

            #print "Diretorio depois"
            startMM(self.nome)
            self.escreveBloco(ant, struct.pack("h", prox)+struct.pack("h", cont)+conteudo)
            endMM()
            #self.leArquivo(ant)
            
            # Usando a FAT
            startMM(self.nome)
            print "Bloco inicial", bl
            pnt = bl
            print "Esse lugar ", pnt, "aponta para", self.FAT[pnt]
            while self.FAT[pnt] != -1:
                #if usedBitmap(self.nome, bl):
                startMM(self.nome)
                switchBitmap(self.nome, bl)
                endMM()
                bl = pnt
                pnt = self.FAT[pnt]
                self.FAT[bl] = None
                print "Setei a FAT", bl, "para", self.FAT[bl], "prox eh", pnt
            #if usedBitmap(self.nome, pnt):
            startMM(self.nome)
            switchBitmap(self.nome, pnt)
            endMM()
            self.FAT[pnt] = None
            print "Setei a FAT", pnt, "para", self.FAT[pnt]
            
            # Nao precisaria disso se tivesse FAT
            #prox, c, ct = self.leBloco(bl)
            
            #print "Proximo", prox
            
            #while prox != -1:
            #    switchBitmap(self.nome, bl)
            #    bl = prox
            #    print "Esses sao os proximos", prox
            #    prox, c, ct = self.leBloco(bl)

            #switchBitmap(self.nome, bl)

            
        else:
            print "Nao achei", arquivo
        endMM()

    #...........................................................
    def removeDiretorio(self, diretorio):
        global ent
        startMM(self.nome)
        bl = self.devolveBloco(diretorio)
        startMM(self.nome)
        prox, cont, conteudo = self.leBloco(bl)

        
        while prox != -1:
            if cont != -1:# Eh um diretorio
                for i in xrange(cont):
                    nome = self.ajustaNome(conteudo[0+i*ent:12+i*ent])
                    bl = struct.unpack("h", conteudo[12+i*ent:14+i*ent])
                    startMM(self.nome)
                    p, c, ctd = self.leBloco(bl[0])
                    #print "O contador e", c
                    if c == -1:
                        print "removeu:", diretorio+"/"+nome
                        self.removeArquivo(diretorio+"/"+nome)
                    else:
                        if c == 0:
                            print "removeu:", diretorio+"/"+nome
                            self.removeArquivo(diretorio+"/"+nome)
                        else:
                            self.removeDiretorio(diretorio+"/"+nome)
            else:
                print "Isto nao e um diretorio"
                return
            startMM(self.nome)
            prox, cont, conteudo = self.leBloco(prox)

        # Ultimo bloco
        if cont != -1: # Eh um diretorio
            for i in xrange(cont):
                    nome = self.ajustaNome(conteudo[0+i*ent:12+i*ent])
                    bl = struct.unpack("h", conteudo[12+i*ent:14+i*ent])

                    p, c, ctd = self.leBloco(bl[0])
                    #print "O contador e", c
                    if c == -1:
                        print "removeu:", diretorio+"/"+nome
                        self.removeArquivo(diretorio+"/"+nome)
                    else:
                        if c != 0:
                            print "removeu:", diretorio+"/"+nome
                            self.removeDiretorio(diretorio+"/"+nome)
                        else:
                            return 
        else:
            print "Isto nao e um diretorio"
            
        
        print "removeu:", diretorio
        self.removeArquivo(diretorio)
      
        endMM()


#............................
# MAIN
#............................
if __name__=="__main__":
    teste = SistemaArquivos("quarto")
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

    #print "Criei o diretorio roupa"
    #teste.criaDiretorio("/roupa")
    #teste.leArquivo(teste.devolveBloco("/"))
    #teste.criaArquivo("/coisa")
    #print "Criei o diretorio /casa"
    #teste.criaDiretorio("/casa")
    #teste.leArquivo(teste.devolveBloco("/"))
    #print "Criei o diretorio movo"
    #teste.criaDiretorio("/movo")
    #teste.leArquivo(teste.devolveBloco("/"))

    #print "Criei arquivo /casa/cachorro"
    #teste.criaArquivo("/casa/cachorro")
    #print "Criei diretorio /casa/animal"
    #teste.criaDiretorio("/casa/animal")
    #teste.criaArquivo("/casa/animal/bicho")
    #print "Conteudo de /casa/animal"
    #teste.leArquivo(teste.devolveBloco("/casa/animal"))
    #teste.leArquivo(teste.devolveBloco("/casa"))
    #print "Criei arquivo /gato"
    #teste.criaArquivo("/gato")
    #teste.leArquivo(2)
    #teste.leArquivo(teste.devolveBloco("/gato"))
    #teste.leArquivo(teste.devolveBloco("/"))
    #teste.criaArquivo("/copia")
    #teste.copiaArquivo("gato", teste.devolveBloco("/copia"))
    #teste.leArquivo(teste.devolveBloco("/copia"))
    #escreveIntBin("terceiro", 2, 2)
    #teste.removeArquivo("/la")
    #teste.removeArquivo("/gaot")
    #teste.removeArquivo("/acola")
    teste.removeArquivo("/alface")
    teste.removeArquivo("/gato")
    teste.leArquivo(teste.raiz)
    teste.criaDiretorio("/casa")
    teste.criaDiretorio("/casa/quarto")
    teste.criaDiretorio("/casa/cozinha")
    teste.criaArquivo("/casa/nova")
    teste.removeDiretorio("/casa/quarto")
    teste.removeDiretorio("/casa")
