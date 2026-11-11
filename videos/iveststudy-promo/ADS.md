# iVest Study · anúncios de performance (cadastro grátis)

Objetivo único: cadastro grátis. Público: 16–20 anos, ENEM / Fuvest / Unicamp / PAES / SAT.
Tudo que aparece do produto é captura real do app logado, em tela de celular (430×932 a 3×), gravada por screencast do Chrome; nenhuma tela foi desenhada ou alterada. Nomes de arquivo em `deliver/`.

## Entregáveis
| Arquivo | Formato | Duração | Uso |
|---|---|---|---|
| `deliver/ad30a.mp4` (+ `.srt`) | 1080×1920 | 30 s | Principal · Reels / TikTok / Shorts · gancho A (redação corrigida) |
| `deliver/ad30b.mp4` | 1080×1920 | 30 s | Teste · gancho B (rosto frustrado: "Errei e não sei por quê.") |
| `deliver/ad30c.mp4` | 1080×1920 | 30 s | Teste · gancho C (contagem "Faltam N dias para o ENEM") |
| `deliver/ad15.mp4` | 1080×1920 | 15 s | Corte curto: gancho + demo + oferta |
| `deliver/ad06.mp4` | 1080×1920 | 6 s | Bumper |
| `deliver/ad45-1920x1080.mp4` | 1920×1080 | 45 s | YouTube / site · + 3 passos + selos das bancas |
| `deliver/ad45-1080x1080.mp4` | 1080×1080 | 45 s | Feed |
| `deliver/ad-sat-en.mp4` | 1080×1920 | 31 s | Versão SAT em inglês: SAT e 3 idiomas como protagonistas |

Cada MP4: H.264 30 fps, AAC, legendas da narração queimadas, −14 LUFS integrado, pico −1 dBTP, sem silêncio no final (assinatura sonora). O `.srt` de cada peça fica ao lado.

## Roteiro da versão de 30 s (A)
| Tempo | Tela | Narração (Matheus, voz jovem, ritmo rápido) |
|---|---|---|
| 0:00–0:02 | Resultado real de redação: a nota sobe e trava em **480/1000**; C2 80/200 pisca em vermelho. "Redação corrigida: 480 de 1000." | "Você estuda, faz simulado… |
| 0:02–0:06 | Três dores em 1,5 s: mesa de estudo / rosto / campo azul. "O problema não é estudar. É estudar sem feedback." | …e continua sem saber onde erra." |
| 0:06–0:17 | Modo Estudo de verdade: pergunta de História (Código de Hamurábi), resposta mediana digitada com o cronômetro correndo, toque em Avaliar, 0,5 s de silêncio, **4/10** com a batida, e a avaliação real da IA em texto grande: verde o que acertou, vermelho o que faltou. | "No iVest Study, cada resposta é corrigida na hora por IA." / "Você vê a nota, o que faltou e o que revisar." |
| 0:17–0:23 | Montagem 1,5 s por recurso, interface real: Redação (0 a 1000), Simulados (formato de cada banca, cronômetro), Flashcards, Mentor IA. | "Redação com nota por competência, simulados de cada banca e um mentor que tira suas dúvidas." |
| 0:23–0:26 | Tela de cadastro real + "Grátis para sempre." / "3 dias de Pro ao criar sua conta." / "Sem cartão." | "Grátis para sempre, com três dias de Pro ao criar sua conta. Sem cartão." |
| 0:26–0:30 | Flood azul: logo **iVest Study**, **iveststudy.com** grande e fixo por 4 s, botão, assinatura sonora. | "Crie sua conta grátis em iveststudy.com." |

Prova social (0:22–0:25 no brief): **cortada**, como o brief manda quando não há número ou depoimento real verificável. Quando existir (usuários, questões corrigidas, depoimento autorizado), o bloco entra entre a montagem e a oferta.

