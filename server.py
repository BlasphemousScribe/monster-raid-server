import json, time, random, string, logging, os
from flask import Flask, request, jsonify

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s  %(message)s", datefmt="%H:%M:%S")
log = logging.getLogger("MonsterRaid")

app = Flask(__name__)

STATE = {
    "user_no":10000001,"nickname":"Adventurer","gold":9999999,"gem":9999,
    "level":1,"exp":0,"stamina":100,"stamina_max":100,"tutorial":1,
    "nation_code":"en","mon_list":[],
    "rune_list":[],"part_list":[],"dungeon_clear_list":[],"quest_list":[],
    "achieve_list":[],"tower_step":0,"arena_battle_pt":1000,
}

def st(): return int(time.time())

def ok(d=None):
    r={"result_code":1,"result_msg":"success","server_time":st()}
    if d: r.update(d)
    return jsonify(r)

def bud():
    return {"user_no":STATE["user_no"],"nickname":STATE["nickname"],
    "gold":STATE["gold"],"gem":STATE["gem"],"level":STATE["level"],
    "exp":STATE["exp"],"stamina":STATE["stamina"],"stamina_max":STATE["stamina_max"],
    "nation_code":STATE["nation_code"],"tutorial":STATE["tutorial"],
    "mon_list":STATE["mon_list"],"rune_list":STATE["rune_list"],
    "part_list":STATE["part_list"],"arena_battle_pt":STATE["arena_battle_pt"],
    "tower_step":STATE["tower_step"]}

@app.route("/", methods=["GET","HEAD"])
def health(): return "Monster Raid Server OK", 200

@app.route("/version", methods=["GET","POST"])
def version():
    return ok({"force_update":0,"cur_ver":57,"notice":0,"notice_main_url":"","notice_err_url":"","cdn_url":"","patch":0})

@app.route("/login2", methods=["GET","POST"])
@app.route("/loginMon", methods=["GET","POST"])
@app.route("/loginRune", methods=["GET","POST"])
def login():
    d=bud(); d["access_key"]="offline_"+"".join(random.choices(string.ascii_lowercase,k=8))
    d["account"]="anonymous"; d["anonymous"]=1; d["bot_id"]=0
    log.info("Login handled")
    return ok(d)

@app.route("/account_check", methods=["GET","POST"])
def account_check(): return ok({"account":"anonymous","anonymous":1})

@app.route("/account_link", methods=["GET","POST"])
def account_link(): return ok({"account":"linked"})

@app.route("/welcome", methods=["GET","POST"])
def welcome(): return ok({"gold":10000,"gem":10,"attend_day":1,"attend_list":[]})

@app.route("/dailyRoutine", methods=["GET","POST"])
def daily_routine(): return ok({"daily_list":[]})

@app.route("/resource", methods=["GET","POST"])
def resource(): return ok({"resource_list":[],"patch":0})

@app.route("/nickname", methods=["GET","POST"])
def nickname():
    STATE["nickname"]=request.form.get("nickname",STATE["nickname"])
    return ok({"nickname":STATE["nickname"]})

@app.route("/tutorialSave", methods=["GET","POST"])
def tutorial_save():
    STATE["tutorial"]=int(request.form.get("tutorial",1))
    return ok({"tutorial":STATE["tutorial"]})

@app.route("/option", methods=["GET","POST"])
def option(): return ok({})

@app.route("/partySetting", methods=["GET","POST"])
def party_setting(): return ok({"party_list":[]})

@app.route("/dungeonEnt", methods=["GET","POST"])
def dungeon_ent():
    STATE["stamina"]=max(0,STATE["stamina"]-int(request.form.get("stamina",5)))
    return ok({"stamina":STATE["stamina"],"dungeon_no":request.form.get("dungeon_no",1),"area_no":request.form.get("area_no",1)})

@app.route("/dungeonClear", methods=["GET","POST"])
@app.route("/dungeonSkip", methods=["GET","POST"])
@app.route("/spDungeonClear", methods=["GET","POST"])
@app.route("/spDungeonSkip", methods=["GET","POST"])
def dungeon_clear():
    g=random.randint(500,3000); e=random.randint(50,200)
    STATE["gold"]+=g; STATE["exp"]+=e
    return ok({"gold":STATE["gold"],"exp":STATE["exp"],"level":STATE["level"],"gold_reward":g,"exp_reward":e,"mon_piece_list":[],"item_list":[]})

