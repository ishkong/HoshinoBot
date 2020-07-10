from hoshino import R,Service,priv
import base64
from hoshino import aiorequests
from hoshino.util import FreqLimiter, DailyNumberLimiter
sv=Service('xsetu',visible=False,enable_on_default=False,manage_priv=priv.SUPERUSER)
_nlmt = DailyNumberLimiter(10)
_flmt = FreqLimiter(15)



async def getsetu():
    resp=await aiorequests.get('填入API地址',timeout=5)
    img=base64.b64encode(await resp.content).decode()
    return f'[CQ:image,cache=0,file=base64://{img}]'


@sv.on_rex(r'^(不够[涩瑟色]|[涩瑟色]图|来一?[点份张].*[涩瑟色]|再来[点份张]|看过了|铜)', normalize=True)
async def pushsetu(bot, ctx, match):
    uid=ctx['user_id']
    if not _nlmt.check(uid):
        await bot.send(ctx, EXCEED_NOTICE, at_sender=True)
        return
    if not _flmt.check(uid):
        await bot.send(ctx, '您冲得太快了，请稍候再冲', at_sender=True)
        return
    _flmt.start_cd(uid)
    _nlmt.increase(uid)
    try:
        msg=await getsetu()
        await bot.send(ctx,msg)
    except:
        await bot.send(ctx,'它太色了，被吃掉了QAQ')
        return
