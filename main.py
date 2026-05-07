import discord
from discord.ext import commands
import config
import asyncio
from ai_engine import AIEngine
from server_factory import ServerFactory

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)
bot.remove_command('help')
ai = AIEngine()

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            title="❌ Acesso Negado",
            description="Apenas usuários com a permissão de **Administrador** podem executar os comandos deste bot.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            title="⚠️ Uso Incorreto",
            description="Verifique como você digitou o comando. Exemplo: `!setup Meu Servidor de Jogos`",
            color=discord.Color.orange()
        )
        await ctx.send(embed=embed)

class SetupConfigView(discord.ui.View):
    def __init__(self, ctx, theme, is_reconstruct=False):
        super().__init__(timeout=60)
        self.ctx = ctx
        self.theme = theme
        self.is_reconstruct = is_reconstruct
        self.use_emojis_channels = True
        self.use_emojis_categories = True
        self.use_emojis_roles = True
        self.num_roles = 5
        self.confirmed = False

    def get_embed(self):
        title = "🔄 Reconstrução Sistêmica" if self.is_reconstruct else "🛠️ Arquiteto de Comunidades"
        desc = (
            f"**Modelo de Operação:** `Google Gemini 3.1 Pro`\n"
            f"**Tema Selecionado:** `{self.theme}`\n\n"
            "Escolha as diretrizes visuais para a geração da infraestrutura."
        )
        
        embed = discord.Embed(description=desc, color=0x5865F2) # Blurple moderno
        embed.set_author(name=f"Configuração Avançada", icon_url=self.ctx.bot.user.display_avatar.url if self.ctx.bot.user.display_avatar else None)
        
        # Layout em Colunas (Inline) para Emojis
        embed.add_field(name="📂 Canais", value="✅ Ativo" if self.use_emojis_channels else "❌ Inativo", inline=True)
        embed.add_field(name="🏷️ Categorias", value="✅ Ativo" if self.use_emojis_categories else "❌ Inativo", inline=True)
        embed.add_field(name="🎭 Cargos", value="✅ Ativo" if self.use_emojis_roles else "❌ Inativo", inline=True)
        
        embed.add_field(name="📊 Hierarquia Proposta", value=f"```ansi\n\u001b[1;34m{self.num_roles} Cargos Estruturais\u001b[0m\n```", inline=False)
        
        embed.set_footer(text="A inteligência artificial irá reconstruir as permissões e canais.")
        return embed

    @discord.ui.button(label="Emojis Canais: ✅", style=discord.ButtonStyle.success, row=0)
    async def toggle_emojis_channels(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.ctx.author: return
        self.use_emojis_channels = not self.use_emojis_channels
        button.label = f"Emojis Canais: {'✅' if self.use_emojis_channels else '❌'}"
        button.style = discord.ButtonStyle.success if self.use_emojis_channels else discord.ButtonStyle.danger
        await interaction.response.edit_message(embed=self.get_embed(), view=self)

    @discord.ui.button(label="Emojis Categorias: ✅", style=discord.ButtonStyle.success, row=0)
    async def toggle_emojis_categories(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.ctx.author: return
        self.use_emojis_categories = not self.use_emojis_categories
        button.label = f"Emojis Categorias: {'✅' if self.use_emojis_categories else '❌'}"
        button.style = discord.ButtonStyle.success if self.use_emojis_categories else discord.ButtonStyle.danger
        await interaction.response.edit_message(embed=self.get_embed(), view=self)

    @discord.ui.button(label="Emojis Cargos: ✅", style=discord.ButtonStyle.success, row=0)
    async def toggle_emojis_roles(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.ctx.author: return
        self.use_emojis_roles = not self.use_emojis_roles
        button.label = f"Emojis Cargos: {'✅' if self.use_emojis_roles else '❌'}"
        button.style = discord.ButtonStyle.success if self.use_emojis_roles else discord.ButtonStyle.danger
        await interaction.response.edit_message(embed=self.get_embed(), view=self)

    @discord.ui.button(label="Mais Cargos (+)", style=discord.ButtonStyle.secondary, row=1)
    async def add_roles(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.ctx.author: return
        self.num_roles = min(self.num_roles + 1, 15)
        await interaction.response.edit_message(embed=self.get_embed(), view=self)

    @discord.ui.button(label="Menos Cargos (-)", style=discord.ButtonStyle.secondary, row=1)
    async def sub_roles(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.ctx.author: return
        self.num_roles = max(self.num_roles - 1, 2)
        await interaction.response.edit_message(embed=self.get_embed(), view=self)

    @discord.ui.button(label="🚀 INICIAR CONSTRUÇÃO", style=discord.ButtonStyle.primary, row=2)
    async def start(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.ctx.author: return
        self.confirmed = True
        self.stop()
        await interaction.response.defer()

@bot.command(name="help")
async def custom_help(ctx):
    """Mostra a lista de comandos disponíveis."""
    embed = discord.Embed(
        title="📚 Comandos do Arquiteto IA",
        description="Aqui estão os comandos disponíveis para gerenciamento e criação do servidor:",
        color=0x5865F2
    )
    
    embed.add_field(name="`!setup <tema>`", value="Configura um novo servidor com perguntas interativas baseadas no tema.", inline=False)
    embed.add_field(name="`!reconstruct`", value="Analisa o servidor atual e o reconstrói melhorado pela IA.", inline=False)
    embed.add_field(name="`!draft <tema>`", value="Cria um rascunho de servidor em uma Thread para aprovação e ajustes.", inline=False)
    embed.add_field(name="`!chat <mensagem>`", value="Conversa com o agente IA e permite que ele execute ações no servidor.", inline=False)
    embed.add_field(name="`!help`", value="Mostra esta mensagem de ajuda.", inline=False)
    
    embed.set_footer(text="Nota: Apenas usuários com permissão de Administrador podem executar os comandos.")
    
    await ctx.send(embed=embed)

@bot.command(name="setup")
@commands.has_permissions(administrator=True)
async def setup_server(ctx, *, theme: str):
    """Configura o servidor com perguntas interativas."""
    
    view = SetupConfigView(ctx, theme, is_reconstruct=False)
    config_msg = await ctx.send(embed=view.get_embed(), view=view)
    
    await view.wait()
    if not view.confirmed:
        cancel_embed = discord.Embed(title="❌ Setup Cancelado", description="A operação foi cancelada por inatividade.", color=discord.Color.red())
        await config_msg.edit(content=None, embed=cancel_embed, view=None)
        return

    await config_msg.delete()

    steps = {
        "limpeza": "⏳ Limpando canais e cargos antigos...",
        "ia": "⏳ Consultando o Arquiteto IA...",
        "cargos": "⏳ Fundindo novos cargos...",
        "estrutura": "⏳ Construindo canais e categorias...",
        "finalizacao": "⏳ Finalizando setup..."
    }

    def get_progress_embed():
        embed = discord.Embed(
            title=f"🏗️ Operação em Curso: {theme}",
            color=0x2b2d31
        )
        
        progress_text = ""
        for key, status in steps.items():
            if "✅" in status:
                progress_text += f"> **{status}**\n"
            elif "⏳" in status:
                progress_text += f"> \u2728 **{status}**\n"
            else:
                progress_text += f"> {status}\n"

        embed.description = f"### Status da Automação\n{progress_text}"
        
        if ctx.bot.user.display_avatar:
            embed.set_thumbnail(url=ctx.bot.user.display_avatar.url)
            
        embed.set_author(name="Arquiteto IA Engine", icon_url="https://cdn.discordapp.com/emojis/1101890333550411837.webp?size=96&quality=lossless")
        embed.set_footer(text="Isso pode levar alguns segundos dependendo da complexidade.")
        return embed

    progress_msg = await ctx.send(embed=get_progress_embed())
    factory = ServerFactory(ctx.guild)

    # 1. Limpeza
    await factory.clear_server(ctx.channel.id)
    steps["limpeza"] = "✅ Servidor limpo!"
    await progress_msg.edit(embed=get_progress_embed())

    # 2. IA
    image_bytes = None
    if ctx.message.attachments:
        attachment = ctx.message.attachments[0]
        if any(attachment.filename.lower().endswith(ext) for ext in ['png', 'jpg', 'jpeg', 'webp']):
            steps["ia"] = "📸 Analisando imagem para clonagem visual..."
            await progress_msg.edit(embed=get_progress_embed())
            image_bytes = await attachment.read()

    structure = await ai.generate_server_structure(
        theme, 
        view.use_emojis_channels, 
        view.use_emojis_categories, 
        view.use_emojis_roles,
        view.num_roles,
        image_bytes=image_bytes
    )
    if not structure:
        steps["ia"] = "❌ Erro ao gerar estrutura."
        await progress_msg.edit(embed=get_progress_embed())
        return
    
    steps["ia"] = "✅ Estrutura gerada (Clonagem Ativa)!"
    await progress_msg.edit(embed=get_progress_embed())

    # 3. Construção (Cargos e Estrutura)
    try:
        steps["cargos"] = "🏗️ Criando cargos..."
        await progress_msg.edit(embed=get_progress_embed())
        
        roles = await factory.create_roles(structure.get("roles", []))
        steps["cargos"] = f"✅ {len(roles)} cargos criados!"
        await progress_msg.edit(embed=get_progress_embed())

        steps["estrutura"] = "🏗️ Construindo categorias e canais..."
        await progress_msg.edit(embed=get_progress_embed())
        
        if structure.get("server_name"):
            await ctx.guild.edit(name=structure["server_name"])
            
        first_text_channel = None
        for cat_info in structure.get("categories", []):
            category = await ctx.guild.create_category(cat_info["name"])
            for chan_info in cat_info.get("channels", []):
                overwrites = factory._get_overwrites(chan_info, roles)
                if chan_info["type"] == "text":
                    channel = await category.create_text_channel(chan_info["name"], topic=chan_info.get("topic"), overwrites=overwrites)
                    if not first_text_channel: first_text_channel = channel
                else:
                    await category.create_voice_channel(chan_info["name"], overwrites=overwrites)
        
        steps["estrutura"] = "✅ Canais e categorias prontos!"
        await progress_msg.edit(embed=get_progress_embed())

        steps["finalizacao"] = "🏗️ Enviando boas-vindas..."
        await progress_msg.edit(embed=get_progress_embed())
        
        if first_text_channel and structure.get("welcome_message"):
            welcome_embed = discord.Embed(
                title=f"Bem-vindo ao {ctx.guild.name}!",
                description=structure["welcome_message"],
                color=discord.Color.gold()
            )
            await first_text_channel.send(embed=welcome_embed)

        steps["finalizacao"] = "✅ Setup concluído com sucesso!"
        final_embed = get_progress_embed()
        final_embed.color = discord.Color.green()
        await progress_msg.edit(embed=final_embed)

    except Exception as e:
        error_embed = discord.Embed(title="❌ Erro Crítico", description=str(e), color=discord.Color.red())
        await ctx.send(embed=error_embed)
        print(f"Erro na construção: {e}")
@bot.command(name="reconstruct")
@commands.has_permissions(administrator=True)
async def reconstruct_server(ctx):
    """Analisa o servidor atual e o reconstrói melhorado."""
    theme = "Reconstrução e Otimização do Servidor"
    view = SetupConfigView(ctx, theme, is_reconstruct=True)
    config_msg = await ctx.send(embed=view.get_embed(), view=view)
    
    await view.wait()
    if not view.confirmed:
        cancel_embed = discord.Embed(title="❌ Reconstrução Cancelada", description="A operação foi cancelada por inatividade.", color=discord.Color.red())
        await config_msg.edit(content=None, embed=cancel_embed, view=None)
        return

    await config_msg.delete()

    steps = {
        "export": "⏳ Analisando estrutura atual...",
        "ia": "⏳ Consultando o Arquiteto IA para melhorias...",
        "limpeza": "⏳ Limpando servidor...",
        "cargos": "⏳ Fundindo novos cargos...",
        "estrutura": "⏳ Construindo canais e categorias...",
        "finalizacao": "⏳ Finalizando setup..."
    }

    def get_progress_embed():
        embed = discord.Embed(
            title=f"🔄 Otimização Sistêmica",
            color=0x2b2d31
        )
        
        progress_text = ""
        for key, status in steps.items():
            if "✅" in status:
                progress_text += f"> **{status}**\n"
            elif "⏳" in status:
                progress_text += f"> \u2728 **{status}**\n"
            else:
                progress_text += f"> {status}\n"

        embed.description = f"### Plano de Melhoria Ativo\n{progress_text}"

        if ctx.bot.user.display_avatar:
            embed.set_thumbnail(url=ctx.bot.user.display_avatar.url)

        embed.set_author(name="IA Reconstructor", icon_url="https://cdn.discordapp.com/emojis/1101890333550411837.webp?size=96&quality=lossless")
        embed.set_footer(text="Recriando hierarquias e permissões...")
        return embed

    progress_msg = await ctx.send(embed=get_progress_embed())
    factory = ServerFactory(ctx.guild)

    current_structure = factory.export_structure()
    steps["export"] = "✅ Estrutura atual analisada!"
    await progress_msg.edit(embed=get_progress_embed())

    structure = await ai.reconstruct_server_structure(
        current_structure, 
        view.use_emojis_channels, 
        view.use_emojis_categories, 
        view.use_emojis_roles,
        view.num_roles
    )
    if not structure:
        steps["ia"] = "❌ Erro ao gerar estrutura melhorada."
        await progress_msg.edit(embed=get_progress_embed())
        return
    
    steps["ia"] = "✅ Estrutura melhorada gerada!"
    await progress_msg.edit(embed=get_progress_embed())

    await factory.clear_server(ctx.channel.id)
    steps["limpeza"] = "✅ Servidor antigo limpo!"
    await progress_msg.edit(embed=get_progress_embed())

    try:
        steps["cargos"] = "🏗️ Criando cargos..."
        await progress_msg.edit(embed=get_progress_embed())
        
        roles = await factory.create_roles(structure.get("roles", []))
        steps["cargos"] = f"✅ {len(roles)} cargos criados!"
        await progress_msg.edit(embed=get_progress_embed())

        steps["estrutura"] = "🏗️ Construindo categorias e canais..."
        await progress_msg.edit(embed=get_progress_embed())
        
        if structure.get("server_name"):
            await ctx.guild.edit(name=structure["server_name"])
            
        first_text_channel = None
        for cat_info in structure.get("categories", []):
            category = await ctx.guild.create_category(cat_info["name"])
            for chan_info in cat_info.get("channels", []):
                overwrites = factory._get_overwrites(chan_info, roles)
                if chan_info["type"] == "text":
                    channel = await category.create_text_channel(chan_info["name"], topic=chan_info.get("topic"), overwrites=overwrites)
                    if not first_text_channel: first_text_channel = channel
                else:
                    await category.create_voice_channel(chan_info["name"], overwrites=overwrites)
        
        steps["estrutura"] = "✅ Canais e categorias prontos!"
        await progress_msg.edit(embed=get_progress_embed())

        steps["finalizacao"] = "🏗️ Enviando boas-vindas..."
        await progress_msg.edit(embed=get_progress_embed())
        
        if first_text_channel and structure.get("welcome_message"):
            welcome_embed = discord.Embed(
                title=f"Servidor Reconstruído: {ctx.guild.name}!",
                description=structure["welcome_message"],
                color=discord.Color.gold()
            )
            await first_text_channel.send(embed=welcome_embed)

        steps["finalizacao"] = "✅ Reconstrução concluída com sucesso!"
        final_embed = get_progress_embed()
        final_embed.color = discord.Color.green()
        await progress_msg.edit(embed=final_embed)

    except Exception as e:
        error_embed = discord.Embed(title="❌ Erro Crítico", description=str(e), color=discord.Color.red())
        await ctx.send(embed=error_embed)
        print(f"Erro na reconstrução: {e}")

@bot.command(name="draft")
@commands.has_permissions(administrator=True)
async def draft_server(ctx, *, theme: str):
    """Cria um rascunho de servidor em uma Thread para aprovação e ajustes via IA."""
    view = SetupConfigView(ctx, theme, is_reconstruct=False)
    config_msg = await ctx.send(embed=view.get_embed(), view=view)
    
    await view.wait()
    if not view.confirmed:
        cancel_embed = discord.Embed(title="❌ Setup Cancelado", description="A operação foi cancelada por inatividade.", color=discord.Color.red())
        await config_msg.edit(content=None, embed=cancel_embed, view=None)
        return

    await config_msg.delete()
    
    progress_msg = await ctx.send("⏳ Consultando o Arquiteto IA para gerar o primeiro rascunho...")
    
    image_bytes = None
    if ctx.message.attachments:
        attachment = ctx.message.attachments[0]
        if any(attachment.filename.lower().endswith(ext) for ext in ['png', 'jpg', 'jpeg', 'webp']):
            image_bytes = await attachment.read()
            
    structure = await ai.generate_server_structure(
        theme, 
        view.use_emojis_channels, 
        view.use_emojis_categories, 
        view.use_emojis_roles,
        view.num_roles,
        image_bytes=image_bytes
    )
    
    if not structure:
        await progress_msg.edit(content="❌ Erro ao gerar estrutura base.")
        return
        
    if isinstance(ctx.channel, discord.TextChannel):
        thread = await ctx.channel.create_thread(
            name=f"Rascunho: {structure.get('server_name', 'Novo Servidor')[:80]}",
            type=discord.ChannelType.public_thread
        )
    else:
        await ctx.send("❌ Este comando precisa ser executado em um canal de texto normal para suportar Threads.")
        return
        
    await progress_msg.edit(content=f"✅ Rascunho gerado! Acesse a thread {thread.mention} para visualizar e ajustar.")
    
    draft_status_msg = None
    
    def generate_draft_embed(current_structure):
        desc = f"**Nome do Servidor:** {current_structure.get('server_name', 'N/A')}\n"
        roles = current_structure.get('roles', [])
        desc += f"**Cargos ({len(roles)}):** " + ", ".join([r.get('name', 'N/A') for r in roles]) + "\n\n"
        desc += "**Estrutura Projetada:**\n"
        
        # Limita o número de caracteres para não estourar o limite do Embed
        structure_text = ""
        for cat in current_structure.get('categories', []):
            structure_text += f"\n📁 **{cat.get('name', 'Categoria')}**\n"
            for chan in cat.get('channels', []):
                icon = "🔊" if chan.get('type') == 'voice' else "💬"
                structure_text += f"> {icon} {chan.get('name', 'canal')}\n"
        
        if len(structure_text) > 3500:
            structure_text = structure_text[:3500] + "\n... (Muitos canais para exibir)"
            
        desc += structure_text
        
        embed = discord.Embed(title="📐 Rascunho do Servidor", description=desc, color=discord.Color.blue())
        embed.set_footer(text="Envie uma mensagem aqui na thread pedindo para a IA alterar algo!")
        return embed

    class DraftControlView(discord.ui.View):
        def __init__(self, author):
            super().__init__(timeout=None)
            self.author = author
            self.action = None

        @discord.ui.button(label="🚀 CONSTRUIR", style=discord.ButtonStyle.success)
        async def build(self, interaction: discord.Interaction, button: discord.ui.Button):
            if interaction.user != self.author: return
            self.action = "build"
            await interaction.response.defer()
            self.stop()

        @discord.ui.button(label="❌ CANCELAR", style=discord.ButtonStyle.danger)
        async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
            if interaction.user != self.author: return
            self.action = "cancel"
            await interaction.response.defer()
            self.stop()

    while True:
        embed = generate_draft_embed(structure)
        view = DraftControlView(ctx.author)
        
        if not draft_status_msg:
            draft_status_msg = await thread.send(content=ctx.author.mention, embed=embed, view=view)
        else:
            draft_status_msg = await thread.send(embed=embed, view=view)
            
        def check_msg(m):
            return m.author == ctx.author and m.channel == thread

        done, pending = await asyncio.wait([
            bot.loop.create_task(bot.wait_for('message', check=check_msg)),
            bot.loop.create_task(view.wait())
        ], return_when=asyncio.FIRST_COMPLETED)
        
        for task in pending:
            task.cancel()
            
        result = done.pop().result()
        
        if isinstance(result, bool) or result is None:
            if view.action == "build":
                break
            elif view.action == "cancel":
                await thread.send("❌ Construção cancelada.")
                await thread.edit(archived=True)
                return
        else:
            user_msg = result
            processing_msg = await thread.send("🔄 *Atualizando o rascunho com o arquiteto IA...*")
            
            new_structure = await ai.update_server_structure(structure, user_msg.content)
            if new_structure:
                structure = new_structure
                await user_msg.add_reaction("✅")
            else:
                await thread.send("❌ Falha ao aplicar as mudanças pelo modelo de IA.")
                
            await processing_msg.delete()
            for c in view.children: c.disabled = True
            await draft_status_msg.edit(view=view)
            draft_status_msg = None

    await thread.send("🚀 **Iniciando Construção no servidor (aguarde)...**")
    factory = ServerFactory(ctx.guild)
    
    build_msg = await thread.send("🏗️ Aplicando a infraestrutura...")
    try:
        await factory.clear_server(ctx.channel.id)
        
        if structure.get("server_name"):
            await ctx.guild.edit(name=structure["server_name"])
            
        roles = await factory.create_roles(structure.get("roles", []))
        
        first_text_channel = None
        for cat_info in structure.get("categories", []):
            category = await ctx.guild.create_category(cat_info["name"])
            for chan_info in cat_info.get("channels", []):
                overwrites = factory._get_overwrites(chan_info, roles)
                if chan_info["type"] == "text":
                    channel = await category.create_text_channel(chan_info["name"], topic=chan_info.get("topic"), overwrites=overwrites)
                    if not first_text_channel: first_text_channel = channel
                else:
                    await category.create_voice_channel(chan_info["name"], overwrites=overwrites)
        
        if first_text_channel and structure.get("welcome_message"):
            welcome_embed = discord.Embed(
                title=f"Bem-vindo ao Novo {ctx.guild.name}!",
                description=structure["welcome_message"],
                color=discord.Color.gold()
            )
            await first_text_channel.send(embed=welcome_embed)
            
        await build_msg.edit(content="✅ **Setup concluído com sucesso via Rascunho!**")
        await thread.edit(archived=True)
    except Exception as e:
        await build_msg.edit(content=f"❌ **Erro fatal durante construção:** {e}")
        print(f"Erro no draft build: {e}")

@bot.command(name="chat")
@commands.has_permissions(administrator=True)
async def chat_command(ctx, *, message: str):
    """Conversa com o agente IA e permite que ele execute ações no servidor."""
    
    # Coletar informações do servidor e menções
    guild_info = {
        "server_name": ctx.guild.name,
        "roles": [{"id": r.id, "name": r.name, "color": str(r.color)} for r in ctx.guild.roles if r.name != "@everyone"],
        "categories": [{"id": cat.id, "name": cat.name} for cat in ctx.guild.categories],
        "channels": [{"id": c.id, "name": c.name, "type": str(c.type), "category_id": getattr(c, 'category_id', None)} for c in ctx.guild.channels if isinstance(c, discord.TextChannel)],
        "mentioned_users": [{"id": m.id, "name": m.name} for m in ctx.message.mentions]
    }
    
    max_loops = 8
    observations = []
    
    log_msg = await ctx.send("🤖 **Iniciando Sistema de Agente com Loop de ReAct (Pensamento -> Ação -> Observação)...**")
    
    for i in range(max_loops):
        # Refresh info slightly if needed, but for simplicity let's stick to base info
        async with ctx.typing():
            response_data = await ai.process_agent_step(message, guild_info, observations)
            
        if not response_data:
            await ctx.send("❌ Erro fatal de processamento do Agente.")
            break
            
        thought = response_data.get("thought", "Nada a pensar fora do padrão")
        is_done = response_data.get("is_done", False)
        reply = response_data.get("reply", "")
        actions = response_data.get("actions", [])
        
        # Publica o raciocínio deste ciclo
        step_header = f"🔄 **Ciclo {i+1}**"
        current_content = log_msg.content
        if len(current_content) > 3000:
            current_content = current_content[-2000:]
            
        await log_msg.edit(content=f"{current_content}\n\n{step_header}\n🧠 *Pensamento: {thought}*\n" + (f"💬 *Falo: {reply}*\n" if reply else ""))
        
        if is_done:
            await ctx.send(f"✅ **Processo Concluído!**\n>>> {reply}")
            break
            
        step_observations = []
        
        if actions:
            exec_log = "🛠️ *Ações Executadas:*\n"
            for action in actions:
                action_type = action.get("type", "unknown")
                try:
                    if action_type == "send_message":
                        channel_id = action.get("channel_id")
                        content = action.get("content")
                        channel = ctx.guild.get_channel(int(channel_id))
                        if channel:
                            await channel.send(content)
                            step_observations.append(f"Ação 'send_message' sucedida no canal {channel_id}.")
                            exec_log += f"- Mensagem enviada em {channel.mention}\n"
                        else:
                            step_observations.append(f"Erro em 'send_message': Canal {channel_id} não encontrado.")
                            exec_log += f"- ❌ Falha: Canal {channel_id} não encontrado.\n"
                            
                    elif action_type == "change_role_color":
                        role_id = action.get("role_id")
                        hex_color = action.get("hex_color", "#ffffff")
                        role = ctx.guild.get_role(int(role_id))
                        if role:
                            color_val = int(hex_color.replace("#", "").replace("0x", ""), 16)
                            await role.edit(color=discord.Color(color_val))
                            step_observations.append(f"Ação 'change_role_color': Sucesso. Cargo {role_id} agora é {hex_color}.")
                            exec_log += f"- Cor modificada do cargo {role.name}\n"
                        else:
                            step_observations.append(f"Erro 'change_role_color': Cargo {role_id} não existe.")
                            exec_log += f"- ❌ Falha em cargo {role_id}\n"
                    
                    elif action_type == "create_channel":
                        name = action.get("name", "novo-canal")
                        cat_id = action.get("category_id")
                        category = ctx.guild.get_channel(int(cat_id)) if cat_id else None
                        channel = await ctx.guild.create_text_channel(name, category=category)
                        step_observations.append(f"Ação 'create_channel': Sucesso. Novo canal '{name}' com ID {channel.id} criado.")
                        exec_log += f"- Canal {channel.mention} criado.\n"
                    
                    elif action_type == "create_role":
                        name = action.get("name", "Novo Cargo")
                        hex_color = action.get("hex_color", "#99aab5")
                        color_val = int(hex_color.replace("#", "").replace("0x", ""), 16)
                        role = await ctx.guild.create_role(name=name, color=discord.Color(color_val))
                        step_observations.append(f"Ação 'create_role': Sucesso. Novo cargo '{name}' com ID {role.id} criado.")
                        exec_log += f"- Cargo `{role.name}` criado.\n"
                    
                    elif action_type == "rename_channel":
                        channel_id = action.get("channel_id")
                        new_name = action.get("new_name")
                        channel = ctx.guild.get_channel(int(channel_id))
                        if channel:
                            await channel.edit(name=new_name)
                            step_observations.append(f"Ação 'rename_channel': Sucesso. Canal ID {channel_id} renomeado para '{new_name}'.")
                            exec_log += f"- Canal renomeado para {channel.mention}\n"
                        else:
                            step_observations.append(f"Erro em 'rename_channel': Canal {channel_id} não encontrado.")
                            exec_log += f"- ❌ Falha em renomear canal {channel_id}\n"
                            
                    elif action_type == "delete_role":
                        role_id = action.get("role_id")
                        role = ctx.guild.get_role(int(role_id))
                        if role:
                            await role.delete()
                            step_observations.append(f"Ação 'delete_role': Sucesso. Cargo {role_id} deletado.")
                            exec_log += f"- Cargo deletado com sucesso.\n"
                        else:
                            step_observations.append(f"Erro em 'delete_role': Cargo {role_id} não encontrado.")
                            
                    elif action_type == "moderate_user":
                        user_id = action.get("user_id")
                        mod_action = action.get("mod_action", "timeout")
                        reason = action.get("reason", "Ação da IA")
                        member = ctx.guild.get_member(int(user_id))
                        if not member:
                            step_observations.append(f"Erro em 'moderate_user': Usuário {user_id} não retornado.")
                        elif mod_action == "ban":
                            await member.ban(reason=reason)
                            step_observations.append(f"Sucesso: {member.name} banido.")
                        elif mod_action == "kick":
                            await member.kick(reason=reason)
                            step_observations.append(f"Sucesso: {member.name} expulso.")
                        elif mod_action == "timeout":
                            minutes = action.get("minutes", 10)
                            import datetime
                            await member.timeout(datetime.timedelta(minutes=minutes), reason=reason)
                            step_observations.append(f"Sucesso: {member.name} silenciado por {minutes}m.")
                        exec_log += f"- Moderação aplicada em base do usuário {user_id}\n"

                    elif action_type == "server_lockdown":
                        enable = action.get("enable", True)
                        default_role = ctx.guild.default_role
                        perms = default_role.permissions
                        perms.update(send_messages=not enable)
                        await default_role.edit(permissions=perms)
                        step_observations.append(f"Ação 'server_lockdown': {'Ativado' if enable else 'Desativado'} impedindo @everyone de digitar.")
                        exec_log += f"- Lockdown modificado.\n"

                    elif action_type == "bulk_delete_messages":
                        channel_id = action.get("channel_id")
                        amount = action.get("amount", 10)
                        channel = ctx.guild.get_channel(int(channel_id))
                        if channel:
                            deleted = await channel.purge(limit=amount)
                            step_observations.append(f"Ação 'bulk_delete_messages': Apagadas {len(deleted)} mensagens em canal {channel_id}.")
                            exec_log += f"- Expurgo realizado em {channel.mention}\n"
                        else:
                            step_observations.append(f"Erro em 'bulk_delete_messages': Canal não achado.")
                            
                    elif action_type == "create_poll":
                        channel_id = action.get("channel_id")
                        question = action.get("question")
                        options = action.get("options", [])
                        channel = ctx.guild.get_channel(int(channel_id))
                        if channel and options:
                            poll_text = f"📊 **ENQUETE: {question}**\n\n"
                            reactions = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
                            for j, opt in enumerate(options[:10]):
                                poll_text += f"{reactions[j]} - {opt}\n"
                            poll_msg = await channel.send(poll_text)
                            for j in range(len(options[:10])):
                                await poll_msg.add_reaction(reactions[j])
                            step_observations.append(f"Ação 'create_poll': Sucesso em canal {channel_id}.")
                            exec_log += f"- Enquete postada em {channel.mention}.\n"
                        else:
                            step_observations.append("Erro em 'create_poll': Falta de opções ou não achou canal.")
                            
                    elif action_type == "get_channel_history":
                        channel_id = action.get("channel_id")
                        limit = action.get("limit", 50)
                        channel = ctx.guild.get_channel(int(channel_id))
                        if channel:
                            msgs = [msg async for msg in channel.history(limit=limit)]
                            text_msgs = "\n".join([f"{m.author.name}: {m.content}" for m in reversed(msgs)])
                            if not text_msgs.strip():
                                step_observations.append(f"Ação 'get_channel_history': Não há mensagens no canal {channel_id}.")
                            else:
                                step_observations.append(f"Ação 'get_channel_history': Histórico coletado no canal {channel_id}:\n'''\n{text_msgs}\n'''")
                            exec_log += f"- Conteúdo de {channel.mention} lido com sucesso pela memória cerebral.\n"
                        else:
                            step_observations.append(f"Erro 'get_channel_history': Canal {channel_id} não achado.")
                            exec_log += f"- ❌ Falha em acessar leitura de {channel_id}.\n"

                    elif action_type == "ask_user_choice":
                        question = action.get("question", "Escolha uma opção manual:")
                        options = action.get("options", [])
                        
                        if not options:
                            step_observations.append("Erro em 'ask_user_choice': Nenhuma opção fornecida pela IA.")
                        else:
                            class DynamicSelect(discord.ui.Select):
                                def __init__(self, opts):
                                    select_options = [
                                        discord.SelectOption(label=str(opt.get("label", "Opção"))[:100], value=str(opt.get("value", i))[:100])
                                        for i, opt in enumerate(opts[:25])
                                    ]
                                    super().__init__(placeholder="Selecione uma opção...", min_values=1, max_values=1, options=select_options)

                                async def callback(self, interaction: discord.Interaction):
                                    if interaction.user != ctx.author:
                                        await interaction.response.send_message("⛔ Apenas quem executou o comando pode responder!", ephemeral=True)
                                        return
                                    self.view.value = self.values[0]
                                    self.view.stop()
                                    await interaction.response.defer()

                            class DynamicSelectView(discord.ui.View):
                                def __init__(self, opts):
                                    super().__init__(timeout=120)
                                    self.value = None
                                    self.add_item(DynamicSelect(opts))

                            view = DynamicSelectView(options)
                            
                            # Atualiza a caixa principal pra não sumir da UX do log
                            exec_log += f"- ⏸️ Aguardando input humano para: '{question}'...\n"
                            await log_msg.edit(content=f"{log_msg.content}\n{exec_log}")
                            exec_log = ""
                            
                            q_msg = await ctx.send(content=f"❓ **O Agente IA parou para perguntar:** {question}", view=view)
                            
                            await view.wait()
                            
                            if view.value is None:
                                step_observations.append("Ação 'ask_user_choice': O usuário não respondeu a tempo (timeout). Você deve abortar a missão.")
                                exec_log += f"- ❌ Falha: Timeout no aguardo do input humano.\n"
                                await q_msg.edit(content="❌ *Tempo esgotado para responder.*", view=None)
                            else:
                                step_observations.append(f"Ação 'ask_user_choice': Sucesso. O usuário escolheu a opção com valor: '{view.value}'.")
                                exec_log += f"- 👤 Usuário confirmou a escolha oculta: '{view.value}'.\n"
                                await q_msg.edit(content=f"✅ **Escolha selecionada registrada no cérebro.**", view=None)
                
                except Exception as e:
                    step_observations.append(f"FALHA na ação {action_type}: {e}")
                    exec_log += f"- ❌ Falha técnica: {e}\n"
                    
            await log_msg.edit(content=f"{log_msg.content}\n{exec_log}")
            
            # Formata obs para o histórico local
            obs_str = f"--- TURNO {i+1} ---\nMensagens enviadas ao usuário na plataforma: {reply}\nObservações das ações tentadas:\n" + "\n".join(step_observations)
            observations.append(obs_str)
        else:
            await log_msg.edit(content=f"{log_msg.content}\n- Nenhuma ação de infraestrutura tomada.\n")
            obs_str = f"--- TURNO {i+1} ---\nMensagem enviada ao usuário: {reply}\nNenhuma ação tomada."
            observations.append(obs_str)
            
    else:
        await ctx.send("⌛ **Agente parou preventivamente.** O número máximo de turnos auto-sustentáveis foi atingido (Loop Control).")

if __name__ == "__main__":
    if config.DISCORD_TOKEN:
        bot.run(config.DISCORD_TOKEN)
    else:
        print("Erro: DISCORD_TOKEN não configurado no arquivo .env")
