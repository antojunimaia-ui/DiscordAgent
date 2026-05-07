import google.generativeai as genai
import json
import config
import httpx
from bs4 import BeautifulSoup
import re
import io
from PIL import Image

genai.configure(api_key=config.GEMINI_API_KEY)

class AIEngine:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-3.1-pro-preview')

    async def _fetch_url_content(self, url: str):
        """Busca o conteúdo de texto de uma URL."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=10.0, follow_redirects=True)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    # Remove scripts e estilos
                    for script in soup(["script", "style"]):
                        script.decompose()
                    text = soup.get_text(separator=' ', strip=True)
                    return text[:5000] # Limite para não estourar o contexto desnecessariamente
        except Exception as e:
            print(f"Erro ao raspar site: {e}")
            return None

    async def generate_server_structure(self, theme: str, use_emojis_channels: bool, use_emojis_categories: bool, use_emojis_roles: bool, num_roles: int, image_bytes: bytes = None):
        website_context = ""
        visual_context = ""
        
        # 1. Processar URL se houver
        url_match = re.search(r'https?://[^\s]+', theme)
        if url_match:
            url = url_match.group(0)
            print(f"Detectada URL: {url}. Analisando...")
            
            # Se for link de template do Discord, damos um contexto especial
            if "discord.new" in url or "discord.com/template" in url:
                website_context = f"\nO usuário forneceu um TEMPLATE do Discord: {url}. Ignore o scraping de site e tente recriar a estrutura baseada no que esse template sugere pelo nome/contexto."
            else:
                content = await self._fetch_url_content(url)
                if content:
                    website_context = f"\nO usuário forneceu esta URL como referência: {url}\nCONTEÚDO EXTRAÍDO DO SITE:\n'''\n{content}\n'''\n\nINSTRUÇÃO: Use essas informações para criar o servidor."

        # 2. Processar Imagem se houver (Visão Multimodal)
        inputs = []
        if image_bytes:
            print("Processando imagem para clonagem visual...")
            img = Image.open(io.BytesIO(image_bytes))
            visual_context = "\nO usuário anexou um PRINT de um servidor. Analise a imagem, identifique os nomes dos canais, emojis e a hierarquia de categorias e REPRODUZA-A fielmente."
            inputs.append(img)
        
        emoji_instr_channels = "Use emojis discretos nos nomes de cada CANAL." if use_emojis_channels else "NÃO use emojis nos nomes dos canais, apenas texto limpo."
        emoji_instr_categories = "Use emojis nos nomes das CATEGORIAS." if use_emojis_categories else "NÃO use emojis nos nomes das categorias."
        emoji_instr_roles = "Use emojis nos nomes de cada CARGO." if use_emojis_roles else "NÃO use emojis nos nomes dos cargos."

        prompt = f"""
        Você é um Visionário de Comunidades e Mestre em Worldbuilding.
        Sua missão é projetar um servidor Discord com uma ATMOSFERA IMERSIVA, CRIATIVA e ÚNICA.

        TEMA/DESCRIÇÃO: "{theme}"
        {website_context}
        {visual_context}

        REQUISITOS DE DESIGN:
        - Emojis nos Canais: {emoji_instr_channels} (Use emojis que reforcem o tema especificamente).
        - Emojis nas Categorias: {emoji_instr_categories}
        - Emojis nos Cargos: {emoji_instr_roles}
        - Quantidade de Cargos: Gere EXATAMENTE {num_roles} cargos hierárquicos e temáticos.

        DIRETRIZES DE CRIATIVIDADE E IMERSÃO:
        1. Nomes Narrativos: NUNCA use nomes genéricos como "geral", "staff" ou "regras" se puder usar algo temático. (Ex: No tema Espacial, use "🛰️-centro-de-comando" em vez de "geral").
        2. Tópicos de Canais: Escreva descrições curtas e criativas para cada canal que ajudem o usuário a entrar no clima do servidor.
        3. Cores de Cargos: Escolha cores HEX que combinem com a paleta visual do tema.

        ENGENHARIA DE SEGURANÇA (Invisível mas Presente):
        - Mantenha a lógica de permissões: Canais de anúncios/regras como leitura e canais de staff privados, mas com nomes temáticos.

        Sua resposta deve ser EXCLUSIVAMENTE um objeto JSON válido:
        {{
            "server_name": "Nome Épico do Servidor",
            "welcome_message": "Uma mensagem de boas-vindas épica e temática...",
            "roles": [ 
                {{"name": "Título Temático Alto", "color": "0xHEX", "permissions": ["administrator"], "hoist": true}},
                {{"name": "Título Temático Base", "color": "0xHEX", "permissions": ["view_channel", "send_messages"], "hoist": false}}
            ],
            "categories": [
                {{
                    "name": "CATEGORIA TEMÁTICA",
                    "channels": [ 
                        {{"name": "nome-imersivo", "type": "text", "topic": "Descrição narrativa...", "overwrites": {{"@everyone": {{"view_channel": true}}}}}} 
                    ]
                }}
            ]
        }}
        """
        inputs.append(prompt)
        
        # Chamada única e correta passando a lista de inputs (imagem + texto)
        response = await self.model.generate_content_async(inputs)
        text = response.text.strip()
        
        # Limpar fatias de markdown se o Gemini insistir em colocar
        if text.startswith("```json"):
            text = text[7:]
        if text.endswith("```"):
            text = text[:-3]
            
        try:
            return json.loads(text.strip())
        except Exception as e:
            print(f"Erro ao parsear JSON da IA: {e}")
            return None

    async def reconstruct_server_structure(self, current_structure: dict, use_emojis_channels: bool, use_emojis_categories: bool, use_emojis_roles: bool, num_roles: int):
        current_json = json.dumps(current_structure, indent=2, ensure_ascii=False)
        
        emoji_instr_channels = "Use emojis discretos nos nomes de cada CANAL." if use_emojis_channels else "NÃO use emojis nos nomes dos canais, apenas texto limpo."
        emoji_instr_categories = "Use emojis nos nomes das CATEGORIAS." if use_emojis_categories else "NÃO use emojis nos nomes das categorias."
        emoji_instr_roles = "Use emojis nos nomes de cada CARGO." if use_emojis_roles else "NÃO use emojis nos nomes dos cargos."

        prompt = f"""
        Você é um Visionário de Comunidades e Mestre em Worldbuilding.
        O usuário quer TRANSFORMAR e ELEVAR a estrutura existente do servidor dele para um novo patamar de IMERSÃO e CRIATIVIDADE.
        
        Abaixo está a ESTRUTURA ATUAL do servidor em formato JSON:
        ```json
        {current_json}
        ```

        Sua missão é atuar como um arquiteto criativo:
        1. Analise o que já existe e identifique o "alma" do servidor.
        2. Proponha uma REFORMA TOTAL BASEADA NO TEMA.
        3. Converta nomes simples (ex: "geral") em nomes épicos e imersivos que contem uma história.
        4. Crie cargos que pareçam uma progressão real dentro de uma organização ou mundo fictício.
        
        DIRETRIZES TÉCNICAS:
        - Mantenha a segurança nas permissões, mas os nomes devem ser 100% criativos.
        - Se houver canais de voz, dê nomes que instiguem a conversa (ex: "🍻-taberna-do-grito").
        
        REQUISITOS DE DESIGN:
        - Emojis nos Canais: {emoji_instr_channels}
        - Emojis nas Categorias: {emoji_instr_categories}
        - Emojis nos Cargos: {emoji_instr_roles}
        - Quantidade de Cargos: Gere EXATAMENTE {num_roles} cargos.

        Sua resposta deve ser EXCLUSIVAMENTE um objeto JSON válido:
        {{
            "server_name": "Nome Transformado e Épico",
            "welcome_message": "Uma celebração da nova era do servidor...",
            "roles": [ {{"name": "Título de Elite", "color": "0xHEX", "permissions": ["administrator"], "hoist": true}} ],
            "categories": [
                {{
                    "name": "NOME DA CATEGORIA ÉPICA",
                    "channels": [ {{"name": "nome-imersivo", "type": "text", "topic": "...", "overwrites": {{"@everyone": {{"view_channel": true}}}}}} ]
                }}
            ]
        }}
        """
        
        response = await self.model.generate_content_async([prompt])
        text = response.text.strip()
        
        if text.startswith("```json"):
            text = text[7:]
        if text.endswith("```"):
            text = text[:-3]
            
        try:
            return json.loads(text.strip())
        except Exception as e:
            print(f"Erro ao parsear JSON da IA na reconstrução: {e}")
            return None

    async def update_server_structure(self, current_structure: dict, user_prompt: str):
        """Atualiza uma estrutura gerada (draft) baseada no feedback do usuário."""
        current_json = json.dumps(current_structure, indent=2, ensure_ascii=False)
        
        prompt = f"""
        Você é um arquiteto do Discord auxiliando um administrador a refinar a estrutura do servidor.
        
        Aqui está o RASCUNHO ATUAL do servidor em formato JSON:
        ```json
        {current_json}
        ```
        
        O administrador solicitou a seguinte modificação:
        "{user_prompt}"
        
        Sua missão é aplicar esta modificação de forma inteligente no rascunho atual.
        Mantenha a mesma formatação e os campos não afetados do JSON original.
        Apenas retorne o JSON atualizado, sem introduções ou marcações markdown, como pedido anteriormente.
        """
        
        response = await self.model.generate_content_async([prompt])
        text = response.text.strip()
        
        if text.startswith("```json"):
            text = text[7:]
        if text.endswith("```"):
            text = text[:-3]
            
        try:
            return json.loads(text.strip())
        except Exception as e:
            print(f"Erro ao atualizar rascunho JSON: {e}")
            return None

    async def process_agent_step(self, user_prompt: str, guild_info: dict, observations: list):
        """Processa um turno do Agent Loop e retorna thought, array de actions e o indicativo is_done."""
        guild_json = json.dumps(guild_info, indent=2, ensure_ascii=False)
        
        obs_text = "Sem observações anteriores. Este é o primeiro turno."
        if observations:
            obs_text = "\n".join(observations)
            
        prompt = f"""
        Você é um Super Agente Autônomo para Discord operando num modelo de pensamento com Loop (ReAct / Observation-Thought-Action).
        Você deve agir passo a passo até atingir o objetivo solicitado pelo usuário.
        
        Contexto do Servidor (categorias, cargos, canais e usuários mencionados):
        ```json
        {guild_json}
        ```
        
        MISSÃO INICIAL DO USUÁRIO:
        "{user_prompt}"
        
        HISTÓRIO E OBSERVAÇÕES ANTERIORES:
        ```text
        {obs_text}
        ```
        
        INSTRUÇÕES DO AGENT LOOP:
        - Analise a Missão e a Observação Atuais.
        - Defina um Pensamento ("thought") do porquê está tomando essas ações agora.
        - Crie a sua lista de ("actions") para executar no servidor neste turno. Execute APENAS 1 AÇÃO por iterada/turno. É vital que você aguarde a observação dessa 1 ação voltar antes de tentar executar o próximo passo do seu raciocínio.
        - Se o seu objetivo foi concluído COM SUCESSO ou se você notou que é IMPOSSÍVEL concluir com essas rotinas, altere "is_done" para true e preencha "reply" com sua resposta e resumo final da missão (que será dito direto ao usuário no chat).
        - NOTA: Se você precisa ler mensagens para resumi-las, use "get_channel_history", e no PRÓXIMO turno (com a observação contendo as mensagens) você usa "reply" ou "send_message" com o resumo já analisado da sua mente!
        
        AÇÕES DISPONÍVEIS:
        - "send_message": Envia uma mensagem em um canal existente. Parâmetros: "channel_id" (int), "content" (string)
        - "change_role_color": Altera a cor de um cargo existente. Parâmetros: "role_id" (int), "hex_color" (string, ex: "#ff0000")
        - "create_channel": Cria um canal de texto. Parâmetros: "name" (string), "category_id" (int, opcional)
        - "create_role": Cria um cargo. Parâmetros: "name" (string), "hex_color" (string, ex: "#ffffff")
        - "rename_channel": Renomeia um canal. Parâmetros: "channel_id" (int), "new_name" (string)
        - "delete_role": Deleta um cargo. Parâmetros: "role_id" (int)
        - "moderate_user": Bane, expulsa ou silencia (timeout) um usuário. Parâmetros: "user_id" (int), "mod_action" (string: "ban", "kick", "timeout"), "minutes" (int, APENAS se for timeout), "reason" (string)
        - "server_lockdown": Ativa ou desativa restrição global impedindo que o cargo base envie mensagens. Parâmetros: "enable" (bool, true ativar / false desativar)
        - "bulk_delete_messages": Apaga diversas mensagens de uma vez de um canal. Parâmetros: "channel_id" (int), "amount" (int, quantidade de mensagens)
        - "create_poll": Cria uma enquete simples. Parâmetros: "channel_id" (int), "question" (string), "options" (lista de strings limitadas a 10)
        - "get_channel_history": LÊ as mensagens do canal e as traz PARA VOCÊ ler com sua própria IA no próximo passo. Útil se alguém pedir resumos. Parâmetros: "channel_id" (int), "limit" (int, max 50)
        - "ask_user_choice": Pausa o loop da IA e envia um Select Menu (DropDown Dinâmico) perguntando ao usuário para escolher algo, caso você esteja em dúvida (ex: encontrou 2 pessoas com o mesmo nome). Parâmetros: "question" (string), "options" (array de objetos ex: [{{"label": "Maria 1", "value": "ID_999"}}, {{"label": "Maria 2", "value": "ID_555"}}]). O loop continuará após a resposta com a observação sendo o valor escolhido!
        
        SAÍDA (EXCLUSIVAMENTE UM JSON VÁLIDO):
        {{
            "thought": "Entendi o histórico. Vi que não criei o cargo C ainda. Vou criar agora e observar se obteve sucesso.",
            "is_done": false,
            "actions": [ {{"type": "create_role", "name": "Vigia", "hex_color": "#00ff00"}} ],
            "reply": "Opcional. Resposta parcial para o usuário. Deixe vazio se não precisar conversar agora."
        }}
        """
        
        response = await self.model.generate_content_async([prompt])
        text = response.text.strip()
        
        if text.startswith("```json"):
            text = text[7:]
        if text.endswith("```"):
            text = text[:-3]
            
        try:
            return json.loads(text.strip())
        except Exception as e:
            print(f"Erro ao processar step da IA: {e}\nTexto retornado: {text}")
            return {"thought": "Erro crítico no parser JSON da minha resposta.", "is_done": True, "actions": [], "reply": "Houve um problema de formatação no pensamento da IA. Missão abortada."}

    async def summarize_text(self, text_history: str):
        prompt = f"""
        Você é um assistente encarregado de resumir as conversas recentes de um canal no Discord.
        Leia o histórico de mensagens abaixo e crie um resumo curto, engajador e fácil de ler (em tópicos) sobre o que foi discutido:
        
        HISTÓRICO:
        {text_history}
        """
        response = await self.model.generate_content_async([prompt])
        return response.text.strip()
