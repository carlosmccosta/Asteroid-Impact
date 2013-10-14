from __future__ import division  #Para não truncar a divisão de inteiros
from visual import *             #Módulo com as funções gráficas do VPython
from random import random        #Gerador de números aleatórios


print """
#############{{{{{{{{{{{{{{{{{{{{{{{{}}}}}}}}}}}}}}}}}}}}}}}}}##############
 ########**********************************************************########
  ###>>>>>>>>>> Simulacao de impacto de asteroides na Terra <<<<<<<<<<<###
   ###>>>>>>>>>>           Fisica 1 - MIEC - 09/10         <<<<<<<<<<<###
  ###>>>>>>>>>>        Carlos Miguel Correia da Costa       <<<<<<<<<<<###
 ########**********************************************************########
#############{{{{{{{{{{{{{{{{{{{{{{{{}}}}}}}}}}}}}}}}}}}}}}}}}##############


#####&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&#######
 ##  $$$$$$                     Introducao                        $$$$$  ##
#####&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&#######

A presente simulacao tem por objectivo mostrar a influencia da gravidade
da Terra e da Lua nos objectos circundantes, e como tal salientar que
asteroides que a partida nao colidiriam com a Terra, poderao entrar em
rota de colisao com a Terra caso a Lua os desvie da sua orbita inicial.

Nesta simulacao para alem das forcas da gravidade foram incluidas as colisoes
inelasticas entre objectos, com coeficiente de restituicao de 0.85, e
incluida a acrecao de materia / objectos apos um certo numero de colisoes.

#############{{{{{{{{{{{{{{{{{{{{{{{{}}}}}}}}}}}}}}}}}}}}}}}}}##############
 ########**********************************************************########
#############{{{{{{{{{{{{{{{{{{{{{{{{}}}}}}}}}}}}}}}}}}}}}}}}}##############
"""

#####&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&#######
 ##  $$$$$$  Configuração da janela de visualização da simulação $$$$$$  ##
#####&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&#######

scene.title = "Frontal impact of an asteroid"
scene.rotate = (pi/4)
scene.forward = (-1,-0.7,-1)
scene.width = 1920
scene.height = 1080
scene.fullscreen = True       #Simulação começa em ecrâ total
scene.autoscale = False       #A escala da visualização não é alterada

Tamanho_eixos = 250000        #Valor usado na determinação de posições aleatórias
                              #dos asteroides e na escala de visualização
scene.range = 0.5 * Tamanho_eixos   #Definição da escala de visualização
scene_rate = 100                    #Definição do número de computações a fazer por ciclo


#Eixos coordenados
L = 15000
xaxis = curve(pos=[(0,0,0), (L,0,0)], color=(0.5,0.5,0.5))
yaxis = curve(pos=[(0,0,0), (0,L,0)], color=(0.5,0.5,0.5))
zaxis = curve(pos=[(0,0,0), (0,0,L)], color=(0.5,0.5,0.5))



#####&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&######
 ## Varíáveis parametrizáveis para simulação de vários tipos de impactos ##
#####&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&######

#Definição do dt a usar nos incrementos de velocidade
dt = 0.5

#Valor que denota o número de frame que se contabiliza nas computações das
#colisões. Serve para excluir erros significativos nos cálculos intermédios
offset_colisao_dt = 2                      

#Valor usado para regular a entrada do efeito da gravidade na simulação
#Ou seja, quando o produto do número de objectos em cena pelo offset
#for maior que o número de impactos, começa a haver coalescência dos objectos
offset_antes_coalescencia = 120

#Valor usado para regular o desaparecimento da Terra após o impacto
offset_antes_desaparecer_terra = 4.

#Algoritmo a ser usado na determinação das componentes da velocidade das esferas após o impacto
#(0 = normal, 1 = usando centro de massa)
algoritmo_colisao = 1

Numero_asteroides_extra = 0  #Número de asteróides extra
G = 6.7e-11                   #Constante gravitacional universal
Crest = 0.85                  #Coeficiente de restituição para os impactos das particulas


####################################
##>> Valores referentes à Terra <<##
####################################

Posicao_terra = vector(0,0,0)
Raio_terra = 6371
Massa_terra = 5.9736E17 #Valor real = 5.9736E24
Velocidade_terra = vector(0,0,0)
Quantidade_mov_terra = Massa_terra * Velocidade_terra

