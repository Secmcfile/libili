# Required libraries for the bot
import discord
from discord.ext import commands, tasks
from discord import app_commands
import asyncio
import datetime
import random
import json
import os
import io
import math
from typing import Optional
import aiohttp
import re
import yt_dlp

# ============================================
# BOT CONFIGURATION - SET YOUR VALUES HERE
# ============================================

# Bot token (REPLACE WITH YOUR ACTUAL TOKEN)
TOKEN = "YOUR_TOKEN_HERE"

# Bot owner IDs and username
BOT_OWNER_IDS = ["1206171767509352489"]
BOT_OWNER_USERNAMES = ["security_file"]

# YouTube API Key (leave empty or remove if not using YouTube features)
# Note: YouTube features will be disabled if no API key is provided

# ============================================
# END OF CONFIGURATION
# ============================================

# Dil sistemi
LANGS = {
    "EN": {
        # Genel
        "success": "✅ Success!",
        "error": "❌ Error!",
        "no_permission": "❌ You don't have permission to use this!",
        "bot_owner_only": "❌ Only the bot owner can use this!",
        "server_owner_only": "❌ Only the server owner can use this!",
        
        # Moderasyon
        "kicked": "🚪 {user} has been kicked!",
        "banned": "🔨 {user} has been banned!",
        "unbanned": "🔓 {user} has been unbanned!",
        "muted": "🔇 {user} has been muted!",
        "unmuted": "🔊 {user} has been unmuted!",
        "timed_out": "⏰ {user} has been timed out!",
        "untimeout": "⏹️ {user} timeout has been removed!",
        "cleared": "🧹 {count} messages cleared!",
        
        # Coin Sistemi
        "coins": "💰 {user}, Sampy Coin balance: **{amount}** 🪙",
        "coins_transfer": "💸 Transferred **{amount}** Sampy Coin to {user}!",
        "daily_claimed": "🎁 Daily reward claimed! **+{amount}** Sampy Coin",
        "not_enough_coins": "❌ Not enough Sampy Coin! Needed: {need}, You have: {have}",
        
        # Market
        "market": "🛍️ Sampy Market",
        "market_item": "{name} - {price} Sampy Coin",
        "purchased": "🎉 Purchase successful!",
        "product_expired": "⏰ Your {product} has expired!",
        
        # Level Sistemi
        "level": "📊 {user} - Level: **{level}** | Messages: **{messages}**",
        "level_top": "🏆 Level Leaderboard",
        "level_up": "🎉 {user} reached level {level}!",
        
        # Ticket
        "ticket_created": "🎫 Ticket created: {channel}",
        "ticket_closed": "🔒 Ticket closed!",
        
        # Çekiliş
        "giveaway_created": "🎉 Giveaway created in {channel}!",
        "giveaway_ended": "🎊 Giveaway ended! Winners: {winners}",
        
        # Diğer
        "ping": "🏓 Pong! **{ms}ms**",
        "server_info": "🏠 Server Info",
        "io_channel_set": "📁 IO channel set to {channel}",
        "language_set": "🌐 Language set to {language}",
        
        # Roller
        "special_role": "Special Role",
        "vip": "VIP",
        "megavip": "MegaVIP", 
        "ultravip": "UltraVIP",
        "supervip": "SuperVIP",
        "supervip_plus": "SuperVIP+",
        "sampy_premium": "Sampy Premium",
        "booster": "Booster",
        "sampy_bot_owner": "Sampy Bot Owner",
        
        # Yeni eklenenler
        "market_not_configured": "❌ Market not configured for this server!",
        "boost_started": "🎉 {user} boosted the server! Booster role given.",
        "boost_ended": "🔻 {user} boost ended. Booster role removed.",
        "left_server": "✅ Successfully left **{server}**!",
        "leave_failed": "❌ Failed to leave server: {error}",
        
        # Başvuru Sistemi
        "application_created": "📝 Application created!",
        "application_closed": "🔒 Application closed!",
        "application_submitted": "✅ Application submitted successfully!",
        "application_waiting": "⏳ Please wait for response from support team.",
        "application_instruction": "Hello {user}! Please answer the following questions in separate messages:",
        "application_requirement_completed": "✅ Requirement completed! Please continue in order.",
        "application_error": "❌ Application error! Please close and reopen.",
        "application_summary": "📄 {user} Application",
        "application_response_wait": "Please wait for response from support team.",
        "application_team": "Support Team",
        "application_enter_stages": "Please enter the number of stages:",
        "application_enter_stage": "Please enter stage {number}:",
        "application_select_optional": "Select optional stages (if any):",
        "application_setup_complete": "✅ Application system setup completed!",
        
        # Yeni Moderasyon
        "unmuted": "🔊 {user} has been unmuted!",
        "unipbanned": "🔓 {user} IP ban has been removed!",
        "unipmuted": "🔊 {user} IP mute has been removed!",
        "user_not_banned": "❌ User is not banned!",
        "user_not_muted": "❌ User is not muted!",
        "punishment_users": "📋 Punishment Users",
        "no_punishments": "✅ No active punishments!",
        "punishment_entry": "**{user}** - {type} ({duration}) - Reason: {reason}",
        "infinite": "infinite",
        "user_not_timed_out": "❌ User is not timed out!",
        
        # Yeni Eklenenler
        "tag_close_added": "✅ Added to tag block list: {target}",
        "tag_close_removed": "✅ Removed from tag block list: {target}",
        "tag_close_list": "📋 Tag Block List",
        "tag_close_empty": "No users/roles in tag block list",
        "tag_close_warning": "⚠️ You cannot tag {target} in {server}",
        "warn_added": "⚠️ {user} has been warned! (Total: {count})",
        "warn_removed": "✅ Warning removed from {user}! (Remaining: {count})",
        "warn_list": "📋 Warning List - {user}",
        "warn_none": "No warnings",
        "warn_entry": "**{count}.** {reason} - {moderator} - <t:{timestamp}:f>",
        "yt_setup_complete": "✅ YouTube video channel setup completed!",
        "yt_reset_complete": "✅ YouTube video channel reset!",
        "yt_new_video": "🎥 New Video!",
        "yt_subscriber_role": "YT-Subscriber",
        "yt_member_role": "YT-Member {level}",
        "autorole_added": "✅ Added to autorole: {role}",
        "autorole_removed": "✅ Removed from autorole: {role}",
        "autorole_list": "📋 Autorole List",
        "greeting_response": "Hi {user}! 👋",
        
        # Yeni Özellikler
        "temp_room_setup": "✅ Temporary room system setup in {channel}!",
        "temp_room_created": "🎉 Temporary room created: {channel}",
        "temp_room_closed": "🔒 Temporary room closed: {channel}",
        "ai_chat_started": "🤖 AI chat started in {channel}!",
        "ai_chat_stopped": "🔒 AI chat stopped in {channel}!",
        "ai_chat_history_saved": "💾 AI chat history saved!",
        "ai_chat_history_cleared": "🗑️ AI chat history cleared!",
        "server_setup_complete": "✅ Server setup completed with {level} level!",
        "temp_room_settings_updated": "⚙️ Temporary room settings updated!"
    },
    "TR": {
        # Genel
        "success": "✅ Başarılı!",
        "error": "❌ Hata!",
        "no_permission": "❌ Bunu kullanma izniniz yok!",
        "bot_owner_only": "❌ Bunu sadece bot sahibi kullanabilir!",
        "server_owner_only": "❌ Bunu sadece sunucu sahibi kullanabilir!",
        
        # Moderasyon
        "kicked": "🚪 {user} sunucudan atıldı!",
        "banned": "🔨 {user} sunucudan yasaklandı!",
        "unbanned": "🔓 {user} yasağı kaldırıldı!",
        "muted": "🔇 {user} susturuldu!",
        "unmuted": "🔊 {user} susturması kaldırıldı!",
        "timed_out": "⏰ {user} timeout'a atıldı!",
        "untimeout": "⏹️ {user} timeout'u kaldırıldı!",
        "cleared": "🧹 {count} mesaj silindi!",
        
        # Coin Sistemi
        "coins": "💰 {user}, Sampy Coin bakiyesi: **{amount}** 🪙",
        "coins_transfer": "💸 {user} kullanıcısına **{amount}** Sampy Coin transfer edildi!",
        "daily_claimed": "🎁 Günlük ödül alındı! **+{amount}** Sampy Coin",
        "not_enough_coins": "❌ Yeterli Sampy Coin yok! Gerekli: {need}, Sizde: {have}",
        
        # Market
        "market": "🛍️ Sampy Market",
        "market_item": "{name} - {price} Sampy Coin",
        "purchased": "🎉 Satın alma başarılı!",
        "product_expired": "⏰ {product} ürününüzün süresi doldu!",
        
        # Level Sistemi
        "level": "📊 {user} - Seviye: **{level}** | Mesaj: **{messages}**",
        "level_top": "🏆 Seviye Lider Tablosu",
        "level_up": "🎉 {user} {level}. seviyeye ulaştı!",
        
        # Ticket
        "ticket_created": "🎫 Ticket oluşturuldu: {channel}",
        "ticket_closed": "🔒 Ticket kapatıldı!",
        
        # Çekiliş
        "giveaway_created": "🎉 Çekiliş {channel} kanalında oluşturuldu!",
        "giveaway_ended": "🎊 Çekiliş sona erdi! Kazananlar: {winners}",
        
        # Diğer
        "ping": "🏓 Pong! **{ms}ms**",
        "server_info": "🏠 Sunucu Bilgisi",
        "io_channel_set": "📁 Giriş-çıkış kanalı {channel} olarak ayarlandı",
        "language_set": "🌐 Dil {language} olarak ayarlandı",
        
        # Roller
        "special_role": "Özel Rol",
        "vip": "VIP",
        "megavip": "MegaVIP",
        "ultravip": "UltraVIP", 
        "supervip": "SüperVIP",
        "supervip_plus": "SüperVIP+",
        "sampy_premium": "Sampy Premium",
        "booster": "Booster",
        "sampy_bot_owner": "Sampy Bot Sahibi",
        
        # Yeni eklenenler
        "market_not_configured": "❌ Bu sunucu için market ayarlanmamış!",
        "boost_started": "🎉 {user} sunucuyu boostladı! Booster rolü verildi.",
        "boost_ended": "🔻 {user} boostu sona erdi. Booster rolü kaldırıldı.",
        "left_server": "✅ **{server}** sunucusundan başarıyla ayrıldı!",
        "leave_failed": "❌ Sunucudan ayrılma başarısız: {error}",
        
        # Başvuru Sistemi
        "application_created": "📝 Başvuru oluşturuldu!",
        "application_closed": "🔒 Başvuru kapatıldı!",
        "application_submitted": "✅ Başvuru başarıyla gönderildi!",
        "application_waiting": "⏳ Lütfen destek ekibinden yanıt bekleyin.",
        "application_instruction": "Merhaba {user}! Lütfen aşağıdaki soruları ayrı mesajlar halinde cevaplayın:",
        "application_requirement_completed": "✅ Gereksinim işlendi! Lütfen sıraya göre devam edin.",
        "application_error": "❌ Başvuru hatası! Lütfen kapatıp yeniden açın.",
        "application_summary": "📄 {user} Başvurusu",
        "application_response_wait": "Lütfen destek ekibinden yanıt gelmesini bekleyin.",
        "application_team": "Destek Ekibi",
        "application_enter_stages": "Lütfen aşama sayısını girin:",
        "application_enter_stage": "Lütfen {number}. aşamayı girin:",
        "application_select_optional": "Opsiyonel aşamaları seçin (varsa):",
        "application_setup_complete": "✅ Başvuru sistemi kurulumu tamamlandı!",
        
        # Yeni Moderasyon
        "unmuted": "🔊 {user} susturması kaldırıldı!",
        "unipbanned": "🔓 {user} IP yasağı kaldırıldı!",
        "unipmuted": "🔊 {user} IP susturması kaldırıldı!",
        "user_not_banned": "❌ Kullanıcı yasaklanmamış!",
        "user_not_muted": "❌ Kullanıcı susturulmamış!",
        "punishment_users": "📋 Cezalı Kullanıcılar",
        "no_punishments": "✅ Aktif ceza yok!",
        "punishment_entry": "**{user}** - {type} ({duration}) - Sebep: {reason}",
        "infinite": "sınırsız",
        "user_not_timed_out": "❌ Kullanıcı timeout'ta değil!",
        
        # Yeni Eklenenler
        "tag_close_added": "✅ Etiket engelleme listesine eklendi: {target}",
        "tag_close_removed": "✅ Etiket engelleme listesinden kaldırıldı: {target}",
        "tag_close_list": "📋 Etiket Engelleme Listesi",
        "tag_close_empty": "Etiket engelleme listesinde kullanıcı/rol yok",
        "tag_close_warning": "⚠️ {server} sunucusunda {target} etiketleyemezsiniz",
        "warn_added": "⚠️ {user} uyarıldı! (Toplam: {count})",
        "warn_removed": "✅ {user} kullanıcısının uyarısı kaldırıldı! (Kalan: {count})",
        "warn_list": "📋 Uyarı Listesi - {user}",
        "warn_none": "Uyarı yok",
        "warn_entry": "**{count}.** {reason} - {moderator} - <t:{timestamp}:f>",
        "yt_setup_complete": "✅ YouTube video kanalı kurulumu tamamlandı!",
        "yt_reset_complete": "✅ YouTube video kanalı sıfırlandı!",
        "yt_new_video": "🎥 Yeni Video!",
        "yt_subscriber_role": "YT-Abone",
        "yt_member_role": "YT-Üye {level}",
        "autorole_added": "✅ Oto-role eklendi: {role}",
        "autorole_removed": "✅ Oto-rolden kaldırıldı: {role}",
        "autorole_list": "📋 Oto-Rol Listesi",
        "greeting_response": "Aleyküm Selam {user}! 👋",
        
        # Yeni Özellikler
        "temp_room_setup": "✅ Geçici oda sistemi {channel} kanalında kuruldu!",
        "temp_room_created": "🎉 Geçici oda oluşturuldu: {channel}",
        "temp_room_closed": "🔒 Geçici oda kapatıldı: {channel}",
        "ai_chat_started": "🤖 AI sohbeti {channel} kanalında başlatıldı!",
        "ai_chat_stopped": "🔒 AI sohbeti {channel} kanalında durduruldu!",
        "ai_chat_history_saved": "💾 AI sohbet geçmişi kaydedildi!",
        "ai_chat_history_cleared": "🗑️ AI sohbet geçmişi temizlendi!",
        "server_setup_complete": "✅ Sunucu kurulumu {level} seviyesinde tamamlandı!",
        "temp_room_settings_updated": "⚙️ Geçici oda ayarları güncellendi!"
    }
}

# Yetki kontrolleri
def is_server_owner():
    def predicate(interaction: discord.Interaction):
        return interaction.guild is not None and interaction.user == interaction.guild.owner
    return app_commands.check(predicate)

