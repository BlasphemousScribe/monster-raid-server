#!/usr/bin/env python3
import json, time, random, string, logging, os
from http.server import HTTPServer, BaseHTTPRequestHandler

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s  %(message)s", datefmt="%H:%M:%S")
log = logging.getLogger("MonsterRaid")

DEFAULT_STATE = {
    "user_no":10000001,"nickname":"Adventurer","gold":9999999,"gem":9999,
    "level":1,"exp":0,"stamina":100,"stamina_max":100,"tutorial":1,
    "nation_code":"en","mon_list":[],
    "rune_list":[],"part_list":[],"dungeon_clear_list":[],"quest_list":[],
    "achieve_list":[],"tower_step":0,"arena_battle_pt":1000,
}

STATE = DEFAULT_STATE.copy()

def st(): return int(time.time())
def ok(d=None):
    r={"result_code":1,"result_msg":"success","server_time":st()}
    if d: r.update(d)
    return r
def bud():
    return {"user_no":STATE["user_no"],"nickname":STATE["nickname"],"gold":STATE["gold"],
    "gem":STATE["gem"],"level":STATE["level"],"exp":STATE["exp"],"stamina":STATE["stamina"],
    "stamina_max":STATE["stamina_max"],"nation_code":STATE["nation_code"],
    "tutorial":STATE["tutorial"],"mon_list":STATE["mon_list"],"rune_list":STATE["rune_list"],
    "part_list":STATE["part_list"],"arena_battle_pt":STATE["arena_battle_pt"],"tower_step":STATE["tower_step"]}

def h_version(p): return ok({"force_update":0,"cur_ver":57,"notice":0,"notice_main_url":"","notice_err_url":"","cdn_url":"","patch":0})
def h_login(p):
    d=bud(); d["access_key"]="offline_"+"".join(random.choices(string.ascii_lowercase,k=8))
    d["account"]="anonymous"; d["anonymous"]=1; d["bot_id"]=0; return ok(d)
def h_dungeon_ent(p):
    STATE["stamina"]=max(0,STATE["stamina"]-int(p.get("stamina",5)))
    return ok({"stamina":STATE["stamina"],"dungeon_no":p.get("dungeon_no",1),"area_no":p.get("area_no",1)})
def h_dungeon_clear(p):
    g=random.randint(500,3000); e=random.randint(50,200)
    STATE["gold"]+=g; STATE["exp"]+=e
    return ok({"gold":STATE["gold"],"exp":STATE["exp"],"level":STATE["level"],"gold_reward":g,"exp_reward":e,"mon_piece_list":[],"item_list":[]})
def h_capsule(p):
    m={"mon_no":random.randint(10101,20101),"level":1,"grade":random.randint(1,3),
    "star":random.randint(1,3),"enhance_lv":0,"awaken":0,"lock_yn":"N",
    "slot":len(STATE["mon_list"])+1,"atk":random.randint(100,400),
    "def":random.randint(100,400),"spd":random.randint(100,400),"hp":random.randint(500,2000)}
    STATE["mon_list"].append(m)
    return ok({"mon_list":STATE["mon_list"],"new_mon":m,"gold":STATE["gold"],"gem":STATE["gem"]})
def h_sell(p):
    STATE["gold"]+=500; return ok({"gold":STATE["gold"],"mon_list":STATE["mon_list"]})
def h_nickname(p):
    STATE["nickname"]=p.get("nickname",STATE["nickname"]); return ok({"nickname":STATE["nickname"]})
def h_tutorial(p):
    STATE["tutorial"]=int(p.get("tutorial",1)); return ok({"tutorial":STATE["tutorial"]})
def h_tower_clear(p):
    STATE["tower_step"]+=1; return ok({"tower_step":STATE["tower_step"],"reward_list":[]})
def h_buy_gold(p):
    STATE["gold"]+=10000; return ok({"gold":STATE["gold"]})