#Desvio horizontal real = 7.155
#Inclinação real (tilt) = 23.44º
#y = 8
#x = tg(7.155) * 8 ~ 1
#z = tg(23.44) * 8 ~ 3.5
Eixo_rotacao_terra = vector(1, 8, 3.5)

#Definição do centro da janela
scene.center = (0, -2*Raio_terra, 0)


##################################
##>> Valores referentes à Lua <<##
##################################

Posicao_lua = vector(78440.5,0,0) #Valor real = 384405 km
Raio_lua = 1737.19
Massa_lua = 7.3477E14 #Valor real = 7.3477E22 kg
Velocidade_lua = 350*norm(-Posicao_lua) #Valor real = 1.022 km/s 
Quantidade_mov_lua = Massa_lua * Velocidade_lua

#Desvio horizontal real = 5.145º
#Inclinação real (tilt) = 6.68º
#y = 11
#x = tg(5.145) * 11 ~ 1
#z = tg(6.68) * 11 ~ 1.3
Eixo_rotacao_lua = vector(-1, 11, 1.3)


###########################################
##>> Valores referentes aos asteróides <<##
###########################################

Posicao_asteroide = vector(12*Raio_terra,-Raio_terra,5*Raio_terra)
Raio_asteroide = 855.010 #6 km (Raio estimado do asteróide que extinguiu os dinossauros
Massa_asteroide = 0.35 * Massa_terra #3E15 kg (Massa estimada do asteróide que extinguiu os dinossauros)
Densidade_asteroide = Massa_asteroide / (4/3*pi*Raio_asteroide**3)


#Número a ser multiplicado por -norm(pos_esfera_a - pos_esfera_b)
Offset_versor_Velocidade_asteroide = 200
offset_versor_velocidade_asteroides_extra = 4000

#Numero a ser multiplicado pela componente x da posição do asteroide principal
Offset_x_asteroide_principal = 4

#Número a ser multiplicado pelo valor que irá ser acrescentado ao raio dos asteróides extra
offset_raio_extra_asteroides = 0.25


##########################################
##>> Valores referentes às partículas <<##
##########################################
Raio_particula = Raio_terra * 0.15
Massa_particula = Massa_terra * 0.025





######&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&######
 ##      Listas para armazenar os dados das partículas e asteróides      ##
######&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&######

Lista_particulas = []       
Lista_posicoes = []         
Lista_quantidade_mov = []   
Lista_massa_particulas = [] 
Lista_raio_particulas = []

Numero_corpos = 0


######&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&######
 ## Criação da Terra, que esconderá as partículas no seu interior        ##
######&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&######

#Criação da máscara da Terra
raio_ext = Raio_terra + Raio_particula
terra = sphere(pos=(0,0,0), radius=raio_ext, material=materials.earth)
terra.opacity = 1


######&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&######
 ##                           Criação da Lua                             ##
######&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&######

#Incorporação das características do Lua nas listas respectivas
Lista_particulas.append(sphere(pos=Posicao_lua, radius=Raio_lua,
                               material=materials.marble))
Lista_posicoes.append(Posicao_lua)
Lista_quantidade_mov.append(Quantidade_mov_lua)
Lista_massa_particulas.append(Massa_lua)
Lista_raio_particulas.append(Raio_lua)

orbita_lua = curve(pos = Posicao_lua, color = color.green)

Numero_corpos += 1



######&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&######
 ##                  Criação do asteróide principal                      ##
######&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&######

#Incorporação das características do asteróide principal nas listas respectivas
Lista_particulas.append(sphere(pos=Posicao_asteroide, radius=5*Raio_asteroide,
                               material=materials.marble, color = (200/256, 170/256, 140/256)))
Lista_posicoes.append(Posicao_asteroide)

#Vector que dá a direcção de impacto das esferas
Dist_lua_asteroide = Posicao_lua - Posicao_asteroide
#Velocidade do asteroide
Velocidade_asteroide_principal = 2*norm(-Posicao_asteroide)
#Quantidade de movimento do asteroide
p_asteroide = Massa_asteroide * Velocidade_asteroide_principal * Offset_versor_Velocidade_asteroide
Lista_quantidade_mov.append(p_asteroide)
#Massa e raio
Lista_massa_particulas.append(Massa_asteroide)
Lista_raio_particulas.append(5*Raio_asteroide)

#Orbita do asteroide principal
orbita_asteroide_principal = curve(pos = Posicao_asteroide, color = color.red)

Numero_corpos += 1



