# REVIEW · iVest promo · corte "pitch" (77 s, 1920×1080, 30 fps, narrado)

## Referências do cliente
1. TikTok de 15,7 s: notebook no escuro, frases digitadas, tiques → impacto no logo, silêncio.
2. TikTok de 38 s: um pitch de slides tocando num notebook. Fundo navy com orbe azul, frases de dor ("Você se identifica?"), logo com arco de luz, "O que você ganha" com 4 cards numerados (um aceso), números contando (+90, +R$11M), "Simples assim, em 3 passos", CTA, flood azul com um único impacto forte (34,0 s, −9 dB) e silêncio. Quase nenhuma captura do produto.

## O que foi aplicado
- Estrutura espelhada na referência 2: gancho com notificações → 4 dores → logo → 6 cards de features → 1 captura real → 4 números → 3 passos → CTA → flood.
- Os ícones são os da barra lateral do próprio app (extraídos do DOM logado, lucide), então quem nunca abriu o iVest entende o que é Modo Estudo, Quiz, Flashcards, Simulados, Redação e Mentor.
- Só uma captura real (a correção 10/10), a única que o argumento precisa.
- O card aceso e os números entram no instante em que a voz diz a palavra (timestamps por caractere da ElevenLabs).
- "Tcham" duplo: tiques acelerando + riser → slam do logo (16,1 s, −5 dB RMS) e → flood azul (71,0 s, −6 dB), música a zero, 5 s de cartão em silêncio.
- Nenhum número inventado: 5 bancas, 0–1000, ranks Bronze→Elite e PT/EN/ES vêm do app.

## Revisão: "trava em alguns pontos"
Medido com `freezedetect` no primeiro render: nenhum quadro duplicado, mas trechos de até 3 s em que a imagem mudava quase nada (só o orbe derivando): o logo depois do slam, a grade de features entre um destaque e outro, os números, o botão. Correção: o orbe respira (escala e opacidade em seno, 2,6 s) e deriva; cada cena tem um push lento contínuo; a cena inclina para o card, o número ou o passo ativo (lean 0,8–0,9 s); o ícone do card ativo pulsa; o arco do logo gira devagar; o botão pulsa o brilho. O cartão final continua parado de propósito, como na referência.
Segunda passada: o orbe saiu das cenas e foi para a raiz (uma luz só, com deriva e respiração contínuas nos 77 s e um flash nos dois impactos), então a luz não pula mais nos cortes. Resultado medido no render final: zero trechos parados antes do cartão final (antes eram 37). Revisão de 77 quadros, um por segundo: sem texto cortado, sem sobreposição, destaque sempre no card falado.

## Medido e olhado
- `hyperframes check`: ok. Avisos restantes: holds curtos nos 3 passos (1,6–1,7 s) e a heurística de "última linha" do cartão final (o cartão fica 5 s parado; o aviso vem do cursor piscando).
- 21 snapshots + folha de contato do MP4 olhados; áudio medido (−14,2 LUFS integrado, pico real −1,2 dB, sem clipping). Ninguém ouviu.
- Para o TikTok: tocar este MP4 em tela cheia no notebook, filmar no escuro com o celular, como nas referências.
