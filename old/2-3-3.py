import discord , asyncio , datetime , sys , os
from web3 import *

def main():
    client = discord.Client()

    #명령어 목록

    Command_list = discord.Embed(title="Command List", description="명령어 목록", color=0x00ff00)
    Command_list.add_field(name="$a", value="도움말", inline=False)
    Command_list.add_field(name="$b", value="버전 정보", inline=False)
    Command_list.add_field(name="$d", value="오늘 날짜", inline=False)
    Command_list.add_field(name="$f", value="내일급식", inline=False)
    Command_list.add_field(name="$g", value="급식정보", inline=False)

    #급식안내
    meal_notice = (
                    "```css\n"
                    "[안내] 날짜와 급식이 맞지 않는 경우 개발자에게 문의해주세요.\n"
                    "[주의] 2018년 3월 5일 인 경우 17035 로 보낼 것.\n"
                    "[주의] 2017년 10월 1일 인 경우 17101 로 보낼 것.\n"
                    "```"
                    )

    plus_meal_notice = ""

    @client.event
    async def on_ready():
        print('Logged in as')
        print(client.user.name)
        print(client.user.id)
        print('---------')
        await client.change_presence(game=discord.Game(name="$a for help"))

    @client.event
    async def on_message(message):

        if message.content.startswith('$a'):
            await client.send_message(message.channel, embed=Command_list)

        elif message.content.startswith('$b'):
            embed = discord.Embed(title="Bot Version", description="updated", color=0x00ff00)
            embed.add_field(name="Version", value="2.3.3", inline=False)
            await client.send_message(message.channel, embed=embed)

        elif message.content.startswith('$d'):
            dt = datetime.datetime.now()
            local_date = dt.strftime("%Y년 %m월 %d일 %H시 %M분 %S초")
            embed = discord.Embed(title="Local Time", description=local_date, color=0x00ff00)
            await client.send_message(message.channel, embed=embed)

        elif message.content.startswith('$f'):
            f_dt = datetime.datetime.today() + datetime.timedelta(days=1)
            local_date2 = f_dt.strftime("%Y.%m.%d")
            local_weekday2 = f_dt.weekday()

            l_diet = get_diet(2, local_date2, local_weekday2)
            d_diet = get_diet(3, local_date2, local_weekday2)

            if len(l_diet) == 1:
                embed = discord.Embed(title="No Meal", description="급식이 없습니다.", color=0x00ff00)
                await client.send_message(message.channel, embed=embed)
            elif len(d_diet) == 1:
                lunch = local_date2 + " 중식\n" + l_diet
                embed = discord.Embed(title="Lunch", description=lunch, color=0x00ff00)
                await client.send_message(message.channel, embed=embed)
            else:
                lunch = local_date2 + " 중식\n" + l_diet
                dinner = local_date2 + " 석식\n" + d_diet
                lunch_e= discord.Embed(title="Lunch", description=lunch, color=0x00ff00)
                await client.send_message(message.channel, embed=lunch_e)
                dinner_e = discord.Embed(title="Dinner", description=dinner, color=0x00ff00)
                await client.send_message(message.channel, embed=dinner_e)

        elif message.content.startswith('$g'):
            request = meal_notice + '\n' + plus_meal_notice + '날짜를 보내주세요...'
            request_e = discord.Embed(title="Send to Me", description=request, color=0xcceeff)
            await client.send_message(message.channel, embed=request_e)
            meal_date = await client.wait_for_message(timeout=15.0, author=message.author)

            if meal_date is None:
                longtimemsg = discord.Embed(title="In 15sec", description='15초내로 입력해주세요. 다시시도 : $g', color=0xff0000)
                await client.send_message(message.channel, embed=longtimemsg)
                return

            else:
                meal_date = str(meal_date.content) # 171121
                meal_date = '20' + meal_date[:2] + '.' + meal_date[2:4] + '.' + meal_date[4:6] # 2017.11.21

                s = meal_date.replace('.', ', ') # 2017, 11, 21

                if int(s[6:8]) < 10:
                    s = s.replace(s[6:8], s[7:8])

                ss = "datetime.datetime(" + s + ").weekday()"
                try:
                    whatday = eval(ss)
                except:
                    warnning = discord.Embed(title="Plz Retry", description='올바른 값으로 다시 시도하세요 : $g', color=0xff0000)
                    await client.send_message(message.channel, embed=warnning)
                    return

                l_diet = get_diet(2, meal_date, whatday)
                d_diet = get_diet(3, meal_date, whatday)

                if len(l_diet) == 1:
                    l_diet = "급식이 없습니다."
                    l_e=discord.Embed(title="Lunch", description=l_diet, color=0x00ff00)
                    await client.send_message(message.channel, embed=l_e)
                elif len(d_diet) == 1:
                    lunch = meal_date + " 중식\n" + l_diet
                    lunch_e= discord.Embed(title="Lunch", description=lunch, color=0x00ff00)
                    await client.send_message(message.channel, embed=lunch_e)
                else:
                    lunch = meal_date + " 중식\n" + l_diet
                    dinner = meal_date + " 석식\n" + d_diet
                    lunch_e= discord.Embed(title="Lunch", description=lunch, color=0x00ff00)
                    await client.send_message(message.channel, embed=lunch_e)
                    dinner_e = discord.Embed(title="Dinner", description=dinner, color=0x00ff00)
                    await client.send_message(message.channel, embed=dinner_e)

    client.run('NDE0NzU0NzM2ODEwNzU0MDY5.DXlfMw.sUeh3BggTGxf_aqBsUhnGB7_2bQ')

    print("respawn!")
    executable = sys.executable
    args = sys.argv[:]
    args.insert(0, sys.executable)
    os.execvp(executable, args)

if __name__ == "__main__":
    main()