ROUTES={
    "/version":h_version,"/login2":h_login,"/loginMon":h_login,"/loginRune":h_login,
    "/account_check":lambda p:ok({"account":"anonymous","anonymous":1}),
    "/account_link":lambda p:ok({"account":"linked"}),
    "/welcome":lambda p:ok({"gold":10000,"gem":10,"attend_day":1,"attend_list":[]}),
    "/dailyRoutine":lambda p:ok({"daily_list":[]}),
    "/resource":lambda p:ok({"resource_list":[],"patch":0}),
    "/nickname":h_nickname,"/tutorialSave":h_tutorial,"/option":lambda p:ok({}),
    "/partySetting":lambda p:ok({"party_list":[]}),
    "/dungeonEnt":h_dungeon_ent,"/dungeonClear":h_dungeon_clear,
    "/dungeonSkip":h_dungeon_clear,"/spDungeonList":lambda p:ok({"sp_dungeon_list":[]}),
    "/spDungeonEnt":h_dungeon_ent,"/spDungeonClear":h_dungeon_clear,"/spDungeonSkip":h_dungeon_clear,
    "/battleContinue":lambda p:ok({"gem":STATE["gem"]}),
    "/monsterEnhance":lambda p:ok({"mon_list":STATE["mon_list"],"gold":STATE["gold"]}),
    "/monsterFusion":lambda p:ok({"mon_list":STATE["mon_list"],"gold":STATE["gold"]}),
    "/monsterEvo":lambda p:ok({"mon_list":STATE["mon_list"]}),
    "/monsterAwaken":lambda p:ok({"mon_list":STATE["mon_list"]}),
    "/monsterSell":h_sell,"/monsterUpgrade":lambda p:ok({"mon_list":STATE["mon_list"]}),
    "/monsterLock":lambda p:ok({"mon_list":STATE["mon_list"]}),
    "/monsterPiece":lambda p:ok({"mon_list":STATE["mon_list"]}),
    "/monsterMutate":lambda p:ok({"mon_list":STATE["mon_list"]}),
    "/monsterRuneEquip":lambda p:ok({"mon_list":STATE["mon_list"],"rune_list":STATE["rune_list"]}),
    "/monsterRuneUnEquip":lambda p:ok({"mon_list":STATE["mon_list"],"rune_list":STATE["rune_list"]}),
    "/monsterMakeTest":lambda p:ok({"mon_list":STATE["mon_list"]}),
    "/markerMon":lambda p:ok({"mon_list":STATE["mon_list"]}),
    "/masteryEnhance":lambda p:ok({}),"/masterySetting":lambda p:ok({}),
    "/runePack":lambda p:ok({"rune_list":STATE["rune_list"]}),
    "/partPack":lambda p:ok({"part_list":STATE["part_list"]}),
    "/capsuleAttr":h_capsule,"/capsuleRare":h_capsule,"/capsuleRare10":h_capsule,
    "/capsuleEvo":h_capsule,"/capsuleEvo10":h_capsule,"/capsuleSocial":h_capsule,
    "/capsuleSocial10":h_capsule,"/capsuleCoupon":h_capsule,
    "/buyGold":h_buy_gold,"/buyItem":lambda p:ok({}),"/buyShopInfo":lambda p:ok({"shop_list":[]}),
    "/buyInapp":lambda p:ok({"gem":STATE["gem"]}),"/buyInappStore":lambda p:ok({"gem":STATE["gem"]}),
    "/buyInapp_test":lambda p:ok({"gem":STATE["gem"]}),
    "/coinShopList":lambda p:ok({"shop_list":[],"coin":9999}),
    "/coinShopBuy":lambda p:ok({"shop_list":[],"coin":9999}),
    "/coinShopRefresh":lambda p:ok({"shop_list":[],"coin":9999}),
    "/guildShopList":lambda p:ok({"guild_shop_list":[],"guild_coin":9999}),
    "/guildShopBuy":lambda p:ok({"guild_shop_list":[],"guild_coin":9999}),
    "/arenaCheck":lambda p:ok({"arena_battle_pt":STATE["arena_battle_pt"],"arena_remain_sec":86400,"arena_ranking_box":[]}),
    "/arenaRank":lambda p:ok({"rank_list":[],"my_rank":1}),
    "/arenaBattleSearch":lambda p:ok({"enemy_list":[]}),
    "/arenaBattleEnt":lambda p:ok({"battle_result":1}),
    "/arenaBattleResult":lambda p:ok({"arena_battle_pt":STATE["arena_battle_pt"],"rank":1}),
    "/arenaBattleRefresh":lambda p:ok({"enemy_list":[]}),
    "/arenaRevengeEnt":lambda p:ok({"battle_result":1}),
    "/arenaRevengeResult":lambda p:ok({"arena_battle_pt":STATE["arena_battle_pt"]}),
    "/arenaShopList":lambda p:ok({"arena_shop_list":[]}),
    "/arenaShopBuy":lambda p:ok({"arena_shop_list":[]}),
    "/arenaTeam":lambda p:ok({"team_list":[]}),
    "/raidList":lambda p:ok({"raid_list":[]}),"/raidCreate":lambda p:ok({"raid_no":1}),
    "/raidEnt":lambda p:ok({"raid_no":1}),"/raidResult":lambda p:ok({"raid_result":1}),
    "/raidRank":lambda p:ok({"rank_list":[]}),"/raidReward":lambda p:ok({"reward_list":[]}),
    "/guildRaidCreate":lambda p:ok({"raid_no":1}),"/guildRaidEnt":lambda p:ok({"raid_no":1}),
    "/guildRaidResult":lambda p:ok({"raid_no":1}),"/guildRaidRank":lambda p:ok({"rank_list":[]}),
    "/guildRaidReward":lambda p:ok({"reward_list":[]}),
    "/towerInfo":lambda p:ok({"tower_step":STATE["tower_step"],"tower_list":[]}),
    "/towerList":lambda p:ok({"tower_list":[]}),
    "/towerEnt":lambda p:ok({"tower_step":STATE["tower_step"]}),
    "/towerClear":h_tower_clear,"/towerReward":lambda p:ok({"reward_list":[]}),
    "/deckBattleEnt":lambda p:ok({"battle_map":"battle_cave"}),
    "/deckBattleEnt_test":lambda p:ok({"battle_map":"battle_cave"}),
    "/deckBattleClear":lambda p:ok({"gold":STATE["gold"],"exp":STATE["exp"]}),
    "/deckBattleMon":lambda p:ok({"mon_list":STATE["mon_list"]}),
    "/deckBattleParty":lambda p:ok({"party_list":[]}),
    "/questList":lambda p:ok({"quest_list":[]}),"/questAccept":lambda p:ok({"quest_list":[]}),
    "/questReward":lambda p:ok({"gold":STATE["gold"],"quest_list":[]}),
    "/achieveList":lambda p:ok({"achieve_list":[]}),"/achieveReward":lambda p:ok({"achieve_list":[]}),
    "/collection":lambda p:ok({"collection_list":[]}),
    "/friendList":lambda p:ok({"friend_list":[],"friend_count":0}),
    "/friendRecommend":lambda p:ok({"friend_list":[]}),
    "/friendRequest":lambda p:ok({"friend_list":[]}),
    "/friendRequestRecv":lambda p:ok({"friend_list":[]}),
    "/friendAccept":lambda p:ok({"friend_list":[]}),
    "/friendDelete":lambda p:ok({"friend_list":[]}),
    "/friendSearch":lambda p:ok({"friend_list":[]}),
    "/friendSendGift":lambda p:ok({}),
    "/guildInfo":lambda p:ok({"guild_info":None}),"/guildSearch":lambda p:ok({"guild_list":[]}),
    "/guildCreate":lambda p:ok({"guild_info":{"guild_no":1,"guild_name":"OfflineGuild"}}),
    "/guildApply":lambda p:ok({}),"/guildApplyList":lambda p:ok({"apply_list":[]}),
    "/guildAccept":lambda p:ok({}),"/guildRank":lambda p:ok({"rank_list":[]}),
    "/guildRetire":lambda p:ok({}),"/guildClose":lambda p:ok({}),"/guildNotice":lambda p:ok({}),
    "/guildAttend":lambda p:ok({"guild_coin":9999}),"/guildMasterChange":lambda p:ok({}),
    "/guildOfficerAppoint":lambda p:ok({}),"/guildOfficerDismissal":lambda p:ok({}),
    "/guildMemberBan":lambda p:ok({}),"/guildMatchInfo":lambda p:ok({"guild_match_info":None}),
    "/guildMatchEnt":lambda p:ok({}),"/guildMatchResult":lambda p:ok({}),
    "/guildMatchTeam":lambda p:ok({"team_list":[]}),
    "/msgBoxList":lambda p:ok({"msg_list":[]}),"/msgBoxRead":lambda p:ok({}),
    "/msgBoxReadAll":lambda p:ok({}),"/teampageAdd":lambda p:ok({}),
    "/couponUse":lambda p:ok({"gold":50000,"gem":50}),
    "/deepLinkCouponUse":lambda p:ok({"gold":50000,"gem":50}),
    "/unityAdsCompleted":lambda p:ok({}),"/cna":lambda p:ok({}),
}

