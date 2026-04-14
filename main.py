import os
from dotenv import load_dotenv
import hikari


load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

BLOCKED_TAG_IDS = {
    1239260433551200276, # XIVIVIDE
}

bot = hikari.GatewayBot(
    token=BOT_TOKEN,
    intents=(
        hikari.Intents.GUILDS
        | hikari.Intents.GUILD_MEMBERS
        | hikari.Intents.GUILD_MESSAGES
    ),
)


def get_blocked_tag_info(member: hikari.Member) -> tuple[int, str] | None:
    if (primary_guild := member.primary_guild) is None:
        return
    if primary_guild.identity_enabled is not True:
        return
    if (tag_id := primary_guild.identity_guild_id) is None:
        return
    if (tag_id := int(tag_id)) not in BLOCKED_TAG_IDS:
        return

    tag_name = primary_guild.tag or "UNKNOWN"
    return tag_id, tag_name


async def dm_user(user: hikari.User, tag_name: str) -> None:
    try:
        await user.send(f"Замечен запрещённый тег: {tag_name}")
    except Exception:
        pass


async def kick_member(member: hikari.Member, tag_id: int, tag_name: str) -> None:
    try:
        await bot.rest.kick_member(
            member.guild_id,
            member.user.id,
            reason=f"Blocked tag: {tag_name} ({tag_id})",
        )
        print(f"Kicked {member.user.username} ({member.user.id}) for tag {tag_name} ({tag_id})")
    except hikari.ForbiddenError:
        print(f"Cannot kick {member.user.username} ({member.user.id}): insufficient permissions")
    except hikari.NotFoundError:
        print(f"{member.user.username} ({member.user.id}) already left")
    except Exception as e:
        print(f"Kick error: {e}")


@bot.listen()
async def on_member_join(event: hikari.MemberCreateEvent) -> None:
    if (member := event.member).user.is_bot:
        return
    if (info := get_blocked_tag_info(member)) is None:
        return

    tag_id, tag_name = info
    await dm_user(member.user, tag_name)
    await kick_member(member, tag_id, tag_name)


@bot.listen()
async def on_message(event: hikari.GuildMessageCreateEvent) -> None:
    if event.author.is_bot:
        return

    try:
        member = await bot.rest.fetch_member(event.guild_id, event.author_id)
    except hikari.NotFoundError:
        return
    except Exception as e:
        print(f"Fetch member error: {e}")
        return

    if (info := get_blocked_tag_info(member)) is None:
        return

    tag_id, tag_name = info

    try:
        await bot.rest.delete_message(event.channel_id, event.message.id)
    except Exception:
        pass

    await dm_user(member.user, tag_name)
    await kick_member(member, tag_id, tag_name)


if __name__ == "__main__":
    bot.run()