######&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&######
 ## Criação das partículas da Terra, agrupadas em forma de esfera        ##
######&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&######

#Criação da esfera de partículas, de baixo para cima e da esquerda para a direita
#De forma a criarem uma esfera
#Quanto menor for o raio das particulas melhor será a simulação
#e o conjunto das partículas melhor se assemelhará a uma esfera

Numero_particulas = 0

#Valores minimos e máximos para o eixo dos y, x e z
ymin = -Raio_terra + Raio_particula
ymax = Raio_terra - Raio_particula

xzmin = -Raio_terra + Raio_particula
xzmax = Raio_terra - Raio_particula

#Valores iniciais
y = ymin
x = xzmin
z = xzmin


#Criação de uma esfera de partículas
while (y <= ymax):
    #Criação de um plano de esferas
    while (x <= xzmax):
        #Criação de uma linha de esferas
        while (z <= xzmax):
            #A esfera só é inserida se estiver dentro da Terra
            if (x**2+y**2+z**2 <= Raio_terra**2):
                #Criação da partícula
                Lista_particulas.append(sphere(pos=(x,y,z),
                    radius=Raio_particula, material=materials.marble,
                    color=(66/256,38/256,10/256)))
                Lista_posicoes.append(vector(x,y,z))
                Lista_quantidade_mov.append(vector(0,0,0))
                Lista_massa_particulas.append(Massa_particula)
                Lista_raio_particulas.append(Raio_particula)

                #Incrementa-se o contador de número de objectos que já foram inseridos nas listas
                Numero_particulas += 1

            #Incrementa-se o z, para passar para a próxima esfera
            z += 2*Raio_particula

        #Incrementa-se o x para passar para a próxima linha de esferas
        x += 2*Raio_particula

        #Reinicializa-se o z, para começar no inicio da linha
        z = xzmin

    #Reinicializa-se o x e o z para começar no "inicio" do novo plano
    z = xzmin
    x = xzmin

    #Incrementa-se o y para passar para o próximo plano de esferas
    y += 2*Raio_particula       


######&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&######
 ##        Criação de Numeric Arrays a partir das listas criadas         ##
######&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&######

Numero_objectos = Numero_corpos + Numero_particulas

#Uso de Numeric arrays (do módulo Numeric), para aumentar o desempenho
Array_particulas = array(Lista_particulas)
Array_posicoes = array(Lista_posicoes)
Array_quantidade_mov = array(Lista_quantidade_mov)
Array_massa_particulas = array(Lista_massa_particulas)
Array_massa_particulas.shape = (Numero_objectos, 1)
Array_raio_particulas = array(Lista_raio_particulas)



######&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&######
 ##  Correcção das massas das partículas, para que o total seja igual à massa da Terra  ##
######&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&######

Massa_particulas_corrigida = Massa_terra / Numero_particulas


for n in range(0, Numero_particulas):
    Array_massa_particulas[Numero_corpos + n] = Massa_particulas_corrigida


######&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&######
 ##$$$$$   Loop que calcula as forças e colisões entre os corpos    $$$$$##
######&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&######


#Cálculo do objecto que tem o maior raio, para o ressalto nos limites de
#movimento dos objectos
maior_raio_objecto = max(Raio_lua, 2*Raio_asteroide, Raio_particula)

Numero_impactos_terra = 0
Numero_impactos = 0