## O que mudou em relação ao brief, e por quê
- **"Sua redação levou 3 segundos para ser corrigida"**: medi duas correções reais de redação: 14,7 s e 22,4 s. A frase seria falsa; o gancho A usa a nota real (480/1000) e a competência real em vermelho (C2 80/200). A correção do Modo Estudo levou 4,5 s; é ela que aparece "na hora".
- **Nota 6/10 e "crise do século III"**: a nota e o comentário são os que a IA deu de verdade à resposta mediana que digitei: 4/10, com dois erros apontados (talião como "justiça de vingança"; leis "para todo mundo"). O texto na tela é o comentário real, só colorido.
- **Trechos em verde/vermelho**: o app não destaca trechos da resposta; a cor entra no cartão de avaliação sobreposto, com o texto real da IA.
- **Imagens de estudantes**: não há filmagem de aluno real. As cenas de mesa e do rosto são imagens geradas por IA (4 fotos, `assets/gen/m/`). Se forem usadas em anúncio, trate como ilustração; o ideal é substituí-las por filmagem própria com autorização.
- **Gancho C (contagem)**: calculado a partir da data oficial do INEP (Edital nº 64/2026: 8 e 15/11/2026). Hoje a contagem aponta para 15/11. Depois dessa data não há data oficial do ENEM 2027; a variante C só deve ser publicada com a data confirmada (`ENEM_DATE` em `tools/ad.py`).
- **"1000 pontos na redação"** virou "Nota de 0 a 1000". **"3 idiomas"** saiu da versão brasileira e virou protagonista na versão SAT.
- **Notificação contraditória**: o gancho com notificações foi removido; não existe mais "10/10. Veja o que faltou".
- **Marca**: "iVest Study" no logo de fechamento, na narração e na URL; `iveststudy.com` em marca d'água discreta a partir de 0:06 e grande no final.
- **Dados de teste**: o nome na conta é "Davi"; o e-mail não aparece na interface de celular; o link "Admin" foi ocultado antes de gravar; nenhuma imagem quebrada (a pergunta com imagem é pulada automaticamente).

## Áudio
- Narração: ElevenLabs, voz "Matheus" (biblioteca, pt-BR jovem), speed 1,1; versão SAT: "Liam" (en). Timestamps por palavra geram as legendas queimadas e os `.srt`.
- Música: ElevenLabs Music, 120 BPM, plano de 5 seções (gancho, demo, impacto, montagem, oferta); cortes no grid de 0,5 s. Silêncio de 0,5 s antes da nota (automação), impacto na nota.
- Efeitos: digitação, toque de envio, ding na nota, blip no erro, whoosh nas transições, pop na oferta, assinatura sonora de 1,5 s no fechamento (gerados na API de efeitos).
- Mixagem: narração ≈ 6 dB acima da música; master normalizado a −14 LUFS / −1 dBTP em dois passos de `loudnorm`.

## Texto na tela
Máximo de 7 palavras por tela e uma ideia por tela; títulos 80–120 px, apoio ≥ 40 px, legendas 46 px, marca d'água 35 px; branco sobre fundo escuro ou azul (≥ 4,5:1); títulos a partir de y = 255 px e legendas até y ≈ 1470 px (fora dos 250 px superiores e 400 px inferiores do 9:16).

## Checklist final
- [x] Correção da IA completa e legível antes de 0:16 (4/10 em 0:13, avaliação em 0:14,5–0:17).
- [x] Oferta grátis antes de 0:30 (0:23) e URL fixa por ≥ 3 s (0:26–0:30).
- [x] Sem imagem quebrada, e-mail de teste ou número contraditório.
- [x] Todos os números são reais: 480/1000, 4/10, C1–C5, 7/10 (SAT), cronômetros do app. Nenhum número de usuários (prova social cortada).
- [ ] Assistir no celular sem som, a um braço de distância: feito só por quadros a 1080 px; peça para alguém assistir no aparelho antes de publicar.
- [x] H.264 30 fps, legenda queimada, `.srt` separado.
- [ ] Variante C: confirmar a data do INEP antes de publicar.

## Reproduzir
`tools/capture-phone.mjs` grava o app (login via `state.json` da sessão, nunca no repositório); `tools/assemble-screencast.py` monta os MP4 a partir dos quadros; `tools/ad.py 30a 30b 30c 15 6 45w 45s sat` gera `builds/*.html` e `deliver/*.srt`; `tools/render-queue.sh` renderiza e normaliza. O projeto HyperFrames usa `index.html` como entrada: copie o build desejado para lá antes de `check`, `snapshot` ou `render`. O filme longo anterior (77 s) está em `builds/film77.html`.
