from __future__ import division  #Para não truncar a divisão de inteiros
from visual import *             #Módulo com as funções gráficas do VPython
from random import random        #Gerador de números aleatórios


print """
#############{{{{{{{{{{{{{{{{{{{{{{{{}}}}}}}}}}}}}}}}}}}}}}}}}##############
 ########**********************************************************########
  ###>>>>>>>> Teste dos algoritmos de colisao e coalescencia <<<<<<<<<<###
   ###>>>>>>>>>>           Fisica 1 - MIEC - 09/10         <<<<<<<<<<<###
  ###>>>>>>>>        Carlos Miguel Correia da Costa          <<<<<<<<<<###
 ########**********************************************************########
#############{{{{{{{{{{{{{{{{{{{{{{{{}}}}}}}}}}}}}}}}}}}}}}}}}##############
"""

scene.title = "Inelastic collision"
scene.fullscreen = True
scene.autoscale = True
scene.center = (0,2.5,0)
scene.width = 1920
scene.height = 1080
scene.range = 100
#scene.rotate = (pi/4)


Crest = 0.9 #Coeficiente de restiruição
#Offset a dar para ter em conta os erros nos cálculos intermédios aquando da computação
#do tempo necessário a retroceder para que esferas fiquem em contacto e não em intersecção
offset_colisao_dt = 2 
offset_antes_coalescencia = 6 #(Numero de impactos antes das partículas se juntarem)
#Algoritmo usado na colisão (0 = normal, 1 = usando centro de massa)
algoritmo_colisao = 1

Tamanho_eixos = 100

#Eixos
L = 8
xaxis = curve(pos=[(0,0,0), (L,0,0)], color=(0.5,0.5,0.5))
yaxis = curve(pos=[(0,0,0), (0,L,0)], color=(0.5,0.5,0.5))
zaxis = curve(pos=[(0,0,0), (0,0,L)], color=(0.5,0.5,0.5))

#criação das esferas
esfera1 = sphere(pos=vector(0,0,0), radius= 5, material=materials.earth)
esfera2 = sphere(pos=vector(25,25,25), radius= 4.9, material=materials.marble)
esfera2.orbita = curve(pos=esfera2.pos)


#Propoiedades das eferas
esfera1.velocidade = vector(0,0,0)
esfera1.massa = 8e14
esfera1.p = esfera1.massa * esfera1.velocidade
esfera1.orbita = curve(pos = esfera1.pos, color = color.green)

esfera2.velocidade = vector(-5,-27,-10)
esfera2.massa = 1e6
esfera2.p = esfera2.massa * esfera2.velocidade
esfera2.orbita = curve(pos = esfera2.pos, color = color.red)

#Constante gravitacional universal
G = 6.7e-11
dt = 0.005

"""
F=ma
p=mv
F=p/dt
F = G*m1*m2/dist**2
F = G*ma*mb*(norm(dist)/mag(dist)**2)
x = xo + vt +1/2at**2

Coeficiente de restituicao
Cr = (vbf - vaf) / (vai - vbi)
vbf = Cr(vai - vbi) + vaf

Momentum
ma*vai + mb*vbi = ma*vaf + mb*vbf
ma*vai + mb*vbi = ma*vaf + mb*(Cr(vai - vbi) + vaf)
ma*vai + mb*vbi = vaf*(ma + mb) + Cr*mb*(vai - vbi)

vaf = (Cr*mb*(vbi - vai) + ma*vai + mb*vbi) / (ma + mb)

Similarmente
vbf = (Cr*ma*(vai - vbi) + ma*vai + mb*vbi) / (ma + mb)
"""

Numero_impactos = 0