while True:
    
    #Número de vezes por segundo que o loop será executado
    rate(scene_rate)

    #Rotação da Terra
    terra.rotate(angle = (pi/90), axis = Eixo_rotacao_terra)

    #Opacidade da Terra
    if (Numero_impactos_terra > 0 and terra.opacity > 0):
        terra.opacity -= terra.opacity * 0.1

    #Rotação da Lua
    Array_particulas[0].rotate(angle = (pi/180), axis = Eixo_rotacao_lua)


    #Computação das componentes das distâcias entre cada par de partículas
    Vector_distancia_par_particulas = Array_posicoes - Array_posicoes[:,newaxis]


    #Computação das distâncias entre cada par de partículas
    Distancia_par_particulas = sqrt(add.reduce(Vector_distancia_par_particulas
                                               * Vector_distancia_par_particulas,-1))



    #Computação das componentes das forças de todos os pares de partículas
    F = G * Array_massa_particulas * Array_massa_particulas[:,newaxis] * Vector_distancia_par_particulas / Distancia_par_particulas[:,:,newaxis]**3
    for n in range(Numero_objectos):
        F[n,n] = 0  #A força de um objecto sobre si próprio é 0...

    #Aplicação das forças aos objectos (às suas componetes de quantidade de movimento)
    #Antes do impacto não são aplicadas as forças às partículas dentro da Terra
    if (Numero_impactos_terra == 0):
        Array_quantidade_mov[0:Numero_corpos] += sum(F[0:Numero_corpos],1) * dt
    else:
        Array_quantidade_mov += sum(F,1) * dt



    #Computação das colisões entre partículas
    #(matriz binária com os pares de objectos que colidiram)
    Colisoes = less_equal(Distancia_par_particulas, (Array_raio_particulas + Array_raio_particulas[:,newaxis]))-identity(Numero_objectos)



    #Antes de haver um impacto com  Terra ignora-se as colisões entre as partículas da Terra
    if Numero_impactos_terra == 0:
        #Antes de haver uma colisão com a Terra, apenas se consideram as colisões dos restantes corpos
        Lista_colisoes = zeros((Numero_objectos, Numero_objectos))

        for i in range(0, Numero_corpos):
            Lista_colisoes[i] = Colisoes[i]

        #Lista com os indices das partículas que colidiram
        #Cada elemento representa um par de particulas (i,j), que colidiu e está codificado da seguinte forma:
        # i * Numero_particulas + j
        Lista_colisoes = sort(nonzero(Lista_colisoes.flat)[0]).tolist()

        #Remoção da colisão inversa (a em colisão com b é o mesmo que b em colisão com a, basta só calcular 1)
        #Uso do try visto que na primeira colisão de uma esfera com as particulas da Terra não há par de
        #colisão simétrico na matriz Lista_colisões_temp, visto que em cima reduzi essa matriz apenas aos elementos
        #que não são partículas para que as colisões entre as partículas antes da colisão fossem ignoradas
        try: Lista_colisoes.remove(j * Numero_objectos + i)
        except: True


        #Lista com as colisões de corpos com particulas da Terra
        Lista_colisoes_com_terra = zeros((Numero_objectos, Numero_objectos))

        for i in range(0, Numero_corpos):
            for j in range(Numero_corpos, Numero_objectos):
                Lista_colisoes_com_terra[i,j] = Colisoes[i,j]
                
        Lista_colisoes_com_terra = sort(nonzero(Lista_colisoes_com_terra.flat)[0]).tolist()

        try: Lista_colisoes_com_terra.remove(j * Numero_objectos + i)
        except: True

    else:
        #Lista com as colisões de todas as partículas
        Lista_colisoes = sort(nonzero(Colisoes.flat)[0]).tolist()

        try: Lista_colisoes.remove(j * Numero_objectos + i)
        except: True
        
    
    #Computação das colisões "elásticas/inelásticas" entre pasrtículas, com conservação de momentum
    for ij in Lista_colisoes:
        i, j = divmod(ij, Numero_objectos) #Descodificação do par de esferas que colidiram
        
        
        #Propriedades físicas das duas esferas
        particula1_massa = Array_massa_particulas[i,0]
        particula1_velocidade = Array_quantidade_mov[i] / particula1_massa

        particula2_massa = Array_massa_particulas[j,0]
        particula2_velocidade = Array_quantidade_mov[j] / particula2_massa


        #Cálculo do momento em que as esferas entraram em contacto, de forma a que a computação das
        #colisões seja feita exactamente quando as esferas se estão a tocar e não quando se estão a intersectar
        #Sem esta parte, caso houvesse um aglomerado de esferas, (particulas da Terra, por exmeplo),
        #muitas delas ficariam coladas e sobrepostas
        #Portanto o objectivo é calcular t (momento entre o inicio e fim de dt em que a esfera1 entra em contacto com a esfera2)
        #Como x = x0 + v0 * t
        #Então P1(f) = P1(i) + V1(i) * t e P2(f) = P2(i) + V2(i) * t
        #Sendo ~ um usado como delta para simplificar a leitura das equações
        #Subtraindo a 2ª equação à 1ª e simplificando fica:  ~P(f) = ~P(i) + t * ~V(i)
        #Elevando ao quadrado ambos e expandindo fica:   ~P(f)^2 = ~P(i)^2 + 2 * ~P(i) . ~V(i) + ~V(i)^2
        #Como ~P(f) corresponde à distância entre as esferas, ~P(f) = D(t),
        #o objectivo seria encontrar um t para o qual a distância fosse igual à soma das raios.
        #Logo D(t)^2 = (r1 + r2)^2, e simplificando na equação anterior fica:
        #~P(i)^2 + 2t * ~P(i) . ~V(i) + t**2 * ~V(i)^2 - (r1 + r2)^2 = 0
        #Como se trata uma função quadrática pode-se determinar o t pela forma resolvente
        #Sendo d = b^2 - 4ac, então x = (-b +- sqrt(d)) / 2a, seria a forma resolvente
        #Portanto:
        #d = (2 * ~P(i) . ~V(i) )^2 - 4 * ~V(i)^2 * (~P(i)^2 - (r1 + r2)^2)
        #t = ( -(2 * ~P(i) . ~V(i)) +- sqrt(d)) / (2 * ~V(i))^2)
        #Que simplificando, (tirando o 2 e o 4),  fica:
        #t = ( -(~P(i).~V(i)) +- sqrt( (~P(i).~V(i))^2 - (~P(i)^2 - (r1 + r2)^2) * ~V(i)^2 ) ) / ~V(i)^2 
        #Ou seja:
        #t = (-b +- sqrt(b^2 - a*c) ) / a
        deltaP_i = Array_posicoes[j] - Array_posicoes[i]
        deltaV_i = particula2_velocidade - particula1_velocidade
        a = mag(deltaV_i)**2
        if a == 0: continue
        #Se a diferença de velocidades é 0 é porque as esferas têm a mesma velocidade e como tal dispensa-se a computação da colisão
        b = dot(deltaP_i, deltaV_i)
        c = mag(deltaP_i)**2 - (Array_particulas[i].radius + Array_particulas[j].radius)**2
        d = b**2 - a*c
        if d < 0: continue   #d nunca pode ser menor que 0 porque a raiz quadrada não admite números negativos. 
        d_sqrt = sqrt(d)
        t1 = (-b+d_sqrt) / a
        t2 = (-b-d_sqrt) / a


        #Se o produto for negativo significa que uma colisão ocorreu no frame anterior e outra irá ocorrer mais tarde
        #Ou seja, interessa determinar o t negativo menor que dt
        #Caso não haja t negativo e menor que dt ignora-se a colisão, porque as esferas já não estão em contacto
        #Por exemplo, no inicio de um dado frame podem haver 4 esferas em contacto, mas... por exemplo após computar a primeira colisão,
        #uma delas pode já não estar em contacto com a esfera que estava no inicio do frame, porque aquela com que colidiu tirou-a de contacto com a outra

        if (t1 * t2 > 0): continue

        if (t1 <= t2):
            tfinal = t1
        else:
            tfinal = t2



        if (-tfinal > offset_colisao_dt * dt): continue #Caso ocorra algum erro de arredondamento significativo, ignora-se a colisão
        
        #Portanto, o que resta fazer é andar para trás no tempo para que se faça a computação da colisão no momento exacto do contacto das esferas
        #e após o cálculo, restituir o tempo que foi retrocedido
        Array_posicoes[i] += particula1_velocidade * tfinal
        Array_posicoes[j] += particula2_velocidade * tfinal

        
        #Quando há coalescência de partículas, elas ficam juntas, logo o coeficiente de restituição é 0
        if (Numero_impactos > Numero_objectos * offset_antes_coalescencia):
            Crest = 0


        ##>>>>>>>>>> Computação das colisões <<<<<<<<<<##
            
        #Vector normal ao plano de tangência entre as duas esferas
        distancia_particulas = Array_particulas[j].pos - Array_particulas[i].pos

        #Versor normal ao plano de tangência
        vec_normal_ponto_impacto = norm(distancia_particulas)

        #Versor tangente ao plano de tengência e perpendicular ao versor normal
        vec_tangente_ponto_impacto = vector(-vec_normal_ponto_impacto.y, vec_normal_ponto_impacto.x, 0)
        #Forma que usei inicialmente e que deu "problemas", e me atrasou considerávelmente no debuging do programa
        #vec_tangente_ponto_impacto = vec_normal_ponto_impacto.rotate(angle = pi/2) #!!!$&!#$"@!!!
        
        #Versor perpendicular ao 2 versores anteriores
        vec_binormal_ponto_impacto = cross(vec_normal_ponto_impacto, vec_tangente_ponto_impacto)


        #Selecção do algoritmo para computar as colisões
        #Coloquei os 2 porque o primeiro dá para perceber melhor como funciona o segundo
        if algoritmo_colisao == 0:

            #Projecção das componentes segundo os versores determinados anteriormente
            vx1 = dot(particula1_velocidade, vec_normal_ponto_impacto)
            vy1 = dot(particula1_velocidade, vec_binormal_ponto_impacto)
            vz1 = dot(particula1_velocidade, vec_tangente_ponto_impacto)

            vx2 = dot(particula2_velocidade, vec_normal_ponto_impacto)
            vy2 = dot(particula2_velocidade, vec_binormal_ponto_impacto)
            vz2 = dot(particula2_velocidade, vec_tangente_ponto_impacto)


            #Determinação das novas componentes do vector normal ao plano tangente usando o coeficiente de restituição
            #(apenas se aplica ao vector normal, porque como os outros 2 versores estão contidos no plano
            #tangente ao impacto, não são aplicadas forças segundo essas direcções)
            particula1_vxfinal = ((Crest * particula2_massa * (vx2 - vx1) + particula1_massa*vx1 +
                                   particula2_massa*vx2) / (particula1_massa + particula2_massa))
            particula2_vxfinal = ((Crest * particula1_massa * (vx1 - vx2) + particula1_massa*vx1 +
                                   particula2_massa*vx2) / (particula1_massa + particula2_massa))

            #Determinação do vector da velocidade após o impacto, para cada uma das esferas
            particula1_vfinal = particula1_vxfinal * vec_normal_ponto_impacto + vy1 * vec_binormal_ponto_impacto + vz1 * vec_tangente_ponto_impacto
            particula2_vfinal = particula2_vxfinal * vec_normal_ponto_impacto + vy2 * vec_binormal_ponto_impacto + vz2 * vec_tangente_ponto_impacto

            #Actualização das quantidades de movimento
            Array_quantidade_mov[i] = particula1_vfinal * particula1_massa
            Array_quantidade_mov[j] = particula2_vfinal * particula2_massa

        else:
            #Computação das colisões "elásticas" entre partículas, com conservação de momentum
            #(versão alternativa, que usa o centro de massa para reduzir o número de cálculos e evitar tantos erros de arredondamento)
            ptotal = Array_quantidade_mov[i] + Array_quantidade_mov[j]
            mtotal = particula1_massa + particula2_massa
        
            #Mudança para o centro de massa (cm frame)
            velocidade_centro_massa = ptotal / mtotal

            #Velocidades das partículas em relação ao centro de massa
            vicm = particula1_velocidade - velocidade_centro_massa
            vjcm = particula2_velocidade - velocidade_centro_massa

            
            #Computação da colisão a partir do centro de massa (vf = -Cr * vi, sendo as componentes de vi correspondem
            #às componentes do vector resultante da projecção de vi segundo o vector normal ao plano de tangente ao ponto de impacto)
            vi_x_cm_f = -Crest * (dot(vicm, vec_normal_ponto_impacto) * vec_normal_ponto_impacto)
            vi_y_cm_f = dot(vicm, vec_binormal_ponto_impacto) * vec_binormal_ponto_impacto
            vi_z_cm_f = dot(vicm, vec_tangente_ponto_impacto) * vec_tangente_ponto_impacto
            
            vj_x_cm_f = -Crest * (dot(vjcm, vec_normal_ponto_impacto) * vec_normal_ponto_impacto)
            vj_y_cm_f = dot(vjcm, vec_binormal_ponto_impacto) * vec_binormal_ponto_impacto
            vj_z_cm_f = dot(vjcm, vec_tangente_ponto_impacto) * vec_tangente_ponto_impacto


            #Mudança para o sistema de eixos anterior (lab frame)
            Array_quantidade_mov[i] = ((vi_x_cm_f + vi_y_cm_f + vi_z_cm_f) + velocidade_centro_massa) * particula1_massa
            Array_quantidade_mov[j] = ((vj_x_cm_f + vj_y_cm_f + vj_z_cm_f) + velocidade_centro_massa) * particula2_massa

                

        #Após a computação das colisões, restitui-se o tempo que foi retrocedido (- porque tfinal é negativo)
        Array_posicoes[i] -= (Array_quantidade_mov[i] / particula1_massa) * tfinal
        Array_posicoes[j] -= (Array_quantidade_mov[j] / particula2_massa) * tfinal
        

        #Incrementa-se 1 para eu detectar quando devo de actualizar as listas (no fim do programa)
        #(para saber que já não estou no frame da 1ª colisão)
        if Numero_impactos_terra == 1:
            Numero_impactos_terra +=1
            
        #Incremento do número de impactos (usado para determinar quando a coalescência entre partículas deve começar)
        if ((Numero_impactos_terra == 0) and (Lista_colisoes_com_terra)):
            Numero_impactos_terra += 1
        else:
            Numero_impactos += 1

                

        #Offset dado para que no início haja impacto entre as partículas e depois de certo
        #tempo elas começas a juntar-se após os impactos
        if (Numero_impactos > Numero_objectos * offset_antes_coalescencia):

            #Se pelo menos uma delas não estiver visivel, ignora-se a colisão
            if not Array_particulas[i].visible: continue 
            if not Array_particulas[j].visible: continue


            #Determinação da partícula que tem o maior raio
            maior_raio, menor_raio = i, j
            if Array_raio_particulas[j] > Array_raio_particulas[i]:
                maior_raio, menor_raio = j, i

            #Fazendo um paralelo com o volume de uma esfera, calcula-se o novo raio (V = 4/3 * pi * r^3)
            #Tem em conta o volume e não a massa / densidade das esferas
            novo_raio = pow(Array_particulas[i].radius**3 + Array_particulas[j].radius**3, 1./3.)
            nova_massa = Array_massa_particulas[i,0] + Array_massa_particulas[j,0]

            #Não precisa de uma nova quantidade de movimento porque isso já foi feito aquando da colisão
            #perfeitamente inelastica (coeficiente de restituição igual a 0)

            #Criação da esfera resultante, na posição da esfera que tinha o maior raio
            Array_particulas[maior_raio].radius = novo_raio
            Array_raio_particulas[maior_raio] = novo_raio
            Array_massa_particulas[maior_raio,0] = nova_massa
            

            #Alteração da esfera de menor raio, para que não tenha quase nenhuma influência sobre as restantes esferas
            #Não foi removida para que o tamanho das matrizes (arrays), não altere, dado que a sua eliminação daria problemas
            #Quando fosse a processar novamente esses arrays
            Array_particulas[menor_raio].visible = False    #Particula fica invisivel
            #Com massa e raio insignificantes
            Array_particulas[menor_raio].radius = Raio_particula*1E-20
            Array_raio_particulas[menor_raio] = Raio_particula*1E-20
            Array_massa_particulas[menor_raio,0] = Massa_particula*1E-10
            #E fora da área de movimento das restentes particulas
            Array_posicoes[menor_raio] = vector(2*Tamanho_eixos + Tamanho_eixos*random(), 0, 0)
            Array_particulas[menor_raio].pos = Array_posicoes[menor_raio]
            #Com quantidade de movimento inicial igual a 0
            Array_quantidade_mov[menor_raio] = vector(0,0,0)
           

            


    #Para evitar problemas de visualização que acontecem no Visual Python quando um objecto está a uma grande distância dos restantes...
    #Faz-se com que as esferas ressaltem quando ultrapassem uma determinada distância a partir do centro

    #Objectos que ultrapassaram os planos x=-limite, y=-limite, z=-limite
    Objectos_fora_simulacao_negativos = less_equal(Array_posicoes, -Tamanho_eixos + maior_raio_objecto) # walls closest to origin
    pn = Array_quantidade_mov * Objectos_fora_simulacao_negativos
    Array_quantidade_mov += -pn + abs(pn) #Faz-se com que o objecto se dirija para dentro

    #Objectos que ultrapassaram os planos x=limite, y=limite, z=limite
    Objectos_fora_simulacao_positivos = greater_equal(Array_posicoes, Tamanho_eixos - maior_raio_objecto) # walls farther from origin
    pp = Array_quantidade_mov * Objectos_fora_simulacao_positivos
    Array_quantidade_mov += -pp - abs(pp) #Faz-se com que o objecto se dirija para dentro


    #Actualização das posições
    Array_posicoes += (Array_quantidade_mov / Array_massa_particulas) * dt

    #Actualização das localizações dos objectos
    for i in range(0, Numero_objectos):
        Array_particulas[i].pos = Array_posicoes[i]

    #Actualização da orbita da lua e do asteróide principal
    #Se tiver ultrapassado os eixos (por exemplo aquando da realocação da particula após coalescer com uma de maior raio),
    #não se faz a actualização
    if (Array_posicoes[0,0] < Tamanho_eixos):
        orbita_lua.append(Array_posicoes[0])

    if (Array_posicoes[1,0] < Tamanho_eixos):
        orbita_asteroide_principal.append(Array_posicoes[1])


    #Actualização das listas que mais tarde irão ser reusadas aquando da criação dos objectos extra
    if (Numero_impactos_terra == 1):
        for i in range(0, Numero_corpos):
            Lista_particulas[i].pos = Array_particulas[i].pos
            Lista_posicoes[i] = Array_posicoes[i]
            Lista_quantidade_mov[i] = Array_quantidade_mov[i]


