GOAL:    um estudante entende tudo que o iVest faz, vendo o app desktop em modo noturno funcionando de verdade, e cria a conta grátis.
OUTPUT:  HyperFrames, 1920 x 1080, 30 fps
TIME:    97 s x 30 = 2910 quadros; a narração (12 falas, VOICEOVER.md) é o relógio; música gerada a 118 BPM a 0,2 sob a voz; flood para o branco em 88,4 s
LOOK:    chão: textura gerada (navy com bokeh sutil, assets/gen/backdrop-dark.jpg) sobre #0F172A; abertura e fechamento em fotos geradas (estudante à noite, campus ao amanhecer) escurecidas, tinta #FFF, cinza #9AA3B2, acento #60A5FA (uma palavra por título); janelas do app 1100x688 (16:10) em left 780 / top 190, raio 20 px, borda 2 px rgba(255,255,255,.1),
         sombra 0 30px 80px rgba(0,0,0,.55); dentro, a gravação ou captura 1440x900 do app desktop com câmera (scale 1,0–2,1, punch de 0,6–0,9 s power2.inOut, origem no controle nomeado pela voz);
         títulos Inter 700 68 px tracking -0,03em em duas linhas (top 300 / 380), linhas de apoio Inter 500 30 px (top 500); etiqueta "TELA REAL DO APP · DESKTOP" 26 px caixa alta sob a janela; end card branco com tinta #0F172A e acento #2563EB.
OBJECTS: só telas reais do app logado: Modo Estudo (pergunta, cronômetro, símbolos, caixa de resposta, "Responder por voz", "Avaliar resposta", 10/10, Avaliação, Resposta de referência, Revisão analítica), tela inicial em modo escuro
         (Nível 3, meta, 1 dia, Treino do dia, Missões, Reta final 363 dias), Flashcards (frente, verso, Não sabia/Quase lá/Sabia!), Quiz ("Correto!"), Simulados (bancas, ENEM 75 min), Redação (920/1000, C1–C5), Mentor,
         Dashboard, Progressão de Ranks, Conquistas, Turma & Ranking, home em EN/ES; marca: capelo + wordmark "iVest".
MOTION:  janelas entram em 0,55 s power4.out deslizando de fora (alternando lado), saem em 0,4 s power3.in com blur; títulos por palavra blur 6→0 em 0,13 s; a câmera só se move quando a voz nomeia algo; vídeo em 1,0–4× conforme a cena; nada em loop.
SHOTS:   ver VOICEOVER.md (12 cenas, uma por fala): hook 0–5,6 · reveal 5,6–11,5 · estudo 11,5–27 · home 27–38,5 · flashcards 38,5–46,6 · quiz 46,6–51,4 · simulados 51,4–59,9 · redação 59,9–66,5 · mentor 66,5–72,1 · progresso 72,1–82,2 · turma/idiomas 82,2–88,8 · end card 88,8–98.
BANNED:  mockups ou telas inventadas; dados pessoais do cliente (e-mail mascarado, Admin oculto); vazio escuro com coisas pequenas (a janela ocupa 57% da largura e sempre há um título); glow, partículas, gradientes; três cards em linha;
         logo no canto; tudo entrando por fade+slide-up; título que continua se movendo; a tela repetindo a frase falada palavra por palavra; quadro cinza de captura (removido da cena de correção).
QA:      f0 janela + título visíveis; f170 reveal; f500 realce 10/10 inteiro no quadro; f660 Avaliação legível; f900 Treino do dia; f1250 verso do flashcard; f1460 "Correto!"; f1700 simulado ENEM 75 min; f1860 920/1000; f2050 Mentor; f2250 heatmap;
         f2400 Bronze→Elite; f2560 Turma; f2880 end card parado.
