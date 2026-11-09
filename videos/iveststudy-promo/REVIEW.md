# REVIEW · iVest promo (76 s, 1920×1080, 30 fps, narrado)

## Decisões criativas
- Versão longa pedida: "todos os features", ~1 min, música nova, pronúncia "aiVest". A narração ficou em 74 s no ritmo natural da voz, então o filme tem 76 s; encurtar exigiria cortar funcionalidades.
- Estrutura: a voz é o relógio. Nove cenas: gancho (digitação + cronômetro) → reveal da marca → correção por IA (voz, modos, nota, checks, "Faltou") → treino do dia / XP / sequência → 11 trilhas → painel + rank Bronze→Elite → plano Pro (Mentor, simulados) → provas + 3 idiomas → end card.
- Dois mundos: o app escuro (0–34 s) e a landing branca (34–76 s), com um flood de cor na entrada das trilhas.
- Tudo que aparece como produto é real: caixa de resposta e cartão de correção reconstruídos em 2× a partir do tour oficial e do exemplo ilustrativo do site; tela inicial real do app (still do tour); grade de trilhas, cards de performance, medalhas e card do plano Pro são capturas da landing; os três tours oficiais (PT/EN/ES) lado a lado. Nenhum dashboard ou tela inventados.
- Copy dos títulos é do site: "Você estudou horas. Mas sabe onde errou?", "Escreva como na prova.", "Veja o que faltou.", "Treino do dia", "Tudo que cai nas grandes provas.", "O que é medido, é melhorado.", "Cada treino te aproxima de virar Elite.", "3 DIAS GRÁTIS NO CADASTRO", "Criar conta grátis →".
- Música: loop instrumental gerado pelo gerador de som da ElevenLabs (prompt: eletrônico otimista, 118 BPM), repetido 4× e a 0,2 sob a voz. A API de música da ElevenLabs e a geração no Runway exigem plano pago. O analisador classificou o arquivo como música (confiança 0,9); ninguém ouviu.
- Pronúncia: "aiVest" escrito no roteiro; em português a leitura natural é "ai-vést". Os títulos na tela mantêm a grafia oficial "iVest".

## O que foi medido e o que só foi olhado
- `hyperframes check`: ok, sem erros nem avisos na versão final.
- `snapshot --review` (18 beats, 8 emendas, folha de celular) + 16 quadros intermediários: olhados; corrigidos: faixa preta no quadro da tela inicial, realce dos modos deslocado, primeira coluna da grade cortada, cards do painel pequenos demais, título "Feedback estruturado." quebrando sobre a linha de baixo.
- Áudio do MP4 medido com `hyperframes audio` (loudness, picos, silêncio). Ninguém ouviu a mixagem nem a voz.

## Ponto mais fraco
- A música é um loop de 22 s gerado por IA; pode soar repetitivo em 76 s. Com uma trilha licenciada do cliente, troca em um minuto (`assets/audio/music-loop.m4a`).
- A voz "Sarah" é uma voz padrão em inglês falando português; pode ter leve sotaque. Com plano pago da ElevenLabs, "Roberta" ou "Paulo" (nativos) já estão na conta.
- Mentor iVest não tem tela capturável sem login; aparece só no título e na fala.

## Avisos mantidos de propósito
- Nenhum. O end card tem `data-hold` (parado de propósito nos últimos 3 s).