######&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&######
 ##  Criação dos asteróides extra, após o impacto do asteróide principal ##
######&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&######

    Numero_corpos_antes_colisao = Numero_corpos
    
    if (Numero_impactos_terra == 1):
        #Criação de asteróides extra
        for i in range(Numero_asteroides_extra):
            #Determinação das posições dos asteroides aleatoriamente
            x = -Tamanho_eixos+2*Tamanho_eixos*random()
            y = -Tamanho_eixos+2*Tamanho_eixos*random()
            z = -Tamanho_eixos+2*Tamanho_eixos*random()
            posicao = vector(x,y,z)
            Lista_posicoes.append(posicao)
            #Determinação aleatória do raio do asteroide (tendo como base o asteroide principal)
            raio = Raio_asteroide + offset_raio_extra_asteroides * Raio_asteroide * random()
            Lista_particulas.append(sphere(pos=posicao, radius=raio, material=materials.marble, color = (175/256, 150/256, 100/256)))
            Lista_raio_particulas.append(raio)
            #Determinação da massa tendo em conta o raio obtido anteriormente e a densidade dos asteroides
            massa = Densidade_asteroide * (4/3*pi*raio**3)
            Lista_massa_particulas.append(massa)
            #Determinação da velocidade de forma a que o asteroide passa pela origem e colida com a Terra
            velocidade = -offset_versor_velocidade_asteroides_extra * norm(posicao)
            #Determinação da quantidade de movimento
            p_asteroide = velocidade * massa
            Lista_quantidade_mov.append(p_asteroide)

            Numero_corpos += 1


        ######&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&######
         ##   Actualização dos Numeric Arrays a partir das listas actualizadas   ##
        ######&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&######

        Numero_objectos = Numero_corpos + Numero_particulas

        #Uso de Numeric arrays (do módulo Numeric), para aumentar o desempenho
        Array_particulas = array(Lista_particulas)
        Array_posicoes = array(Lista_posicoes)
        Array_quantidade_mov = array(Lista_quantidade_mov)
        Array_massa_particulas = array(Lista_massa_particulas)
        Array_massa_particulas.shape = (Numero_objectos, 1)
        Array_raio_particulas = array(Lista_raio_particulas)


        ######&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&######
         ##  Correcção das massas das partículas, para que o total seja igual à massa da Terra  ##
        ######&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&######

        Massa_particulas_corrigida = Massa_terra / Numero_particulas


        for n in range(0, Numero_particulas):
            Array_massa_particulas[Numero_corpos_antes_colisao + n] = Massa_particulas_corrigida




