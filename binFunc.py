from datetime import datetime
import struct
import mmap
import os


def makeEmptyBin(filename, size):
    with open(filename, 'wb') as f:
        for i in xrange(size):
            f.seek(i)
            f.write(b'\x00')
        f.close()

def escreveDados(arquivo, dados, posicao):
    with open(arquivo, 'ab') as f:
        f.seek(posicao)
        f.write(dados)

"""        
def copiaArquivo(origem, destino, posicao):
    with open(origem,'rb') as f1:
        with open(destino,'wb') as f2:
            # escrever no sistema de arquivos a partir de uma posicao
            f2.seek(posicao)#f2 sera o nosso sistema de arquivos
            # posicao eh a posicao (em bytes) em que comecam os dados do arquivo
            while True:
                # 4kB - 4B
                bytes=f1.read(3996)
                if bytes: 
                    for byte in bytes:
                        pass    # process the bytes if this is what you want
                    # Coloca o endereco do primeiro bloco livre encontrado
                    # Seta o contador com -1
                    n = f2.write("22")
                    # Coloca o resto do conteudo do arquivo no bloco
                    n=f2.write(bytes)
                else:
                    break
"""

def leDados(arquivo, inicio, fim):
    with open(arquivo, 'rb') as f:
        f.seek(inicio)
        data = f.read(fim-inicio)
    return data

# Pos no intervalo [0:25000], refere-se aos bits do bitmap
# Troca o valor do bitmap da posicao para seu complementar
def switchBitmap(arqmem, pos):
    # Acessa uma posicao especifica do arquivo de memoria
    mapmem = memory_map(arqmem)

    val = pos/8
    rest = pos % 8

    p = ord(mapmem[val+4000])

    # Seta o bit da posicao "pos" para o valor "bit" 
    p^= 1 << rest
    mapmem[val+4000] = chr(p)

    mapmem.close()

def getBitmap(arqmem, pos):
    mapmem = memory_map(arqmem)
    val = pos/8
    rest = pos % 8

    p = ord(mapmem[val+4000])

    # Seta o bit da posicao "pos" para o valor "bit" 
    p&= 1 << rest
    mapmem.close()
    
    return p
    
    


def memory_map(filename, access=mmap.ACCESS_WRITE):
    size = os.path.getsize(filename)
    fd = os.open(filename, os.O_RDWR)
    return mmap.mmap(fd, size, access=access)

def escreveIntBin(arqmem, ini, pid):
    # Acessa uma posicao especifica do arquivo de memoria
    mapmem = memory_map(arqmem)

    data = struct.pack("h", pid)
    mapmem[ini:ini+2] = data

    mapmem.close()

def leIntBin(arqmem, pos):
    # Acessa uma posicao especifica do arquivo de memoria
    mapmem = memory_map(arqmem)
    data = mapmem[pos:pos+2]
    data = struct.unpack("h", data)
    mapmem.close()
    return int(data[0])

def escreveIntervalo(arqmem, ini, fim, conteudo):
    # Acessa uma posicao especifica do arquivo de memoria
    mapmem = memory_map(arqmem)

    print len(conteudo), fim-ini
    mapmem[ini:ini+len(conteudo)] = conteudo

    mapmem.close()
                    


def leIntervalo(arqmem, ini, fim):
    # Acessa uma posicao especifica do arquivo de memoria
    mapmem = memory_map(arqmem)
    data = mapmem[ini : fim]
        
    #print mapmem[pos]
    mapmem.close()
    return data

if __name__=="__main__":
    escreveDados("test", "ABCDEFGHSHAYENNE", 0)

    escreveDados("test", "ESCREVI", 30)


    escreveIntBin("primeiro", 0, 1)
    escreveIntBin("primeiro", 2, 2)
    escreveIntBin("primeiro", 4, 3)
    escreveIntBin("primeiro", 6, 25000)

    bitmap = leIntBin("primeiro", 0)
    raiz = leIntBin("primeiro", 2)
    dirs = leIntBin("primeiro", 6)

    print bitmap, raiz, dirs

    escreveDados("data", bin(100000000), 0)

    copiaArquivo("test", "me", 10)

    # le dados de um arquivo [inicio, fim)
    print leDados("me", 10, 18)


    copiaArquivo("test", "primeiro", 4000)
