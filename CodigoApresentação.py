# nao_sesi_senai.py
# Apresentação do robô NAO para o estande SESI SENAI Canedo
# Movimentos sincronizados com as falas — fluidos e expressivos

import time
import threading
from naoqi import ALProxy

# ─── CONFIGURAÇÃO ────────────────────────────────────────────────
NAO_IP = "169.254.62.247"
PORT   = 9559

motion  = ALProxy("ALMotion",       NAO_IP, PORT)
posture = ALProxy("ALRobotPosture", NAO_IP, PORT)
leds    = ALProxy("ALLeds",         NAO_IP, PORT)
tts     = ALProxy("ALTextToSpeech", NAO_IP, PORT)

# Velocidade da fala (pode ajustar entre 80-100 para mais natural)
tts.setParameter("speed", 90)

# ─── INICIALIZAÇÃO ───────────────────────────────────────────────
motion.wakeUp()
posture.goToPosture("StandInit", 0.6)
motion.wbEnable(True)
motion.setMoveArmsEnabled(False, False)

# ─── UTILITÁRIOS ─────────────────────────────────────────────────

def sa(joints, angles, speed=0.14):
    """Atalho para setAngles."""
    motion.setAngles(joints, angles, speed)

def falar(texto):
    """Dispara a fala em thread separada para não bloquear os movimentos."""
    t = threading.Thread(target=tts.say, args=(texto,))
    t.start()
    return t

def leds_cor(cor=0xffffff, dur=0.3):
    leds.fadeRGB("FaceLeds", cor, dur)

def piscar_leds(cor=0xffffff, vezes=2):
    for _ in range(vezes):
        leds.fadeRGB("FaceLeds", cor, 0.08)
        time.sleep(0.12)
        leds.fadeRGB("FaceLeds", 0x000000, 0.08)
        time.sleep(0.10)
    leds.fadeRGB("FaceLeds", cor, 0.2)

# ─── POSTURA BASE ────────────────────────────────────────────────

def postura_base(speed=0.13):
    """Postura ereta e receptiva — ponto de retorno entre gestos."""
    sa([
        "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LHand",
        "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RHand",
        "HeadPitch", "HeadYaw"
    ], [
        1.05,  0.20, -1.2, -0.35, 0.6,
        1.05, -0.20,  1.2,  0.35, 0.6,
        -0.05, 0.0
    ], speed)

# ─── GESTOS FLUIDOS ──────────────────────────────────────────────

def gesto_convidar():
    """Braços se abrem como quem convida — fala 1."""
    # fase 1: abre
    sa([
        "LShoulderPitch", "LShoulderRoll", "LElbowRoll", "LHand",
        "RShoulderPitch", "RShoulderRoll", "RElbowRoll", "RHand",
        "HeadPitch", "HeadYaw"
    ], [
        0.55,  0.65, -0.25, 1.0,
        0.55, -0.65,  0.25, 1.0,
        -0.12, 0.0
    ], 0.14)
    time.sleep(0.5)
    # fase 2: suaviza levemente — gesto de "venha"
    sa([
        "LShoulderPitch", "LShoulderRoll", "LElbowRoll",
        "RShoulderPitch", "RShoulderRoll", "RElbowRoll",
        "HeadPitch"
    ], [
        0.65,  0.50, -0.35,
        0.65, -0.50,  0.35,
        -0.08
    ], 0.10)

def gesto_olhar_plateia():
    """Vira cabeça para os dois lados, incluindo todos."""
    sa("HeadYaw",  0.45, 0.12); time.sleep(0.55)
    sa("HeadYaw", -0.45, 0.12); time.sleep(0.55)
    sa("HeadYaw",  0.0,  0.12); time.sleep(0.35)

def gesto_apontar_frente():
    """Mão direita aponta para frente — 'entre aqui'."""
    sa([
        "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll",
        "RWristYaw", "RHand",
        "LShoulderPitch", "LHand",
        "HeadYaw"
    ], [
        0.35, -0.12, 1.55, 0.08,
        -0.25, 0.1,
        1.05, 0.6,
        -0.18
    ], 0.14)

def gesto_saude():
    """Braços em posição de cuidado — fala 2 (saúde e segurança)."""
    # mão no peito
    sa([
        "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll",
        "RWristYaw", "RHand",
        "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LHand",
        "HeadPitch"
    ], [
        0.65, -0.05, 0.9, 1.25,
        -0.45, 0.7,
        0.70,  0.22, -1.1, -0.55, 0.7,
        -0.05
    ], 0.13)
    time.sleep(0.6)
    # abre levemente — "cuidamos de você"
    sa([
        "LShoulderPitch", "LShoulderRoll", "LElbowRoll", "LHand",
        "RShoulderPitch", "RElbowRoll", "RHand",
        "HeadPitch"
    ], [
        0.60,  0.40, -0.40, 1.0,
        0.60,  0.40,  1.0,
        -0.1
    ], 0.12)

