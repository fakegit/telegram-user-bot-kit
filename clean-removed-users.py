#!/usr/bin/env python3
import sys
from itertools import chain

from pyrogram import Client, ChatMember

from user_bot_kit import retry
from user_bot_kit.users import remove_member

app = Client("bot")


def is_scp_079(member: ChatMember):
    if not member.restricted_by:
        return False
    username = member.restricted_by.username
    if not username:
        return False
    return username.startswith("SCP_079")


def clean_removed_users(chat_id: int):
    remove = retry(remove_member)
    members = chain(
        app.iter_chat_members(chat_id=chat_id, filter="kicked"),
        app.iter_chat_members(chat_id=chat_id, filter="restricted")
    )
    for member in members:
        if is_scp_079(member):
            continue
        remove(app, chat_id, member)


def main():
    app.start()
    for chat_id in sys.argv[1:]:
        clean_removed_users(int(chat_id))
    app.stop()


if __name__ == "__main__":
    main()
