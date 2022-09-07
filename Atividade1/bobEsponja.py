class Animal:
    def __init__(self, nome, idade, altura, cor):
       self.nome    = nome
       self.idade   = idade
       self.altura  = altura
       self.cor     = cor
       
    def imprime(self):
        print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
        print(f'Animal: {self.nome}\nIdade: {self.idade if self.idade != None else "Não informada" }\nAltura: {self.altura if self.altura != None else "Não informada"}\nCor: {self.cor}')

#Herança   
class Personagem(Animal):
    def __init__(self, nome, idade, altura, cor, protagonista, nomePersonagem, bondade, ocupacao, descricao):
        super().__init__(nome, idade, altura, cor)
        self.protagonista   = protagonista
        self.nomePersonagem = nomePersonagem
        self.bondade        = bondade
        self.ocupacao       = ocupacao
        self.descricao      = descricao
    
    #Encapsulamento    
    def __melhoresFrases(self):
        if self.nome == 'Patrick Estrela':
            return "O conhecimento não pode substituir a amizade. Eu prefiro ser um idiota a ter que te perder"
        
        if self.nome == 'Bob Esponja Calça Quadrada':
            return "Se você acreditar em si mesmo, todos os seus sonhos podem se tornar realidade.\n"\
                    "Você pode ser o que você quiser se tiver imaginação."
                    
        if self.nome == 'Plankton':
            return "O que me falta em tamanho, tenho de sobra em maldade."
     
    #Polimorfismo
    def imprime(self):
        super().imprime()
        print(f'Personagem: {self.nomePersonagem}\nProtagonista: {"Sim" if self.protagonista == True else "Não"}')
        if self.bondade == False:
            print("Vilão") 
        print(f'Ocupação: {self.ocupacao}')
        print(f'Descricao: {self.descricao}')
        frases = self.__melhoresFrases()
        if frases != None:
            print(f'Melhores frases:{frases}\n')
        
        
#Bob Esponja ---------------------------------------------------------------------------------------------------------------------------------------          
bobEsponja = Personagem("Esponja do Mar", 33, "4 polegadas", "Amarela", True, "Bob Esponja Calça Quadrada", True, \
                        "Mestre-cuca do Siri Cascudo", \
                        "Ele foi projetado desenhado para se parecer com uma esponja de cozinha, sendo retangular, amarelo e brilhante.\n \
                        É um personagem sem noção, imaturo, e com uma personalidade hiperativa, mas também é Bob Esponja é muito bondoso e inocente.\n\
                        Seus melhores amigos são o Patrick Estrela e a Sandy")                       
bobEsponja.imprime()

#Patrick Estrela -----------------------------------------------------------------------------------------------------------------------------------
patrickEstrela = Personagem("Estrela", 34, "6 polegadas", "Rosa", False, "Patrick Estrela", True, \
                        "Desempregado", \
                        "Ele é uma estrela do mar estúpida, mas bem-intencionada.  Patrick é bastante gordo e adora sorvete e muitos outras porcarias.\n\
                        Ele é o deuteragonista do show. Ele mora debaixo de uma pedra. Bob Esponja e Lula Molusco são seus vizinhos.")                                            
patrickEstrela.imprime()

#Sandy ----------------------------------------------------------------------------------------------------------------------------------------------
sandy = Personagem("Esquilo", None, None, "Marrom", False, "Sandy Bochechas", True, \
                        "Cientista", \
                        "Utiliza uma roupa especial com um capacete de oxigênio pois é quase terreste. Sa casa écomo uma 'estufa' cheia de ar.\n\
                         Gosta muito de lutar Karatê, e praticar vários esportes radicais, quase sempre com Bob Esponja.")                                         
sandy.imprime()

#Plankton --------------------------------------------------------------------------------------------------------------------------------------------
plankton= Personagem("Copepóde planctônico", 77, "1 mg", "Verde escuro", False, "Plankton", False, \
                        "Dono do Balde de Lixo", \
                        "Ele é inimigo do Sr. Siriguejo e como não pode ser salvo com seus clientes, com receita garantida do Hambúrguer de Siri.\n\
                        Ele é muito mal.")                                         
plankton.imprime()