def gesto_enfase_pulso(lado="R", repeticoes=2):
    """Leve pulsação do braço para baixo — ênfase em palavras-chave."""
    if lado == "R":
        jts = ["RShoulderPitch", "RElbowRoll", "RHand", "HeadPitch"]
        up  = [0.28, 0.50, 0.7, 0.04]
        dn  = [0.52, 0.85, 0.7, 0.10]
    else:
        jts = ["LShoulderPitch", "LElbowRoll", "LHand", "HeadPitch"]
        up  = [0.28, -0.50, 0.7, 0.04]
        dn  = [0.52, -0.85, 0.7, 0.10]
    for _ in range(repeticoes):
        sa(jts, up, 0.14)
        time.sleep(0.22)
        sa(jts, dn, 0.12)
        time.sleep(0.22)

def gesto_palmas_cima():
    """Palmas abertas para cima — 'apresento a vocês'."""
    sa([
        "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll",
        "LWristYaw", "LHand",
        "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll",
        "RWristYaw", "RHand",
        "HeadPitch"
    ], [
        0.50,  0.38, -1.45, -0.18,
        -1.55, 1.0,
        0.50, -0.38,  1.45,  0.18,
         1.55, 1.0,
        -0.12
    ], 0.13)

def gesto_enumerar(lado="L"):
    """Levanta braço para enumerar um ponto — fala 3 e 5."""
    if lado == "L":
        sa([
            "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll",
            "LWristYaw", "LHand", "HeadYaw"
        ], [
            0.25, 0.42, -1.05, -0.58,
            0.55, 0.18, 0.28
        ], 0.13)
    else:
        sa([
            "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll",
            "RWristYaw", "RHand", "HeadYaw"
        ], [
            0.25, -0.42, 1.05, 0.58,
            -0.55, 0.18, -0.28
        ], 0.13)

def gesto_expansao():
    """Braços se expandem para os lados — grandiosidade, 'maior escola'."""
    sa([
        "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LHand",
        "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RHand",
        "HeadPitch"
    ], [
        0.30,  0.80, -1.60, -0.12, 1.0,
        0.30, -0.80,  1.60,  0.12, 1.0,
        -0.15
    ], 0.13)

def gesto_futuro():
    """Aponta para cima — olhar para o futuro, fala 5 (STEAM)."""
    sa([
        "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll",
        "RWristYaw", "RHand",
        "LShoulderPitch", "LHand",
        "HeadPitch", "HeadYaw"
    ], [
        -0.25, -0.20, 1.60, 0.05,
        -0.30, 0.1,
        1.00, 0.6,
        -0.25, -0.15
    ], 0.14)

def gesto_inclinacao():
    """Leve inclinação da cabeça — gesto de atenção e respeito."""
    sa("HeadPitch", 0.30, 0.10)
    time.sleep(0.60)
    sa("HeadPitch", -0.05, 0.10)
    time.sleep(0.30)

def gesto_acenar():
    """Acena com mão direita — encerramento amigável."""
    sa([
        "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll",
        "RWristYaw", "RHand"
    ], [
        0.0, -0.5, 1.5, 0.1,
        0.0, 1.0
    ], 0.13)
    for angulo in [0.55, -0.55, 0.55, -0.55, 0.0]:
        sa("RWristYaw", angulo, 0.10)
        time.sleep(0.28)

def gesto_parceria():
    """Mãos unidas à frente — 'somos parceiros'."""
    sa([
        "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll",
        "LWristYaw", "LHand",
        "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll",
        "RWristYaw", "RHand",
        "HeadPitch"
    ], [
        0.55,  0.12, -0.95, -1.05,
        0.85, 0.55,
        0.55, -0.12,  0.95,  1.05,
        -0.85, 0.55,
        0.0
    ], 0.12)

# ─── SEQUÊNCIA PRINCIPAL ─────────────────────────────────────────

print("NAO iniciando apresentação SESI SENAI...")
leds_cor(0xffffff, 0.5)
postura_base()
time.sleep(0.6)

# ════════════════════════════════════════════════════════════════
# FALA 1 — Convite para o estande
# "Oi, eu sou o NAO, quer saber como o SESI SENAI pode te ajudar
#  a crescer? Entre e conheça nossos serviços!"
# ════════════════════════════════════════════════════════════════
piscar_leds(0x00ccff, 3)         # piscada animada de "olá!"
leds_cor(0x00ccff, 0.4)