@app.route("/spDungeonList", methods=["GET","POST"])
def sp_dungeon_list(): return ok({"sp_dungeon_list":[]})

@app.route("/spDungeonEnt", methods=["GET","POST"])
def sp_dungeon_ent():
    STATE["stamina"]=max(0,STATE["stamina"]-int(request.form.get("stamina",5)))
    return ok({"stamina":STATE["stamina"]})

@app.route("/battleContinue", methods=["GET","POST"])
def battle_continue(): return ok({"gem":STATE["gem"]})

@app.route("/monsterEnhance", methods=["GET","POST"])
@app.route("/monsterMakeTest", methods=["GET","POST"])
def monster_enhance(): return ok({"mon_list":STATE["mon_list"],"gold":STATE["gold"]})

@app.route("/monsterFusion", methods=["GET","POST"])
def monster_fusion(): return ok({"mon_list":STATE["mon_list"],"gold":STATE["gold"]})

@app.route("/monsterEvo", methods=["GET","POST"])
@app.route("/monsterAwaken", methods=["GET","POST"])
def monster_awaken(): return ok({"mon_list":STATE["mon_list"]})

@app.route("/monsterSell", methods=["GET","POST"])
def monster_sell():
    STATE["gold"]+=500
    return ok({"gold":STATE["gold"],"mon_list":STATE["mon_list"]})

@app.route("/monsterUpgrade", methods=["GET","POST"])
@app.route("/monsterLock", methods=["GET","POST"])
@app.route("/monsterPiece", methods=["GET","POST"])
@app.route("/monsterMutate", methods=["GET","POST"])
@app.route("/markerMon", methods=["GET","POST"])
def monster_misc(): return ok({"mon_list":STATE["mon_list"]})

@app.route("/monsterRuneEquip", methods=["GET","POST"])
@app.route("/monsterRuneUnEquip", methods=["GET","POST"])
def monster_rune(): return ok({"mon_list":STATE["mon_list"],"rune_list":STATE["rune_list"]})

@app.route("/masteryEnhance", methods=["GET","POST"])
@app.route("/masterySetting", methods=["GET","POST"])
def mastery(): return ok({})

@app.route("/runePack", methods=["GET","POST"])
def rune_pack(): return ok({"rune_list":STATE["rune_list"]})

@app.route("/partPack", methods=["GET","POST"])
def part_pack(): return ok({"part_list":STATE["part_list"]})

@app.route("/capsuleAttr", methods=["GET","POST"])
@app.route("/capsuleRare", methods=["GET","POST"])
@app.route("/capsuleRare10", methods=["GET","POST"])
@app.route("/capsuleEvo", methods=["GET","POST"])
@app.route("/capsuleEvo10", methods=["GET","POST"])
@app.route("/capsuleSocial", methods=["GET","POST"])
@app.route("/capsuleSocial10", methods=["GET","POST"])
@app.route("/capsuleCoupon", methods=["GET","POST"])
def capsule():
    m={"mon_no":random.randint(10101,20101),"level":1,"grade":random.randint(1,3),
    "star":random.randint(1,3),"enhance_lv":0,"awaken":0,"lock_yn":"N",
    "slot":len(STATE["mon_list"])+1,"atk":random.randint(100,400),
    "def":random.randint(100,400),"spd":random.randint(100,400),"hp":random.randint(500,2000)}
    STATE["mon_list"].append(m)
    return ok({"mon_list":STATE["mon_list"],"new_mon":m,"gold":STATE["gold"],"gem":STATE["gem"]})

@app.route("/buyGold", methods=["GET","POST"])
def buy_gold():
    STATE["gold"]+=10000
    return ok({"gold":STATE["gold"]})

@app.route("/buyItem", methods=["GET","POST"])
@app.route("/buyShopInfo", methods=["GET","POST"])
def buy_item(): return ok({"shop_list":[]})