######&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&######
 ##$$$$$           Alguma da bibliografia relevante usada           $$$$$##
######&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&######

"""
http://vpython.org/contents/docs/visual/index.html
http://docs.python.org/tutorial/
http://homes.esat.kuleuven.be/~python/doc/numpy/array.html
http://www.gamedev.net/reference/articles/article1234.asp
http://qbx6.ltu.edu/s_schneider/physlets/main/momenta4.shtml
http://www.phy.ntnu.edu.tw/ntnujava/index.php?topic=4
http://academicearth.org/lectures/elastic-and-inelastic-collisions
http://cnx.org/content/m14852/latest/
http://vam.anest.ufl.edu/physics/collisionphysics.html
http://en.wikipedia.org/wiki/Inelastic_collision
http://www.vobarian.com/collisions/
http://www.vobarian.com/collisions/2dcollisions2.pdf
http://www.lightandmatter.com/html_books/2cl/ch04/ch04.html
"""




###########$$$$$$$$$>>>>>>>>>>      Nota       <<<<<<<<<<$$$$$$$$$###########
#     Parte do código referente aos numeric arrays é baseado no que está    #
# presente nos ficheiros de exemplo stars.py e gas.py que vêm com o VPython #
###########&&&&&&&&&>>>>>>>>>>>>>>>>>  <<<<<<<<<<<<<<<<<<$$$$$$$$$###########