fala1 = falar(
    "Oi, eu sou o NAO, quer saber como o SESI SENAI "
    "pode te ajudar a crescer? Entre e conheça nossos serviços!"
)

gesto_olhar_plateia()            # olha para a plateia toda
time.sleep(0.3)
gesto_convidar()                 # abre os braços — "venha!"
time.sleep(0.5)
gesto_apontar_frente()           # aponta para o estande
time.sleep(0.5)
gesto_inclinacao()               # inclinação receptiva

fala1.join()
postura_base(0.11)
time.sleep(0.5)

# ════════════════════════════════════════════════════════════════
# FALA 2 — Saúde & Segurança
# "Trabalhador saudável é trabalhador produtivo. No SESI, cuidamos
#  da saúde e segurança de quem faz a nossa economia acontecer."
# ════════════════════════════════════════════════════════════════
leds_cor(0x00ff88, 0.5)          # verde — saúde

fala2 = falar(
    "Trabalhador saudável é trabalhador produtivo. "
    "No SESI, cuidamos da saúde e segurança de quem faz "
    "a nossa economia acontecer."
)

gesto_saude()                    # mão no peito depois abre
time.sleep(0.4)
gesto_enfase_pulso("L", 2)       # "trabalhador produtivo"
time.sleep(0.3)
gesto_olhar_plateia()            # inclui a todos
time.sleep(0.3)
gesto_enfase_pulso("R", 2)       # "economia acontecer"

fala2.join()
postura_base(0.11)
time.sleep(0.5)

# ════════════════════════════════════════════════════════════════
# FALA 3 — Carreira SENAI
# "O SENAI é a maior escola profissional da América Latina.
#  Vem transformar o seu talento em profissão com a gente."
# ════════════════════════════════════════════════════════════════
leds_cor(0xffaa00, 0.5)          # laranja — energia e conquista

fala3 = falar(
    "O SENAI é a maior escola profissional da América Latina. "
    "Vem transformar o seu talento em profissão com a gente."
)

gesto_expansao()                 # "a maior" — braços bem abertos
time.sleep(0.5)
gesto_enumerar("R")              # destaca o ponto
time.sleep(0.4)
gesto_palmas_cima()              # "vem com a gente"
time.sleep(0.4)
gesto_enfase_pulso("R", 2)       # ênfase em "talento"

fala3.join()
postura_base(0.11)
time.sleep(0.5)

# ════════════════════════════════════════════════════════════════
# FALA 4 — SESI SENAI Canedo
# "O SESI SENAI é o parceiro oficial para acelerar a indústria
#  e a sua carreira em Senador Canedo."
# ════════════════════════════════════════════════════════════════
leds_cor(0x0055ff, 0.5)          # azul institucional

fala4 = falar(
    "O SESI SENAI é o parceiro oficial para acelerar a indústria "
    "e a sua carreira em Senador Canedo."
)

gesto_parceria()                 # mãos unidas — "parceiro oficial"
time.sleep(0.6)
gesto_olhar_plateia()            # olha para todos
time.sleep(0.3)
gesto_enfase_pulso("R", 2)       # "acelerar"
time.sleep(0.3)
gesto_apontar_frente()           # "aqui, em Senador Canedo"

fala4.join()
postura_base(0.11)
time.sleep(0.5)

# ════════════════════════════════════════════════════════════════
# FALA 5 — Metodologia STEAM
# "Você sabia que no SESI unimos Ciência, Tecnologia e Arte?
#  Venha conhecer nossa metodologia e descobrir o futuro hoje!"
# ════════════════════════════════════════════════════════════════
piscar_leds(0xff00cc, 2)         # magenta — criatividade
leds_cor(0xff00cc, 0.4)

fala5 = falar(
    "Você sabia que no SESI unimos Ciência, Tecnologia e Arte? "
    "Venha conhecer nossa metodologia e descobrir o futuro hoje!"
)

gesto_enumerar("L")              # "Ciência"
time.sleep(0.45)
gesto_enumerar("R")              # "Tecnologia"
time.sleep(0.45)
gesto_expansao()                 # "e Arte!" — abre bem os braços
time.sleep(0.5)
gesto_futuro()                   # aponta para cima — "o futuro"
time.sleep(0.5)
gesto_convidar()                 # "venha!"

fala5.join()

# ─── ENCERRAMENTO ────────────────────────────────────────────────
postura_base(0.12)
time.sleep(0.4)
gesto_olhar_plateia()
gesto_inclinacao()
gesto_acenar()                   # aceno de tchau

leds.fadeRGB("FaceLeds", 0x000000, 1.2)

posture.goToPosture("StandZero", 0.4)
motion.wbEnable(False)
motion.rest()

print("Apresentação concluída.")