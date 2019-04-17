'''

Atividade  que simula um sistema de log UNDO/REDO
A classe Parser recebe o nome do arquivo de log
e retorna os valores após a execução do parser

Desenvolvido por: Juliana Rosin e Vinicius Rifam

16/04/2019
'''
class Parser:
    def __init__(self,nomeArquivo):
        self.nomeArquivo = nomeArquivo
        self.arquivo = open(nomeArquivo,'r')
        self.dados = {}
        self.alteracoes = []
        self.transacoes = {}
        self.checkpoints = {}
        self.undoRedo()

    def parseDados(self,linha):
        dados = linha.split(' | ')
        for d in dados:
            e = d.split('=')
            if e[0] not in self.dados:
                self.dados[e[0]]=e[1]
        print(self.dados)

    def startTransacao(self,i,linha):
        t = linha.split(' ')
        ti = t[1][0:2]
        if ti not in self.transacoes:
            self.transacoes[ti] = (i,'X',-1)

    def addAlteracoes(self,i,linha):
        dt = linha.split(',') #dados transacoes ['<T1', 'A', '10', '20>']
        if i not in self.alteracoes:
            self.alteracoes.append((dt[0][1:3],dt[1],dt[2],dt[3][0:-1]))

    def commitaTransacoes(self,i,linha):
        ct = linha.split(' ')[1][0:-1] #'T1' ou T2 ...'
        linha = self.transacoes[ct][0] # 1
        self.transacoes[ct] = (linha,'C',i)

    def addCkpt(self,i,linha):
        sc = linha.split('(')
        sc = sc[1].split(',')
        list_t = []
        for j,t in enumerate(sc):
            if j == len(sc)-1:
                list_t.append(t[0:2])
            else:
                list_t.append(t)
        if i not in self.checkpoints:
            self.checkpoints[i]=[list_t,'X']

    def endCkpt(self,i,linha):
        for c in self.checkpoints:
            self.checkpoints[c][1] = 'E'

    def closeArquivo(self):
        self.arquivo.close()

    def readOperacoes(self):
        for i,l in enumerate(self.arquivo):
            linha = l.strip()
            if i==0:
                self.parseDados(linha)
            elif linha[0:2] =='<s':
                self.startTransacao(i,linha)
            elif linha[0:2] =='<T':
                self.addAlteracoes(i,linha)
            elif linha[0:2] == '<c':
                self.commitaTransacoes(i,linha)
            elif linha[0:2] == '<S':
                self.addCkpt(i,linha)
            elif linha[0:2] =='<E':
                self.endCkpt(i,linha)

    def verificaCheckPoint(self):
        self.list_tU = []
        self.list_tR = []
        for c in self.checkpoints:
            if self.checkpoints[c][1] == 'E':
                flag = c
            else:
                flag = 0
            for t in self.transacoes:
                if self.transacoes[t][1] != 'C':
                    if t not in self.list_tU:
                        self.list_tU.append(t)
                elif self.transacoes[t][2] > flag:
                    if t not in self.list_tR:
                        self.list_tR.append(t)

    def undoRecovery(self):
        for alt in self.alteracoes[::-1]:
            if alt[0] in self.list_tU:
                self.dados[alt[1]] = alt[2]

    def redoRecovery(self):
        for alt in self.alteracoes:
            if alt[0] in self.list_tR:
                self.dados[alt[1]] = alt[3]

    def undoRedo(self):
        self.readOperacoes()
        self.verificaCheckPoint()
        self.undoRecovery()
        self.redoRecovery()
        print(self.dados)

p = Parser('ent2.txt')
#p = Parser('ent.txt')