@app.route("/buyInapp", methods=["GET","POST"])
@app.route("/buyInappStore", methods=["GET","POST"])
@app.route("/buyInapp_test", methods=["GET","POST"])
def buy_inapp(): return ok({"gem":STATE["gem"]})

@app.route("/coinShopList", methods=["GET","POST"])
@app.route("/coinShopBuy", methods=["GET","POST"])
@app.route("/coinShopRefresh", methods=["GET","POST"])
def coin_shop(): return ok({"shop_list":[],"coin":9999})

@app.route("/guildShopList", methods=["GET","POST"])
@app.route("/guildShopBuy", methods=["GET","POST"])
def guild_shop(): return ok({"guild_shop_list":[],"guild_coin":9999})

@app.route("/arenaCheck", methods=["GET","POST"])
def arena_check(): return ok({"arena_battle_pt":STATE["arena_battle_pt"],"arena_remain_sec":86400,"arena_ranking_box":[]})

@app.route("/arenaRank", methods=["GET","POST"])
def arena_rank(): return ok({"rank_list":[],"my_rank":1})

@app.route("/arenaBattleSearch", methods=["GET","POST"])
@app.route("/arenaBattleRefresh", methods=["GET","POST"])
def arena_search(): return ok({"enemy_list":[]})

@app.route("/arenaBattleEnt", methods=["GET","POST"])
@app.route("/arenaRevengeEnt", methods=["GET","POST"])
def arena_ent(): return ok({"battle_result":1})

@app.route("/arenaBattleResult", methods=["GET","POST"])
@app.route("/arenaRevengeResult", methods=["GET","POST"])
def arena_result(): return ok({"arena_battle_pt":STATE["arena_battle_pt"],"rank":1})

@app.route("/arenaShopList", methods=["GET","POST"])
@app.route("/arenaShopBuy", methods=["GET","POST"])
def arena_shop(): return ok({"arena_shop_list":[]})

@app.route("/arenaTeam", methods=["GET","POST"])
def arena_team(): return ok({"team_list":[]})

@app.route("/raidList", methods=["GET","POST"])
def raid_list(): return ok({"raid_list":[]})

@app.route("/raidCreate", methods=["GET","POST"])
@app.route("/guildRaidCreate", methods=["GET","POST"])
def raid_create(): return ok({"raid_no":1})

@app.route("/raidEnt", methods=["GET","POST"])
@app.route("/guildRaidEnt", methods=["GET","POST"])
def raid_ent(): return ok({"raid_no":1})

@app.route("/raidResult", methods=["GET","POST"])
def raid_result(): return ok({"raid_result":1})

@app.route("/guildRaidResult", methods=["GET","POST"])
def guild_raid_result(): return ok({"raid_no":1})

@app.route("/raidRank", methods=["GET","POST"])
@app.route("/guildRaidRank", methods=["GET","POST"])
def raid_rank(): return ok({"rank_list":[]})

@app.route("/raidReward", methods=["GET","POST"])
@app.route("/guildRaidReward", methods=["GET","POST"])
def raid_reward(): return ok({"reward_list":[]})

@app.route("/towerInfo", methods=["GET","POST"])
def tower_info(): return ok({"tower_step":STATE["tower_step"],"tower_list":[]})

@app.route("/towerList", methods=["GET","POST"])
def tower_list(): return ok({"tower_list":[]})

@app.route("/towerEnt", methods=["GET","POST"])
def tower_ent(): return ok({"tower_step":STATE["tower_step"]})

@app.route("/towerClear", methods=["GET","POST"])
def tower_clear():
    STATE["tower_step"]+=1
    return ok({"tower_step":STATE["tower_step"],"reward_list":[]})

@app.route("/towerReward", methods=["GET","POST"])
def tower_reward(): return ok({"reward_list":[]})

@app.route("/deckBattleEnt", methods=["GET","POST"])
@app.route("/deckBattleEnt_test", methods=["GET","POST"])
def deck_battle_ent(): return ok({"battle_map":"battle_cave"})

@app.route("/deckBattleClear", methods=["GET","POST"])
def deck_battle_clear(): return ok({"gold":STATE["gold"],"exp":STATE["exp"]})

