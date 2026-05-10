#!/usr/bin/env python3
"""
Nablus Complaints Telegram Bot - Fixed Version
"""

import os
import logging
import json
from datetime import datetime
from typing import Optional, Dict, List

import firebase_admin
from firebase_admin import credentials, firestore
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# ===== Configuration =====
TELEGRAM_TOKEN = "8756259726:AAFojt3xGhcB3uLXcahVdebZAtt7xgzl3zk"
BOT_USERNAME = "shakaweebot"

# Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ===== Firebase Initialization =====
# تم تضمين مفاتيح الاتصال الخاصة بمشروع nablus-e8a6d مباشرة
firebase_credentials = {
  "type": "service_account",
  "project_id": "nablus-e8a6d",
  "private_key_id": "2f927302f1ad8660587fc4c14e39af673790229f",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDBb+QV4JZ6ntce\nS4qHgZpAorSfIV+ezAoCz0majSVuKPEAmnmkzn+Eae0Dt94NHpTOR3DNOrIl/b9+\nFOocakQTOTJZf8AnG119s8fo/YXyDbVLVpOpmACVYueX7k0F62wzwk/vnNrSASe1\nrcflTUkyKGGwzY6jN0v/9484uz5ucvAh7kHIUwjTS7LLxoTU5S6bQtNrFmWj5A+q\nwJ/JoheYIvzXM5K4tVP6yi+wXTMGYZPEWz2ooAfV5oXYjttHbWrC9p6vpxJFLSS0\nW6HorxgzA4ZNZQ2wG6uG7o9KCxRbIaaZ6kNG5Uo9fxZWSxM9ZYgzR1ukM3ZRSL23\nOmnfR60TAgMBAAECggEAUUZB/y8uCrdSi1gSDH1X4nB6k6HiG0Z/rk6KDnXflDl/\niVFeavCYg3o+K6HFmp2OyF0b+B8BWxUSsFb5RpcfozQVA6W5hrTowzgWdr6O2PUJ\nh24I/Ojw1dOImz10/1e7TsQF8hdlmXcCyEMMCjw+1ORCp5a2p71EIXhSpPOHd7/3\n+s+aCEBBdSoHzw3IyhU+A+6z1elTTiX+Orb0e/+jVGUA78/kpSPmSHMtTgZmLAFQ\nyB8L7xcuVLRcpztB0nsu0pFi18VXDWCfn79wgQRPVMc1QY4HPUn5MtW0cW9Io22L\nzQMs8G8e40Cwj2z6MGSoMXnhQSxD4ylCCyuDWiDBAQKBgQDrTYlaAqY94Tu6i+Ct\nO2w+cLE6DGgyJNe1RG4XlKjyGxZskijBZ1SzHeRD9atIk6AD+NLix9rdbTtdCxxl\nQNXZ0oISjuOoywsLRtE8stcMGctRhgzlP7M/SMWrjJl5A24Jkl3tDv9RQ9UsycNw\nHKIQUqVNt57SSEmXNAsplAWbGwKBgQDSc6K9mkr5KBnQvwcW5OhG84+962zQW9tM\njy4+jEBnfw3aTYNpvZaq3PV8c9rul0d3nBUvKaELD4q4FydoEG/8gchkeaPjR1Z8\nyjiUgkHOSFAPzppFMQdghWvolRkBqGpvaeHGo+2Qrc4F9ZIb8CH+cJq9fvlyW5Ry\nobOBGMsdaQKBgQCz2XPeZKAENB+fGkMEpaK6pxAPOmR5z0dAuakcRPhM9P9SxPR5\nvy0yKurKNwBQXOW1o34s8G0NSexR1ahCjCfoccoRvT2tSmSKnfpX1qogCacqDLfW\nkbXD7S+JS9ISeNimYEWCaDAmQR6zORQ0oO4OY90NZgfy2mXFOHY/tXADeQKBgGsQ\ncyGcZjn9gaymEng+OkEmVeFb7P7PTHDVgsRFW9qLU8PUnV9lGUqRoL4QvreU9MHQ\nASL+PbS/0mW3OdACVMaUTBt5mrvcpg5UXpaG8e188mYoSGmc+NDM78niWFd0k7lc\nl4UUDp8FHQQBG7Tk5JZqOP7gowzftFThGM47i9HJAoGBAI3x9Qzl183q5NMA1tdZ\nIBoT/ahD7CbemkwKbog6ObK5SVgCJeA7vE/eZrugXDZQN1WX9g5hQHxm0BJxnIIe\nw1u4AckP49nWlnFooGqqUSutJXrKAXJOU32Ypovdsr1aE7GYQoKNTuTbFQIpxvM+\nIiW5Hk5k0YBj2IZcQcdhMiJR\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-fbsvc@nablus-e8a6d.iam.gserviceaccount.com",
  "client_id": "114407167271558940931",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40nablus-e8a6d.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

try:
    if not firebase_admin._apps:
        cred = credentials.Certificate(firebase_credentials)
        firebase_admin.initialize_app(cred)
    db = firestore.client()
    logger.info("Firebase connected successfully")
except Exception as e:
    logger.error(f"Firebase Initialization Error: {e}")
    db = None

# ===== Helper Functions =====

def extract_complaint_data(start_param: str) -> Optional[Dict]:
    try:
        parts = start_param.split("_")
        if len(parts) >= 3 and parts[0] == "complaint":
            return {"ticket_id": parts[1], "phone": parts[2]}
    except Exception as e:
        logger.error(f"Error parsing start param: {e}")
    return None

def get_user_complaints(phone: str) -> List[Dict]:
    if not db: return []
    try:
        complaints = []
        docs = db.collection("complaints").where("phone", "==", phone).stream()
        for doc in docs:
            data = doc.to_dict()
            data["id"] = doc.id
            complaints.append(data)
        
        # Sort by createdAt if available
        complaints.sort(key=lambda x: x.get("createdAt") if x.get("createdAt") else 0, reverse=True)
        return complaints
    except Exception as e:
        logger.error(f"Error fetching complaints: {e}")
        return []

def get_complaint_details(ticket_id: str) -> Optional[Dict]:
    if not db: return None
    try:
        doc = db.collection("complaints").document(ticket_id).get()
        if doc.exists:
            return doc.to_dict()
    except Exception as e:
        logger.error(f"Error fetching complaint details: {e}")
    return None

def format_complaint_message(complaint: Dict) -> str:
    ticket_id = complaint.get("ticketId", "N/A")
    status = complaint.get("status", "مستلمة")
    problem_type = complaint.get("type", "غير محدد")
    description = complaint.get("description", "لا توجد تفاصيل")
    location = complaint.get("location", {})
    manual_location = location.get("manual", "غير محدد")

    status_emoji = "🔵" if "جديدة" in status else "🟡" if "معالجة" in status else "🟢"
    
    # Format date
    date_str = "غير متوفر"
    created_at = complaint.get("createdAt")
    if created_at:
        try:
            # Firebase timestamps often need to be converted
            if hasattr(created_at, 'strftime'):
                date_str = created_at.strftime("%Y-%m-%d %H:%M")
            else:
                date_str = str(created_at)
        except:
            pass

    msg = f"""
📋 <b>تفاصيل الشكوى: {ticket_id}</b>
━━━━━━━━━━━━━━━━━━
{status_emoji} <b>الحالة:</b> {status}
📂 <b>التصنيف:</b> {problem_type}
📅 <b>التاريخ:</b> {date_str}

📝 <b>الوصف:</b>
{description}

📍 <b>الموقع:</b>
{manual_location}
"""
    if location.get("mapUrl"):
        msg += f"\n🗺️ <a href='{location['mapUrl']}'>عرض الموقع على الخريطة</a>"
    
    return msg

# ===== Handlers =====

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    args = context.args
    
    logger.info(f"User {user.id} started the bot with args: {args}")

    welcome_text = f"مرحباً بك يا {user.first_name} في بوت بلدية نابلس للشكاوى. 👋\n\n"
    
    if args and args[0].startswith("complaint_"):
        data = extract_complaint_data(args[0])
        if data and db:
            # Save user link
            try:
                db.collection("telegram_users").document(str(user.id)).set({
                    "chat_id": user.id,
                    "phone": data["phone"],
                    "username": user.username,
                    "linked_at": datetime.now()
                })
                welcome_text += f"✅ تم ربط حسابك بالشكوى رقم <code>{data['ticket_id']}</code> بنجاح.\n"
                
                # Show complaint details
                complaint = get_complaint_details(data["ticket_id"])
                if complaint:
                    await update.message.reply_text(welcome_text, parse_mode="HTML")
                    await update.message.reply_text(format_complaint_message(complaint), parse_mode="HTML")
                    return
            except Exception as e:
                logger.error(f"Error linking user: {e}")

    keyboard = [
        [InlineKeyboardButton("📊 متابعة شكاويي", callback_data="list_complaints")],
        [InlineKeyboardButton("ℹ️ حول الخدمة", callback_data="about")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        welcome_text + "يمكنك استخدام الأزرار أدناه لمتابعة طلباتك.",
        reply_markup=reply_markup,
        parse_mode="HTML"
    )

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = update.effective_user.id
    await query.answer()

    if query.data == "list_complaints":
        if not db:
            await query.edit_message_text("⚠️ خدمة قاعدة البيانات غير متوفرة حالياً.")
            return

        # Get user phone
        user_doc = db.collection("telegram_users").document(str(user_id)).get()
        if not user_doc.exists:
            await query.edit_message_text("❌ لم يتم العثور على رقم هاتف مرتبط بحسابك. يرجى التقديم عبر الموقع أولاً.")
            return
        
        phone = user_doc.get("phone")
        complaints = get_user_complaints(phone)
        
        if not complaints:
            await query.edit_message_text(f"📭 لا توجد شكاوى مسجلة لرقم الهاتف {phone}")
            return

        text = f"📋 <b>قائمة شكاويك ({len(complaints)}):</b>\n\n"
        keyboard = []
        for c in complaints:
            t_id = c.get("ticketId", "N/A")
            status = c.get("status", "مستلمة")
            text += f"• <code>{t_id}</code>: {status}\n"
            keyboard.append([InlineKeyboardButton(f"عرض تفاصيل {t_id}", callback_data=f"view_{t_id}")])
        
        keyboard.append([InlineKeyboardButton("🔙 العودة", callback_data="main_menu")])
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")

    elif query.data.startswith("view_"):
        t_id = query.data.split("_")[1]
        complaint = get_complaint_details(t_id)
        if complaint:
            keyboard = [[InlineKeyboardButton("🔙 العودة للقائمة", callback_data="list_complaints")]]
            await query.edit_message_text(
                format_complaint_message(complaint),
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode="HTML"
            )

    elif query.data == "main_menu":
        keyboard = [
            [InlineKeyboardButton("📊 متابعة شكاويي", callback_data="list_complaints")],
            [InlineKeyboardButton("ℹ️ حول الخدمة", callback_data="about")]
        ]
        await query.edit_message_text("اختر من القائمة أدناه:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == "about":
        text = "🏢 <b>بلدية نابلس - نظام الشكاوى الإلكتروني</b>\n\nهذا البوت يساعدك على متابعة حالة الشكاوى التي قمت بتقديمها عبر موقعنا الرسمي وتلقي التحديثات فور حدوثها."
        keyboard = [[InlineKeyboardButton("🔙 العودة", callback_data="main_menu")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")

# ===== Main =====

def main():
    logger.info("Starting bot...")
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CallbackQueryHandler(handle_callback))

    logger.info("Bot is polling...")
    application.run_polling()

if __name__ == "__main__":
    main()
