# REVIEW · iVest promo desktop (98 s, 1920×1080, 30 fps, narrado)

## O que mudou nesta versão
- Pedido: capturas e takes novos do app na versão desktop, cobrindo todos os recursos e benefícios. Entrei no app com a conta do cliente e gravei os fluxos reais em 1440×900 (vídeo) e 2× (capturas): Modo Estudo com três respostas corrigidas pela IA ao vivo (todas 10/10), Quiz, Flashcards, Simulado ENEM, Redação avaliada por competência (920/1000), Mentor respondendo, Dashboard, Ranks, Conquistas, Turma & Ranking, tela inicial em modo escuro e em EN/ES.
- Privacidade: o e-mail do cliente foi substituído por "ana@exemplo.com" e o link Admin ocultado via injeção de script nas capturas. A senha ficou só no diretório temporário da sessão, fora do repositório. As respostas, a redação e os cliques ficaram registrados na conta (3 tentativas 10/10 em Biologia, 2 quizzes certos, 1 redação, 2 flashcards).
- Look: chão navy #0F172A (a faixa escura da própria landing), janelas do app com raio 20 px e sombra ocupando 57% da largura, títulos Inter 700 68 px à esquerda com uma palavra em #60A5FA, câmera com punch-ins de 1,2× a 2,1× nos controles que a voz nomeia, etiqueta "Tela real do app · desktop". End card branco.
- Estrutura em 12 cenas guiadas pela narração (VOICEOVER.md). Música: loop gerado pela ElevenLabs a 118 BPM, 0,2 sob a voz.

## Medido e olhado
- `hyperframes check`: ok, sem erros nem avisos na versão final.
- `snapshot --review` (24 beats) + quadros intermediários: olhados. Corrigido: um trecho da gravação do Modo Estudo em que a captura de página inteira deixou meio quadro cinza; a cena passa a usar a captura estática da página completa com a câmera rolando pela Avaliação, Resposta de referência e Revisão analítica.
- Áudio do MP4 medido com `hyperframes audio`; ninguém ouviu a mixagem nem a voz.

## Pontos fracos
- O Dashboard do cliente carrega dados antigos de teste (média 2,5 de 10, 23% de acerto); a câmera foca no mapa de atividade e no desempenho por trilha, mas a linha de KPIs aparece por um instante. Responder mais questões com nota alta na conta melhora isso.
- "Ranks" mostra "Sem rank" porque a conta tem menos de 10 respostas no modo Estudo; a tela inicial mostra "Elite". Usei a faixa Bronze→Elite da página de Ranks, sem o status.
- A voz "Sarah" é uma voz padrão em inglês falando português. Voz nativa exige o plano Starter da ElevenLabs.
- A música é um loop de 22 s gerado por IA; uma trilha licenciada seria melhor em 98 s.

## Avisos mantidos de propósito
- Nenhum. `data-hold` na linha de apoio do reveal e no botão do end card marcam as paradas deliberadas.
