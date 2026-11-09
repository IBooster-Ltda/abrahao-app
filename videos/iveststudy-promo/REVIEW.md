# REVIEW · iVest promo (26,4 s, 1920×1080, 30 fps, narrado)

## Decisões criativas
- Storyline A ("Faltou") construída; B ("Horas sem feedback", antes/depois em split screen) e C ("Três provas, uma tela", tipografia na batida) ficaram em `STORYLINES.md`.
- Tudo que aparece como produto vem do site: a caixa de resposta e o cartão "Correção por IA" foram reconstruídos em 2× a partir do tour oficial e do exemplo ilustrativo da landing (rótulo "Exemplo ilustrativo" mantido, como o site faz); as telas de quiz e rank são o vídeo real do tour (`/video/ivest-pt.mp4`), recortado para esconder os títulos do próprio tour.
- Copy verbatim do site e do tour: "Você estudou horas. Mas sabe onde errou?", "A IA corrige. Veja o que faltou.", "Quiz rápido. Correção na hora.", "Suba de nível, do Bronze ao Elite.", "Prepare-se para o exame que muda tudo.", "Criar conta grátis →", "Cadastre-se grátis e ganhe 3 dias de Pro.". Números: 2600+ questões, 11 disciplinas, 5 provas (da landing).
- Marca: o capelo azul do favicon/OG do site e o wordmark "iVest" com o "i" azul, como no cabeçalho do site. Só no end card.
- Narração: cinco falas em pt-BR (`VOICEOVER.md`) com a voz local Kokoro `pf_dora`, gratuita, porque não há credencial HeyGen; a tela nunca repete a frase falada. Alternativas prontas: `pm_alex` (masculina) ou HeyGen com chave. A música ficou a 0,2 sob a voz.
- Música: a trilha do próprio tour (120 BPM, pico em 19,56 s), porque não há credencial HeyGen nem chave Gemini nesta sessão; o flood para o branco cai sobre esse pico. Efeitos: teclas na digitação, pops nos checks, riser + impacto no "Faltou", whoosh nas entradas e no flood, pop na marca, clique no botão.

## O que foi medido e o que só foi olhado
- `hyperframes check`: ok, sem erros e sem avisos na versão final.
- `snapshot --review` + quadros em 0, 2,4, 5,6, 9,9, 13,5, 16,5, 17, 19,45, 19,9, 25,9 s: olhados.
- Áudio do MP4: medido com `hyperframes audio` (presença, picos, loudness). Ninguém ouviu o resultado.
- Não verificado: como a trilha do tour se comporta nos 3,9 s finais em loop (corte em 22,5 s com crossfade de 0,4 s).

## Ponto mais fraco
- O trecho 12,6–15,2 s mostra, no vídeo real, o cartão de correção que acabamos de reconstruir; é prova de que existe, mas repete a ideia. Com mais tempo: capturar a tela do quiz direto no app com login e dar 1 s a mais ao rank.
- O quadro 0 tem só a caixa de resposta (o título entra em 0,3 s); como thumbnail funciona, mas um quadro com o título já pousado seria mais forte.

## Avisos mantidos de propósito
- Nenhum. Os de tamanho de tipo nas etiquetas da UI foram resolvidos subindo para 28 px; o texto digitado está marcado como `data-layout-ignore` porque é digitação, não linha para ler.

## Licença e dependências
- HyperFrames (Apache/MIT), GSAP 3.15 embutido em `assets/vendor/` porque o navegador de render não alcança o CDN nesta sessão; efeitos sonoros do pacote `media-use` (créditos em `assets/sfx/CREDITS.md`); trilha e vídeo do tour pertencem ao iVest.