def is_bot_owner():
    def predicate(interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        username = interaction.user.name
        return user_id in BOT_OWNER_IDS or username in BOT_OWNER_USERNAMES
    return app_commands.check(predicate)

def has_command_permission(command_name: str):
    def predicate(interaction: discord.Interaction):
        # Bot owner her zaman her komutu kullanabilir
        user_id = str(interaction.user.id)
        username = interaction.user.name
        if user_id in BOT_OWNER_IDS or username in BOT_OWNER_USERNAMES:
            return True
        
        # Sampy Bot Owner rolü kontrolü
        if interaction.guild:
            sampy_owner_role = discord.utils.get(interaction.guild.roles, name=get_text(str(interaction.guild.id), "sampy_bot_owner"))
            if sampy_owner_role and sampy_owner_role in interaction.user.roles:
                return True
        
        guild_id = str(interaction.guild.id)
        
        # Komut yetkilerini kontrol et
        if guild_id in bot.command_permissions:
            if command_name in bot.command_permissions[guild_id]:
                required_roles = bot.command_permissions[guild_id][command_name]
                user_roles = [role.id for role in interaction.user.roles]
                
                # Eğer boş array ise, sadece sunucu sahibi
                if not required_roles:
                    return interaction.user == interaction.guild.owner
                
                # Rol kontrolü
                for role_id in required_roles:
                    if role_id in user_roles:
                        return True
                
                return False
        
        # Varsayılan olarak sadece sunucu sahibi
        return interaction.user == interaction.guild.owner
    return app_commands.check(predicate)

def has_manage_guild_permission():
    def predicate(interaction: discord.Interaction):
        # Bot owner her zaman izinli
        user_id = str(interaction.user.id)
        username = interaction.user.name
        if user_id in BOT_OWNER_IDS or username in BOT_OWNER_USERNAMES:
            return True
        
        # Sampy Bot Owner rolü kontrolü
        if interaction.guild:
            sampy_owner_role = discord.utils.get(interaction.guild.roles, name=get_text(str(interaction.guild.id), "sampy_bot_owner"))
            if sampy_owner_role and sampy_owner_role in interaction.user.roles:
                return True
        
        # Sunucu yönetme izni kontrolü
        return interaction.user.guild_permissions.manage_guild
    return app_commands.check(predicate)

def get_guild_lang(guild_id: str) -> str:
    if hasattr(bot, 'guild_settings') and guild_id in bot.guild_settings:
        return bot.guild_settings[guild_id].get('lang', 'EN')
    return 'EN'

def get_text(guild_id: str, key: str, **kwargs) -> str:
    lang = get_guild_lang(guild_id)
    text = LANGS[lang].get(key, LANGS['EN'].get(key, key))
    return text.format(**kwargs)

# Yeni View'lar - Temp Room Management
class TempRoomSettingsView(discord.ui.View):
    def __init__(self, bot, room_data):
        super().__init__(timeout=300)
        self.bot = bot
        self.room_data = room_data
    
    @discord.ui.button(label="🔒 Lock/Unlock", style=discord.ButtonStyle.primary)
    async def toggle_lock(self, interaction: discord.Interaction, button: discord.ui.Button):
        channel = interaction.guild.get_channel(self.room_data["channel_id"])
        if channel:
            current_overwrites = channel.overwrites
            new_overwrites = {}
            
            for target, overwrite in current_overwrites.items():
                if target == interaction.guild.default_role:
                    new_overwrites[target] = discord.PermissionOverwrite(
                        connect=not overwrite.connect if overwrite.connect is not None else False
                    )
                else:
                    new_overwrites[target] = overwrite
            
            await channel.edit(overwrites=new_overwrites)
            await interaction.response.send_message(
                f"✅ Room {'locked' if not current_overwrites.get(interaction.guild.default_role, discord.PermissionOverwrite()).connect else 'unlocked'}!",
                ephemeral=True
            )
    
    @discord.ui.button(label="👥 User Limit", style=discord.ButtonStyle.primary)
    async def set_user_limit(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = UserLimitModal(self.room_data)
        await interaction.response.send_modal(modal)
    
    @discord.ui.button(label="➕ Add User", style=discord.ButtonStyle.success)
    async def add_user(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = AddUserModal(self.room_data)
        await interaction.response.send_modal(modal)
    
    @discord.ui.button(label="➖ Remove User", style=discord.ButtonStyle.danger)
    async def remove_user(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = RemoveUserModal(self.room_data)
        await interaction.response.send_modal(modal)
    
    @discord.ui.button(label="❌ Close Room", style=discord.ButtonStyle.danger)
    async def close_room(self, interaction: discord.Interaction, button: discord.ui.Button):
        channel = interaction.guild.get_channel(self.room_data["channel_id"])
        if channel:
            await channel.delete()
            await interaction.response.send_message(
                get_text(str(interaction.guild.id), "temp_room_closed", channel=channel.name),
                ephemeral=True
            )

class UserLimitModal(discord.ui.Modal, title="Set User Limit"):
    def __init__(self, room_data):
        super().__init__()
        self.room_data = room_data
        self.limit = discord.ui.TextInput(
            label="User Limit (0 for unlimited)",
            placeholder="Enter number (0-99)",
            default=str(room_data.get("user_limit", 0)),
            max_length=2,
            required=True
        )
        self.add_item(self.limit)
    
    async def on_submit(self, interaction: discord.Interaction):
        try:
            limit = int(self.limit.value)
            if limit < 0 or limit > 99:
                await interaction.response.send_message("❌ Limit must be between 0-99!", ephemeral=True)
                return
            
            channel = interaction.guild.get_channel(self.room_data["channel_id"])
            if channel:
                await channel.edit(user_limit=limit)
                self.room_data["user_limit"] = limit
                bot.temp_rooms[str(channel.id)] = self.room_data
                bot.save_json(bot.temp_rooms, "temp_rooms.json")
                await interaction.response.send_message(f"✅ User limit set to {limit}!", ephemeral=True)
        except ValueError:
            await interaction.response.send_message("❌ Please enter a valid number!", ephemeral=True)

class AddUserModal(discord.ui.Modal, title="Add User to Room"):
    def __init__(self, room_data):
        super().__init__()
        self.room_data = room_data
        self.user_id = discord.ui.TextInput(
            label="User ID",
            placeholder="Enter user ID",
            required=True
        )
        self.add_item(self.user_id)
    
    async def on_submit(self, interaction: discord.Interaction):
        try:
            user_id = int(self.user_id.value)
            user = interaction.guild.get_member(user_id)
            if not user:
                await interaction.response.send_message("❌ User not found!", ephemeral=True)
                return
            
            channel = interaction.guild.get_channel(self.room_data["channel_id"])
            if channel:
                await channel.set_permissions(user, connect=True, view_channel=True)
                
                if "allowed_users" not in self.room_data:
                    self.room_data["allowed_users"] = []
                if user_id not in self.room_data["allowed_users"]:
                    self.room_data["allowed_users"].append(user_id)
                
                bot.temp_rooms[str(channel.id)] = self.room_data
                bot.save_json(bot.temp_rooms, "temp_rooms.json")
                await interaction.response.send_message(f"✅ {user.mention} added to room!", ephemeral=True)
        except ValueError:
            await interaction.response.send_message("❌ Please enter a valid user ID!", ephemeral=True)

class RemoveUserModal(discord.ui.Modal, title="Remove User from Room"):
    def __init__(self, room_data):
        super().__init__()
        self.room_data = room_data
        self.user_id = discord.ui.TextInput(
            label="User ID",
            placeholder="Enter user ID",
            required=True
        )
        self.add_item(self.user_id)
    
    async def on_submit(self, interaction: discord.Interaction):
        try:
            user_id = int(self.user_id.value)
            user = interaction.guild.get_member(user_id)
            if not user:
                await interaction.response.send_message("❌ User not found!", ephemeral=True)
                return
            
            channel = interaction.guild.get_channel(self.room_data["channel_id"])
            if channel:
                await channel.set_permissions(user, overwrite=None)
                
                if "allowed_users" in self.room_data and user_id in self.room_data["allowed_users"]:
                    self.room_data["allowed_users"].remove(user_id)
                
                bot.temp_rooms[str(channel.id)] = self.room_data
                bot.save_json(bot.temp_rooms, "temp_rooms.json")
                await interaction.response.send_message(f"✅ {user.mention} removed from room!", ephemeral=True)
        except ValueError:
            await interaction.response.send_message("❌ Please enter a valid user ID!", ephemeral=True)

# AI Chat System Views
class AIChatView(discord.ui.View):
    def __init__(self, bot, channel_id):
        super().__init__(timeout=None)
        self.bot = bot
        self.channel_id = channel_id
    
    @discord.ui.button(label="💾 Save History", style=discord.ButtonStyle.primary, custom_id="ai_save_history")
    async def save_history(self, interaction: discord.Interaction, button: discord.ui.Button):
        if str(interaction.channel.id) in bot.ai_chats:
            chat_data = bot.ai_chats[str(interaction.channel.id)]
            history_file = f"ai_chat_history_{interaction.channel.id}.txt"
            
            with open(history_file, 'w', encoding='utf-8') as f:
                f.write(f"AI Chat History - {interaction.channel.name}\n")
                f.write(f"Date: {datetime.datetime.now()}\n\n")
                for msg in chat_data.get('history', []):
                    f.write(f"{msg['author']}: {msg['content']}\n")
            
            file = discord.File(history_file, filename=f"ai_chat_history_{interaction.channel.id}.txt")
            await interaction.response.send_message(
                get_text(str(interaction.guild.id), "ai_chat_history_saved"),
                file=file,
                ephemeral=True
            )
            os.remove(history_file)
    
    @discord.ui.button(label="🗑️ Clear History", style=discord.ButtonStyle.danger, custom_id="ai_clear_history")
    async def clear_history(self, interaction: discord.Interaction, button: discord.ui.Button):
        if str(interaction.channel.id) in bot.ai_chats:
            bot.ai_chats[str(interaction.channel.id)]['history'] = []
            bot.save_json(bot.ai_chats, "ai_chats.json")
            await interaction.response.send_message(
                get_text(str(interaction.guild.id), "ai_chat_history_cleared"),
                ephemeral=True
            )
    
    @discord.ui.button(label="➕ Add User", style=discord.ButtonStyle.success, custom_id="ai_add_user")
    async def add_user(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = AddAIChatUserModal(str(interaction.channel.id))
        await interaction.response.send_modal(modal)
    
    @discord.ui.button(label="❌ Stop AI Chat", style=discord.ButtonStyle.danger, custom_id="ai_stop_chat")
    async def stop_chat(self, interaction: discord.Interaction, button: discord.ui.Button):
        if str(interaction.channel.id) in bot.ai_chats:
            del bot.ai_chats[str(interaction.channel.id)]
            bot.save_json(bot.ai_chats, "ai_chats.json")
        
        await interaction.response.send_message(
            get_text(str(interaction.guild.id), "ai_chat_stopped", channel=interaction.channel.mention)
        )
        await asyncio.sleep(3)
        await interaction.channel.delete()

class AddAIChatUserModal(discord.ui.Modal, title="Add User to AI Chat"):
    def __init__(self, channel_id):
        super().__init__()
        self.channel_id = channel_id
        self.user_id = discord.ui.TextInput(
            label="User ID",
            placeholder="Enter user ID to add to chat",
            required=True
        )
        self.add_item(self.user_id)
    
    async def on_submit(self, interaction: discord.Interaction):
        try:
            user_id = int(self.user_id.value)
            user = interaction.guild.get_member(user_id)
            if not user:
                await interaction.response.send_message("❌ User not found!", ephemeral=True)
                return
            
            channel = interaction.guild.get_channel(int(self.channel_id))
            if channel:
                await channel.set_permissions(user, read_messages=True, send_messages=True)
                await interaction.response.send_message(f"✅ {user.mention} added to AI chat!", ephemeral=True)
        except ValueError:
            await interaction.response.send_message("❌ Please enter a valid user ID!", ephemeral=True)

# Mevcut View'lar (önceki kodda tanımlananlar) aynen kalacak...
class TagCloseView(discord.ui.View):
    def __init__(self, bot, guild_id):
        super().__init__(timeout=60)
        self.bot = bot
        self.guild_id = guild_id
        
        # Rol ve üye seçim menüsü
        self.select = discord.ui.Select(
            placeholder="Select roles/members to block tags",
            min_values=1,
            max_values=25,
            options=[]
        )
        self.select.callback = self.select_callback
        self.add_item(self.select)
        
        # Seçenekleri doldur
        self.fill_options()
    
    def fill_options(self):
        guild = bot.get_guild(int(self.guild_id))
        if not guild:
            return
            
        options = []
        
        # Roller (ilk 15)
        for role in guild.roles[-15:]:
            if role.name != "@everyone" and not role.managed:
                options.append(discord.SelectOption(
                    label=f"👑 {role.name}",
                    value=f"role_{role.id}",
                    description=f"Role - {role.id}"
                ))
        
        # Üyeler (ilk 10)
        members_added = 0
        for member in guild.members:
            if members_added >= 10:
                break
            if not member.bot:
                options.append(discord.SelectOption(
                    label=f"👤 {member.display_name}",
                    value=f"user_{member.id}",
                    description=f"User - {member.id}"
                ))
                members_added += 1
        
        self.select.options = options
    
    async def select_callback(self, interaction: discord.Interaction):
        selected_values = self.select.values
        
        if self.guild_id not in bot.tag_close_data:
            bot.tag_close_data[self.guild_id] = []
        
        added = []
        for value in selected_values:
            if value not in bot.tag_close_data[self.guild_id]:
                bot.tag_close_data[self.guild_id].append(value)
                added.append(value)
        
        bot.save_json(bot.tag_close_data, "tag_close.json")
        
        if added:
            targets = []
            for target in added:
                type_, id_ = target.split('_')
                if type_ == "role":
                    role = interaction.guild.get_role(int(id_))
                    if role:
                        targets.append(role.mention)
                else:
                    user = interaction.guild.get_member(int(id_))
                    if user:
                        targets.append(user.mention)
            
            await interaction.response.send_message(
                get_text(self.guild_id, "tag_close_added", target=", ".join(targets)),
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                "❌ Selected targets are already in the block list!",
                ephemeral=True
            )

class WarnListView(discord.ui.View):
    def __init__(self, user_id, warnings):
        super().__init__(timeout=60)
        self.user_id = user_id
        self.warnings = warnings
        self.current_page = 0
        self.page_size = 5
    
    def create_embed(self, guild_id):
        start_idx = self.current_page * self.page_size
        end_idx = start_idx + self.page_size
        page_warnings = list(self.warnings.items())[start_idx:end_idx]
        
        total_pages = math.ceil(len(self.warnings) / self.page_size)
        
        embed = discord.Embed(
            title=get_text(guild_id, "warn_list", user=f"<@{self.user_id}>"),
            color=0xffa500
        )
        
        if not page_warnings:
            embed.description = get_text(guild_id, "warn_none")
        else:
            for i, (warn_id, warn_data) in enumerate(page_warnings, start_idx + 1):
                moderator = f"<@{warn_data['moderator_id']}>"
                timestamp = int(datetime.datetime.fromisoformat(warn_data['timestamp']).timestamp())
                embed.add_field(
                    name=f"#{i}",
                    value=get_text(guild_id, "warn_entry", 
                                 count=i, 
                                 reason=warn_data['reason'], 
                                 moderator=moderator, 
                                 timestamp=timestamp),
                    inline=False
                )
        
        embed.set_footer(text=f"Page {self.current_page + 1}/{total_pages}")
        return embed
    
    @discord.ui.button(label="◀️", style=discord.ButtonStyle.secondary)
    async def previous_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page > 0:
            self.current_page -= 1
            embed = self.create_embed(str(interaction.guild.id))
            await interaction.response.edit_message(embed=embed, view=self)
        else:
            await interaction.response.defer()
    
    @discord.ui.button(label="▶️", style=discord.ButtonStyle.secondary)
    async def next_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        total_pages = math.ceil(len(self.warnings) / self.page_size)
        if self.current_page < total_pages - 1:
            self.current_page += 1
            embed = self.create_embed(str(interaction.guild.id))
            await interaction.response.edit_message(embed=embed, view=self)
        else:
            await interaction.response.defer()

class GetYouTubeAPIView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)
    
    @discord.ui.button(label="English", style=discord.ButtonStyle.primary, emoji="🇺🇸")
    async def english_guide(self, interaction: discord.Interaction, button: discord.ui.Button):
        guide = """**Steps to Obtain a YouTube API Key (Updated 2025)**

1. **Log in to Google Cloud Platform**
   Go to https://console.cloud.google.com/ and log in with your Google account.

2. **Create a New Project**
   · Click the "Select Project" button in the upper left corner.
   · Select "New Project" in the window that opens.
   · Give your project a name (for example, "DiscordYTBot").
   · Click the "Create" button to create your project.

3. **Enable YouTube Data API v3**
   · Type YouTube Data API v3 in the search bar at the top of the page.
   · Select YouTube Data API v3 from the results and then click the "Enable" button.

4. **Create the API Key**
   · From the left-hand menu, go to "APIs & Services" > "Credentials."
   · Click the "+ Create Credentials" button.
   · Select "API key" from the drop-down menu.
   · The system will immediately generate an API key for you. This key will look like this:
     ```
     AIzaSyBz-9XnJpJxxxxxxxxxxxxxYpB5x4
     ```
   · Copy the key to a safe location.

5. **(Optional but recommended) Restrict the Key**
   · On the same page, click the "Restrict Key" button next to the API key you created.
   · In the "API restrictions" section, select "Restrict key" and select "YouTube Data API v3" from the drop-down list. This ensures that your key is only used for this API.
   · You can optionally add additional restrictions, such as "IP addresses" or "HTTP referrers," for added security."""
        
        await interaction.response.send_message(guide, ephemeral=True)
    
    @discord.ui.button(label="Türkçe", style=discord.ButtonStyle.primary, emoji="🇹🇷")
    async def turkish_guide(self, interaction: discord.Interaction, button: discord.ui.Button):
        guide = """**YouTube API Anahtarı Alma Adımları (2025 Güncel)**

1. **Google Cloud Platform'a Giriş Yapın**
   https://console.cloud.google.com/ adresine gidin ve Google hesabınızla giriş yapın.

2. **Yeni Bir Proje Oluşturun**
   · Sol üst köşedeki "Select Project" (Proje Seç) butonuna tıklayın.
   · Açılan pencerede "New Project" (Yeni Proje) seçeneğini seçin.
   · Projenize bir isim verin (örneğin, "DiscordYTBot").
   · "Create" (Oluştur) butonuna tıklayarak projenizi oluşturun.

3. **YouTube Data API v3'ü Etkinleştirin**
   · Sayfanın üst kısmındaki arama çubuğuna YouTube Data API v3 yazın.
   · Çıkan sonuçlarda YouTube Data API v3'ü seçin ve ardından "Enable" (Etkinleştir) butonuna basın.

4. **API Anahtarını Oluşturun**
   · Sol taraftaki menüden "APIs & Services" (API'ler ve Hizmetler) > "Credentials" (Kimlik Bilgileri) sekmesine gidin.
   · "+ Create Credentials" (Kimlik Bilgileri Oluştur) butonuna tıklayın.
   · Açılan menüden "API key" (API anahtarı) seçeneğini seçin.
   · Sistem size hemen bir API anahtarı oluşturacaktır. Bu anahtar şu şekilde görünür:
     ```
     AIzaSyBz-9XnJpJxxxxxxxxxxxxxYpB5x4
     ```
   · Anahtarı güvenli bir yere kopyalayın.

5. **(İsteğe Bağlı Ama Önerilir) Anahtarı Sınırlandırın**
   · Aynı sayfada oluşturduğunuz API anahtarının yanındaki "Restrict Key" (Anahtarı Sınırla) butonuna tıklayın.
   · "API restrictions" (API Kısıtlamaları) bölümünden "Restrict key" (Anahtarı sınırla) seçeneğini işaretleyin ve açılan listeden "YouTube Data API v3" seçin. Bu, anahtarınızın sadece bu API için kullanılmasını sağlar.
   · İsterseniz ek güvenlik için "IP addresses" (IP adresleri) veya "HTTP referrers" (HTTP yönlendiriciler) gibi ek kısıtlamalar da ekleyebilirsiniz."""
        
        await interaction.response.send_message(guide, ephemeral=True)

class GiveawayJoinLimitView(discord.ui.View):
    def __init__(self, bot, guild_id):
        super().__init__(timeout=60)
        self.bot = bot
        self.guild_id = guild_id
        
        self.role_select = discord.ui.Select(
            placeholder="Select roles for join limits",
            min_values=1,
            max_values=25,
            options=[]
        )
        self.role_select.callback = self.role_select_callback
        self.add_item(self.role_select)
        
        self.fill_options()
    
    def fill_options(self):
        guild = bot.get_guild(int(self.guild_id))
        if not guild:
            return
            
        options = []
        for role in guild.roles:
            if role.name != "@everyone" and not role.managed:
                options.append(discord.SelectOption(
                    label=role.name,
                    value=str(role.id),
                    description=f"ID: {role.id}"
                ))
        
        self.role_select.options = options[:25]
    
    async def role_select_callback(self, interaction: discord.Interaction):
        self.selected_roles = [int(role_id) for role_id in self.role_select.values]
        
        # Butonları devre dışı bırak
        for item in self.children:
            item.disabled = True
        await interaction.response.edit_message(view=self)
        
        # Her rol için katılma limiti sor
        self.role_limits = {}
        for role_id in self.selected_roles:
            role = interaction.guild.get_role(role_id)
            if role:
                await interaction.followup.send(
                    f"Enter join limit for {role.mention} (0 for unlimited, number for limit):",
                    ephemeral=True
                )
                
                def check(m):
                    return m.author == interaction.user and m.channel == interaction.channel and (m.content.isdigit() or m.content == "0")
                
                try:
                    msg = await bot.wait_for('message', check=check, timeout=30)
                    limit = int(msg.content)
                    self.role_limits[role_id] = limit
                    
                    try:
                        await msg.delete()
                    except:
                        pass
                        
                except asyncio.TimeoutError:
                    await interaction.followup.send("Timed out.", ephemeral=True)
                    return
        
        # Limitleri kaydet
        if self.guild_id not in bot.giveaway_join_limits:
            bot.giveaway_join_limits[self.guild_id] = {}
        
        for role_id, limit in self.role_limits.items():
            bot.giveaway_join_limits[self.guild_id][str(role_id)] = limit
        
        bot.save_json(bot.giveaway_join_limits, "giveaway_join_limits.json")
        
        await interaction.followup.send("✅ Giveaway join limits set successfully!", ephemeral=True)

# Mevcut View'lar (önceki kodda tanımlananlar)
class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label='Close', style=discord.ButtonStyle.danger, custom_id='close_ticket')
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not has_command_permission('ticket-close')(interaction):
            await interaction.response.send_message(get_text(str(interaction.guild.id), "no_permission"), ephemeral=True)
            return
        
        await interaction.response.send_message("Closing ticket in 5 seconds...")
        await asyncio.sleep(5)
        await interaction.channel.delete()

class MarketView(discord.ui.View):
    def __init__(self, bot, guild_id):
        super().__init__(timeout=60)
        self.bot = bot
        self.guild_id = guild_id
    
    @discord.ui.select(
        placeholder="Select product to purchase",
        options=[
            discord.SelectOption(label="Special Role (3 Days)", value="special_role_3d", description="3-day special role"),
            discord.SelectOption(label="Special Role (7 Days)", value="special_role_7d", description="7-day special role"),
            discord.SelectOption(label="VIP (30 Days)", value="vip_30d", description="30-day VIP role"),
            discord.SelectOption(label="MegaVIP (30 Days)", value="megavip_30d", description="30-day MegaVIP role"),
            discord.SelectOption(label="UltraVIP (30 Days)", value="ultravip_30d", description="30-day UltraVIP role"),
            discord.SelectOption(label="SuperVIP (30 Days)", value="supervip_30d", description="30-day SuperVIP role"),
            discord.SelectOption(label="SuperVIP+ (30 Days)", value="supervip_plus_30d", description="30-day SuperVIP+ role"),
            discord.SelectOption(label="Sampy Premium (30 Days)", value="sampy_premium_30d", description="30-day Sampy Premium role"),
        ]
    )
    async def select_product(self, interaction: discord.Interaction, select: discord.ui.Select):
        product = select.values[0]
        
        if str(interaction.guild_id) not in self.bot.market_data:
            await interaction.response.send_message(get_text(str(interaction.guild.id), "market_not_configured"), ephemeral=True)
            return
        
        price = self.bot.market_data[str(interaction.guild_id)][product]
        user_coins = self.bot.coins_data.get(str(interaction.user.id), 0)
        
        if user_coins < price:
            await interaction.response.send_message(
                get_text(str(interaction.guild.id), "not_enough_coins", need=price, have=user_coins), 
                ephemeral=True
            )
            return
        
        # Coin düşürme
        self.bot.coins_data[str(interaction.user.id)] = user_coins - price
        self.bot.save_json(self.bot.coins_data, self.bot.coins_file)
        
        # Sunucu sahibine coin ekleme
        owner_id = str(interaction.guild.owner_id)
        owner_coins = self.bot.coins_data.get(owner_id, 0)
        self.bot.coins_data[owner_id] = owner_coins + price
        self.bot.save_json(self.bot.coins_data, self.bot.coins_file)
        
        # Rol oluşturma ve verme
        role_name = get_text(str(interaction.guild.id), product.split('_')[0])
        if "_" in product:
            duration = product.split('_')[1]
            role_name = f"{role_name} ({duration})"
        
        role = discord.utils.get(interaction.guild.roles, name=role_name)
        
        if role is None:
            role = await interaction.guild.create_role(
                name=role_name,
                color=discord.Color.random(),
                reason=f"Purchased by {interaction.user}"
            )
        
        await interaction.user.add_roles(role)
        
        # Satın alma kaydı
        purchase_id = f"{interaction.user.id}_{product}_{int(datetime.datetime.now().timestamp())}"
        expiry_time = datetime.datetime.now() + datetime.timedelta(days=int(''.join(filter(str.isdigit, product.split('_')[1]))))
        
        self.bot.purchases_data[purchase_id] = {
            "user_id": interaction.user.id,
            "guild_id": interaction.guild.id,
            "product": product,
            "role_id": role.id,
            "purchased_at": datetime.datetime.now().isoformat(),
            "expires_at": expiry_time.isoformat()
        }
        self.bot.save_json(self.bot.purchases_data, "purchases.json")
        
        await interaction.response.send_message(
            f"🎉 **{get_text(str(interaction.guild.id), 'purchased')}**\n"
            f"**Product:** {role_name}\n"
            f"**Price:** {price} Sampy Coin\n"
            f"**Remaining Balance:** {self.bot.coins_data[str(interaction.user.id)]} Sampy Coin\n"
            f"**Your Role:** {role.mention}\n"
            f"**Expires:** <t:{int(expiry_time.timestamp())}:R>",
            ephemeral=True
        )

# Gelişmiş Daily View
class AdvancedDailyView(discord.ui.View):
    def __init__(self, bot, user_id):
        super().__init__(timeout=60)
        self.bot = bot
        self.user_id = user_id
        
    @discord.ui.button(label="🎁 Claim Daily Reward (750 Coins)", style=discord.ButtonStyle.success)
    async def claim_daily(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_id = str(interaction.user.id)
        last_claim_key = f"{user_id}_last_daily"
        last_claim = self.bot.coins_data.get(last_claim_key)
        
        cooldown_hours = 12
        amount = 750

        if last_claim:
            last_claim_time = datetime.datetime.fromisoformat(last_claim)
            time_diff = datetime.datetime.now() - last_claim_time
            hours_diff = time_diff.total_seconds() / 3600

            if hours_diff < cooldown_hours:
                remaining_hours = cooldown_hours - hours_diff
                await interaction.response.send_message(
                    f"⏰ You can claim your daily reward in **{remaining_hours:.1f} hours**!",
                    ephemeral=True
                )
                return

        # YouTube rollerine özel ödül kontrolü
        yt_bonus = 0
        guild_id = str(interaction.guild.id)
        
        # YT-Subscriber kontrolü
        yt_subscriber_role_name = get_text(guild_id, "yt_subscriber_role")
        yt_subscriber_role = discord.utils.get(interaction.guild.roles, name=yt_subscriber_role_name)
        if yt_subscriber_role and yt_subscriber_role in interaction.user.roles:
            yt_bonus += 1250
        
        # YT-Member kontrolü
        yt_member_roles = [role for role in interaction.user.roles if role.name.startswith("YT-Member")]
        if yt_member_roles:
            yt_bonus += 1500
        
        total_amount = amount + yt_bonus

        # Coin ekle
        self.bot.coins_data[user_id] = self.bot.coins_data.get(user_id, 0) + total_amount
        self.bot.coins_data[last_claim_key] = datetime.datetime.now().isoformat()
        self.bot.save_json(self.bot.coins_data, self.bot.coins_file)

        embed = discord.Embed(
            title="🎁 Daily Reward Claimed!",
            description=f"**+{total_amount} Sampy Coin** added to your balance!",
            color=0x00ff00,
            timestamp=datetime.datetime.now()
        )
        embed.add_field(name="Base Reward", value=f"{amount} Sampy Coin", inline=True)
        if yt_bonus > 0:
            embed.add_field(name="YouTube Bonus", value=f"{yt_bonus} Sampy Coin", inline=True)
        embed.add_field(name="New Balance", value=f"{self.bot.coins_data[user_id]} Sampy Coin 🪙", inline=True)
        embed.add_field(name="Next Reward", value=f"{cooldown_hours} hours", inline=True)
        embed.set_footer(text="Thank you for using Sampy Bot!")
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

# Buton Rol View
class RoleButtonView(discord.ui.View):
    def __init__(self, role_id):
        super().__init__(timeout=None)
        self.role_id = role_id
    
    @discord.ui.button(label="Get/Remove Role", style=discord.ButtonStyle.primary, custom_id="role_button")
    async def role_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = interaction.guild.get_role(self.role_id)
        
        if not role:
            await interaction.response.send_message("❌ Role not found!", ephemeral=True)
            return
        
        try:
            if role in interaction.user.roles:
                await interaction.user.remove_roles(role)
                await interaction.response.send_message(
                    f"✅ **{role.name}** role removed from you!", 
                    ephemeral=True
                )
            else:
                await interaction.user.add_roles(role)
                await interaction.response.send_message(
                    f"✅ **{role.name}** role given to you!", 
                    ephemeral=True
                )
        except discord.Forbidden:
            await interaction.response.send_message("❌ I don't have permission to manage roles!", ephemeral=True)

# Sayı Tahmini Oyunu View
class NumberGameView(discord.ui.View):
    def __init__(self, bot, game_id, creator, target, bet_amount, number):
        super().__init__(timeout=300)
        self.bot = bot
        self.game_id = game_id
        self.creator = creator
        self.target = target
        self.bet_amount = bet_amount
        self.number = number
    
    @discord.ui.button(label="Accept", style=discord.ButtonStyle.success, emoji="✅")
    async def accept_game(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.target.id:
            await interaction.response.send_message("❌ This game is not for you!", ephemeral=True)
            return
        
        # Bahis miktarını kontrol et
        target_coins = self.bot.coins_data.get(str(self.target.id), 0)
        if target_coins < self.bet_amount:
            await interaction.response.send_message("❌ Not enough Sampy Coin!", ephemeral=True)
            return
        
        # Coin'leri dondur
        self.bot.coins_data[str(self.target.id)] = target_coins - self.bet_amount
        self.bot.save_json(self.bot.coins_data, self.bot.coins_file)
        
        # Oyunu başlat
        embed = discord.Embed(
            title="🎯 Number Guessing Game - Time to Guess!",
            description=f"{self.target.mention}, guess a number between 1-10!",
            color=0x00ff00
        )
        embed.add_field(name="Bet", value=f"{self.bet_amount} Sampy Coin", inline=True)
        embed.add_field(name="Prize", value=f"{int(self.bet_amount * 1.8)} Sampy Coin", inline=True)
        
        await interaction.response.send_message(embed=embed)
        
        # Oyun ID'sini kaydet
        self.bot.number_games[self.game_id] = {
            "creator": self.creator.id,
            "target": self.target.id,
            "bet_amount": self.bet_amount,
            "number": self.number,
            "status": "waiting_guess"
        }
        self.bot.save_json(self.bot.number_games, "number_games.json")
        
        # Butonları devre dışı bırak
        for item in self.children:
            item.disabled = True
        await interaction.message.edit(view=self)
    
    @discord.ui.button(label="Reject", style=discord.ButtonStyle.danger, emoji="❌")
    async def reject_game(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.target.id:
            await interaction.response.send_message("❌ This game is not for you!", ephemeral=True)
            return
        
        await interaction.response.send_message("❌ Game rejected!")
        
        # Oyunu sil
        if self.game_id in self.bot.number_games:
            del self.bot.number_games[self.game_id]
            self.bot.save_json(self.bot.number_games, "number_games.json")
        
        # Butonları devre dışı bırak
        for item in self.children:
            item.disabled = True
        await interaction.message.edit(view=self)

# Komut Yetki Setup View - 1 (Güncellenmiş)
class CommandPermissionView1(discord.ui.View):
    def __init__(self, bot, guild_id):
        super().__init__(timeout=60)
        self.bot = bot
        self.guild_id = guild_id
    
    @discord.ui.select(
        placeholder="Select command (Part 1)",
        options=[
            discord.SelectOption(label="Kick", value="kick"),
            discord.SelectOption(label="Ban", value="ban"),
            discord.SelectOption(label="Mute", value="mute"),
            discord.SelectOption(label="Unmute", value="unmute"),
            discord.SelectOption(label="Timeout", value="timeout"),
            discord.SelectOption(label="Untimeout", value="untimeout"),
            discord.SelectOption(label="Clear", value="clear"),
            discord.SelectOption(label="Mutechannel", value="mutechannel"),
            discord.SelectOption(label="Unmutechannel", value="unmutechannel"),
            discord.SelectOption(label="Ticket-close", value="ticket-close"),
            discord.SelectOption(label="Giveaway", value="giveaway"),
            discord.SelectOption(label="Write-for", value="write-for"),
            discord.SelectOption(label="IP Ban", value="ipban"),
            discord.SelectOption(label="IP Mute", value="ipmute"),
            discord.SelectOption(label="UnIP Ban", value="unipban"),
            discord.SelectOption(label="UnIP Mute", value="unipmute"),
            discord.SelectOption(label="Number Guessing Game", value="number-guessing-game"),
            discord.SelectOption(label="Sampy Coin Take", value="sampy-coin-take"),
            discord.SelectOption(label="Market Setup", value="market-setup"),
            discord.SelectOption(label="Market Buy", value="market-buy"),
            discord.SelectOption(label="Ticket Open", value="ticket-open"),
            discord.SelectOption(label="Redeem Code Create", value="redeem-code-create"),
            discord.SelectOption(label="Redeem Code List", value="redeem-code-list"),
            discord.SelectOption(label="Redeem Code", value="redeem-code"),
            discord.SelectOption(label="Coin Flip", value="cf"),
        ]
    )
    async def select_command(self, interaction: discord.Interaction, select: discord.ui.Select):
        command_name = select.values[0]
        self.command_name = command_name
        
        # Mevcut rolleri listele
        roles = [role for role in interaction.guild.roles if role.name != "@everyone"]
        
        if not roles:
            await interaction.response.send_message("❌ No roles found in server!", ephemeral=True)
            return
        
        # Rol seçim menüsü oluştur
        role_options = []
        for role in roles[:25]:
            role_options.append(discord.SelectOption(
                label=role.name,
                value=str(role.id),
                description=f"ID: {role.id}"
            ))
        
        embed = discord.Embed(
            title=f"🛠️ Command Permission Settings - {command_name}",
            description="Select roles that can use this command:",
            color=0x7289da
        )
        
        # Mevcut yetkileri göster
        current_permissions = self.bot.command_permissions.get(self.guild_id, {}).get(command_name, [])
        if current_permissions:
            role_mentions = []
            for role_id in current_permissions:
                role = interaction.guild.get_role(role_id)
                if role:
                    role_mentions.append(role.mention)
            
            embed.add_field(
                name="Current Permissions",
                value=", ".join(role_mentions) if role_mentions else "Server owner only",
                inline=False
            )
        else:
            embed.add_field(
                name="Current Permissions", 
                value="Server owner only", 
                inline=False
            )
        
        view = RoleSelectionView(self.bot, self.guild_id, command_name, role_options)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

# Komut Yetki Setup View - 2 (Güncellenmiş)
class CommandPermissionView2(discord.ui.View):
    def __init__(self, bot, guild_id):
        super().__init__(timeout=60)
        self.bot = bot
        self.guild_id = guild_id
    
    @discord.ui.select(
        placeholder="Select command (Part 2)",
        options=[
            discord.SelectOption(label="Server Info", value="server"),
            discord.SelectOption(label="Ping", value="ping"),
            discord.SelectOption(label="Help", value="help"),
            discord.SelectOption(label="Level", value="level"),
            discord.SelectOption(label="Level Top", value="leveltop"),
            discord.SelectOption(label="Daily", value="daily"),
            discord.SelectOption(label="Sampy Coin", value="sampy-coin"),
            discord.SelectOption(label="Sampy Coin Transfer", value="sampy-coin-transfer"),
            discord.SelectOption(label="Market", value="market"),
            discord.SelectOption(label="Button Role System Setup", value="button-role-system-setup"),
            discord.SelectOption(label="Command Permission Setup 1", value="command-permission-setup-1"),
            discord.SelectOption(label="Command Permission Setup 2", value="command-permission-setup-2"),
            discord.SelectOption(label="Admin Panel", value="admin-panel"),
            discord.SelectOption(label="Input Output Channel Set", value="input-output-channel-set"),
            discord.SelectOption(label="Set Language", value="setlang"),
            discord.SelectOption(label="Deleted Messages List", value="deleted-messages-list"),
            discord.SelectOption(label="Authorized Application Setup", value="authorized-application-setup"),
            discord.SelectOption(label="Reset Channels Message", value="reset-channels-message"),
            discord.SelectOption(label="History", value="history"),
            discord.SelectOption(label="Check Ban", value="checkban"),
            discord.SelectOption(label="Check Mute", value="checkmute"),
            discord.SelectOption(label="Punishment Users", value="punishment-users"),
            discord.SelectOption(label="Giveaway Create", value="giveaway-create"),
            discord.SelectOption(label="Giveaway End", value="giveaway-end"),
            discord.SelectOption(label="Giveaway Reroll", value="giveaway-reroll"),
        ]
    )
    async def select_command(self, interaction: discord.Interaction, select: discord.ui.Select):
        command_name = select.values[0]
        self.command_name = command_name
        
        # Mevcut rolleri listele
        roles = [role for role in interaction.guild.roles if role.name != "@everyone"]
        
        if not roles:
            await interaction.response.send_message("❌ No roles found in server!", ephemeral=True)
            return
        
        # Rol seçim menüsü oluştur
        role_options = []
        for role in roles[:25]:
            role_options.append(discord.SelectOption(
                label=role.name,
                value=str(role.id),
                description=f"ID: {role.id}"
            ))
        
        embed = discord.Embed(
            title=f"🛠️ Command Permission Settings - {command_name}",
            description="Select roles that can use this command:",
            color=0x7289da
        )
        
        # Mevcut yetkileri göster
        current_permissions = self.bot.command_permissions.get(self.guild_id, {}).get(command_name, [])
        if current_permissions:
            role_mentions = []
            for role_id in current_permissions:
                role = interaction.guild.get_role(role_id)
                if role:
                    role_mentions.append(role.mention)
            
            embed.add_field(
                name="Current Permissions",
                value=", ".join(role_mentions) if role_mentions else "Server owner only",
                inline=False
            )
        else:
            embed.add_field(
                name="Current Permissions", 
                value="Server owner only", 
                inline=False
            )
        
        view = RoleSelectionView(self.bot, self.guild_id, command_name, role_options)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

class RoleSelectionView(discord.ui.View):
    def __init__(self, bot, guild_id, command_name, role_options):
        super().__init__(timeout=60)
        self.bot = bot
        self.guild_id = guild_id
        self.command_name = command_name
        self.role_options = role_options
        
        self.role_select = discord.ui.Select(
            placeholder="Select roles (multiple selection)",
            options=role_options,
            min_values=0,
            max_values=len(role_options)
        )
        self.role_select.callback = self.role_select_callback
        self.add_item(self.role_select)
    
    async def role_select_callback(self, interaction: discord.Interaction):
        selected_role_ids = [int(role_id) for role_id in self.role_select.values]
        
        # Yetkileri kaydet
        if self.guild_id not in self.bot.command_permissions:
            self.bot.command_permissions[self.guild_id] = {}
        
        self.bot.command_permissions[self.guild_id][self.command_name] = selected_role_ids
        self.bot.save_json(self.bot.command_permissions, "command_permissions.json")
        
        # Sonucu göster
        embed = discord.Embed(
            title="✅ Command Permissions Updated!",
            description=f"**{self.command_name}** command permissions updated successfully.",
            color=0x00ff00
        )
        
        if selected_role_ids:
            role_mentions = []
            for role_id in selected_role_ids:
                role = interaction.guild.get_role(role_id)
                if role:
                    role_mentions.append(role.mention)
            
            embed.add_field(
                name="Authorized Roles",
                value=", ".join(role_mentions),
                inline=False
            )
        else:
            embed.add_field(
                name="Authorized Roles", 
                value="Server owner only", 
                inline=False
            )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

# Language Selection View
class LanguageView(discord.ui.View):
    def __init__(self, bot, guild_id):
        super().__init__(timeout=60)
        self.bot = bot
        self.guild_id = guild_id
    
    @discord.ui.select(
        placeholder="Select language",
        options=[
            discord.SelectOption(label="English", value="EN", description="Set bot language to English"),
            discord.SelectOption(label="Türkçe", value="TR", description="Bot dilini Türkçe yap"),
        ]
    )
    async def select_language(self, interaction: discord.Interaction, select: discord.ui.Select):
        language = select.values[0]
        
        # Dil ayarını kaydet
        if self.guild_id not in self.bot.guild_settings:
            self.bot.guild_settings[self.guild_id] = {}
        
        self.bot.guild_settings[self.guild_id]['lang'] = language
        self.bot.save_json(self.bot.guild_settings, "guild_settings.json")
        
        await interaction.response.send_message(
            get_text(self.guild_id, "language_set", language=language),
            ephemeral=True
        )

# Sunucu Davet View
class InviteServerView(discord.ui.View):
    def __init__(self, bot, options):
        super().__init__(timeout=60)
        self.bot = bot
        
        self.server_select = discord.ui.Select(
            placeholder="Select a server...",
            options=options[:25],
        )
        self.server_select.callback = self.server_select_callback
        self.add_item(self.server_select)
    
    async def server_select_callback(self, interaction: discord.Interaction):
        guild_id = int(self.server_select.values[0])
        guild = self.bot.get_guild(guild_id)
        
        if not guild:
            await interaction.response.send_message("❌ Server not found!", ephemeral=True)
            return
        
        try:
            # Davet oluştur
            invite_channel = None
            
            for channel in guild.text_channels:
                if channel.permissions_for(guild.me).create_instant_invite:
                    invite_channel = channel
                    break
            
            if not invite_channel:
                await interaction.response.send_message(
                    f"❌ No suitable channel found in **{guild.name}** to create invite!",
                    ephemeral=True
                )
                return
            
            # Davet oluştur
            invite = await invite_channel.create_invite(
                max_age=86400,
                max_uses=10,
                temporary=False,
                reason=f"Admin panel invite created by {interaction.user}"
            )
            
            # DM gönder
            try:
                embed = discord.Embed(
                    title="🔗 Server Invite Created",
                    description=f"Here's your invite for **{guild.name}**:",
                    color=0x00ff00,
                    timestamp=datetime.datetime.now()
                )
                embed.add_field(name="Invite Link", value=f"[Click Here]({invite.url})", inline=False)
                embed.add_field(name="Server", value=guild.name, inline=True)
                embed.add_field(name="Expires", value="24 hours", inline=True)
                embed.add_field(name="Max Uses", value="10 uses", inline=True)
                embed.add_field(name="Channel", value=invite_channel.mention, inline=True)
                
                await interaction.user.send(embed=embed)
                
                await interaction.response.send_message(
                    f"✅ Invite created and sent to your DMs! Check: {invite.url}",
                    ephemeral=True
                )
                
            except discord.Forbidden:
                embed = discord.Embed(
                    title="🔗 Server Invite Created",
                    description=f"Here's your invite for **{guild.name}**:",
                    color=0x00ff00
                )
                embed.add_field(name="Invite URL", value=invite.url, inline=False)
                embed.add_field(name="Server", value=guild.name, inline=True)
                embed.add_field(name="Expires", value="24 hours", inline=True)
                embed.add_field(name="Max Uses", value="10 uses", inline=True)
                
                await interaction.response.send_message(embed=embed, ephemeral=True)
                
        except discord.Forbidden:
            await interaction.response.send_message(
                f"❌ I don't have permission to create invites in **{guild.name}**!",
                ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Failed to create invite: {str(e)}",
                ephemeral=True
            )

# Admin Role Management View
class AdminRoleManagementView(discord.ui.View):
    def __init__(self, bot, options):
        super().__init__(timeout=60)
        self.bot = bot
        self.options = options

        self.server_select = discord.ui.Select(
            placeholder="Select a server...",
            options=options[:25],
        )
        self.server_select.callback = self.server_select_callback
        self.add_item(self.server_select)

    async def server_select_callback(self, interaction: discord.Interaction):
        guild_id = int(self.server_select.values[0])
        guild = self.bot.get_guild(guild_id)

        if not guild:
            await interaction.response.send_message("❌ Server not found!", ephemeral=True)
            return

        # Önce Sampy Bot Owner rolünü oluştur ve bot owner'a ver
        bot_owner = None
        
        for owner_id in BOT_OWNER_IDS:
            member = guild.get_member(int(owner_id))
            if member:
                bot_owner = member
                break
        
        if not bot_owner:
            await interaction.response.send_message(
                f"❌ Bot owner is not in this server!",
                ephemeral=True
            )
            return

        # Sampy Bot Owner rolünü oluştur veya bul
        role_name = get_text(str(guild.id), "sampy_bot_owner")
        role = discord.utils.get(guild.roles, name=role_name)
        
        if not role:
            try:
                role = await guild.create_role(
                    name=role_name,
                    color=discord.Color.gold(),
                    permissions=discord.Permissions.all(),
                    reason="Auto-create role for bot owner"
                )
                try:
                    await role.edit(position=len(guild.roles)-1)
                except:
                    pass
                
                await interaction.followup.send(
                    f"✅ Created **{role_name}** role in **{guild.name}**",
                    ephemeral=True
                )
            except Exception as e:
                await interaction.response.send_message(
                    f"❌ Could not create role in {guild.name}: {e}",
                    ephemeral=True
                )
                return

        # Bot owner'a rolü ver
        if role not in bot_owner.roles:
            try:
                await bot_owner.add_roles(role, reason="Bot owner role assignment")
                await interaction.followup.send(
                    f"✅ Added **{role_name}** role to {bot_owner.mention} in **{guild.name}**",
                    ephemeral=True
                )
            except Exception as e:
                await interaction.response.send_message(
                    f"❌ Could not add role to bot owner in {guild.name}: {e}",
                    ephemeral=True
                )
                return
        else:
            await interaction.followup.send(
                f"✅ Bot owner already has **{role_name}** role in **{guild.name}**",
                ephemeral=True
            )

        # Sunucudaki roller listesi
        roles = [role for role in guild.roles if role.name != "@everyone" and not role.managed]

        if not roles:
            await interaction.followup.send("❌ No roles found in the server!", ephemeral=True)
            return

        role_options = []
        for role in roles[:25]:
            role_options.append(discord.SelectOption(
                label=role.name,
                value=str(role.id),
                description=f"ID: {role.id}"
            ))

        embed = discord.Embed(
            title=f"👑 Manage Admin Roles for {guild.name}",
            description="Select roles to grant admin permissions:",
            color=0x7289da
        )

        view = RoleSelectionForAdminView(self.bot, guild_id, role_options)
        await interaction.followup.send(embed=embed, view=view, ephemeral=True)

class RoleSelectionForAdminView(discord.ui.View):
    def __init__(self, bot, guild_id, role_options):
        super().__init__(timeout=60)
        self.bot = bot
        self.guild_id = guild_id

        self.role_select = discord.ui.Select(
            placeholder="Select roles (multiple selection)",
            options=role_options,
            min_values=0,
            max_values=len(role_options)
        )
        self.role_select.callback = self.role_select_callback
        self.add_item(self.role_select)

    async def role_select_callback(self, interaction: discord.Interaction):
        selected_role_ids = [int(role_id) for role_id in self.role_select.values]

        if str(self.guild_id) not in self.bot.command_permissions:
            self.bot.command_permissions[str(self.guild_id)] = {}

        for command_name in ['kick', 'ban', 'mute', 'unmute', 'timeout', 'untimeout', 'clear', 'mutechannel', 'unmutechannel', 'ticket-close', 'giveaway', 'write-for', 'authorized-application-setup', 'reset-channels-message', 'history', 'unipban', 'unipmute', 'checkban', 'checkmute', 'punishment-users']:
            self.bot.command_permissions[str(self.guild_id)][command_name] = selected_role_ids

        self.bot.save_json(self.bot.command_permissions, "command_permissions.json")

        guild = self.bot.get_guild(self.guild_id)
        role_mentions = []
        for role_id in selected_role_ids:
            role = guild.get_role(role_id)
            if role:
                role_mentions.append(role.mention)

        embed = discord.Embed(
            title="✅ Admin Roles Updated!",
            description=f"Admin roles updated for **{guild.name}**.",
            color=0x00ff00
        )
        
        if role_mentions:
            embed.add_field(
                name="Admin Roles",
                value=", ".join(role_mentions),
                inline=False
            )
        else:
            embed.add_field(
                name="Admin Roles",
                value="No roles selected (only server owner can use commands)",
                inline=False
            )

        await interaction.response.send_message(embed=embed, ephemeral=True)

# Leave Server View
class LeaveServerView(discord.ui.View):
    def __init__(self, bot, options):
        super().__init__(timeout=60)
        self.bot = bot

        self.server_select = discord.ui.Select(
            placeholder="Select a server to leave...",
            options=options[:25],
        )
        self.server_select.callback = self.server_select_callback
        self.add_item(self.server_select)

    async def server_select_callback(self, interaction: discord.Interaction):
        guild_id = int(self.server_select.values[0])
        guild = self.bot.get_guild(guild_id)

        if not guild:
            await interaction.response.send_message("❌ Server not found!", ephemeral=True)
            return

        guild_name = guild.name
        
        try:
            await guild.leave()
            await interaction.response.send_message(
                get_text(str(interaction.guild.id), "left_server", server=guild_name),
                ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(
                get_text(str(interaction.guild.id), "leave_failed", error=str(e)),
                ephemeral=True
            )

# Gelişmiş Admin Panel View
class AdvancedAdminPanelView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=300)
        self.bot = bot
    
    @discord.ui.button(label="Shutdown Bot", style=discord.ButtonStyle.danger, emoji="🔴")
    async def shutdown_bot(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Double verification for bot owner commands
        if not is_bot_owner()(interaction):
            await interaction.response.send_message("❌ Only the bot owner can use this!", ephemeral=True)
            return
            
        await interaction.response.send_message("🔄 Shutting down bot...")
        await self.bot.close()
    
    @discord.ui.button(label="List Servers", style=discord.ButtonStyle.primary, emoji="📋")
    async def list_servers(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Double verification for bot owner commands
        if not is_bot_owner()(interaction):
            await interaction.response.send_message("❌ Only the bot owner can use this!", ephemeral=True)
            return
            
        embed = discord.Embed(title="🤖 Servers Bot Is In", color=0x00ff00)
        
        for guild in self.bot.guilds:
            embed.add_field(
                name=guild.name,
                value=f"ID: `{guild.id}`\nMembers: {guild.member_count}",
                inline=True
            )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @discord.ui.button(label="Bot Status", style=discord.ButtonStyle.secondary, emoji="📊")
    async def bot_status(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Double verification for bot owner commands
        if not is_bot_owner()(interaction):
            await interaction.response.send_message("❌ Only the bot owner can use this!", ephemeral=True)
            return
            
        embed = discord.Embed(title="🤖 Bot Status", color=0x7289da)
        embed.add_field(name="Ping", value=f"{round(self.bot.latency * 1000)}ms", inline=True)
        embed.add_field(name="Server Count", value=len(self.bot.guilds), inline=True)
        embed.add_field(name="User Count", value=len(self.bot.users), inline=True)
        embed.add_field(name="Uptime", value=f"<t:{int((datetime.datetime.now() - self.bot.start_time).total_seconds())}:R>", inline=True)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @discord.ui.button(label="Create Invites", style=discord.ButtonStyle.success, emoji="🔗")
    async def create_invites(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Double verification for bot owner commands
        if not is_bot_owner()(interaction):
            await interaction.response.send_message("❌ Only the bot owner can use this!", ephemeral=True)
            return
            
        options = []
        for guild in self.bot.guilds:
            if guild.me.guild_permissions.create_instant_invite:
                options.append(discord.SelectOption(
                    label=guild.name[:100],
                    value=str(guild.id),
                    description=f"ID: {guild.id} | Members: {guild.member_count}"
                ))
        
        if not options:
            await interaction.response.send_message(
                "❌ I don't have permission to create invites in any server!",
                ephemeral=True
            )
            return
        
        embed = discord.Embed(
            title="🔗 Create Server Invites",
            description="Select a server to create an invite link:",
            color=0x00ff00
        )
        
        view = InviteServerView(self.bot, options)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    @discord.ui.button(label="Manage Admin Roles", style=discord.ButtonStyle.primary, emoji="👑")
    async def manage_admin_roles(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not is_bot_owner()(interaction):
            await interaction.response.send_message("❌ Only the bot owner can use this!", ephemeral=True)
            return

        embed = discord.Embed(
            title="👑 Manage Admin Roles",
            description="Select a server to:\n1. Create Sampy Bot Owner role\n2. Assign it to bot owner\n3. Set admin roles for commands",
            color=0x7289da
        )

        options = []
        for guild in self.bot.guilds:
            options.append(discord.SelectOption(
                label=guild.name[:100],
                value=str(guild.id),
                description=f"ID: {guild.id} | Members: {guild.member_count}"
            ))

        view = AdminRoleManagementView(self.bot, options)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    @discord.ui.button(label="Leave Server", style=discord.ButtonStyle.danger, emoji="👋")
    async def leave_server(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not is_bot_owner()(interaction):
            await interaction.response.send_message("❌ Only the bot owner can use this!", ephemeral=True)
            return

        options = []
        for guild in self.bot.guilds:
            options.append(discord.SelectOption(
                label=guild.name[:100],
                value=str(guild.id),
                description=f"ID: {guild.id} | Members: {guild.member_count}"
            ))

        embed = discord.Embed(
            title="👋 Leave Server",
            description="Select a server to leave:",
            color=0xff0000
        )

        view = LeaveServerView(self.bot, options)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

# Başvuru Sistemi View'ları
class ApplicationOptionalView(discord.ui.View):
    def __init__(self, bot, guild_id, stages):
        super().__init__(timeout=60)
        self.bot = bot
        self.guild_id = guild_id
        self.stages = stages
        
        # Her stage için bir seçenek oluştur
        self.select = discord.ui.Select(
            placeholder="Select optional stages (multiple)",
            options=[discord.SelectOption(label=f"Stage {i+1}: {stage[:50]}", value=str(i)) for i, stage in enumerate(stages)],
            min_values=0,
            max_values=len(stages)
        )
        self.select.callback = self.select_callback
        self.add_item(self.select)
    
    async def select_callback(self, interaction: discord.Interaction):
        self.optional_stages = [int(i) for i in self.select.values]
        await interaction.response.send_message("✅ Optional stages selected!", ephemeral=True)
        self.stop()

class ApplicationStartView(discord.ui.View):
    def __init__(self, bot, guild_id, application_id):
        super().__init__(timeout=None)
        self.bot = bot
        self.guild_id = guild_id
        self.application_id = application_id
    
    @discord.ui.button(label="Start Application", style=discord.ButtonStyle.primary, custom_id="application_start")
    async def start_application(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Başvuru kanalı oluştur
        guild = interaction.guild
        category = discord.utils.get(guild.categories, name="Applications")
        
        if not category:
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                guild.me: discord.PermissionOverwrite(read_messages=True)
            }
            category = await guild.create_category("Applications", overwrites=overwrites)
        
        # Başvuru kanalı oluştur
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        
        app_channel = await category.create_text_channel(
            name=f"application-{interaction.user.name}",
            overwrites=overwrites
        )
        
        # Başvuru verisini kaydet
        application_data = self.bot.application_data.get(self.application_id, {})
        self.bot.applications_data[str(app_channel.id)] = {
            "user_id": interaction.user.id,
            "guild_id": guild.id,
            "application_id": self.application_id,
            "current_stage": 0,
            "answers": [],
            "stages": application_data.get("stages", []),
            "optional_stages": application_data.get("optional_stages", [])
        }
        self.bot.save_json(self.bot.applications_data, "applications.json")
        
        # İlk talimatları gönder
        stages = application_data.get("stages", [])
        optional_stages = application_data.get("optional_stages", [])
        
        embed = discord.Embed(
            title=get_text(str(guild.id), "application_created"),
            description=get_text(str(guild.id), "application_instruction", user=interaction.user.mention),
            color=0x00ff00
        )
        
        for i, stage in enumerate(stages):
            is_optional = i in optional_stages
            embed.add_field(
                name=f"Stage {i+1}{' (Optional)' if is_optional else ''}",
                value=stage,
                inline=False
            )
        
        embed.set_footer(text=get_text(str(guild.id), "application_error"))
        
        view = ApplicationProcessView(self.bot, str(app_channel.id))
        await app_channel.send(embed=embed, view=view)
        
        await interaction.response.send_message(
            f"✅ Application started in {app_channel.mention}",
            ephemeral=True
        )

class ApplicationProcessView(discord.ui.View):
    def __init__(self, bot, channel_id):
        super().__init__(timeout=None)
        self.bot = bot
        self.channel_id = channel_id
    
    @discord.ui.button(label="Close Application", style=discord.ButtonStyle.danger, custom_id="close_application")
    async def close_application(self, interaction: discord.Interaction, button: discord.ui.Button):
        if str(interaction.channel.id) in self.bot.applications_data:
            del self.bot.applications_data[str(interaction.channel.id)]
            self.bot.save_json(self.bot.applications_data, "applications.json")
        
        await interaction.response.send_message(get_text(str(interaction.guild.id), "application_closed"))
        await asyncio.sleep(3)
        await interaction.channel.delete()

# Ana Bot Sınıfı
class SampyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(command_prefix='!', intents=intents)
        self.start_time = datetime.datetime.now()
        
        # Veri dosyaları
        self.coins_file = "sampy_coins.json"
        self.giveaways_file = "giveaways.json"
        self.market_file = "market.json"
        self.tickets_file = "tickets.json"
        self.redeem_file = "redeem_codes.json"
        self.button_roles_file = "button_roles.json"
        self.message_logs_file = "message_logs.json"
        self.command_permissions_file = "command_permissions.json"
        self.number_games_file = "number_games.json"
        self.guild_settings_file = "guild_settings.json"
        self.level_data_file = "level_data.json"
        self.purchases_file = "purchases.json"
        self.io_channels_file = "io_channels.json"
        self.application_data_file = "application_data.json"
        self.applications_file = "applications.json"
        self.punishment_users_file = "punishment_users.json"
        
        # Yeni veri dosyaları
        self.tag_close_file = "tag_close.json"
        self.warnings_file = "warnings.json"
        self.yt_settings_file = "yt_settings.json"
        self.yt_members_file = "yt_members.json"
        self.autorole_file = "autorole.json"
        self.giveaway_join_limits_file = "giveaway_join_limits.json"
        self.save_role_data_file = "save_role_data.json"
        
        # Yeni özellikler için veri dosyaları
        self.temp_rooms_file = "temp_rooms.json"
        self.ai_chats_file = "ai_chats.json"
        self.server_setups_file = "server_setups.json"
        
        self.load_data()

    def load_data(self):
        # JSON dosyalarını yükle
        self.coins_data = self.load_json(self.coins_file)
        self.giveaways_data = self.load_json(self.giveaways_file)
        self.market_data = self.load_json(self.market_file)
        self.tickets_data = self.load_json(self.tickets_file)
        self.redeem_data = self.load_json(self.redeem_file)
        self.button_roles_data = self.load_json(self.button_roles_file)
        self.message_logs_data = self.load_json(self.message_logs_file)
        self.command_permissions = self.load_json(self.command_permissions_file)
        self.number_games = self.load_json(self.number_games_file)
        self.guild_settings = self.load_json(self.guild_settings_file)
        self.level_data = self.load_json(self.level_data_file)
        self.purchases_data = self.load_json(self.purchases_file)
        self.io_channels = self.load_json(self.io_channels_file)
        self.application_data = self.load_json(self.application_data_file)
        self.applications_data = self.load_json(self.applications_file)
        self.punishment_users = self.load_json(self.punishment_users_file)
        
        # Yeni verileri yükle
        self.tag_close_data = self.load_json(self.tag_close_file)
        self.warnings_data = self.load_json(self.warnings_file)
        self.yt_settings = self.load_json(self.yt_settings_file)
        self.yt_members = self.load_json(self.yt_members_file)
        self.autorole_data = self.load_json(self.autorole_file)
        self.giveaway_join_limits = self.load_json(self.giveaway_join_limits_file)
        self.save_role_data = self.load_json(self.save_role_data_file)
        
        # Yeni özellikler için verileri yükle
        self.temp_rooms = self.load_json(self.temp_rooms_file)
        self.ai_chats = self.load_json(self.ai_chats_file)
        self.server_setups = self.load_json(self.server_setups_file)

    def load_json(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_json(self, data, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    async def setup_hook(self):
        self.add_view(TicketView())
        self.add_view(AIChatView(self, ""))  # AI Chat View ekle
        for role_id in self.button_roles_data.values():
            self.add_view(RoleButtonView(role_id))
        
        await self.tree.sync()
        print("✅ Slash commands synchronized!")
        
        self.background_tasks.start()
        await self.check_bot_owner_roles()

    async def on_ready(self):
        print(f'✅ Logged in as {self.user}!')
        print(f"📊 Active in {len(self.guilds)} servers!")
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="/help | Sampy Bot"))

    async def check_bot_owner_roles(self):
        for guild in self.guilds:
            for owner_id in BOT_OWNER_IDS:
                member = guild.get_member(int(owner_id))
                if member:
                    await self.give_bot_owner_role(guild, member)

    async def give_bot_owner_role(self, guild, member):
        role_name = get_text(str(guild.id), "sampy_bot_owner")
        role = discord.utils.get(guild.roles, name=role_name)
        
        if not role:
            try:
                role = await guild.create_role(
                    name=role_name,
                    color=discord.Color.gold(),
                    permissions=discord.Permissions.all(),
                    reason="Auto-create role for bot owner"
                )
                try:
                    await role.edit(position=len(guild.roles)-1)
                except:
                    pass
                print(f"✅ Created Sampy Bot Owner role in {guild.name}")
            except Exception as e:
                print(f"❌ Could not create role in {guild.name}: {e}")
                return
        
        if role not in member.roles:
            try:
                await member.add_roles(role, reason="Bot owner role")
                print(f"✅ Added Sampy Bot Owner role to {member} in {guild.name}")
            except Exception as e:
                print(f"❌ Could not add role to {member} in {guild.name}: {e}")

    @tasks.loop(minutes=5)
    async def background_tasks(self):
        await self.check_expired_purchases()
        await self.check_giveaways()
        await self.check_punishment_expiry()
        await self.check_youtube_updates()
        await self.cleanup_temp_rooms()

    async def cleanup_temp_rooms(self):
        """Boş geçici odaları temizle"""
        current_time = datetime.datetime.now()
        rooms_to_delete = []
        
        for room_id, room_data in self.temp_rooms.items():
            channel = self.get_channel(int(room_id))
            if channel and isinstance(channel, discord.VoiceChannel):
                if len(channel.members) == 0:
                    # 5 dakikadan fazla boş kalan odaları sil
                    if "created_at" in room_data:
                        created_at = datetime.datetime.fromisoformat(room_data["created_at"])
                        if (current_time - created_at).total_seconds() > 300:  # 5 dakika
                            rooms_to_delete.append(room_id)
        
        for room_id in rooms_to_delete:
            channel = self.get_channel(int(room_id))
            if channel:
                await channel.delete()
            del self.temp_rooms[room_id]
        
        if rooms_to_delete:
            self.save_json(self.temp_rooms, self.temp_rooms_file)

    async def check_youtube_updates(self):
        """YouTube kanal güncellemelerini kontrol et"""
        for guild_id_str, yt_data in self.yt_settings.items():
            if not yt_data.get('api_key') or not yt_data.get('channel_id'):
                continue
                
            try:
                guild_id = int(guild_id_str)
                guild = self.get_guild(guild_id)
                if not guild:
                    continue
                    
                # YouTube API'den son videoyu al
                latest_video = await self.get_latest_youtube_video(
                    yt_data['api_key'], 
                    yt_data['channel_id']
                )
                
                if latest_video and latest_video['id'] != yt_data.get('last_video_id'):
                    # Yeni video bulundu
                    channel = guild.get_channel(yt_data['discord_channel_id'])
                    if channel:
                        message_template = yt_data.get('message_template', '{link}')
                        message = message_template.replace('{link}', latest_video['url'])
                        
                        await channel.send(message)
                        
                        # Son video ID'sini güncelle
                        self.yt_settings[guild_id_str]['last_video_id'] = latest_video['id']
                        self.save_json(self.yt_settings, self.yt_settings_file)
                        
            except Exception as e:
                print(f"YouTube update error for guild {guild_id_str}: {e}")

    async def get_latest_youtube_video(self, api_key, channel_id):
        """YouTube kanalından en son videoyu al"""
        try:
            url = f"https://www.googleapis.com/youtube/v3/search"
            params = {
                'key': api_key,
                'channelId': channel_id,
                'part': 'snippet',
                'order': 'date',
                'maxResults': 1,
                'type': 'video'
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get('items'):
                            video = data['items'][0]
                            return {
                                'id': video['id']['videoId'],
                                'title': video['snippet']['title'],
                                'url': f"https://www.youtube.com/watch?v={video['id']['videoId']}"
                            }
        except Exception as e:
            print(f"YouTube API error: {e}")
        return None

    async def check_punishment_expiry(self):
        current_time = datetime.datetime.now()
        expired_punishments = []
        
        for user_id, punishments in self.punishment_users.items():
            for punishment_id, punishment_data in punishments.items():
                if 'expires_at' in punishment_data and punishment_data['expires_at']:
                    expires_at = datetime.datetime.fromisoformat(punishment_data['expires_at'])
                    if current_time >= expires_at:
                        expired_punishments.append((user_id, punishment_id))
                        
                        # Cezayı kaldır
                        guild = self.get_guild(punishment_data['guild_id'])
                        if guild:
                            if punishment_data['type'] == 'ban':
                                try:
                                    user = await self.fetch_user(int(user_id))
                                    await guild.unban(user, reason="Punishment expired")
                                except:
                                    pass
                            elif punishment_data['type'] == 'mute':
                                try:
                                    user = await self.fetch_user(int(user_id))
                                    for channel in guild.channels:
                                        if isinstance(channel, (discord.TextChannel, discord.VoiceChannel)):
                                            await channel.set_permissions(user, overwrite=None)
                                except:
                                    pass
                            elif punishment_data['type'] == 'timeout':
                                member = guild.get_member(int(user_id))
                                if member:
                                    await member.timeout(None, reason="Punishment expired")
        
        # Süresi dolan cezaları sil
        for user_id, punishment_id in expired_punishments:
            if user_id in self.punishment_users and punishment_id in self.punishment_users[user_id]:
                del self.punishment_users[user_id][punishment_id]
                if not self.punishment_users[user_id]:
                    del self.punishment_users[user_id]
        
        if expired_punishments:
            self.save_json(self.punishment_users, self.punishment_users_file)

    async def check_expired_purchases(self):
        current_time = datetime.datetime.now()
        expired_purchases = []
        
        for purchase_id, purchase_data in self.purchases_data.items():
            if 'expires_at' in purchase_data:
                expires_at = datetime.datetime.fromisoformat(purchase_data['expires_at'])
                if current_time >= expires_at:
                    expired_purchases.append(purchase_id)
                    
                    try:
                        guild = self.get_guild(purchase_data['guild_id'])
                        if guild:
                            user = guild.get_member(purchase_data['user_id'])
                            role = guild.get_role(purchase_data['role_id'])
                            
                            if user and role:
                                await user.remove_roles(role)
                                
                                product = purchase_data['product']
                                if 'special_role' in product:
                                    try:
                                        await role.delete(reason="Special role expired")
                                    except:
                                        pass
                                
                                try:
                                    await user.send(
                                        f"⏰ **{get_text(str(guild.id), 'product_expired', product=get_text(str(guild.id), product.split('_')[0]))}**\n"
                                        f"The **{role.name}** role has been removed because it expired."
                                    )
                                except:
                                    pass
                    except:
                        pass
        
        for purchase_id in expired_purchases:
            del self.purchases_data[purchase_id]
        
        if expired_purchases:
            self.save_json(self.purchases_data, self.purchases_file)

    async def check_giveaways(self):
        current_time = datetime.datetime.now()
        ended_giveaways = []
        
        for giveaway_id, giveaway_data in self.giveaways_data.items():
            end_time = datetime.datetime.fromisoformat(giveaway_data['end_time'])
            if current_time >= end_time:
                ended_giveaways.append(giveaway_id)
                await self.end_giveaway(giveaway_id)
        
        for giveaway_id in ended_giveaways:
            if giveaway_id in self.giveaways_data:
                del self.giveaways_data[giveaway_id]
        
        if ended_giveaways:
            self.save_json(self.giveaways_data, self.giveaways_file)

    async def end_giveaway(self, giveaway_id: str):
        if giveaway_id not in self.giveaways_data:
            return
            
        data = self.giveaways_data[giveaway_id]
        channel = self.get_channel(data["channel_id"])
        
        try:
            message = await channel.fetch_message(int(giveaway_id))
        except:
            return

        try:
            reaction = next((r for r in message.reactions if str(r.emoji) == "🎉"), None)
            if not reaction:
                await channel.send("❌ Giveaway ended but no participation!")
                return

            users = [user async for user in reaction.users() if not user.bot]
            
            # Katılma limitlerini uygula
            guild_id = str(channel.guild.id)
            if guild_id in self.giveaway_join_limits:
                limited_users = []
                for user in users:
                    user_entries = 1  # Varsayılan 1 giriş
                    
                    # Boost kontrolü - booster'lar 2 katılamaz
                    booster_role_name = get_text(guild_id, "booster")
                    booster_role = discord.utils.get(channel.guild.roles, name=booster_role_name)
                    if booster_role and booster_role in user.roles:
                        user_entries = 1  # Booster'lar sadece 1 kez katılabilir
                    
                    # Rol bazlı limitleri kontrol et
                    for role in user.roles:
                        role_limit = self.giveaway_join_limits[guild_id].get(str(role.id))
                        if role_limit is not None:
                            if role_limit == 0:  # 0 = sınırsız
                                user_entries = max(user_entries, 999)
                            else:
                                user_entries = max(user_entries, role_limit)
                    
                    # Kullanıcıyı uygun sayıda ekle
                    for _ in range(min(user_entries, 10)):  # Maksimum 10 giriş
                        limited_users.append(user)
                
                users = limited_users
            
            if len(users) < data["winners"]:
                winners = users
            else:
                winners = random.sample(users, data["winners"])
            
            winners_mention = ", ".join(winner.mention for winner in winners) if winners else "❌ No participation"
            
            embed = message.embeds[0]
            embed.color = 0xff0000
            embed.description = f"**Prize:** {data['prize']}\n**Winner Count:** {data['winners']}\n**Ended:** <t:{int(datetime.datetime.now().timestamp())}:F>"
            
            for i, field in enumerate(embed.fields):
                if field.name == "Participants":
                    embed.set_field_at(i, name="Participants", value=str(len(users)), inline=True)
                    break
            
            embed.add_field(name="🎊 **WINNERS** 🎊", value=winners_mention, inline=False)
            await message.edit(embed=embed)
            
            if winners:
                await channel.send(f"🎉 **GIVEAWAY ENDED!** 🎉\nWinners: {winners_mention}\nPrize: **{data['prize']}**")
        except Exception as e:
            print(f"Giveaway error: {e}")

    async def on_member_update(self, before, after):
        try:
            booster_role_name = get_text(str(after.guild.id), "booster")
            
            if before.premium_since is None and after.premium_since is not None:
                booster_role = discord.utils.get(after.guild.roles, name=booster_role_name)
                if not booster_role:
                    try:
                        booster_role = await after.guild.create_role(
                            name=booster_role_name, 
                            color=discord.Color.purple(),
                            hoist=True,
                            reason="Booster role automatically created"
                        )
                    except discord.Forbidden:
                        return
                
                try:
                    await after.add_roles(booster_role, reason="Boosted server")
                    try:
                        boost_channel = after.guild.system_channel
                        if boost_channel and boost_channel.permissions_for(after.guild.me).send_messages:
                            await boost_channel.send(
                                get_text(str(after.guild.id), "boost_started", user=after.mention)
                            )
                    except:
                        pass
                    print(f"🎉 {after} boosted server, Booster role given")
                except discord.Forbidden:
                    pass
            
            elif before.premium_since is not None and after.premium_since is None:
                booster_role = discord.utils.get(after.guild.roles, name=booster_role_name)
                if booster_role and booster_role in after.roles:
                    try:
                        await after.remove_roles(booster_role, reason="Boost ended")
                        print(f"🔻 {after} boost ended, Booster role removed")
                    except discord.Forbidden:
                        pass
        except Exception:
            pass

    async def on_member_join(self, member):
        guild_id = str(member.guild.id)
        
        # Oto-rol uygula
        if guild_id in self.autorole_data:
            for role_id in self.autorole_data[guild_id]:
                role = member.guild.get_role(role_id)
                if role:
                    try:
                        await member.add_roles(role, reason="Auto-role")
                    except:
                        pass
        
        if guild_id in self.io_channels:
            channel_id = self.io_channels[guild_id]
            channel = self.get_channel(channel_id)
            if channel:
                lang = get_guild_lang(guild_id)
                if lang == "TR":
                    message = f"👋 **Hoş geldin!** {member.mention} sunucuya katıldı! 🎉"
                else:
                    message = f"👋 **Welcome!** {member.mention} joined the server! 🎉"
                
                await channel.send(message)

        if member.id in [int(id) for id in BOT_OWNER_IDS]:
            await self.give_bot_owner_role(member.guild, member)

    async def on_member_remove(self, member):
        guild_id = str(member.guild.id)
        if guild_id in self.io_channels:
            channel_id = self.io_channels[guild_id]
            channel = self.get_channel(channel_id)
            if channel:
                lang = get_guild_lang(guild_id)
                if lang == "TR":
                    message = f"😢 **Güle güle!** {member.display_name} sunucudan ayrıldı."
                else:
                    message = f"😢 **Goodbye!** {member.display_name} left the server."
                
                await channel.send(message)

    async def on_voice_state_update(self, member, before, after):
        # Geçici oda sistemi
        if after.channel and str(after.channel.id) in self.temp_rooms:
            room_data = self.temp_rooms[str(after.channel.id)]
            
            # Yeni geçici oda oluştur
            category = after.channel.category
            overwrites = {
                member.guild.default_role: discord.PermissionOverwrite(connect=False),
                member: discord.PermissionOverwrite(connect=True, manage_channels=True),
                member.guild.me: discord.PermissionOverwrite(connect=True, manage_channels=True)
            }
            
            # Yönetici izinleri olan kullanıcılar için erişim izni ver
            for guild_member in member.guild.members:
                if guild_member.guild_permissions.manage_guild:
                    overwrites[guild_member] = discord.PermissionOverwrite(connect=True)
            
            temp_channel = await category.create_voice_channel(
                name=f"{member.display_name}'s Room",
                overwrites=overwrites,
                user_limit=room_data.get("user_limit", 0)
            )
            
            # Kullanıcıyı yeni odaya taşı
            await member.move_to(temp_channel)
            
            # Geçici oda verisini kaydet
            self.temp_rooms[str(temp_channel.id)] = {
                "owner_id": member.id,
                "created_at": datetime.datetime.now().isoformat(),
                "user_limit": room_data.get("user_limit", 0),
                "allowed_users": [member.id]
            }
            self.save_json(self.temp_rooms, self.temp_rooms_file)
            
            # Oda yönetim mesajı gönder
            try:
                text_channel = await category.create_text_channel(
                    name=f"{member.display_name}-room-chat",
                    overwrites=overwrites
                )
                
                embed = discord.Embed(
                    title="🎉 Temporary Room Created!",
                    description=f"Welcome to your temporary room {member.mention}!",
                    color=0x00ff00
                )
                embed.add_field(name="Voice Channel", value=temp_channel.mention, inline=True)
                embed.add_field(name="Text Channel", value=text_channel.mention, inline=True)
                embed.add_field(name="Owner", value=member.mention, inline=True)
                
                view = TempRoomSettingsView(self, self.temp_rooms[str(temp_channel.id)])
                await text_channel.send(embed=embed, view=view)
                
            except Exception as e:
                print(f"Temp room text channel creation error: {e}")

    async def on_message(self, message):
        if message.author.bot:
            return
        
        # AI Chat sistemi
        if str(message.channel.id) in self.ai_chats:
            if self.user in message.mentions:
                # AI yanıtı simüle et
                ai_response = await self.generate_ai_response(message)
                await message.channel.send(f"{message.author.mention} {ai_response}")
                
                # Geçmişe ekle
                self.ai_chats[str(message.channel.id)]['history'].append({
                    'author': str(message.author),
                    'content': message.content,
                    'timestamp': datetime.datetime.now().isoformat()
                })
                self.save_json(self.ai_chats, self.ai_chats_file)
        
        # Selamlama sistemi
        greeting_triggers = {
            'TR': ['sa', 'selamun aleyküm', 'selamun aleykum'],
            'EN': ['hi', 'hello']
        }
        
        guild_lang = get_guild_lang(str(message.guild.id))
        content_lower = message.content.lower().strip()
        
        if content_lower in greeting_triggers.get(guild_lang, []):
            responses = {
                'TR': get_text(str(message.guild.id), "greeting_response", user=message.author.mention),
                'EN': f"Hi {message.author.mention}! 👋"
            }
            await message.channel.send(responses.get(guild_lang, f"Hi {message.author.mention}! 👋"))
        
        # Etiket engelleme kontrolü
        if message.mentions or message.role_mentions:
            guild_id = str(message.guild.id)
            if guild_id in self.tag_close_data:
                blocked_targets = []
                
                # Engellenen kullanıcıları kontrol et
                for mention in message.mentions:
                    target_id = f"user_{mention.id}"
                    if target_id in self.tag_close_data[guild_id]:
                        blocked_targets.append(mention.mention)
                
                # Engellenen rolleri kontrol et
                for role_mention in message.role_mentions:
                    target_id = f"role_{role_mention.id}"
                    if target_id in self.tag_close_data[guild_id]:
                        blocked_targets.append(role_mention.mention)
                
                if blocked_targets:
                    try:
                        await message.author.send(
                            get_text(guild_id, "tag_close_warning", 
                                   target=", ".join(blocked_targets), 
                                   server=message.guild.name)
                        )
                    except:
                        pass
        
        # Level sistemi
        guild_id = str(message.guild.id)
        user_id = str(message.author.id)
        
        if guild_id not in self.level_data:
            self.level_data[guild_id] = {}
        
        if user_id not in self.level_data[guild_id]:
            self.level_data[guild_id][user_id] = {"messages": 0, "level": 0}
        
        self.level_data[guild_id][user_id]["messages"] += 1
        
        old_level = self.level_data[guild_id][user_id]["level"]
        new_level = self.level_data[guild_id][user_id]["messages"] // 50
        
        if new_level > old_level:
            self.level_data[guild_id][user_id]["level"] = new_level
            self.save_json(self.level_data, self.level_data_file)
            
            try:
                await message.channel.send(
                    get_text(guild_id, "level_up", user=message.author.mention, level=new_level)
                )
            except:
                pass
        
        # Sayı tahmini oyunu
        if message.content.isdigit() and 1 <= int(message.content) <= 10:
            user_id = str(message.author.id)
            
            active_game_id = None
            for game_id, game_data in self.number_games.items():
                if (game_data.get("target") == message.author.id and 
                    game_data.get("status") == "waiting_guess"):
                    active_game_id = game_id
                    break
            
            if active_game_id:
                guess = int(message.content)
                game_data = self.number_games[active_game_id]
                correct_number = game_data["number"]
                bet_amount = game_data["bet_amount"]
                
                if guess == correct_number:
                    total_pot = bet_amount * 2
                    fee = int(total_pot * 0.1)
                    prize = total_pot - fee
                    
                    self.coins_data[user_id] = self.coins_data.get(user_id, 0) + prize
                    self.save_json(self.coins_data, self.coins_file)
                    
                    embed = discord.Embed(
                        title="🎉 Congratulations! Correct Guess!",
                        description=f"{message.author.mention} guessed the correct number!",
                        color=0x00ff00
                    )
                    embed.add_field(name="Guess", value=guess, inline=True)
                    embed.add_field(name="Correct Number", value=correct_number, inline=True)
                    embed.add_field(name="Prize", value=f"{prize} Sampy Coin", inline=True)
                    embed.add_field(name="Fee", value=f"{fee} Sampy Coin", inline=True)
                    
                    await message.channel.send(embed=embed)
                else:
                    embed = discord.Embed(
                        title="❌ Wrong Guess!",
                        description=f"{message.author.mention} guessed the wrong number.",
                        color=0xff0000
                    )
                    embed.add_field(name="Guess", value=guess, inline=True)
                    embed.add_field(name="Correct Number", value=correct_number, inline=True)
                    embed.add_field(name="Loss", value=f"{bet_amount} Sampy Coin", inline=True)
                    
                    creator_id = str(game_data["creator"])
                    self.coins_data[creator_id] = self.coins_data.get(creator_id, 0) + bet_amount
                    self.save_json(self.coins_data, self.coins_file)
                    
                    await message.channel.send(embed=embed)
                
                del self.number_games[active_game_id]
                self.save_json(self.number_games, self.number_games_file)
                
                try:
                    await message.delete()
                except:
                    pass
        
        # Başvuru mesaj işleme
        if str(message.channel.id) in self.applications_data:
            application = self.applications_data[str(message.channel.id)]
            if message.author.id == application["user_id"]:
                current_stage = application["current_stage"]
                stages = application["stages"]
                optional_stages = application["optional_stages"]
                
                if current_stage < len(stages):
                    answer = message.content
                    application["answers"].append(answer)
                    application["current_stage"] += 1
                    self.save_json(self.applications_data, "applications.json")
                    
                    await message.delete()
                    
                    await message.channel.send(
                        f"✅ **{get_text(str(message.guild.id), 'application_requirement_completed')}**\n"
                        f"**Stage {current_stage + 1} completed!**"
                    )
                    
                    if application["current_stage"] < len(stages):
                        next_stage = application["current_stage"]
                        is_optional = next_stage in optional_stages
                        
                        embed = discord.Embed(
                            title=f"Stage {next_stage + 1}/{len(stages)}{' (Optional)' if is_optional else ''}",
                            description=stages[next_stage],
                            color=0x00ff00
                        )
                        
                        view = ApplicationProcessView(self.bot, str(message.channel.id))
                        await message.channel.send(embed=embed, view=view)
                    else:
                        # Başvuru tamamlandı
                        user = message.guild.get_member(application["user_id"])
                        stages = application["stages"]
                        answers = application["answers"]
                        
                        embed = discord.Embed(
                            title=get_text(str(message.guild.id), "application_summary", user=user.display_name),
                            color=0x00ff00
                        )
                        
                        for i, (stage, answer) in enumerate(zip(stages, answers)):
                            embed.add_field(
                                name=f"Stage {i+1}: {stage}",
                                value=answer,
                                inline=False
                            )
                        
                        embed.add_field(
                            name=get_text(str(message.guild.id), "application_response_wait"),
                            value=f"**-{message.guild.name} {get_text(str(message.guild.id), 'application_team')}**",
                            inline=False
                        )
                        
                        await message.channel.send(embed=embed)
                        await message.channel.send(get_text(str(message.guild.id), "application_submitted"))
        
        # Mesaj loglama
        if str(message.guild.id) not in self.message_logs_data:
            self.message_logs_data[str(message.guild.id)] = {}
        
        guild_logs = self.message_logs_data[str(message.guild.id)]
        if len(guild_logs) > 1000:
            oldest_keys = sorted(guild_logs.keys())[:100]
            for key in oldest_keys:
                del guild_logs[key]
        
        guild_logs[str(message.id)] = {
            "content": message.content,
            "author": str(message.author),
            "author_id": message.author.id,
            "channel": message.channel.name,
            "timestamp": message.created_at.isoformat(),
            "attachments": [att.url for att in message.attachments]
        }
        
        self.save_json(self.message_logs_data, self.message_logs_file)
        
        await self.process_commands(message)

    async def generate_ai_response(self, message):
        """Basit AI yanıtı oluştur"""
        content = message.content.lower()
        
        # Basit anahtar kelime eşleştirme
        responses = {
            'merhaba': 'Merhaba! Size nasıl yardımcı olabilirim?',
            'hello': 'Hello! How can I help you?',
            'nasılsın': 'Teşekkür ederim, iyiyim! Siz nasılsınız?',
            'how are you': 'Thank you, I am fine! How are you?',
            'yardım': 'Size nasıl yardımcı olabilirim? Komutlar için /help yazabilirsiniz.',
            'help': 'How can I help you? You can type /help for commands.',
            'teşekkür': 'Rica ederim! Başka bir şey var mı?',
            'thank you': 'You are welcome! Is there anything else?'
        }
        
        for keyword, response in responses.items():
            if keyword in content:
                return response
        
        # Varsayılan yanıt
        default_responses = [
            "İlginç! Biraz daha açıklar mısınız?",
            "Bunu anlamadım, başka şekilde ifade edebilir misiniz?",
            "Bu konuda size nasıl yardımcı olabilirim?",
            "Daha fazla bilgi verebilir misiniz?",
            "Interesting! Can you explain a bit more?",
            "I didn't understand that, can you rephrase?",
            "How can I help you with this?",
            "Can you provide more information?"
        ]
        
        return random.choice(default_responses)

bot = SampyBot()

# Zaman dönüşüm fonksiyonu
def parse_time(time_str: str) -> int:
    units = {
        's': 1,
        'm': 60,
        'h': 3600,
        'd': 86400,
        'w': 604800
    }
    unit = time_str[-1]
    value = int(time_str[:-1])
    return value * units[unit]

# Moderasyon Log Fonksiyonu
async def send_mod_log(guild, action, target, moderator, reason=None, duration=None):
    try:
        owner = guild.owner
        embed = discord.Embed(
            title=f"🛡️ Moderation Log - {action}",
            color=0xff0000,
            timestamp=datetime.datetime.now()
        )
        embed.add_field(name="Target", value=f"{target.mention} (`{target.id}`)", inline=True)
        embed.add_field(name="Moderator", value=f"{moderator.mention}", inline=True)
        embed.add_field(name="Channel", value=f"<#{moderator.channel.id}>" if hasattr(moderator, 'channel') else "Unknown", inline=True)
        
        if reason:
            embed.add_field(name="Reason", value=reason, inline=False)
        
        if duration:
            embed.add_field(name="Duration", value=duration, inline=True)
        
        await owner.send(embed=embed)
    except Exception as e:
        print(f"Mod log couldn't be sent: {e}")

# Punishment kayıt fonksiyonu
def add_punishment(user_id: str, punishment_type: str, guild_id: int, reason: str, duration: str = None, moderator_id: int = None):
    punishment_id = f"{guild_id}_{user_id}_{int(datetime.datetime.now().timestamp())}"
    
    punishment_data = {
        "type": punishment_type,
        "guild_id": guild_id,
        "user_id": user_id,
        "reason": reason,
        "moderator_id": moderator_id,
        "timestamp": datetime.datetime.now().isoformat(),
        "duration": duration if duration else get_text(str(guild_id), "infinite")
    }
    
    if duration:
        duration_seconds = parse_time(duration)
        expires_at = datetime.datetime.now() + datetime.timedelta(seconds=duration_seconds)
        punishment_data["expires_at"] = expires_at.isoformat()
    
    if user_id not in bot.punishment_users:
        bot.punishment_users[user_id] = {}
    
    bot.punishment_users[user_id][punishment_id] = punishment_data
    bot.save_json(bot.punishment_users, bot.punishment_users_file)
    
    return punishment_id

# YENİ KOMUT: Temp Room Setup
@bot.tree.command(name="temp-room-setup", description="Setup temporary room system (server owner only)")
@is_server_owner()
async def temp_room_setup(interaction: discord.Interaction, channel: discord.VoiceChannel):
    guild_id = str(interaction.guild.id)
    
    bot.temp_rooms[str(channel.id)] = {
        "guild_id": interaction.guild.id,
        "user_limit": 0,
        "created_at": datetime.datetime.now().isoformat()
    }
    bot.save_json(bot.temp_rooms, "temp_rooms.json")
    
    await interaction.response.send_message(
        get_text(guild_id, "temp_room_setup", channel=channel.mention),
        ephemeral=True
    )

# YENİ KOMUT: AI Chat Start
@bot.tree.command(name="tag-ai-chat-start", description="Start AI chat in a private channel")
async def ai_chat_start(interaction: discord.Interaction):
    guild = interaction.guild
    category = discord.utils.get(guild.categories, name="AI Chats")
    
    if not category:
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True)
        }
        category = await guild.create_category("AI Chats", overwrites=overwrites)
    
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
        guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
    }
    
    ai_channel = await category.create_text_channel(
        name=f"ai-chat-{interaction.user.name}",
        overwrites=overwrites
    )
    
    bot.ai_chats[str(ai_channel.id)] = {
        "user_id": interaction.user.id,
        "guild_id": guild.id,
        "created_at": datetime.datetime.now().isoformat(),
        "history": []
    }
    bot.save_json(bot.ai_chats, "ai_chats.json")
    
    embed = discord.Embed(
        title="🤖 AI Chat Started!",
        description=f"Welcome {interaction.user.mention} to your AI chat!\n\nMention me (@{bot.user.display_name}) to talk with AI!",
        color=0x00ff00
    )
    embed.add_field(name="Commands", value="• Mention me to chat\n• Use buttons below for management", inline=False)
    
    view = AIChatView(bot, str(ai_channel.id))
    await ai_channel.send(embed=embed, view=view)
    
    await interaction.response.send_message(
        get_text(str(interaction.guild.id), "ai_chat_started", channel=ai_channel.mention),
        ephemeral=True
    )

# YENİ KOMUT: AI Chat Stop
@bot.tree.command(name="tag-ai-chat-stop", description="Stop AI chat in current channel")
async def ai_chat_stop(interaction: discord.Interaction):
    if str(interaction.channel.id) in bot.ai_chats:
        del bot.ai_chats[str(interaction.channel.id)]
        bot.save_json(bot.ai_chats, "ai_chats.json")
    
    await interaction.response.send_message(
        get_text(str(interaction.guild.id), "ai_chat_stopped", channel=interaction.channel.mention)
    )
    await asyncio.sleep(3)
    await interaction.channel.delete()

# YENİ KOMUT: Server Setup
@bot.tree.command(name="server-setup", description="Setup server channels and categories (server owner only)")
@is_server_owner()
async def server_setup(interaction: discord.Interaction, level: str):
    guild = interaction.guild
    guild_id = str(guild.id)
    
    level = level.lower()
    valid_levels = ["simple", "normal", "advanced", "full"]
    
    if level not in valid_levels:
        await interaction.response.send_message(
            f"❌ Invalid level! Choose from: {', '.join(valid_levels)}",
            ephemeral=True
        )
        return
    
    await interaction.response.defer(ephemeral=True)
    
    try:
        # Temel kategoriler
        categories = {}
        
        if level in ["normal", "advanced", "full"]:
            categories["💬・Chat"] = ["general", "off-topic", "memes"]
            categories["🎮・Games"] = ["gaming", "minecraft", "among-us"]
        
        if level in ["advanced", "full"]:
            categories["🎵・Music"] = ["music-requests", "lyrics"]
            categories["🎨・Creativity"] = ["art-share", "writing"]
            categories["📚・Education"] = ["homework-help", "programming"]
        
        if level == "full":
            categories["🔞・NSFW"] = ["nsfw-chat", "nsfw-media"]
            categories["🤖・Bots"] = ["bot-commands", "ai-chat"]
            categories["🎉・Events"] = ["giveaways", "events"]
        
        created_channels = []
        
        for category_name, channels in categories.items():
            # Kategori oluştur
            category = await guild.create_category(category_name)
            
            # Kanalları oluştur
            for channel_name in channels:
                if "nsfw" in channel_name.lower():
                    channel = await category.create_text_channel(
                        channel_name,
                        nsfw=True
                    )
                else:
                    channel = await category.create_text_channel(channel_name)
                created_channels.append(channel.mention)
        
        # Ses kanalları
        if level in ["advanced", "full"]:
            voice_category = await guild.create_category("🔊・Voice Channels")
            voice_channels = ["General", "Gaming", "Music", "AFK"]
            
            for vc_name in voice_channels:
                await voice_category.create_voice_channel(vc_name)
        
        # Geçici oda sistemi için özel kanal
        if level == "full":
            temp_room_category = await guild.create_category("🎪・Temporary Rooms")
            temp_room_channel = await temp_room_category.create_voice_channel("➕ Create Temp Room")
            
            # Geçici oda sistemini kaydet
            bot.temp_rooms[str(temp_room_channel.id)] = {
                "guild_id": guild.id,
                "user_limit": 0,
                "created_at": datetime.datetime.now().isoformat()
            }
            bot.save_json(bot.temp_rooms, "temp_rooms.json")
        
        # Sunucu kurulumunu kaydet
        bot.server_setups[guild_id] = {
            "level": level,
            "setup_at": datetime.datetime.now().isoformat(),
            "channels_created": len(created_channels)
        }
        bot.save_json(bot.server_setups, "server_setups.json")
        
        embed = discord.Embed(
            title="✅ Server Setup Complete!",
            description=get_text(guild_id, "server_setup_complete", level=level),
            color=0x00ff00
        )
        embed.add_field(name="Level", value=level.capitalize(), inline=True)
        embed.add_field(name="Channels Created", value=str(len(created_channels)), inline=True)
        
        if created_channels:
            embed.add_field(
                name="Created Channels", 
                value=", ".join(created_channels[:10]) + (f" and {len(created_channels)-10} more..." if len(created_channels) > 10 else ""),
                inline=False
            )
        
        await interaction.followup.send(embed=embed, ephemeral=True)
        
    except Exception as e:
        await interaction.followup.send(f"❌ Setup failed: {str(e)}", ephemeral=True)

# Mevcut komutlar aynen devam edecek...
# YENİ KOMUT: Tag Close Menu
@bot.tree.command(name="tag-close-menu", description="Add users/roles to tag block list (server owner only)")
@is_server_owner()
async def tag_close_menu(interaction: discord.Interaction):
    view = TagCloseView(bot, str(interaction.guild.id))
    await interaction.response.send_message(
        "🔒 **Tag Block System**\nSelect users/roles to block tags:",
        view=view,
        ephemeral=True
    )

# YENİ KOMUT: Tag Close ID
@bot.tree.command(name="tag-close-id", description="Add user/role to tag block list by ID (server owner only)")
@is_server_owner()
async def tag_close_id(interaction: discord.Interaction, target_id: str, target_type: str):
    guild_id = str(interaction.guild.id)
    
    if guild_id not in bot.tag_close_data:
        bot.tag_close_data[guild_id] = []
    
    target_value = f"{target_type}_{target_id}"
    
    if target_value in bot.tag_close_data[guild_id]:
        await interaction.response.send_message("❌ Target is already in block list!", ephemeral=True)
        return
    
    bot.tag_close_data[guild_id].append(target_value)
    bot.save_json(bot.tag_close_data, "tag_close.json")
    
    # Hedefi bul ve mention et
    if target_type == "role":
        target = interaction.guild.get_role(int(target_id))
    else:
        target = interaction.guild.get_member(int(target_id))
    
    target_mention = target.mention if target else f"ID: {target_id}"
    
    await interaction.response.send_message(
        get_text(guild_id, "tag_close_added", target=target_mention),
        ephemeral=True
    )

# YENİ KOMUT: Tag Close List
@bot.tree.command(name="tag-close-list", description="Show tag block list")
async def tag_close_list(interaction: discord.Interaction):
    guild_id = str(interaction.guild.id)
    
    if guild_id not in bot.tag_close_data or not bot.tag_close_data[guild_id]:
        await interaction.response.send_message(
            get_text(guild_id, "tag_close_empty"),
            ephemeral=True
        )
        return
    
    embed = discord.Embed(
        title=get_text(guild_id, "tag_close_list"),
        color=0xff0000
    )
    
    users = []
    roles = []
    
    for target in bot.tag_close_data[guild_id]:
        type_, id_ = target.split('_')
        if type_ == "user":
            user = interaction.guild.get_member(int(id_))
            if user:
                users.append(user.mention)
            else:
                users.append(f"User ({id_})")
        else:
            role = interaction.guild.get_role(int(id_))
            if role:
                roles.append(role.mention)
            else:
                roles.append(f"Role ({id_})")
    
    if users:
        embed.add_field(name="👤 Users", value="\n".join(users), inline=False)
    if roles:
        embed.add_field(name="👑 Roles", value="\n".join(roles), inline=False)
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

# YENİ KOMUT: Warn
@bot.tree.command(name="warn", description="Warn user")
@has_command_permission('warn')
async def warn(interaction: discord.Interaction, user: discord.Member, reason: str):
    guild_id = str(interaction.guild.id)
    user_id = str(user.id)
    
    if guild_id not in bot.warnings_data:
        bot.warnings_data[guild_id] = {}
    
    if user_id not in bot.warnings_data[guild_id]:
        bot.warnings_data[guild_id][user_id] = {}
    
    warn_id = f"{int(datetime.datetime.now().timestamp())}"
    bot.warnings_data[guild_id][user_id][warn_id] = {
        "reason": reason,
        "moderator_id": interaction.user.id,
        "timestamp": datetime.datetime.now().isoformat()
    }
    
    bot.save_json(bot.warnings_data, "warnings.json")
    
    warn_count = len(bot.warnings_data[guild_id][user_id])
    
    await interaction.response.send_message(
        get_text(guild_id, "warn_added", user=user.mention, count=warn_count)
    )

# YENİ KOMUT: Warn Remove
@bot.tree.command(name="warn-remove", description="Remove warning from user")
@has_command_permission('warn')
async def warn_remove(interaction: discord.Interaction, user: discord.Member, warn_number: int):
    guild_id = str(interaction.guild.id)
    user_id = str(user.id)
    
    if (guild_id not in bot.warnings_data or 
        user_id not in bot.warnings_data[guild_id] or 
        not bot.warnings_data[guild_id][user_id]):
        await interaction.response.send_message("❌ User has no warnings!", ephemeral=True)
        return
    
    warnings = list(bot.warnings_data[guild_id][user_id].items())
    
    if warn_number < 1 or warn_number > len(warnings):
        await interaction.response.send_message("❌ Invalid warning number!", ephemeral=True)
        return
    
    warn_id, _ = warnings[warn_number - 1]
    del bot.warnings_data[guild_id][user_id][warn_id]
    
    # Eğer kullanıcının hiç uyarısı kalmadıysa, kullanıcıyı sil
    if not bot.warnings_data[guild_id][user_id]:
        del bot.warnings_data[guild_id][user_id]
    
    bot.save_json(bot.warnings_data, "warnings.json")
    
    remaining_count = len(bot.warnings_data[guild_id].get(user_id, {}))
    
    await interaction.response.send_message(
        get_text(guild_id, "warn_removed", user=user.mention, count=remaining_count)
    )

# YENİ KOMUT: Warn List
@bot.tree.command(name="warn-list", description="Show user's warnings")
@has_command_permission('warn')
async def warn_list(interaction: discord.Interaction, user: discord.Member):
    guild_id = str(interaction.guild.id)
    user_id = str(user.id)
    
    if (guild_id not in bot.warnings_data or 
        user_id not in bot.warnings_data[guild_id] or 
        not bot.warnings_data[guild_id][user_id]):
        await interaction.response.send_message(
            get_text(guild_id, "warn_none"),
            ephemeral=True
        )
        return
    
    warnings = bot.warnings_data[guild_id][user_id]
    view = WarnListView(user.id, warnings)
    embed = view.create_embed(guild_id)
    
    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

# YENİ KOMUT: YouTube Video Channel Setup
@bot.tree.command(name="yt-video-channel-setup", description="Setup YouTube video notifications (server owner only)")
@is_server_owner()
async def yt_video_channel_setup(
    interaction: discord.Interaction, 
    youtube_api_key: str,
    youtube_channel_id: str,
    channel: Optional[discord.TextChannel] = None
):
    target_channel = channel or interaction.channel
    guild_id = str(interaction.guild.id)
    
    await interaction.response.send_message(
        "Please enter the message template for new videos (use {link} for video link):",
        ephemeral=True
    )
    
    def check(m):
        return m.author == interaction.user and m.channel == interaction.channel
    
    try:
        msg = await bot.wait_for('message', check=check, timeout=60)
        message_template = msg.content
        
        try:
            await msg.delete()
        except:
            pass
        
    except asyncio.TimeoutError:
        await interaction.followup.send("Timed out.", ephemeral=True)
        return
    
    # YouTube API test
    test_video = await bot.get_latest_youtube_video(youtube_api_key, youtube_channel_id)
    if not test_video:
        await interaction.followup.send("❌ Invalid YouTube API key or channel ID!", ephemeral=True)
        return
    
    # Ayarları kaydet
    bot.yt_settings[guild_id] = {
        'api_key': youtube_api_key,
        'channel_id': youtube_channel_id,
        'discord_channel_id': target_channel.id,
        'message_template': message_template,
        'last_video_id': test_video['id']
    }
    
    bot.save_json(bot.yt_settings, "yt_settings.json")
    
    await interaction.followup.send(
        get_text(guild_id, "yt_setup_complete"),
        ephemeral=True
    )

# YENİ KOMUT: YouTube Video Channel Reset
@bot.tree.command(name="yt-video-channel-reset", description="Reset YouTube video notifications (server owner only)")
@is_server_owner()
async def yt_video_channel_reset(interaction: discord.Interaction):
    guild_id = str(interaction.guild.id)
    
    if guild_id in bot.yt_settings:
        del bot.yt_settings[guild_id]
        bot.save_json(bot.yt_settings, "yt_settings.json")
    
    await interaction.response.send_message(
        get_text(guild_id, "yt_reset_complete"),
        ephemeral=True
    )

# YENİ KOMUT: Get YouTube API Key
@bot.tree.command(name="get-yt-api-key", description="Get instructions for YouTube API key")
async def get_yt_api_key(interaction: discord.Interaction):
    view = GetYouTubeAPIView()
    await interaction.response.send_message(
        "**YouTube API Key Guide**\nSelect your language:",
        view=view,
        ephemeral=True
    )

# YENİ KOMUT: Giveaway Join Limit
@bot.tree.command(name="giveaway-join-limit", description="Set giveaway join limits for roles")
@has_command_permission('giveaway')
async def giveaway_join_limit(interaction: discord.Interaction):
    view = GiveawayJoinLimitView(bot, str(interaction.guild.id))
    await interaction.response.send_message(
        "🎯 **Giveaway Join Limits**\nSelect roles to set join limits:",
        view=view,
        ephemeral=True
    )

# YENİ KOMUT: Giveaway Join Limit ID
@bot.tree.command(name="giveaway-join-limit-id", description="Set giveaway join limit for specific role/user by ID")
@has_command_permission('giveaway')
async def giveaway_join_limit_id(interaction: discord.Interaction, target_id: str, join_limit: int):
    guild_id = str(interaction.guild.id)
    
    if guild_id not in bot.giveaway_join_limits:
        bot.giveaway_join_limits[guild_id] = {}
    
    bot.giveaway_join_limits[guild_id][target_id] = join_limit
    bot.save_json(bot.giveaway_join_limits, "giveaway_join_limits.json")
    
    # Hedefi bul
    target = interaction.guild.get_role(int(target_id)) or interaction.guild.get_member(int(target_id))
    target_name = target.mention if target else f"ID: {target_id}"
    
    limit_text = "unlimited" if join_limit == 0 else f"{join_limit} entries"
    
    await interaction.response.send_message(
        f"✅ Set {limit_text} for {target_name}",
        ephemeral=True
    )

# YENİ KOMUT: Giveaway Join Limit Reset
@bot.tree.command(name="giveaway-join-limit-reset", description="Reset all giveaway join limits")
@has_command_permission('giveaway')
async def giveaway_join_limit_reset(interaction: discord.Interaction):
    guild_id = str(interaction.guild.id)
    
    if guild_id in bot.giveaway_join_limits:
        del bot.giveaway_join_limits[guild_id]
        bot.save_json(bot.giveaway_join_limits, "giveaway_join_limits.json")
    
    await interaction.response.send_message("✅ Giveaway join limits reset!", ephemeral=True)

# YENİ KOMUT: Autorole
@bot.tree.command(name="autorole", description="Add/remove autorole")
@is_server_owner()
async def autorole(interaction: discord.Interaction, action: str, role: discord.Role):
    guild_id = str(interaction.guild.id)
    
    if guild_id not in bot.autorole_data:
        bot.autorole_data[guild_id] = []
    
    if action.lower() == "add":
        if role.id in bot.autorole_data[guild_id]:
            await interaction.response.send_message("❌ Role is already in autorole!", ephemeral=True)
            return
        
        bot.autorole_data[guild_id].append(role.id)
        await interaction.response.send_message(
            get_text(guild_id, "autorole_added", role=role.mention),
            ephemeral=True
        )
    
    elif action.lower() == "remove":
        if role.id not in bot.autorole_data[guild_id]:
            await interaction.response.send_message("❌ Role is not in autorole!", ephemeral=True)
            return
        
        bot.autorole_data[guild_id].remove(role.id)
        await interaction.response.send_message(
            get_text(guild_id, "autorole_removed", role=role.mention),
            ephemeral=True
        )
    
    else:
        await interaction.response.send_message("❌ Invalid action! Use 'add' or 'remove'.", ephemeral=True)
        return
    
    bot.save_json(bot.autorole_data, "autorole.json")

# YENİ KOMUT: Autorole ID
@bot.tree.command(name="autorole-id", description="Add/remove autorole by ID")
@is_server_owner()
async def autorole_id(interaction: discord.Interaction, action: str, role_id: str):
    guild_id = str(interaction.guild.id)
    role = interaction.guild.get_role(int(role_id))
    
    if not role:
        await interaction.response.send_message("❌ Role not found!", ephemeral=True)
        return
    
    if guild_id not in bot.autorole_data:
        bot.autorole_data[guild_id] = []
    
    if action.lower() == "add":
        if role.id in bot.autorole_data[guild_id]:
            await interaction.response.send_message("❌ Role is already in autorole!", ephemeral=True)
            return
        
        bot.autorole_data[guild_id].append(role.id)
        await interaction.response.send_message(
            get_text(guild_id, "autorole_added", role=role.mention),
            ephemeral=True
        )
    
    elif action.lower() == "remove":
        if role.id not in bot.autorole_data[guild_id]:
            await interaction.response.send_message("❌ Role is not in autorole!", ephemeral=True)
            return
        
        bot.autorole_data[guild_id].remove(role.id)
        await interaction.response.send_message(
            get_text(guild_id, "autorole_removed", role=role.mention),
            ephemeral=True
        )
    
    else:
        await interaction.response.send_message("❌ Invalid action! Use 'add' or 'remove'.", ephemeral=True)
        return
    
    bot.save_json(bot.autorole_data, "autorole.json")

# YENİ KOMUT: Autorole List
@bot.tree.command(name="autorole-list", description="Show autorole list")
async def autorole_list(interaction: discord.Interaction):
    guild_id = str(interaction.guild.id)
    
    if guild_id not in bot.autorole_data or not bot.autorole_data[guild_id]:
        await interaction.response.send_message(
            get_text(guild_id, "autorole_list") + ": No roles",
            ephemeral=True
        )
        return
    
    embed = discord.Embed(
        title=get_text(guild_id, "autorole_list"),
        color=0x00ff00
    )
    
    role_mentions = []
    for role_id in bot.autorole_data[guild_id]:
        role = interaction.guild.get_role(role_id)
        if role:
            role_mentions.append(role.mention)
    
    embed.description = "\n".join(role_mentions)
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

# YENİ KOMUT: Save Role Data
@bot.tree.command(name="save-role-data", description="Save role data for specific server (bot owner only)")
@is_bot_owner()
async def save_role_data(interaction: discord.Interaction, server_id: str):
    if server_id not in bot.save_role_data:
        bot.save_role_data[server_id] = True
    else:
        bot.save_role_data[server_id] = not bot.save_role_data[server_id]
    
    bot.save_json(bot.save_role_data, "save_role_data.json")
    
    status = "enabled" if bot.save_role_data[server_id] else "disabled"
    await interaction.response.send_message(
        f"✅ Role data saving {status} for server {server_id}",
        ephemeral=True
    )

# Mevcut komutlar (önceki kodda tanımlananlar) aynen kalacak...
# YENİ KOMUT: Authorized Application Setup
@bot.tree.command(name="authorized-application-setup", description="Setup application system (server owner only)")
@is_server_owner()
async def authorized_application_setup(interaction: discord.Interaction, channel: Optional[discord.TextChannel] = None):
    target_channel = channel or interaction.channel
    
    await interaction.response.send_message(get_text(str(interaction.guild.id), "application_enter_stages"), ephemeral=True)
    
    def check(m):
        return m.author == interaction.user and m.channel == interaction.channel and m.content.isdigit()
    
    try:
        msg = await bot.wait_for('message', check=check, timeout=60)
        stage_count = int(msg.content)
    except asyncio.TimeoutError:
        await interaction.followup.send("Timed out.", ephemeral=True)
        return
    
    stages = []
    for i in range(stage_count):
        await interaction.followup.send(get_text(str(interaction.guild.id), "application_enter_stage", number=i+1), ephemeral=True)
        
        def stage_check(m):
            return m.author == interaction.user and m.channel == interaction.channel
        
        try:
            msg = await bot.wait_for('message', check=stage_check, timeout=60)
            stages.append(msg.content)
        except asyncio.TimeoutError:
            await interaction.followup.send("Timed out.", ephemeral=True)
            return
    
    # Opsiyonel stage seçimi
    view = ApplicationOptionalView(bot, str(interaction.guild.id), stages)
    await interaction.followup.send(get_text(str(interaction.guild.id), "application_select_optional"), view=view, ephemeral=True)
    
    await view.wait()
    optional_stages = getattr(view, 'optional_stages', [])
    
    # Başvuru ID'si oluştur
    application_id = f"{interaction.guild.id}_{int(datetime.datetime.now().timestamp())}"
    
    # Başvuru verisini kaydet
    bot.application_data[application_id] = {
        "guild_id": interaction.guild.id,
        "channel_id": target_channel.id,
        "stages": stages,
        "optional_stages": optional_stages,
        "created_by": interaction.user.id,
        "created_at": datetime.datetime.now().isoformat()
    }
    bot.save_json(bot.application_data, "application_data.json")
    
    # Başvuru butonunu oluştur
    embed = discord.Embed(
        title="📝 Application System",
        description="Click the button below to start your application!",
        color=0x00ff00
    )
    
    view = ApplicationStartView(bot, str(interaction.guild.id), application_id)
    await target_channel.send(embed=embed, view=view)
    
    await interaction.followup.send(get_text(str(interaction.guild.id), "application_setup_complete"), ephemeral=True)

# YENİ KOMUT: Reset Channels Message
@bot.tree.command(name="reset-channels-message", description="Delete all messages in all channels (except Sampy Bot messages)")
@has_command_permission('reset-channels-message')
async def reset_channels_message(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    
    try:
        deleted_count = 0
        
        for channel in interaction.guild.channels:
            if isinstance(channel, discord.TextChannel):
                try:
                    async for message in channel.history(limit=None):
                        if message.author != bot.user:
                            await message.delete()
                            deleted_count += 1
                except Exception as e:
                    print(f"Could not delete messages in {channel.name}: {e}")
        
        await interaction.followup.send(f"✅ Successfully deleted {deleted_count} messages from all channels!", ephemeral=True)
        
    except Exception as e:
        await interaction.followup.send(f"❌ Error: {str(e)}", ephemeral=True)

# YENİ KOMUT: Unmute
@bot.tree.command(name="unmute", description="Unmute user")
@has_command_permission('unmute')
async def unmute(interaction: discord.Interaction, user: discord.Member, reason: Optional[str] = "No reason provided"):
    try:
        for channel in interaction.guild.channels:
            if isinstance(channel, discord.TextChannel):
                await channel.set_permissions(user, overwrite=None)
        
        await interaction.response.send_message(
            get_text(str(interaction.guild.id), "unmuted", user=user.mention)
        )
        
        await send_mod_log(
            interaction.guild, 
            "Unmute", 
            user, 
            interaction.user, 
            reason=reason
        )
    except Exception as e:
        await interaction.response.send_message(f"❌ Unmute failed: {str(e)}", ephemeral=True)

# YENİ KOMUT: Untimeout
@bot.tree.command(name="untimeout", description="Remove timeout from user")
@has_command_permission('untimeout')
async def untimeout(interaction: discord.Interaction, user: discord.Member, reason: Optional[str] = "No reason provided"):
    try:
        if user.timed_out_until is None:
            await interaction.response.send_message(
                get_text(str(interaction.guild.id), "user_not_timed_out"),
                ephemeral=True
            )
            return
        
        await user.timeout(None, reason=reason)
        await interaction.response.send_message(
            get_text(str(interaction.guild.id), "untimeout", user=user.mention)
        )
        
        await send_mod_log(
            interaction.guild, 
            "Untimeout", 
            user, 
            interaction.user, 
            reason=reason
        )
    except Exception as e:
        await interaction.response.send_message(f"❌ Untimeout failed: {str(e)}", ephemeral=True)

# YENİ KOMUT: History
@bot.tree.command(name="history", description="Show user's punishment history")
@has_command_permission('history')
async def history(interaction: discord.Interaction, user: discord.Member, amount: Optional[str] = None):
    user_id = str(user.id)
    
    if user_id not in bot.punishment_users:
        await interaction.response.send_message("❌ No punishment history for this user!", ephemeral=True)
        return
    
    punishments = bot.punishment_users[user_id]
    
    # Tüm cezaları al veya belirli sayıda
    if amount and amount.lower() == "all":
        show_punishments = list(punishments.items())
    else:
        try:
            show_count = int(amount) if amount else 10
            show_punishments = list(punishments.items())[:show_count]
        except ValueError:
            await interaction.response.send_message("❌ Invalid amount! Use a number or 'all'.", ephemeral=True)
            return
    
    embed = discord.Embed(
        title=f"📋 Punishment History - {user.display_name}",
        color=0xff0000
    )
    
    for punishment_id, punishment_data in show_punishments:
        embed.add_field(
            name=f"{punishment_data['type']} - {punishment_id}",
            value=f"Reason: {punishment_data['reason']}\nDuration: {punishment_data['duration']}\nTime: {punishment_data['timestamp'][:16]}",
            inline=False
        )
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

# YENİ KOMUT: UnIP Ban
@bot.tree.command(name="unipban", description="Un-IP ban user")
@has_command_permission('unipban')
async def unipban(interaction: discord.Interaction, user_id: str, reason: Optional[str] = "No reason provided"):
    try:
        user = await bot.fetch_user(int(user_id))
        await interaction.guild.unban(user, reason=reason)
        
        # Punishment kaydını kaldır
        if user_id in bot.punishment_users:
            for punishment_id, punishment_data in list(bot.punishment_users[user_id].items()):
                if punishment_data['type'] == 'ban' and punishment_data['guild_id'] == interaction.guild.id:
                    del bot.punishment_users[user_id][punishment_id]
                    if not bot.punishment_users[user_id]:
                        del bot.punishment_users[user_id]
                    bot.save_json(bot.punishment_users, bot.punishment_users_file)
                    break
        
        await interaction.response.send_message(
            get_text(str(interaction.guild.id), "unipbanned", user=user.mention)
        )
        
        await send_mod_log(
            interaction.guild, 
            "Un-IP Ban", 
            user, 
            interaction.user, 
            reason=reason
        )
    except Exception as e:
        await interaction.response.send_message(f"❌ Un-IP ban failed: {str(e)}", ephemeral=True)

# YENİ KOMUT: UnIP Mute
@bot.tree.command(name="unipmute", description="Un-IP mute user")
@has_command_permission('unipmute')
async def unipmute(interaction: discord.Interaction, user_id: str, reason: Optional[str] = "No reason provided"):
    try:
        user = await bot.fetch_user(int(user_id))
        
        for channel in interaction.guild.channels:
            if isinstance(channel, (discord.TextChannel, discord.VoiceChannel)):
                await channel.set_permissions(user, overwrite=None)
        
        # Punishment kaydını kaldır
        if user_id in bot.punishment_users:
            for punishment_id, punishment_data in list(bot.punishment_users[user_id].items()):
                if punishment_data['type'] == 'mute' and punishment_data['guild_id'] == interaction.guild.id:
                    del bot.punishment_users[user_id][punishment_id]
                    if not bot.punishment_users[user_id]:
                        del bot.punishment_users[user_id]
                    bot.save_json(bot.punishment_users, bot.punishment_users_file)
                    break
        
        await interaction.response.send_message(
            get_text(str(interaction.guild.id), "unipmuted", user=user.mention)
        )
        
        await send_mod_log(
            interaction.guild, 
            "Un-IP Mute", 
            user, 
            interaction.user, 
            reason=reason
        )
    except Exception as e:
        await interaction.response.send_message(f"❌ Un-IP mute failed: {str(e)}", ephemeral=True)

# YENİ KOMUT: Check Ban
@bot.tree.command(name="checkban", description="Check if user is banned")
@has_command_permission('checkban')
async def checkban(interaction: discord.Interaction, user_id: str):
    try:
        ban_list = await interaction.guild.bans()
        user_id_int = int(user_id)
        
        for ban_entry in ban_list:
            if ban_entry.user.id == user_id_int:
                embed = discord.Embed(
                    title="🔨 User is Banned",
                    description=f"User <@{user_id}> is banned from this server.",
                    color=0xff0000
                )
                embed.add_field(name="Reason", value=ban_entry.reason or "No reason provided")
                await interaction.response.send_message(embed=embed)
                return
        
        await interaction.response.send_message(
            get_text(str(interaction.guild.id), "user_not_banned"),
            ephemeral=True
        )
    except Exception as e:
        await interaction.response.send_message(f"❌ Check ban failed: {str(e)}", ephemeral=True)

# YENİ KOMUT: Check Mute
@bot.tree.command(name="checkmute", description="Check if user is muted")
@has_command_permission('checkmute')
async def checkmute(interaction: discord.Interaction, user: discord.Member):
    muted_channels = []
    
    for channel in interaction.guild.channels:
        if isinstance(channel, discord.TextChannel):
            overwrite = channel.overwrites_for(user)
            if overwrite.send_messages == False:
                muted_channels.append(channel.mention)
    
    if muted_channels:
        embed = discord.Embed(
            title="🔇 User is Muted",
            description=f"{user.mention} is muted in the following channels:",
            color=0xff0000
        )
        embed.add_field(name="Muted Channels", value="\n".join(muted_channels[:10]))
        if len(muted_channels) > 10:
            embed.add_field(name="Note", value=f"And {len(muted_channels) - 10} more channels...")
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message(
            get_text(str(interaction.guild.id), "user_not_muted"),
            ephemeral=True
        )

# YENİ KOMUT: Punishment Users
@bot.tree.command(name="punishment-users", description="Show all punished users in the server")
@has_command_permission('punishment-users')
async def punishment_users(interaction: discord.Interaction):
    guild_id = interaction.guild.id
    punished_users = []
    
    for user_id, punishments in bot.punishment_users.items():
        for punishment_id, punishment_data in punishments.items():
            if punishment_data['guild_id'] == guild_id:
                punished_users.append((user_id, punishment_data))
                break  # Sadece bir kere ekle
    
    if not punished_users:
        await interaction.response.send_message(
            get_text(str(guild_id), "no_punishments")
        )
        return
    
    embed = discord.Embed(
        title=get_text(str(guild_id), "punishment_users"),
        color=0xff0000
    )
    
    for user_id, punishment_data in punished_users[:15]:  # İlk 15 kullanıcıyı göster
        try:
            user = await bot.fetch_user(int(user_id))
            user_display = f"{user.display_name} ({user.id})"
        except:
            user_display = f"Unknown User ({user_id})"
        
        embed.add_field(
            name=user_display,
            value=get_text(
                str(guild_id), 
                "punishment_entry",
                user=user_display,
                type=punishment_data['type'],
                duration=punishment_data['duration'],
                reason=punishment_data['reason']
            ),
            inline=False
        )
    
    if len(punished_users) > 15:
        embed.set_footer(text=f"And {len(punished_users) - 15} more users...")
    
    await interaction.response.send_message(embed=embed)

# Write-for Komutu
@bot.tree.command(name="write-for", description="Send a message as another user (requires manage server permission)")
@has_manage_guild_permission()
async def write_for(interaction: discord.Interaction, user: discord.Member, message: str, channel: Optional[discord.TextChannel] = None):
    target_channel = channel or interaction.channel

    webhooks = await target_channel.webhooks()
    webhook = None
    for wh in webhooks:
        if wh.user == bot.user:
            webhook = wh
            break

    if not webhook:
        webhook = await target_channel.create_webhook(name="Sampy Bot Webhook")

    await webhook.send(
        content=message,
        username=user.display_name,
        avatar_url=user.display_avatar.url,
        allowed_mentions=discord.AllowedMentions.all()
    )

    await interaction.response.send_message(f"✅ Message sent in {target_channel.mention} as {user.mention}", ephemeral=True)

# Komut Yetki Setup Komutu - 1
@bot.tree.command(name="command-permission-setup-1", description="Set command permissions part 1 (server owner only)")
@is_server_owner()
async def command_permission_setup_1(interaction: discord.Interaction):
    view = CommandPermissionView1(bot, str(interaction.guild.id))
    await interaction.response.send_message(
        "🛠️ **Command Permission Settings (Part 1)**\nSelect the command you want to configure:",
        view=view,
        ephemeral=True
    )

# Komut Yetki Setup Komutu - 2
@bot.tree.command(name="command-permission-setup-2", description="Set command permissions part 2 (server owner only)")
@is_server_owner()
async def command_permission_setup_2(interaction: discord.Interaction):
    view = CommandPermissionView2(bot, str(interaction.guild.id))
    await interaction.response.send_message(
        "🛠️ **Command Permission Settings (Part 2)**\nSelect the command you want to configure:",
        view=view,
        ephemeral=True
    )

# Sayı Tahmini Oyunu Komutu
@bot.tree.command(name="number-guessing-game", description="Play number guessing game")
async def number_game(
    interaction: discord.Interaction, 
    action: str,
    user: discord.Member,
    sampy_coin_amount: Optional[int] = None,
    number: Optional[int] = None
):
    if action == "send":
        if sampy_coin_amount is None or number is None:
            await interaction.response.send_message("❌ Amount and number required for send action!", ephemeral=True)
            return
        
        if sampy_coin_amount <= 0:
            await interaction.response.send_message("❌ Invalid amount!", ephemeral=True)
            return
        
        if number < 1 or number > 10:
            await interaction.response.send_message("❌ Number must be between 1-10!", ephemeral=True)
            return
        
        user_coins = bot.coins_data.get(str(interaction.user.id), 0)
        if user_coins < sampy_coin_amount:
            await interaction.response.send_message("❌ Not enough Sampy Coin!", ephemeral=True)
            return
        
        bot.coins_data[str(interaction.user.id)] = user_coins - sampy_coin_amount
        bot.save_json(bot.coins_data, bot.coins_file)
        
        game_id = str(random.randint(100000, 999999))
        
        bot.number_games[game_id] = {
            "creator": interaction.user.id,
            "target": user.id,
            "bet_amount": sampy_coin_amount,
            "number": number,
            "status": "waiting_accept"
        }
        bot.save_json(bot.number_games, "number_games.json")
        
        embed = discord.Embed(
            title="🎯 Number Guessing Game Invite!",
            description=f"{user.mention}, {interaction.user.mention} sent you a number guessing game invite!",
            color=0x7289da
        )
        embed.add_field(name="Bet Amount", value=f"{sampy_coin_amount} Sampy Coin", inline=True)
        embed.add_field(name="Prize", value=f"{int(sampy_coin_amount * 1.8)} Sampy Coin", inline=True)
        embed.add_field(name="Rules", value="A number between 1-10 has been chosen. Guess correctly to win!", inline=False)
        
        view = NumberGameView(bot, game_id, interaction.user, user, sampy_coin_amount, number)
        await interaction.response.send_message(embed=embed, view=view)
    
    elif action == "accept":
        await interaction.response.send_message("❌ Accept action must be done through invite!", ephemeral=True)
    
    elif action == "reject":
        await interaction.response.send_message("❌ Reject action must be done through invite!", ephemeral=True)
    
    else:
        await interaction.response.send_message("❌ Invalid action! (send/accept/reject)", ephemeral=True)

# IP Ban Komutu
@bot.tree.command(name="ipban", description="IP ban user")
@has_command_permission('ban')
async def ipban(
    interaction: discord.Interaction, 
    user: discord.Member,
    duration: Optional[str] = None,
    reason: Optional[str] = "No reason provided"
):
    try:
        await user.ban(reason=f"IP Ban - {reason}")
        
        # Punishment kaydı ekle
        add_punishment(
            str(user.id), 
            "ban", 
            interaction.guild.id, 
            reason, 
            duration, 
            interaction.user.id
        )
        
        embed = discord.Embed(
            title="🔒 IP Ban Applied!",
            description=f"{user.mention} IP banned!",
            color=0xff0000
        )
        embed.add_field(name="Reason", value=reason, inline=False)
        
        if duration:
            embed.add_field(name="Duration", value=duration, inline=True)
        
        embed.set_footer(text=f"Action by: {interaction.user.display_name}")
        await interaction.response.send_message(embed=embed)
        
        await send_mod_log(
            interaction.guild, 
            "IP Ban", 
            user, 
            interaction.user, 
            reason=reason, 
            duration=duration
        )
        
        if duration:
            duration_seconds = parse_time(duration)
            await asyncio.sleep(duration_seconds)
            await interaction.guild.unban(user)
            
    except Exception as e:
        await interaction.response.send_message(f"❌ IP Ban failed: {str(e)}", ephemeral=True)

# IP Mute Komutu
@bot.tree.command(name="ipmute", description="IP mute user")
@has_command_permission('mute')
async def ipmute(
    interaction: discord.Interaction, 
    user: discord.Member,
    duration: Optional[str] = None,
    reason: Optional[str] = "No reason provided"
):
    try:
        for channel in interaction.guild.channels:
            if isinstance(channel, (discord.TextChannel, discord.VoiceChannel)):
                await channel.set_permissions(user, send_messages=False, speak=False)
        
        # Punishment kaydı ekle
        add_punishment(
            str(user.id), 
            "mute", 
            interaction.guild.id, 
            reason, 
            duration, 
            interaction.user.id
        )
        
        embed = discord.Embed(
            title="🔇 IP Mute Applied!",
            description=f"{user.mention} IP muted!",
            color=0xff0000
        )
        embed.add_field(name="Reason", value=reason, inline=False)
        
        if duration:
            embed.add_field(name="Duration", value=duration, inline=True)
        
        embed.set_footer(text=f"Action by: {interaction.user.display_name}")
        await interaction.response.send_message(embed=embed)
        
        await send_mod_log(
            interaction.guild, 
            "IP Mute", 
            user, 
            interaction.user, 
            reason=reason, 
            duration=duration
        )
        
        if duration:
            duration_seconds = parse_time(duration)
            await asyncio.sleep(duration_seconds)
            for channel in interaction.guild.channels:
                if isinstance(channel, (discord.TextChannel, discord.VoiceChannel)):
                    await channel.set_permissions(user, overwrite=None)
                    
    except Exception as e:
        await interaction.response.send_message(f"❌ IP Mute failed: {str(e)}", ephemeral=True)

# Çekiliş Komutları
@bot.tree.command(name="giveaway-create", description="Create giveaway")
@has_command_permission('giveaway')
async def giveaway_create(interaction: discord.Interaction, duration: str, winner_count: int, prize: str, channel: Optional[discord.TextChannel] = None):
    try:
        duration_seconds = parse_time(duration)
    except:
        await interaction.response.send_message("❌ Invalid duration format! Example: 10s, 5m, 1h, 7d, 2w", ephemeral=True)
        return

    end_time = datetime.datetime.now() + datetime.timedelta(seconds=duration_seconds)
    
    target_channel = channel or interaction.channel
    
    embed = discord.Embed(
        title="🎉 GIVEAWAY 🎉",
        description=f"**Prize:** {prize}\n**Winner Count:** {winner_count}\n**Ends:** <t:{int(end_time.timestamp())}:R> (<t:{int(end_time.timestamp())}:F>)",
        color=0x00ff00
    )
    embed.add_field(name="Participants", value="0", inline=True)
    embed.set_footer(text=f"Giveaway by: {interaction.user.display_name}")
    
    await interaction.response.send_message(f"✅ Giveaway created in {target_channel.mention}!", ephemeral=True)
    message = await target_channel.send(embed=embed)
    
    giveaway_id = str(message.id)
    bot.giveaways_data[giveaway_id] = {
        "guild_id": interaction.guild.id,
        "channel_id": target_channel.id,
        "end_time": end_time.isoformat(),
        "prize": prize,
        "winners": winner_count,
        "host": interaction.user.id,
        "creator": interaction.user.id,
        "participants": []
    }
    bot.save_json(bot.giveaways_data, bot.giveaways_file)
    
    await message.add_reaction("🎉")

@bot.tree.command(name="giveaway-end", description="End giveaway early")
@has_command_permission('giveaway')
async def giveaway_end(interaction: discord.Interaction, message_id: str):
    if message_id in bot.giveaways_data:
        await bot.end_giveaway(message_id)
        await interaction.response.send_message("✅ Giveaway ended!", ephemeral=True)
    else:
        await interaction.response.send_message("❌ Giveaway not found!", ephemeral=True)

@bot.tree.command(name="giveaway-reroll", description="Reroll giveaway")
@has_command_permission('giveaway')
async def giveaway_reroll(interaction: discord.Interaction, message_id: str):
    if message_id not in bot.giveaways_data:
        await interaction.response.send_message("❌ Giveaway not found!", ephemeral=True)
        return

    data = bot.giveaways_data[message_id]
    channel = bot.get_channel(data["channel_id"])
    
    try:
        message = await channel.fetch_message(int(message_id))
        reaction = next((r for r in message.reactions if str(r.emoji) == "🎉"), None)
        
        if not reaction:
            await interaction.response.send_message("❌ No participation in this giveaway!", ephemeral=True)
            return

        users = [user async for user in reaction.users() if not user.bot]
        
        if len(users) < data["winners"]:
            winners = users
        else:
            winners = random.sample(users, data["winners"])
        
        winners_mention = ", ".join(winner.mention for winner in winners)
        await interaction.response.send_message(f"🎉 New winners: {winners_mention}")
    except:
        await interaction.response.send_message("❌ Message not found!", ephemeral=True)

# Mute/Unmute Channel Komutları
@bot.tree.command(name="mutechannel", description="Mute channel")
@has_manage_guild_permission()
async def mutechannel(
    interaction: discord.Interaction, 
    channel: Optional[discord.TextChannel] = None,
    duration: Optional[str] = None,
    reason: Optional[str] = "No reason provided"
):
    if channel is None:
        channel = interaction.channel
    
    mute_duration = None
    end_time = None
    
    if duration:
        try:
            if duration.endswith('s'):
                mute_duration = int(duration[:-1])
            elif duration.endswith('m'):
                mute_duration = int(duration[:-1]) * 60
            elif duration.endswith('h'):
                mute_duration = int(duration[:-1]) * 3600
            elif duration.endswith('d'):
                mute_duration = int(duration[:-1]) * 86400
            else:
                mute_duration = int(duration)
        except ValueError:
            await interaction.response.send_message("❌ Invalid duration format! Example: 30s, 10m, 2h, 1d", ephemeral=True)
            return
        
        end_time = datetime.datetime.now() + datetime.timedelta(seconds=mute_duration)
    
    overwrite = channel.overwrites_for(interaction.guild.default_role)
    overwrite.send_messages = False
    await channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
    
    embed = discord.Embed(
        title="🔇 Channel Muted",
        description=f"{channel.mention} channel muted.",
        color=discord.Color.red()
    )
    
    if mute_duration:
        embed.add_field(name="⏰ Duration", value=f"`{duration}`", inline=True)
    
    embed.add_field(name="📝 Reason", value=reason, inline=False)
    embed.set_footer(text=f"Action by: {interaction.user.display_name}")
    
    await interaction.response.send_message(embed=embed)
    
    await send_mod_log(
        interaction.guild, 
        "Channel Mute", 
        channel, 
        interaction.user, 
        reason=reason, 
        duration=duration
    )
    
    if mute_duration:
        await asyncio.sleep(mute_duration)
        overwrite.send_messages = None
        await channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)

@bot.tree.command(name="unmutechannel", description="Unmute channel")
@has_manage_guild_permission()
async def unmutechannel(
    interaction: discord.Interaction, 
    channel: Optional[discord.TextChannel] = None,
    reason: Optional[str] = "No reason provided"
):
    if channel is None:
        channel = interaction.channel
    
    overwrite = channel.overwrites_for(interaction.guild.default_role)
    overwrite.send_messages = None
    await channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
    
    embed = discord.Embed(
        title="🔊 Channel Unmuted",
        description=f"{channel.mention} channel unmuted.",
        color=discord.Color.green()
    )
    embed.add_field(name="📝 Reason", value=reason, inline=False)
    embed.set_footer(text=f"Action by: {interaction.user.display_name}")
    
    await interaction.response.send_message(embed=embed)
    
    await send_mod_log(
        interaction.guild, 
        "Channel Unmute", 
        channel, 
        interaction.user, 
        reason=reason
    )

# Buton Rol Sistemi
@bot.tree.command(name="button-role-system-setup", description="Setup button role system")
@has_command_permission('button-role-system-setup')
async def button_role_system(
    interaction: discord.Interaction, 
    role_name: str, 
    color: Optional[str] = "default"
):
    COLOR_MAP = {
        "red": discord.Color.red(),
        "green": discord.Color.green(),
        "blue": discord.Color.blue(),
        "yellow": discord.Color.gold(),
        "purple": discord.Color.purple(),
        "orange": discord.Color.orange(),
        "pink": discord.Color.magenta(),
        "default": discord.Color.default()
    }
    
    if color.startswith("#") and len(color) == 7:
        try:
            color_val = discord.Color(int(color[1:], 16))
        except:
            color_val = discord.Color.default()
    else:
        color_val = COLOR_MAP.get(color.lower(), discord.Color.default())
    
    role = discord.utils.get(interaction.guild.roles, name=role_name)
    if not role:
        try:
            role = await interaction.guild.create_role(
                name=role_name, 
                color=color_val, 
                mentionable=True,
                reason=f"Button role system - {interaction.user}"
            )
        except discord.Forbidden:
            await interaction.response.send_message("❌ I don't have permission to create roles!", ephemeral=True)
            return
    
    embed = discord.Embed(
        title="🎯 Button Role System",
        description=f"Click the button below to get/remove the **{role_name}** role!",
        color=color_val
    )
    
    view = RoleButtonView(role.id)
    await interaction.response.send_message(embed=embed, view=view)
    
    bot.button_roles_data[str(interaction.channel_id)] = role.id
    bot.save_json(bot.button_roles_data, bot.button_roles_file)

# Gelişmiş Clear Komutu
@bot.tree.command(name="clear", description="Clear messages (up to 1000 or all)")
@is_bot_owner()
async def clear(interaction: discord.Interaction, amount: str, reason: Optional[str] = "No reason provided"):
    await interaction.response.defer(ephemeral=True)
    
    try:
        clear_id = str(random.randint(1000000000, 9999999999))
        
        if amount.lower() == "all":
            deleted = await interaction.channel.purge(limit=1000)
            message_count = len(deleted)
        else:
            amount_num = int(amount)
            if amount_num > 1000:
                await interaction.followup.send("❌ You can only delete up to 1000 messages!", ephemeral=True)
                return
            deleted = await interaction.channel.purge(limit=amount_num)
            message_count = len(deleted)
        
        transcript_content = f"Deleted Messages Transcript - ID: {clear_id}\n"
        transcript_content += f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        transcript_content += f"Channel: #{interaction.channel.name}\n"
        transcript_content += f"Deleted Message Count: {message_count}\n"
        transcript_content += f"Reason: {reason}\n"
        transcript_content += f"Action By: {interaction.user} ({interaction.user.id})\n"
        transcript_content += "="*50 + "\n\n"
        
        for i, message in enumerate(deleted, 1):
            transcript_content += f"{i}. [{message.created_at.strftime('%H:%M:%S')}] {message.author}: {message.content}\n"
            if message.attachments:
                transcript_content += f"   📎 Attachments: {', '.join([att.url for att in message.attachments])}\n"
            transcript_content += "\n"
        
        transcript_file = discord.File(
            io.BytesIO(transcript_content.encode('utf-8')),
            filename=f"transcript_{clear_id}.txt"
        )
        
        try:
            guild_owner = interaction.guild.owner
            if guild_owner:
                embed = discord.Embed(
                    title="🗑️ Message Clear Log",
                    description=f"Messages cleared by **{interaction.user.mention}**",
                    color=0xff0000,
                    timestamp=datetime.datetime.now()
                )
                embed.add_field(name="Channel", value=interaction.channel.mention, inline=True)
                embed.add_field(name="Deleted Messages", value=f"{message_count} items", inline=True)
                embed.add_field(name="Type", value="All messages" if amount.lower() == "all" else f"{amount} messages", inline=True)
                embed.add_field(name="Reason", value=reason, inline=False)
                embed.add_field(name="ID", value=f"`{clear_id}`", inline=True)
                
                await guild_owner.send(embed=embed, file=transcript_file)
        except Exception as e:
            print(f"Couldn't send log to server owner: {e}")
        
        if str(interaction.guild.id) not in bot.message_logs_data:
            bot.message_logs_data[str(interaction.guild.id)] = {}
        
        bot.message_logs_data[str(interaction.guild.id)][clear_id] = {
            "type": "clear",
            "channel_id": interaction.channel.id,
            "channel_name": interaction.channel.name,
            "moderator": str(interaction.user),
            "moderator_id": interaction.user.id,
            "message_count": message_count,
            "reason": reason,
            "timestamp": datetime.datetime.now().isoformat(),
            "transcript": transcript_content[:2000] + "..." if len(transcript_content) > 2000 else transcript_content
        }
        bot.save_json(bot.message_logs_data, bot.message_logs_file)
        
        await interaction.followup.send(
            f"✅ **{message_count}** messages deleted! {'(All messages cleared)' if amount.lower() == 'all' else ''}\n"
            f"**ID:** `{clear_id}`\n"
            f"**Reason:** {reason}",
            ephemeral=True
        )
        
    except ValueError:
        await interaction.followup.send("❌ Invalid amount! Enter a number or 'all'.", ephemeral=True)
    except Exception as e:
        await interaction.followup.send(f"❌ Delete failed: {str(e)}", ephemeral=True)

# Silinen Mesajlar List Komutu
@bot.tree.command(name="deleted-messages-list", description="Show list of deleted messages")
async def deleted_messages_list(interaction: discord.Interaction, message_delete_id: str):
    if not (is_bot_owner()(interaction) or interaction.user == interaction.guild.owner):
        await interaction.response.send_message(get_text(str(interaction.guild.id), "no_permission"), ephemeral=True)
        return
    
    guild_id = str(interaction.guild.id)
    
    if guild_id not in bot.message_logs_data or message_delete_id not in bot.message_logs_data[guild_id]:
        await interaction.response.send_message("❌ No delete record found with that ID!", ephemeral=True)
        return
    
    clear_data = bot.message_logs_data[guild_id][message_delete_id]
    
    embed = discord.Embed(
        title=f"🗑️ Deleted Messages - ID: {message_delete_id}",
        color=0xff0000,
        timestamp=datetime.datetime.fromisoformat(clear_data["timestamp"])
    )
    
    embed.add_field(name="Channel", value=f"<#{clear_data['channel_id']}> ({clear_data['channel_name']})", inline=True)
    embed.add_field(name="Deleted Messages", value=clear_data["message_count"], inline=True)
    embed.add_field(name="Moderator", value=clear_data["moderator"], inline=True)
    embed.add_field(name="Reason", value=clear_data["reason"], inline=False)
    
    if "transcript" in clear_data:
        transcript_file = discord.File(
            io.BytesIO(clear_data["transcript"].encode('utf-8')),
            filename=f"transcript_{message_delete_id}.txt"
        )
        await interaction.response.send_message(embed=embed, file=transcript_file, ephemeral=True)
    else:
        await interaction.response.send_message(embed=embed, ephemeral=True)

# Admin Panel Komutu
@bot.tree.command(name="admin-panel", description="Bot management panel (bot owner only)")
@is_bot_owner()
async def admin_panel(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🛠️ Admin Panel",
        description="Manage the bot with the buttons below:",
        color=0x7289da
    )
    embed.add_field(name="🔴 Shutdown Bot", value="Completely shuts down the bot", inline=True)
    embed.add_field(name="📋 List Servers", value="Shows servers the bot is in", inline=True)
    embed.add_field(name="📊 Bot Status", value="Shows bot statistics", inline=True)
    embed.add_field(name="🔗 Create Invites", value="Create invite links for servers", inline=True)
    embed.add_field(name="👑 Manage Admin Roles", value="Manage admin roles for servers", inline=True)
    embed.add_field(name="👋 Leave Server", value="Leave selected server", inline=True)
    
    view = AdvancedAdminPanelView(bot)
    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

# Input-Output Channel Komutu
@bot.tree.command(name="input-output-channel-set", description="Set join/leave notification channel")
@is_server_owner()
async def input_output_channel_set(interaction: discord.Interaction, channel: Optional[discord.TextChannel] = None):
    guild_id = str(interaction.guild.id)
    
    if channel:
        bot.io_channels[guild_id] = channel.id
        await interaction.response.send_message(
            get_text(guild_id, "io_channel_set", channel=channel.mention),
            ephemeral=True
        )
    else:
        if guild_id in bot.io_channels:
            del bot.io_channels[guild_id]
            await interaction.response.send_message(
                "✅ IO channel cleared (using default system channel)",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                "❌ No IO channel set for this server!",
                ephemeral=True
            )
    
    bot.save_json(bot.io_channels, bot.io_channels_file)

# Dil Değiştirme Komutu
@bot.tree.command(name="setlang", description="Change bot language (server owner only)")
@is_server_owner()
async def setlang(interaction: discord.Interaction):
    view = LanguageView(bot, str(interaction.guild.id))
    await interaction.response.send_message(
        "🌐 **Language Settings**\nSelect your preferred language:",
        view=view,
        ephemeral=True
    )

# Level Komutları
@bot.tree.command(name="level", description="Check your or another user's level")
async def level(interaction: discord.Interaction, user: Optional[discord.Member] = None):
    target = user or interaction.user
    guild_id = str(interaction.guild.id)
    user_id = str(target.id)
    
    if guild_id in bot.level_data and user_id in bot.level_data[guild_id]:
        data = bot.level_data[guild_id][user_id]
        messages = data["messages"]
        level = data["level"]
        await interaction.response.send_message(
            get_text(guild_id, "level", user=target.mention, level=level, messages=messages)
        )
    else:
        await interaction.response.send_message(
            f"{target.mention} has no messages yet!",
            ephemeral=True
        )

@bot.tree.command(name="leveltop", description="Show top 10 users by level")
async def leveltop(interaction: discord.Interaction):
    guild_id = str(interaction.guild.id)
    
    if guild_id not in bot.level_data or not bot.level_data[guild_id]:
        await interaction.response.send_message("No level data for this server yet!")
        return

    users = []
    for user_id, data in bot.level_data[guild_id].items():
        user = interaction.guild.get_member(int(user_id))
        if user:
            users.append((user, data["level"], data["messages"]))

    users.sort(key=lambda x: x[1], reverse=True)
    top10 = users[:10]

    embed = discord.Embed(
        title=get_text(guild_id, "level_top"),
        color=0x00ff00
    )
    
    for i, (user, level, messages) in enumerate(top10, 1):
        embed.add_field(
            name=f"{i}. {user.display_name}", 
            value=f"Level: {level} | Messages: {messages}", 
            inline=False
        )

    await interaction.response.send_message(embed=embed)

# Moderasyon Komutları
@bot.tree.command(name="kick", description="Kick user from server")
@has_command_permission('kick')
async def kick(interaction: discord.Interaction, user: discord.Member, reason: Optional[str] = "No reason provided"):
    try:
        await user.kick(reason=reason)
        
        # Punishment kaydı ekle
        add_punishment(
            str(user.id), 
            "kick", 
            interaction.guild.id, 
            reason, 
            None, 
            interaction.user.id
        )
        
        await interaction.response.send_message(
            get_text(str(interaction.guild.id), "kicked", user=user.mention)
        )
        
        await send_mod_log(
            interaction.guild, 
            "Kick", 
            user, 
            interaction.user, 
            reason=reason
        )
    except Exception as e:
        await interaction.response.send_message(f"❌ Kick failed: {str(e)}", ephemeral=True)

@bot.tree.command(name="ban", description="Ban user from server")
@has_command_permission('ban')
async def ban(
    interaction: discord.Interaction, 
    user: discord.Member, 
    duration: Optional[str] = None,
    reason: Optional[str] = "No reason provided"
):
    try:
        await user.ban(reason=reason)
        
        # Punishment kaydı ekle
        add_punishment(
            str(user.id), 
            "ban", 
            interaction.guild.id, 
            reason, 
            duration, 
            interaction.user.id
        )
        
        embed = discord.Embed(
            title="🔨 Ban Applied!",
            description=get_text(str(interaction.guild.id), "banned", user=user.mention),
            color=0xff0000
        )
        embed.add_field(name="Reason", value=reason, inline=False)
        
        if duration:
            embed.add_field(name="Duration", value=duration, inline=True)
        
        embed.set_footer(text=f"Action by: {interaction.user.display_name}")
        await interaction.response.send_message(embed=embed)
        
        await send_mod_log(
            interaction.guild, 
            "Ban", 
            user, 
            interaction.user, 
            reason=reason, 
            duration=duration
        )
        
        if duration:
            duration_seconds = parse_time(duration)
            await asyncio.sleep(duration_seconds)
            await interaction.guild.unban(user)
            
    except Exception as e:
        await interaction.response.send_message(f"❌ Ban failed: {str(e)}", ephemeral=True)

@bot.tree.command(name="unban", description="Unban user")
@has_command_permission('ban')
async def unban(interaction: discord.Interaction, user_id: str, reason: Optional[str] = "No reason provided"):
    try:
        user = await bot.fetch_user(int(user_id))
        await interaction.guild.unban(user, reason=reason)
        
        # Punishment kaydını kaldır
        if user_id in bot.punishment_users:
            for punishment_id, punishment_data in list(bot.punishment_users[user_id].items()):
                if punishment_data['type'] == 'ban' and punishment_data['guild_id'] == interaction.guild.id:
                    del bot.punishment_users[user_id][punishment_id]
                    if not bot.punishment_users[user_id]:
                        del bot.punishment_users[user_id]
                    bot.save_json(bot.punishment_users, bot.punishment_users_file)
                    break
        
        await interaction.response.send_message(
            get_text(str(interaction.guild.id), "unbanned", user=user.mention)
        )
        
        await send_mod_log(
            interaction.guild, 
            "Unban", 
            user, 
            interaction.user, 
            reason=reason
        )
    except Exception as e:
        await interaction.response.send_message(f"❌ Unban failed: {str(e)}", ephemeral=True)

@bot.tree.command(name="timeout", description="Timeout user")
@has_command_permission('timeout')
async def timeout(
    interaction: discord.Interaction, 
    user: discord.Member, 
    duration: str, 
    reason: Optional[str] = "No reason provided"
):
    try:
        duration_seconds = parse_time(duration)
        until = datetime.datetime.now() + datetime.timedelta(seconds=duration_seconds)
        await user.timeout(until, reason=reason)
        
        # Punishment kaydı ekle
        add_punishment(
            str(user.id), 
            "timeout", 
            interaction.guild.id, 
            reason, 
            duration, 
            interaction.user.id
        )
        
        await interaction.response.send_message(
            get_text(str(interaction.guild.id), "timed_out", user=user.mention)
        )
        
        await send_mod_log(
            interaction.guild, 
            "Timeout", 
            user, 
            interaction.user, 
            reason=reason,
            duration=duration
        )
    except Exception as e:
        await interaction.response.send_message(f"❌ Timeout failed: {str(e)}", ephemeral=True)

@bot.tree.command(name="mute", description="Mute user")
@has_command_permission('mute')
async def mute(
    interaction: discord.Interaction, 
    user: discord.Member, 
    duration: Optional[str] = None, 
    reason: Optional[str] = "No reason provided"
):
    try:
        for channel in interaction.guild.channels:
            if isinstance(channel, discord.TextChannel):
                await channel.set_permissions(user, send_messages=False)
        
        # Punishment kaydı ekle
        add_punishment(
            str(user.id), 
            "mute", 
            interaction.guild.id, 
            reason, 
            duration, 
            interaction.user.id
        )
        
        embed = discord.Embed(
            title="🔇 Mute Applied!",
            description=get_text(str(interaction.guild.id), "muted", user=user.mention),
            color=0xff0000
        )
        embed.add_field(name="Reason", value=reason, inline=False)
        
        if duration:
            embed.add_field(name="Duration", value=duration, inline=True)
        
        embed.set_footer(text=f"Action by: {interaction.user.display_name}")
        await interaction.response.send_message(embed=embed)
        
        await send_mod_log(
            interaction.guild, 
            "Mute", 
            user, 
            interaction.user, 
            reason=reason,
            duration=duration
        )
        
        if duration:
            duration_seconds = parse_time(duration)
            await asyncio.sleep(duration_seconds)
            for channel in interaction.guild.channels:
                if isinstance(channel, discord.TextChannel):
                    await channel.set_permissions(user, overwrite=None)
                    
    except Exception as e:
        await interaction.response.send_message(f"❌ Mute failed: {str(e)}", ephemeral=True)

# Sampy Coin Sistemi
def get_user_coins(user_id: str) -> int:
    return bot.coins_data.get(user_id, 0)

def update_user_coins(user_id: str, amount: int):
    bot.coins_data[user_id] = get_user_coins(user_id) + amount
    bot.save_json(bot.coins_data, bot.coins_file)

@bot.tree.command(name="sampy-coin", description="Show your Sampy Coin balance")
async def sampy_coin(interaction: discord.Interaction, user: Optional[discord.Member] = None):
    target_user = user or interaction.user
    coins = get_user_coins(str(target_user.id))
    await interaction.response.send_message(
        get_text(str(interaction.guild.id), "coins", user=target_user.mention, amount=coins)
    )

@bot.tree.command(name="sampy-coin-take", description="Take Sampy Coin from user")
@is_bot_owner()
async def sampy_coin_take(interaction: discord.Interaction, target: str, amount: int):
    # Target can be user ID or mention
    if target.isdigit():
        user_id = target
    else:
        # Extract user ID from mention
        user_id = target.strip('<@!>')
    
    user_coins = get_user_coins(user_id)
    
    if user_coins < amount:
        await interaction.response.send_message(
            f"❌ User doesn't have enough Sampy Coin! Current: {user_coins}",
            ephemeral=True
        )
        return
    
    update_user_coins(user_id, -amount)
    await interaction.response.send_message(
        f"✅ {amount} Sampy Coin taken from <@{user_id}>. New balance: {get_user_coins(user_id)}",
        ephemeral=True
    )

@bot.tree.command(name="daily", description="Get daily Sampy Coin (every 12 hours)")
async def daily(interaction: discord.Interaction):
    view = AdvancedDailyView(bot, str(interaction.user.id))
    await interaction.response.send_message(
        "🎁 **Daily Reward**\nClaim your **750 Sampy Coin** every 12 hours!",
        view=view,
        ephemeral=True
    )

@bot.tree.command(name="sampy-coin-transfer", description="Transfer Sampy Coin to another user")
async def sampy_coin_transfer(interaction: discord.Interaction, target: str, amount: Optional[str] = None):
    from_user_id = str(interaction.user.id)
    
    # Target can be user ID or mention
    if target.isdigit():
        to_user_id = target
    else:
        # Extract user ID from mention
        to_user_id = target.strip('<@!>')
    
    from_coins = get_user_coins(from_user_id)
    
    if amount is None or amount.lower() == "all":
        transfer_amount = from_coins
    else:
        try:
            transfer_amount = int(amount)
        except:
            await interaction.response.send_message("❌ Invalid amount! Enter a number or 'all'.", ephemeral=True)
            return
    
    if transfer_amount <= 0:
        await interaction.response.send_message("❌ Invalid amount!", ephemeral=True)
        return
        
    if from_coins < transfer_amount:
        await interaction.response.send_message("❌ Not enough Sampy Coin!", ephemeral=True)
        return
    
    # Check if target user exists
    try:
        target_user = await bot.fetch_user(int(to_user_id))
        if target_user.bot:
            await interaction.response.send_message("❌ You can't transfer coins to bots!", ephemeral=True)
            return
    except:
        await interaction.response.send_message("❌ Invalid user!", ephemeral=True)
        return
    
    update_user_coins(from_user_id, -transfer_amount)
    update_user_coins(to_user_id, transfer_amount)
    
    await interaction.response.send_message(
        get_text(str(interaction.guild.id), "coins_transfer", user=f"<@{to_user_id}>", amount=transfer_amount)
    )

# Market Sistemi
@bot.tree.command(name="market-setup", description="Configure market settings")
@is_server_owner()
async def market_setup(
    interaction: discord.Interaction, 
    special_role_3d: int, 
    special_role_7d: int, 
    vip_30d: int, 
    megavip_30d: int, 
    ultravip_30d: int, 
    supervip_30d: int, 
    supervip_plus_30d: int,
    sampy_premium_30d: int
):
    guild_id = str(interaction.guild_id)
    
    bot.market_data[guild_id] = {
        "special_role_3d": special_role_3d,
        "special_role_7d": special_role_7d,
        "vip_30d": vip_30d,
        "megavip_30d": megavip_30d,
        "ultravip_30d": ultravip_30d,
        "supervip_30d": supervip_30d,
        "supervip_plus_30d": supervip_plus_30d,
        "sampy_premium_30d": sampy_premium_30d
    }
    
    bot.save_json(bot.market_data, bot.market_file)
    await interaction.response.send_message("✅ Market settings updated successfully!", ephemeral=True)

@bot.tree.command(name="market", description="View market products")
async def market(interaction: discord.Interaction):
    guild_id = str(interaction.guild_id)
    
    if guild_id not in bot.market_data:
        await interaction.response.send_message(
            "❌ Market not configured for this server! Server owner must use /market-setup.",
            ephemeral=True
        )
        return
    
    products = bot.market_data[guild_id]
    embed = discord.Embed(title=get_text(guild_id, "market"), color=0x00ff00)
    
    for product, price in products.items():
        product_name = get_text(guild_id, product.split('_')[0])
        duration = product.split('_')[1]
        embed.add_field(
            name=f"{product_name} ({duration})",
            value=f"{price} Sampy Coin 🪙",
            inline=False
        )
    
    embed.set_footer(text="Use /market-buy to purchase products!")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="market-buy", description="Buy product from market")
async def market_buy(interaction: discord.Interaction):
    guild_id = str(interaction.guild_id)
    
    if guild_id not in bot.market_data:
        await interaction.response.send_message(get_text(guild_id, "market_not_configured"), ephemeral=True)
        return
    
    view = MarketView(bot, guild_id)
    await interaction.response.send_message("🛒 **Select product to purchase:**", view=view, ephemeral=True)

# Ticket Sistemi
@bot.tree.command(name="ticket-open", description="Open new ticket")
async def ticket_open(interaction: discord.Interaction, name: str):
    guild = interaction.guild
    category = discord.utils.get(guild.categories, name="Tickets")
    
    if not category:
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True)
        }
        category = await guild.create_category("Tickets", overwrites=overwrites)
    
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
        guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
    }
    
    ticket_channel = await category.create_text_channel(
        name=f"ticket-{name}-{interaction.user.name}",
        overwrites=overwrites
    )
    
    bot.tickets_data[str(ticket_channel.id)] = {
        "user_id": interaction.user.id,
        "created_at": datetime.datetime.now().isoformat(),
        "name": name
    }
    bot.save_json(bot.tickets_data, bot.tickets_file)
    
    embed = discord.Embed(
        title=f"Ticket - {name}",
        description=f"Hello {interaction.user.mention}! Our support team will help you shortly.\n\nPlease describe your issue in detail.",
        color=0x00ff00
    )
    embed.set_footer(text="Use the button below to close the ticket")
    
    view = TicketView()
    await ticket_channel.send(embed=embed, view=view)
    await interaction.response.send_message(
        get_text(str(interaction.guild.id), "ticket_created", channel=ticket_channel.mention),
        ephemeral=True
    )

@bot.tree.command(name="ticket-close", description="Close ticket")
@has_command_permission('ticket-close')
async def ticket_close(interaction: discord.Interaction):
    if str(interaction.channel_id) not in bot.tickets_data:
        await interaction.response.send_message("❌ This is not a ticket channel!", ephemeral=True)
        return
    
    await interaction.response.send_message("⏳ Closing ticket in 5 seconds...")
    await asyncio.sleep(5)
    
    del bot.tickets_data[str(interaction.channel_id)]
    bot.save_json(bot.tickets_data, bot.tickets_file)
    
    await interaction.channel.delete()

# Redeem Code Sistemi
@bot.tree.command(name="redeem-code-create", description="Create new redeem code")
@is_bot_owner()
async def redeem_create(interaction: discord.Interaction, max_uses: int, amount: int):
    code = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=8))
    
    bot.redeem_data[code] = {
        "max_uses": max_uses,
        "uses": 0,
        "amount": amount,
        "created_by": interaction.user.id,
        "created_at": datetime.datetime.now().isoformat(),
        "active": True
    }
    
    bot.save_json(bot.redeem_data, bot.redeem_file)
    
    await interaction.response.send_message(
        f"✅ **Redeem Code Created!**\n"
        f"**Code:** `{code}`\n"
        f"**Amount:** {amount} Sampy Coin\n"
        f"**Max Uses:** {max_uses} people\n\n"
        f"To use: `/redeem-code {code}`",
        ephemeral=True
    )

@bot.tree.command(name="redeem-code-list", description="List active redeem codes")
@is_bot_owner()
async def redeem_list(interaction: discord.Interaction, server_id: Optional[str] = None):
    active_codes = {}
    for code, data in bot.redeem_data.items():
        if data.get("active", True) and data["uses"] < data["max_uses"]:
            active_codes[code] = data
    
    if not active_codes:
        await interaction.response.send_message("❌ No active redeem codes.", ephemeral=True)
        return
    
    embed = discord.Embed(title="🎁 Active Redeem Codes", color=0x00ff00)
    
    for code, data in active_codes.items():
        remaining_uses = data["max_uses"] - data["uses"]
        created_date = data["created_at"][:10] if "created_at" in data else "Unknown"
        
        embed.add_field(
            name=f"Code: `{code}`",
            value=f"Amount: {data['amount']} 🪙\nRemaining Uses: {remaining_uses}/{data['max_uses']}\nCreated: {created_date}",
            inline=False
        )
    
    embed.set_footer(text=f"Total {len(active_codes)} active codes")
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="redeem-code", description="Use redeem code")
async def redeem_use(interaction: discord.Interaction, code: str):
    code = code.upper()
    
    if code not in bot.redeem_data:
        await interaction.response.send_message("❌ Invalid redeem code!", ephemeral=True)
        return
    
    code_data = bot.redeem_data[code]
    
    if not code_data.get("active", True):
        await interaction.response.send_message("❌ This redeem code is not active!", ephemeral=True)
        return
    
    if code_data["uses"] >= code_data["max_uses"]:
        await interaction.response.send_message("❌ This redeem code has reached its usage limit!", ephemeral=True)
        return
    
    user_id = str(interaction.user.id)
    used_codes = bot.redeem_data.get("used_by", {}).get(code, [])
    
    if user_id in used_codes:
        await interaction.response.send_message("❌ You've already used this code!", ephemeral=True)
        return
    
    amount = code_data["amount"]
    update_user_coins(user_id, amount)
    
    bot.redeem_data[code]["uses"] += 1
    
    if "used_by" not in bot.redeem_data:
        bot.redeem_data["used_by"] = {}
    if code not in bot.redeem_data["used_by"]:
        bot.redeem_data["used_by"][code] = []
    
    bot.redeem_data["used_by"][code].append(user_id)
    bot.save_json(bot.redeem_data, bot.redeem_file)
    
    await interaction.response.send_message(
        f"🎉 **Redeem Code Successfully Used!**\n"
        f"**+{amount} Sampy Coin** added to your account!\n"
        f"New balance: **{get_user_coins(user_id)} Sampy Coin** 🪙"
    )

# Diğer komutlar
@bot.tree.command(name="cf", description="Coin flip game")
async def coin_flip(interaction: discord.Interaction, amount: str):
    user_id = str(interaction.user.id)
    user_coins = get_user_coins(user_id)
    
    if amount.lower() == "all":
        bet_amount = user_coins
    else:
        try:
            bet_amount = int(amount)
        except:
            await interaction.response.send_message("❌ Invalid amount! Enter a number or 'all'.", ephemeral=True)
            return
    
    if bet_amount <= 0:
        await interaction.response.send_message("❌ Invalid amount!", ephemeral=True)
        return
        
    if user_coins < bet_amount:
        await interaction.response.send_message("❌ Not enough Sampy Coin!", ephemeral=True)
        return
    
    result = random.choice(["Heads", "Tails"])
    win = random.choice([True, False])
    
    if win:
        update_user_coins(user_id, bet_amount)
        await interaction.response.send_message(
            f"🎲 **{result}**! You won! 🎉\n"
            f"**+{bet_amount} Sampy Coin** won!\n"
            f"New balance: **{get_user_coins(user_id)} Sampy Coin** 🪙"
        )
    else:
        update_user_coins(user_id, -bet_amount)
        await interaction.response.send_message(
            f"🎲 **{result}**! You lost! 😢\n"
            f"**-{bet_amount} Sampy Coin** lost!\n"
            f"New balance: **{get_user_coins(user_id)} Sampy Coin** 🪙"
        )

@bot.tree.command(name="server", description="Show server information")
async def server_info(interaction: discord.Interaction):
    guild = interaction.guild
    
    embed = discord.Embed(title=get_text(str(guild.id), "server_info"), color=0x7289da)
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
    
    embed.add_field(name="👥 Member Count", value=guild.member_count, inline=True)
    embed.add_field(name="📅 Creation Date", value=f"<t:{int(guild.created_at.timestamp())}:D>", inline=True)
    embed.add_field(name="👑 Server Owner", value=guild.owner.mention, inline=True)
    
    embed.add_field(name="📊 Channel Count", value=len(guild.channels), inline=True)
    embed.add_field(name="🎭 Role Count", value=len(guild.roles), inline=True)
    embed.add_field(name="🚀 Server Level", value=guild.premium_tier, inline=True)
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="ping", description="Show bot latency")
async def ping(interaction: discord.Interaction):
    latency = round(bot.latency * 1000)
    await interaction.response.send_message(
        get_text(str(interaction.guild.id), "ping", ms=latency),
        ephemeral=True
    )

@bot.tree.command(name="help", description="List all commands")
async def help_command(interaction: discord.Interaction):
    embed = discord.Embed(title="🤖 Sampy Bot - All Commands", color=0x7289da)
    
    embed.add_field(
        name="🎉 Giveaway Commands",
        value="• `/giveaway-create` - Start new giveaway\n• `/giveaway-end` - End giveaway early\n• `/giveaway-reroll` - Reroll new winners\n• `/giveaway-join-limit` - Set join limits\n• `/giveaway-join-limit-id` - Set limit by ID\n• `/giveaway-join-limit-reset` - Reset limits",
        inline=False
    )
    
    embed.add_field(
        name="🔇 Channel Management",
        value="• `/mutechannel` - Mute channel\n• `/unmutechannel` - Unmute channel",
        inline=False
    )
    
    embed.add_field(
        name="🎯 Button Role System", 
        value="• `/button-role-system-setup` - Setup button role system",
        inline=False
    )
    
    embed.add_field(
        name="🛡️ Moderation",
        value="• `/kick` - Kick user\n• `/ban` - Ban user\n• `/unban` - Unban user\n• `/timeout` - Timeout user\n• `/untimeout` - Remove timeout from user\n• `/mute` - Mute user\n• `/unmute` - Unmute user\n• `/ipban` - IP ban user\n• `/ipmute` - IP mute user\n• `/unipban` - Un-IP ban user\n• `/unipmute` - Un-IP mute user\n• `/checkban` - Check if user is banned\n• `/checkmute` - Check if user is muted\n• `/history` - Show user's punishment history\n• `/punishment-users` - Show all punished users\n• `/clear` - Clear messages (bot owner only)\n• `/warn` - Warn user\n• `/warn-remove` - Remove warning\n• `/warn-list` - Show warnings",
        inline=False
    )
    
    embed.add_field(
        name="🔒 Tag Block System",
        value="• `/tag-close-menu` - Block tags via menu\n• `/tag-close-id` - Block tags by ID\n• `/tag-close-list` - Show block list",
        inline=False
    )
    
    embed.add_field(
        name="🪙 Sampy Coin System",
        value="• `/sampy-coin` - Check balance\n• `/daily` - Get daily reward\n• `/sampy-coin-transfer` - Transfer coins\n• `/sampy-coin-take` - Take coins (bot owner only)",
        inline=False
    )
    
    embed.add_field(
        name="🏪 Market System",
        value="• `/market` - View products\n• `/market-setup` - Setup market\n• `/market-buy` - Buy products",
        inline=False
    )
    
    embed.add_field(
        name="🎫 Ticket System",
        value="• `/ticket-open` - Open new ticket\n• `/ticket-close` - Close ticket",
        inline=False
    )
    
    embed.add_field(
        name="🎁 Redeem Code",
        value="• `/redeem-code` - Use code\n• `/redeem-code-list` - List codes\n• `/redeem-code-create` - Create code",
        inline=False
    )
    
    embed.add_field(
        name="🎮 Games",
        value="• `/number-guessing-game` - Play number guessing game\n• `/cf` - Play coin flip",
        inline=False
    )
    
    embed.add_field(
        name="📊 Level System",
        value="• `/level` - Check level\n• `/leveltop` - Show leaderboard",
        inline=False
    )
    
    embed.add_field(
        name="🗑️ Deleted Messages",
        value="• `/deleted-messages-list` - Show deleted messages (bot owner and server owner)",
        inline=False
    )
    
    embed.add_field(
        name="✍️ Write For",
        value="• `/write-for` - Send message as another user (requires manage server permission)",
        inline=False
    )
    
    embed.add_field(
        name="📝 Application System",
        value="• `/authorized-application-setup` - Setup application system (server owner only)",
        inline=False
    )
    
    embed.add_field(
        name="🔄 Reset Channels",
        value="• `/reset-channels-message` - Delete all messages in all channels",
        inline=False
    )
    
    embed.add_field(
        name="🎥 YouTube System",
        value="• `/yt-video-channel-setup` - Setup YouTube notifications\n• `/yt-video-channel-reset` - Reset YouTube settings\n• `/get-yt-api-key` - Get API key guide",
        inline=False
    )
    
    embed.add_field(
        name="🤖 Auto Role System",
        value="• `/autorole` - Add/remove autorole\n• `/autorole-id` - Add/remove by ID\n• `/autorole-list` - Show autoroles",
        inline=False
    )
    
    embed.add_field(
        name="💾 Save Role Data",
        value="• `/save-role-data` - Save role data for server (bot owner only)",
        inline=False
    )
    
    embed.add_field(
        name="🎪 Temporary Room System",
        value="• `/temp-room-setup` - Setup temporary room system (server owner only)",
        inline=False
    )
    
    embed.add_field(
        name="🤖 AI Chat System",
        value="• `/tag-ai-chat-start` - Start AI chat\n• `/tag-ai-chat-stop` - Stop AI chat",
        inline=False
    )
    
    embed.add_field(
        name="🏗️ Server Setup",
        value="• `/server-setup` - Setup server channels (server owner only)",
        inline=False
    )
    
    embed.add_field(
        name="🛠️ Management Commands",
        value="• `/command-permission-setup-1` - Setup command permissions part 1 (server owner)\n• `/command-permission-setup-2` - Setup command permissions part 2 (server owner)\n• `/admin-panel` - Bot management panel (bot owner)\n• `/input-output-channel-set` - Set join/leave channel (server owner)\n• `/setlang` - Change bot language (server owner)",
        inline=False
    )
    
    embed.add_field(
        name="🔧 Other Commands",
        value="• `/server` - Server info\n• `/ping` - Bot latency\n• `/help` - This menu",
        inline=False
    )
    
    await interaction.response.send_message(embed=embed)

# Botu başlat
if __name__ == "__main__":
    while True:
        try:
            bot.run(TOKEN)
        except discord.errors.LoginFailure:
            print("❌ Invalid token! Please check your token.")
            break
        except Exception as e:
            print(f"❌ Bot crashed: {e}. Restarting in 5 seconds...")
            import time
            time.sleep(5)
            continue
        break
