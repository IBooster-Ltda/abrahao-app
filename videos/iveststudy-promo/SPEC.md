GOAL:    o viewer entende que no iVest ele escreve a resposta e a IA mostra o que faltou, e quer criar a conta grátis.
OUTPUT:  HyperFrames, 1920 x 1080, 30 fps
TIME:    26 s x 30 = 780 quadros; trilha do tour a 120 BPM = 15 quadros por batida, 60 por compasso; pico da trilha em 19,56 s = flood para o branco
LOOK:    mundo app (0–19,5 s): chão #0F1115 liso, cartões #171A21 com borda 2 px #262B35 e raio 20 px, tinta #E6E8EC, cinza #9AA3B2,
         acento #2563EB (botões, ring) e #60A5FA (uma linha do título por cena), âmbar #FBBF24 só na linha "Faltou", verde #22C55E só nos checks;
         mundo landing (19,5–26 s): chão #FFFFFF, tinta #0F172A, acento #2563EB em "que muda tudo." e no botão.
         Display Inter 700 92 px tracking -0.03em (8,5% da altura), linhas de apoio Inter 500 40 px; UI reconstruída em 2x: corpo Inter 400 34 px,
         rótulos Inter 600 22 px tracking 0.12em caixa alta, cronômetro JetBrains Mono 700 64 px.
         Sem textura, sem glow; sombra dos cartões 0 24px 60px rgba(0,0,0,.45). Vídeo real do app dentro de um recorte 648x900 com raio 28 px.
OBJECTS: caixa de resposta do app (rótulo "CRONÔMETRO DA PERGUNTA", 2:52 caindo por segundo, chips Normal/Rápido/Turbo, área de texto, rodapé
         "Responder por voz · PT EN · Limpar"); cartão "Correção por IA" (anel 7/10, dois checks verdes, uma linha âmbar "Faltou:");
         telefone sem moldura: só o recorte do vídeo real do tour (quiz com resposta verde, rank Bronze→Elite); a marca: quadrado azul com capelo
         (ivest-cap.svg do próprio site) + wordmark "iVest" (Inter 700, "i" azul como no site).
MOTION:  entrada de título: por palavra blur 6px→0 + opacidade em 0,13 s, 0,07 s entre palavras, sem translate; título parado depois que pousa.
         chegada de cartão: power4.out 0,5 s; carry (cartão→telefone): scale 1→0,6 com blur pico 6 px em 0,45 s power2.inOut;
         punch-in no "Faltou": scale 1→1,32 em 0,5 s power2.inOut com origem na linha, segura 2,4 s; flood: cor do chão em 0,4 s power2.inOut;
         marca no end card: scale 0,2→1 back.out(1.4) 0,6 s; wordmark: clip-path wipe 0,35 s power3.out. Digitação 47 caracteres/s. Nada em loop.
SHOTS:   0–198 (0–6,6 s) HOOK: caixa de resposta em 2x à direita, texto digitando de 0,8 a 5,4 s, cronômetro 2:52→2:46; "Você estudou horas." pousa em 0,3–0,9 s,
                 "Mas sabe onde errou?" em 2,6 s com "onde" em #60A5FA; som: teclas. Handoff: a caixa empurra para dentro (scale 1,08 + blur) nos últimos 12 quadros.
         198–378 (6,6–12,6 s) CORREÇÃO: cartão "Correção por IA" chega do centro da caixa (scale 0,6→1, blur 8→0); anel 0→7/10 em 0,8 s; check 1 em 8,0 s, check 2 em 8,5 s (pops),
                 "Faltou: por que caudas insaturadas dão fluidez" em 9,2 s (riser 8,2→impacto 9,2); punch-in 9,4–9,9 s, segura até 12,2 s; título "A IA corrige." / "Veja o que faltou.".
                 Handoff: o cartão encolhe e some com blur (carry) nos últimos 14 quadros.
         378–588 (12,6–19,6 s) PROVA: recorte do vídeo real do app (tour 12–19 s) entra da direita com whoosh; títulos à esquerda: "Quiz rápido." / "Correção na hora." (12,9 s),
                 "Suba de nível" / "do Bronze ao Elite." (15,8 s); linha de apoio "2600+ questões guiadas · 11 disciplinas · ENEM, Fuvest, Unicamp, PAES e SAT" (17,4 s).
         588–678 (19,6–22,6 s) CLAIM: flood branco em 19,56 s sobre o pico da trilha; "Prepare-se para o exame" / "que muda tudo." (azul), por palavra; segura 2 s.
         678–780 (22,6–26 s) END CARD: marca entra com mola, wordmark wipe, botão real "Criar conta grátis →" sobe, "3 dias de Pro grátis" e "iveststudy.com"; segura 2,5 s; trilha fade 1,5 s.
BANNED:  vazio escuro com coisas pequenas no meio (a UI ocupa ≥45% da altura e tem um título ao lado); glow, partículas, gradientes; três cards em linha; KPI grid; logo no canto;
         tudo entrando por fade+slide-up; título que continua se movendo; dashboard inventado; botão ou rótulo que o site não tem; moldura de celular desenhada;
         cursor clicando em algo que não existe no app.
QA:      f0 (não vazio: caixa + cronômetro visíveis), f27 (título pousado), f210 (cartão chegou), f276 ("Faltou" legível em 2x), f390 (vídeo real visível, título lido),
         f587→f590 (flood sem salto nos títulos), f700 (marca + botão + domínio legíveis), f779 (último quadro = end card parado).
