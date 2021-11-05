import discord
from discord.ext import commands
from libs.utils import *
import datetime
import asyncio


class Servers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_before_invoke(self, ctx: commands.Context):
        if check_if_admin(ctx):
            return ctx.command.reset_cooldown(ctx)

    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def create_server(self, ctx, *, server_name=None):
        global type_server
        config = loadf('./config.json')
        if config['server_creation'] is False:
            await ctx.send(
                'Server creations is disabled currently. Please wait for it to be enabled by an administrator. Opening a ticket regarding this will result in a warn :smile:')
        else:
            server_price = config['server_price']
            if server_name is None:
                await ctx.send('<a:crossGif:878972402317557781> Please provide a `name` for your server.')
            else:
                message = await ctx.send('Attempting to get Dashactyl Details')
                user_info = await get_user_info(discord_id=ctx.author.id)
                if user_info['status'] == "could not find user on panel" or user_info['status'] == "invalid id":
                    failed_embed = discord.Embed(title='Failed to get details',
                                                 description='We could not find your account on Dashactyl.\n Please register yourself [here](https://cp.cygennodes.com/)',
                                                 colour=discord.Colour.red(),
                                                 timestamp=datetime.datetime.now(tz=datetime.timezone.utc))
                    failed_embed.set_footer(text='CygenNodes',
                                            icon_url='https://media.discordapp.net/attachments/801034454155395082/890871710717448202/cygen_logo.png')
                    await message.edit(content=None, embed=failed_embed)
                else:
                    initial_coins = user_info['coins']
                    if initial_coins >= server_price:
                        user_id = user_info['userinfo']['attributes']['id']

                        await message.edit(
                            content=f'Dashactyl account found and has {server_price} coins. Please, select the type of server you want',
                            embed=None)
                        types_embed = discord.Embed(title='Types of servers', colour=discord.Color.blue(),
                                                    timestamp=datetime.datetime.now(tz=datetime.timezone.utc))
                        types_embed.add_field(name='__Minecraft Java __',
                                              value='1. Type `1` to select the [Paper Server jar](https://papermc.io/)\n **(Recommended Version)**\n2. Type `2` to select the [Vanilla Server Jar](https://www.minecraft.net/en-us/download/server) \n**(Not recommended)**\n\n',
                                              inline=False)
                        types_embed.add_field(name='__Modded Minecraft Java__',
                                              value='1. Type `3` to select the [Forge Server Jar](https://forums.minecraftforge.net/)\n',
                                              inline=False)
                        types_embed.add_field(name='__Minecraft Java Proxy__',
                                              value='1. Type `4` to select the [BungeeCord Server Jar](https://github.com/SpigotMC/BungeeCord)\n',
                                              inline=False)
                        types_embed.add_field(name='__Minecraft Bedrock__',
                                              value='1. Type `5` to select the [PocketMineMP Server Jar](https://www.pocketmine.net/)\n2. Type `6` to select the [Vanilla Bedrock Server Jar](https://www.minecraft.net/en-us/download/server/bedrock)',
                                              inline=False)
                        types_embed.set_thumbnail(
                            url='https://media.discordapp.net/attachments/801034454155395082/890871710717448202/cygen_logo.png')
                        types_embed.set_footer(text='CygenNodes',
                                               icon_url='https://media.discordapp.net/attachments/801034454155395082/890871710717448202/cygen_logo.png')
                        types_embed_message = await ctx.send(embed=types_embed)

                        def check(m):
                            return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id

                        try:
                            response = await self.bot.wait_for('message', check=check, timeout=30)
                            if response.content == "1":
                                type_server = 1
                                pass
                            elif response.content == "2":
                                type_server = 2
                                pass
                            elif response.content == "3":
                                type_server = 3
                                pass
                            elif response.content == "4":
                                type_server = 4
                                pass
                            elif response.content == "5":
                                type_server = 5
                                pass
                            elif response.content == "6":
                                type_server = 6
                                pass
                            else:
                                await ctx.send('Not a valid, type of server. Please try again.')
                                return
                        except asyncio.TimeoutError:
                            failed_embed = discord.Embed(title='Timed Out',
                                                         description='You did not respond in time, please try again.',
                                                         colour=discord.Colour.red(),
                                                         timestamp=datetime.datetime.now(tz=datetime.timezone.utc))
                            failed_embed.set_footer(text='CygenNodes',
                                                    icon_url='https://media.discordapp.net/attachments/801034454155395082/890871710717448202/cygen_logo.png')
                            await types_embed_message.edit(embed=failed_embed, content=None)
                            return

                        final_message = await ctx.send('Searching for allocations.')
                        allocation_id = await get_allocation_id()
                        await final_message.edit(
                            content='Allocation found successfully, attempting to create a server.',
                            embed=None)
                        server = await create_ptero_server(name=server_name, user_id=user_id,
                                                           allocation_id=allocation_id,
                                                           type_server=type_server)
                        if int(server) == 201:
                            await final_message.edit(
                                content=f'Attempting to remove `{server_price}` coins from your account.',
                                embed=None)
                            coins_left = initial_coins - server_price
                            await set_coins(coins=coins_left, discord_id=ctx.author.id)
                            successful_embed = discord.Embed(title='Success!',
                                                             description=f'Server successfully created. You have `{coins_left}` coins left.\nYou can manage your server [here](https://gp.cygennodes.com)',
                                                             timestamp=datetime.datetime.now(tz=datetime.timezone.utc),
                                                             colour=discord.Color.green())
                            successful_embed.set_footer(text='CygenNodes',
                                                        icon_url='https://media.discordapp.net/attachments/801034454155395082/890871710717448202/cygen_logo.png')
                            await final_message.edit(embed=successful_embed, content=None)
                        else:
                            await ctx.send('Some unknown error occurred, please contact the staff team.')
                    else:
                        coins_needed = server_price - int(initial_coins)
                        coins_needed_embed = discord.Embed(title='Error!',
                                                           description=f'<a:crossGif:878972402317557781> You have only {initial_coins} coins. You need {coins_needed} coins more to create a server. Afk [here to get more coins](https://cp.cygennodes.com/afk)',
                                                           colour=discord.Color.red(),
                                                           timestamp=datetime.datetime.now(tz=datetime.timezone.utc))
                        coins_needed_embed.set_footer(text='CygenNodes',
                                                      icon_url='https://media.discordapp.net/attachments/801034454155395082/890871710717448202/cygen_logo.png')
                        await message.edit(embed=coins_needed_embed, content=None)

    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def change_egg(self, ctx):
        pass

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f'This command is on cooldown, please try again in {round(error.retry_after)} seconds')


def setup(bot):
    bot.add_cog(Servers(bot))