@app.route("/deckBattleMon", methods=["GET","POST"])
def deck_battle_mon(): return ok({"mon_list":STATE["mon_list"]})

@app.route("/deckBattleParty", methods=["GET","POST"])
def deck_battle_party(): return ok({"party_list":[]})

@app.route("/questList", methods=["GET","POST"])
@app.route("/questAccept", methods=["GET","POST"])
def quest_list(): return ok({"quest_list":[]})

@app.route("/questReward", methods=["GET","POST"])
def quest_reward(): return ok({"gold":STATE["gold"],"quest_list":[]})

@app.route("/achieveList", methods=["GET","POST"])
@app.route("/achieveReward", methods=["GET","POST"])
def achieve(): return ok({"achieve_list":[]})

@app.route("/collection", methods=["GET","POST"])
def collection(): return ok({"collection_list":[]})

@app.route("/friendList", methods=["GET","POST"])
def friend_list(): return ok({"friend_list":[],"friend_count":0})

@app.route("/friendRecommend", methods=["GET","POST"])
@app.route("/friendRequest", methods=["GET","POST"])
@app.route("/friendRequestRecv", methods=["GET","POST"])
@app.route("/friendAccept", methods=["GET","POST"])
@app.route("/friendDelete", methods=["GET","POST"])
@app.route("/friendSearch", methods=["GET","POST"])
def friend_misc(): return ok({"friend_list":[]})

@app.route("/friendSendGift", methods=["GET","POST"])
def friend_gift(): return ok({})

@app.route("/guildInfo", methods=["GET","POST"])
def guild_info(): return ok({"guild_info":None})

@app.route("/guildSearch", methods=["GET","POST"])
def guild_search(): return ok({"guild_list":[]})

@app.route("/guildCreate", methods=["GET","POST"])
def guild_create(): return ok({"guild_info":{"guild_no":1,"guild_name":"OfflineGuild"}})

@app.route("/guildApply", methods=["GET","POST"])
@app.route("/guildAccept", methods=["GET","POST"])
@app.route("/guildRetire", methods=["GET","POST"])
@app.route("/guildClose", methods=["GET","POST"])
@app.route("/guildNotice", methods=["GET","POST"])
@app.route("/guildMasterChange", methods=["GET","POST"])
@app.route("/guildOfficerAppoint", methods=["GET","POST"])
@app.route("/guildOfficerDismissal", methods=["GET","POST"])
@app.route("/guildMemberBan", methods=["GET","POST"])
@app.route("/guildMatchEnt", methods=["GET","POST"])
@app.route("/guildMatchResult", methods=["GET","POST"])
def guild_misc(): return ok({})

@app.route("/guildApplyList", methods=["GET","POST"])
def guild_apply_list(): return ok({"apply_list":[]})

@app.route("/guildRank", methods=["GET","POST"])
def guild_rank(): return ok({"rank_list":[]})

@app.route("/guildAttend", methods=["GET","POST"])
def guild_attend(): return ok({"guild_coin":9999})

@app.route("/guildMatchInfo", methods=["GET","POST"])
def guild_match_info(): return ok({"guild_match_info":None})

@app.route("/guildMatchTeam", methods=["GET","POST"])
def guild_match_team(): return ok({"team_list":[]})

@app.route("/msgBoxList", methods=["GET","POST"])
def msg_box_list(): return ok({"msg_list":[]})

@app.route("/msgBoxRead", methods=["GET","POST"])
@app.route("/msgBoxReadAll", methods=["GET","POST"])
@app.route("/teampageAdd", methods=["GET","POST"])
@app.route("/unityAdsCompleted", methods=["GET","POST"])
@app.route("/cna", methods=["GET","POST"])
def misc(): return ok({})

@app.route("/couponUse", methods=["GET","POST"])
@app.route("/deepLinkCouponUse", methods=["GET","POST"])
def coupon(): return ok({"gold":50000,"gem":50})

@app.errorhandler(404)
def not_found(e):
    log.warning(f"Unknown route: {request.path}")
    return ok({})

if __name__=="__main__":
    port=int(os.environ.get("PORT",10000))
    app.run(host="0.0.0.0",port=port,debug=False)