while True:
    rate(25)

    #Rotação das esferas
    esfera1.rotate(angle = (pi / 90), axis = vector(1, 8, 3.5))
    esfera2.rotate(angle = (pi / 180), axis = vector(-1, 11, 1.3))
    
    #Vector normal ao plano de tangência entre as duas esferas
    distancia_particulas = esfera2.pos - esfera1.pos

    #Aplicação das forças
    F = G*esfera1.massa * esfera2.massa * (norm(distancia_particulas) / mag(distancia_particulas)**2)
    esfera1.p += F*dt
    esfera2.p -= F*dt

    #Computação das colisões / coalescência das particulas
    if (mag(distancia_particulas) <= (esfera1.radius + esfera2.radius)):

        Numero_impactos += 1
        
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

        deltaP_i = esfera2.pos - esfera1.pos
        deltaV_i = (esfera2.p / esfera2.massa) - (esfera1.p / esfera1.massa)
        a = mag(deltaV_i)**2
        if a == 0: continue
        #Se a diferença de velocidades é 0 é porque as esferas têm a mesma velocidade e como tal dispensa-se a computação da colisão
        b = dot(deltaP_i, deltaV_i)
        c = mag(deltaP_i)**2 - (esfera1.radius + esfera2.radius)**2
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
        esfera1.pos += (esfera1.p / esfera1.massa) * tfinal
        esfera2.pos += (esfera2.p / esfera2.massa) * tfinal


        #Quando há coalescência de partículas, elas ficam juntas, logo o coeficiente de restituição é 0
        if (Numero_impactos > offset_antes_coalescencia):
            Crest = 0


        #Computação das colisões

        #Versor normal ao plano de tangência
        vec_normal_ponto_impacto = norm(distancia_particulas)

        #Versor tangente ao plano de tengência e perpendicular ao versor normal
        vec_tangente_ponto_impacto = vector(-vec_normal_ponto_impacto.y, vec_normal_ponto_impacto.x, 0)
        #Forma que usei inicialmente e que deu "problemas", e me atrasou no debuging do programa
        #vec_tangente_ponto_impacto = vec_normal_ponto_impacto.rotate(angle=pi/2)

        #Versor perpendicular ao 2 versores anteriores
        vec_binormal_ponto_impacto = norm(cross(vec_normal_ponto_impacto, vec_tangente_ponto_impacto))


       #Velocidade das esferas
        velocidade_esf1 = esfera1.p / esfera1.massa
        velocidade_esf2 = esfera2.p / esfera2.massa 
        
        if algoritmo_colisao == 0:
            
            #Projecção das componentes segundo os versores determinados anteriormente
            vx1 = dot(velocidade_esf1, vec_normal_ponto_impacto)
            vy1 = dot(velocidade_esf1, vec_binormal_ponto_impacto)
            vz1 = dot(velocidade_esf1, vec_tangente_ponto_impacto)

            vx2 = dot(velocidade_esf2, vec_normal_ponto_impacto)
            vy2 = dot(velocidade_esf2, vec_binormal_ponto_impacto)
            vz2 = dot(velocidade_esf2, vec_tangente_ponto_impacto)

            #Determinação das novas componentes do vector normal ao plano tangente usando o coeficiente de restituição
            #(apenas se aplica ao vector normal, porque como os outros 2 versores estão contidos no plano
            #tangente ao impacto, não são aplicadas forças segundo essas direcções)
            vf_x_esfera1 = ((Crest*esfera2.massa*(vx2 - vx1) + esfera1.massa*vx1 + esfera2.massa*vx2) / (esfera1.massa + esfera2.massa))
            vf_x_esfera2 = ((Crest*esfera1.massa*(vx1 - vx2) + esfera1.massa*vx1 + esfera2.massa*vx2) / (esfera1.massa + esfera2.massa))

            #Determinação do vector da velocidade após o impacto, para cada uma das esferas
            vfinal_fesfera1 = vf_x_esfera1 * vec_normal_ponto_impacto + vy1 * vec_binormal_ponto_impacto + vz1 * vec_tangente_ponto_impacto
            vfinal_fesfera2 = vf_x_esfera2 * vec_normal_ponto_impacto + vy2 * vec_binormal_ponto_impacto + vz2 * vec_tangente_ponto_impacto
    
            
            #Actualização das quantidades de movimento
            esfera1.p = vfinal_fesfera1*esfera1.massa
            esfera2.p = vfinal_fesfera2*esfera2.massa

        else:
            #Computação das colisões "elásticas" entre partículas, com conservação de momentum
            #(versão alternativa, que usa o centro de massa para reduzir o número de cálculos e evitar tantos erros de arredondamento)
            ptotal = esfera1.p + esfera2.p
            mtotal = esfera1.massa + esfera2.massa
        
            #Mudança para o centro de massa (cm frame)
            velocidade_centro_massa = ptotal / mtotal

            #Velocidades das partículas em relação ao centro de massa
            vicm = velocidade_esf1 - velocidade_centro_massa
            vjcm = velocidade_esf2 - velocidade_centro_massa

            
            #Computação da colisão a partir do centro de massa (vf = -Cr * vi, sendo as componentes de vi correspondem
            #às componentes do vector resultante da projecção de vi segundo o vector normal ao plano de tangente ao ponto de impacto)
            vi_x_cm_f = -Crest * (dot(vicm, vec_normal_ponto_impacto) * vec_normal_ponto_impacto)
            vi_y_cm_f = dot(vicm, vec_binormal_ponto_impacto) * vec_binormal_ponto_impacto
            vi_z_cm_f = dot(vicm, vec_tangente_ponto_impacto) * vec_tangente_ponto_impacto
            
            vj_x_cm_f = -Crest * (dot(vjcm, vec_normal_ponto_impacto) * vec_normal_ponto_impacto)
            vj_y_cm_f = dot(vjcm, vec_binormal_ponto_impacto) * vec_binormal_ponto_impacto
            vj_z_cm_f = dot(vjcm, vec_tangente_ponto_impacto) * vec_tangente_ponto_impacto


            #Mudança para o sistema de eixos anterior (lab frame)
            esfera1.p = ((vi_x_cm_f + vi_y_cm_f + vi_z_cm_f) + velocidade_centro_massa) * esfera1.massa
            esfera2.p = ((vj_x_cm_f + vj_y_cm_f + vj_z_cm_f) + velocidade_centro_massa) * esfera2.massa

                

        #Após a computação das colisões, restitui-se o tempo que foi retrocedido (- porque tfinal é negativo)
        esfera1.pos -= (esfera1.p / esfera1.massa) * tfinal
        esfera2.pos -= (esfera2.p / esfera2.massa) * tfinal



        #Offset dado para que no início haja impacto entre as partículas e depois de certo
        #tempo elas começas a juntar-se após os impactos
        if (Numero_impactos > offset_antes_coalescencia):

            #Se pelo menos uma delas não estiver visivel, ignora-se a colisão
            if not esfera1.visible: continue 
            if not esfera2.visible: continue
            

            #Fazendo um paralelo com o volume de uma esfera, calcula-se o novo raio (V = 4/3 * pi * r^3)
            #Tem em conta o volume e não a massa / densidade das esferas
            novo_raio = pow(esfera1.radius**3 + esfera2.radius**3, 1./3.)
            nova_massa = esfera1.massa + esfera2.massa

            #Não precisa de uma nova quantidade de movimento porque isso já foi feito aquando da colisão
            #perfeitamente inelastica (coeficiente de restituição igual a 0)
            
            if esfera1.radius > esfera2.radius:
                #Criação da esfera resultante, na posição da esfera que tinha o maior raio
                esfera1.radius = novo_raio
                esfera1.massa = nova_massa


                #Alteração da esfera de menor raio, para que não tenha quase nenhuma influência sobre as restantes esferas
                esfera2.visible = False    #Particula fica invisivel
                #Com massa e raio insignificantes
                esfera2.radius *= 1E-20
                esfera2.massa *= 1E-10
                #E fora da área de movimento das restentes particulas
                esfera2.pos = vector(2*Tamanho_eixos + Tamanho_eixos*random(), 0, 0)
                #Com quantidade de movimento inicial igual a 0
                esfera2.p = vector(0,0,0)


            else:
                #Criação da esfera resultante, na posição da esfera que tinha o maior raio
                esfera2.radius = novo_raio
                esfera2.massa = nova_massa

                #Alteração da esfera de menor raio, para que não tenha quase nenhuma influência sobre as restantes esferas
                esfera1.visible = False    #Particula fica invisivel
                #Com massa e raio insignificantes
                esfera1.radius *= 1E-20
                esfera1.massa *= 1E-10
                #E fora da área de movimento das restentes particulas
                esfera1.pos = vector(2*Tamanho_eixos + Tamanho_eixos*random(), 0, 0)
                #Com quantidade de movimento inicial igual a 0
                esfera1.p = vector(0,0,0)


            
    #Actualização das localizações dos objectos
    esfera1.pos += (esfera1.p / esfera1.massa) * dt
    esfera2.pos += (esfera2.p / esfera2.massa) * dt


    #Actualização das orbitas dos objectos
    if esfera1.pos.x < Tamanho_eixos:
        esfera1.orbita.append(esfera1.pos)

    if esfera2.pos.x < Tamanho_eixos:
        esfera2.orbita.append(esfera2.pos)

    