class Handler(BaseHTTPRequestHandler):
    def log_message(self,fmt,*args): pass
    def parse_body(self):
        n=int(self.headers.get("Content-Length",0))
        if not n: return {}
        raw=self.rfile.read(n).decode("utf-8",errors="replace")
        p={}
        for part in raw.split("&"):
            if "=" in part:
                from urllib.parse import unquote_plus
                k,v=part.split("=",1); p[unquote_plus(k)]=unquote_plus(v)
        return p
    def send_json(self,data):
        body=json.dumps(data).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type","application/json; charset=utf-8")
        self.send_header("Content-Length",str(len(body)))
        self.send_header("Connection","close")
        self.end_headers()
        self.wfile.write(body)
    def do_POST(self):
        path=self.path.split("?")[0]
        params=self.parse_body()
        h=ROUTES.get(path)
        if h:
            log.info(f"POST {path} -> handled")
            try: resp=h(params)
            except Exception as e: log.error(f"Error: {e}"); resp=ok()
        else:
            log.warning(f"POST {path} -> UNKNOWN"); resp=ok()
        self.send_json(resp)
    def do_GET(self):
        log.info(f"GET {self.path}")
        self.send_json(ok())

if __name__=="__main__":
    port=int(os.environ.get("PORT",10000))
    server=HTTPServer(("0.0.0.0",port),Handler)
    log.info(f"Monster Raid mock server running on port {port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
