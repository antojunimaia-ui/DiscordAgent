import discord
import asyncio

class ServerFactory:
    def __init__(self, guild: discord.Guild):
        self.guild = guild

    def export_structure(self):
        """Exporta a estrutura atual do servidor para um dicionário."""
        data = {
            "server_name": self.guild.name,
            "roles": [{"name": r.name} for r in self.guild.roles if not r.is_default() and not r.managed],
            "categories": []
        }
        
        for category in self.guild.categories:
            cat_data = {"name": category.name, "channels": []}
            for channel in category.channels:
                if isinstance(channel, discord.TextChannel):
                    cat_data["channels"].append({"name": channel.name, "type": "text", "topic": channel.topic or ""})
                elif isinstance(channel, discord.VoiceChannel):
                    cat_data["channels"].append({"name": channel.name, "type": "voice"})
            data["categories"].append(cat_data)
            
        uncategorized = {"name": "Geral (Sem Categoria)", "channels": []}
        for channel in self.guild.channels:
            if channel.category is None and not isinstance(channel, discord.CategoryChannel):
                if isinstance(channel, discord.TextChannel):
                    uncategorized["channels"].append({"name": channel.name, "type": "text", "topic": channel.topic or ""})
                elif isinstance(channel, discord.VoiceChannel):
                    uncategorized["channels"].append({"name": channel.name, "type": "voice"})
                    
        if uncategorized["channels"]:
            data["categories"].append(uncategorized)
            
        return data

    async def create_roles(self, roles_data):
        created_roles = {}
        for role_info in roles_data:
            color_int = int(role_info.get("color", "0xFFFFFF"), 16)
            perms = discord.Permissions()
            
            raw_perms = role_info.get("permissions", [])
            if isinstance(raw_perms, list):
                for p in raw_perms:
                    if hasattr(perms, p):
                        setattr(perms, p, True)
            elif isinstance(raw_perms, dict):
                for p, val in raw_perms.items():
                    if hasattr(perms, p):
                        setattr(perms, p, val)
            
            role = await self.guild.create_role(
                name=role_info["name"],
                color=discord.Color(color_int),
                permissions=perms,
                hoist=role_info.get("hoist", False),
                reason="AI Server Setup"
            )
            created_roles[role_info["name"]] = role
            print(f"Cargo criado: {role.name}")
        return created_roles

    def _get_overwrites(self, channel_data, created_roles):
        overwrites = {}
        raw_overwrites = channel_data.get("overwrites", {})
        
        if not isinstance(raw_overwrites, dict):
            return overwrites

        for name, perms_data in raw_overwrites.items():
            target = None
            if name == "@everyone":
                target = self.guild.default_role
            elif name in created_roles:
                target = created_roles[name]
            else:
                # Tenta busca case-insensitive se não achar direto
                for r_name, r_obj in created_roles.items():
                    if r_name.lower() == name.lower():
                        target = r_obj
                        break
                
            if target and isinstance(perms_data, dict):
                # Limpa permissões inválidas para o discord.py
                valid_perms = {}
                for k, v in perms_data.items():
                    # Mapeia nomes comuns se a IA errar (ex: 'read_messages' -> 'view_channel')
                    key = k.lower()
                    if key == 'read_messages': key = 'view_channel'
                    
                    if hasattr(discord.PermissionOverwrite, key):
                        valid_perms[key] = v
                
                overwrites[target] = discord.PermissionOverwrite(**valid_perms)
        
        return overwrites

    async def create_structure(self, structure_data):
        # 1. Ajustar nome do servidor
        if structure_data.get("server_name"):
            try:
                await self.guild.edit(name=structure_data["server_name"])
            except: pass

        # 2. Criar Cargos
        roles = await self.create_roles(structure_data.get("roles", []))

        # 3. Criar Categorias e Canais
        first_text_channel = None
        
        for cat_info in structure_data.get("categories", []):
            category = await self.guild.create_category(cat_info["name"])
            print(f"Categoria criada: {category.name}")
            
            for chan_info in cat_info.get("channels", []):
                overwrites = self._get_overwrites(chan_info, roles)
                channel = None
                
                if chan_info["type"] == "text":
                    channel = await category.create_text_channel(
                        chan_info["name"], 
                        topic=chan_info.get("topic"),
                        overwrites=overwrites
                    )
                    if not first_text_channel:
                        first_text_channel = channel
                elif chan_info["type"] == "voice":
                    channel = await category.create_voice_channel(
                        chan_info["name"],
                        overwrites=overwrites
                    )
                
                print(f"Canal criado: {chan_info['name']}")

        # 4. Mensagem de Boas-Vindas
        if first_text_channel and structure_data.get("welcome_message"):
            embed = discord.Embed(
                title=f"Bem-vindo ao {self.guild.name}!",
                description=structure_data["welcome_message"],
                color=discord.Color.blue()
            )
            await first_text_channel.send(embed=embed)

    async def clear_server(self, keep_channel_id: int):
        """Limpa o servidor mantendo apenas o canal atual e cargos de bots."""
        # Deletar Canais
        for channel in self.guild.channels:
            if channel.id != keep_channel_id:
                try:
                    await channel.delete()
                except:
                    pass
        
        # Deletar Cargos
        for role in self.guild.roles:
            if not role.is_default() and not role.managed:
                try:
                    await role.delete()
                except:
                    pass
        print("Servidor limpo (preservando canal de comando)!")
