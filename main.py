import discord
import asyncio
import random
from discord.ext import commands
from discord import app_commands, Interaction, Object
from discord.ui import Button, View
from discord import ButtonStyle


intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix="ㅎ ", intents=intents)


@client.event
async def on_ready():
    print(f'HURAI 실행 {client.user}')

# 기본정보 (변형 세팅)
card_land = [0]  # 카드 로그
card_type = [0]
card_point: dict = {'키라1': 7, '키라2': 7, '의사': 3,  '경찰A': 6, '경찰B': 3, '건달': 3, '주술사': 0,
                    '용병': 5, '마술사': 4, '기자': 4, '엘': 3, '니아': 7, '판사': 2, '테러리스트': 5, '영매': 10,
                    '사제': 4, '좀비': 5, '사신': 2, '조커': 0, '키라X': 7, '조력자': 5, '암살자': 6, '해커': 3, 0: 0, '신도': 3}

card_ab_exp = {'키라1': '다음 유저를 공격합니다.',
               '키라2': '다음 유저를 공격합니다.',
               '의사': '(시전 효과 없음)',
               '경찰A': '(시전 효과 없음)',
               '경찰B': '자신의 차례가 돌아올 때까지 "키라" 사용 불가',
               '건달': '다른 모든 유저의 점수를 3점씩 깎습니다.',
               # '다음 턴에 내는 카드의 점수가 12점으로 고정됩니다.(12점으로 고정된 카드의 점수는 변하지 않습니다 , 주술사 효과를 받는 카드는 추가 점수 획득 능력이 발동되지 않습니다)',
               '주술사': '(시전 효과 없음)',
               '용병': '다음 턴, 시전자가 공격을 하는 효과 발동 시 이전 유저에게 공격 효과가 적용됩니다.',
               '마술사': '다음 상대가 내는 카드의 점수를 1/2로 변경합니다. (소수값 버림)',
               '기자': "'대상'과  '카드'를 선택해, 해당 대상이 '카드'를 보유하고 있다면 강제 제출시킵니다",
               '엘': '다음 유저의 모든 카드를 확인합니다.',
               '니아': '(시전 효과 없음)',
               '판사': '이전 유저가 낸 카드의 점수를 추가로 획득합니다.',
               '테러리스트': '다음 유저를 공격, 다음 유저가 카드를 버릴 경우 추가점수 4점을 획득합니다.',
               '영매': '공격받았을 때 사용 시 3점을 추가로 획득합니다.',
               '사제': '다음 턴 유저가 낼 카드를 기도카드로 변경합니다.',
               '좀비': '1등까지 필요한 점수의 1/2를 추가로 획득합니다. (소수값 버림)',
               '사신': '최근에 버려진 카드의 점수를 추가 획득하고, 그 카드의 효과를 발동합니다.',
               '조커': '이 카드를 버렸을 경우, 모든 유저(자신 제외)의 점수를 2점 깎고, 다음 유저를 공격합니다.',
               '키라X': '다음 유저를 공격합니다.',
               '조력자': '다음 턴부터, 순서가 반대로 진행되며 다음 턴에 받는 공격 효과를 무시할 수 있습니다.',
               '암살자': '다음 유저는 키라 카드를 내야 합니다.',
               '해커': '다음 턴동안 경찰/의사 카드를 낸 유저를 다다음 턴에 공격받은 상태로 만듭니다.'}


round = 0  # 라운드
roundcard = 0  # 해당 라운드에 제출된 카드

# 가상정보값1
BotID = 1183419161507008522  # 봇 아이디 입력
gameplayer = {'사용자 아이디 ': '사용자 이름',
              '사용자 아이디': '사용자 이름'}
seq = 0  # 4명의 유저들의 차례 - 시퀀스
lastseq = {0: 3, 1: 0, 2: 1, 3: 2}  # 이전 유저의 차례 번호
nextseq = {0: 1, 1: 2, 2: 3, 3: 0}

add_point_message = ['', '', '', '']  # 해당 유저 점수의 변동폭

# 카드 특별 능력 적용
attack = 0
ab_helper = 0
hack = 0

# class


class Player:
    def __init__(self, deck: list, name) -> str:
        self.name = name
        self.deck: str = ['키라1', '키라2', '의사']+deck
        self.ab_policeB = 0
        self.ab_sorcerer = 0
        self.ab_mercenary = 0
        self.ab_magician = 0
        self.ab_attacked = 0
        self.ab_reporter = 0
        self.ab_hacked = 0
        self.throw = 0
        self.point = 0
        self.rank = None
        self.defend = 0
        self.last_place = 0
        self.neutra = 0  # 무력화 당했는가?
        self.ab_terror = 0
        self.ab_priest = 0
        '''
        self.card_count : dict = {'키라' : 2,'의사'  : 1,  '경찰A' : 0, '경찰B' : 0, '건달' : 0, '주술사' : 0, 
                    '용병' : 0, '마술사' : 0, '기자' : 0, '엘' : 0, '니아' : 0, '판사' : 0, '테러리스트' : 0, '영매' : 0,
                    '사제' : 0, '좀비' : 0, '사신' : 0, '조커' : 0, '키라X' : 0, '조력자' : 0, '암살자' : 0, '해커' : 0}
        for i in range(2,8):
            self.card_count[self.deck[i]] = 1 #모든 카드 갯수  = 1'''


# ab 감소


# 4턴마다해야함..
def decrease(A):
    for i in range(len(A)):
        if A[i] > 0:
            A[i] -= 1


# 가상정보값2
p1 = Player(['경찰A', '사신', '건달', '용병', '판사', '엘'], "사용자 아이디")
p2 = Player(['경찰B', '사신', '영매', '용병', '좀비', '조력자'], "사용자 아이디")
p3 = Player(['경찰B', '사신', '기자', '용병', '해커', '조커'], "사용자 아이디")
p4 = Player(['경찰A', '사신', '키라X', '용병', '해커', '사제'], "사용자 아이디")

player_number = {0: p1, 1: p2, 2: p3, 3: p4}
playername = [p1.name, p2.name, p3.name, p4.name]


# rank
def rank_players(players):
    # last_place 초기화
    for i in range(4):
        player_number[i].last_place = 0
    # (이름, 플레이어) 튜플의 리스트로 변환
    enumerated_players = list(players.items())

    # point를 기준으로 내림차순으로 정렬
    sorted_players = sorted(
        enumerated_players, key=lambda x: x[1].point, reverse=True)

    # 동점자를 처리하면서 순위 부여
    current_rank = 1
    current_score = sorted_players[0][1].point
    for i, (player_name, player) in enumerate(sorted_players, start=1):
        if i > 1 and player.point < current_score:
            # 이전 플레이어보다 점수가 낮은 경우
            current_rank += 1

        # 순위 부여
        players[player_name].rank = current_rank
        current_score = player.point

    last_players = [player[1]
                    for player in sorted_players if player[1].rank == current_rank]
    for last_player in last_players:
        last_player.last_place = 1

    '''
    for player_name, player in player_number.items():
        print(f"{player_name} - Rank: {player.rank} - Point: {player.point}")
        '''


# 좀비카드
players = {
    '1': p1,
    '2': p2,
    '3': p3,
    '4': p4}


def rank():
    # point를 기준으로 플레이어를 정렬
    sorted_players = sorted(
        players.items(), key=lambda x: x[1].point, reverse=True)

    # 정렬된 플레이어 순위 출력
    for i, (player_name, player) in enumerate(sorted_players, start=1):
        players[player_name].rank = i


def find_player_by_rank(players_dict, rank_to_find):
    # rank_to_find이 지정된 값인 플레이어를 찾음
    found_player = None
    for player_name, player in players_dict.items():
        if player.rank == rank_to_find:
            found_player = player
            break

    # 찾은 플레이어를 반환, 없으면 None 반환
    return found_player
# ㅡㅡ

# 카드 시전가능 여부 판단 함수


def avail(deck):
    avail_deck = set()
    deck = set(deck)
    after_kira = {'키라X', '경찰A', '경찰B'}  # 키라 후 제출 가능한 카드
    minusdeck = set()
    after_attack = {'용병', '테러리스트'}  # 공격 후 시전 가능
    every_card = deck & {'의사', '조력자'}  # 공격 면역
    if player_number[seq].last_place == 1:
        every_card |= (deck & {'판사'})
    if player_number[seq].throw > 0:
        every_card |= (deck & {'영매'})
    after_police = {'엘', '니아'}
    after_docter = {'암살자'}
    base_deck = deck - (after_attack | after_police | after_docter |
                        {'좀비', '사제', '판사', '영매', '암살자', '사신'} | after_kira)  # 일반카드

    # ――――――공격을 당했는가 ―――――――
    if player_number[seq].ab_attacked == 1:  # 공격을 당했는가
        avail_deck = avail_deck | (deck & after_attack)
        # ――――――"키라에게" 공격을 당했는가 ―――――――
        if card_land[round-1] == '키라1' or card_land[round-1] == '키라2':  # 공격카드가 키라인가?
            avail_deck = avail_deck | (deck & after_kira)

    # ――――――시민팀(경찰)가 이전 카드인가 ―――――――
    if card_land[round-1] == '경찰A' or card_land[round-1] == '경찰B':
        base_deck = base_deck | (deck & after_police)

    # ――――――시민팀(의사)가 이전 카드인가 ―――――――
    if card_land[round-1] == '의사':
        base_deck = base_deck | (deck & after_docter)

    # ――――――카드 수가 3장 이하인가 ―――――――
    if len(player_number[seq].deck) <= 3:
        base_deck = base_deck | (deck & {'좀비', '사제'})

    # ――――――경찰b 능력 적용――――――
    policeB = [p1.ab_policeB, p2.ab_policeB, p3.ab_policeB, p4.ab_policeB]
    if 1 in policeB and player_number[seq].ab_policeB != 1:
        minusdeck = {'키라1', '키라2'}

    # ――――――이전 유저가 카드를 버렸는 가 ―――――――
    if card_type[round-1] == '버림':
        base_deck = base_deck | (deck & {'사신'})

    # 정리
    if player_number[seq].ab_attacked != 1:
        deck = base_deck - minusdeck
    else:
        deck = avail_deck - minusdeck

    deck = list(deck | every_card)
    return deck

    # 버렸는가? 나중에
    # 카드 일정수 이하에 시전


def effect_set(card):
    global ab_helper, hack, round
    attackcard = ['키라1', '키라2', '테러리스트', '키라X', '용병']
    if card_type[round] == '버림':
        attackcard.append('조커')
    # 소모된 능력 제거
    if player_number[seq].ab_policeB == 1 and card != '경찰B':
        player_number[seq].ab_policeB = 0
        # 용병 능력 발동
    if player_number[seq].ab_mercenary == 1:
        player_number[seq].ab_mercenary = 0
        if card in attackcard and player_number[seq].neutra != 1:
            player_number[lastseq[seq]].ab_attacked = 1

    if card_type[round] == '일반':
        if player_number[seq].neutra == 0:  # 무력화가 아니라면
            # 능력 적용 판정
            if card == '키라1' or card == '키라2':
                if not player_number[nextseq[seq]].defend > 0:
                    player_number[nextseq[seq]].ab_attacked = 1
            if card == '암살자':
                player_number[nextseq[seq]].neutra = 1

            if card == '경찰B':
                player_number[seq].ab_policeB = 1

            if card == '주술사':  # 현재 내 카드가 주술사 ->지금은 아니야 , 1-> 지금이야
                player_number[seq].ab_sorcerer = 2
            else:
                if player_number[seq].ab_sorcerer == 2:
                    player_number[seq].ab_sorcerer = 1

            if card == '용병':
                player_number[seq].ab_mercenary = 1

            if player_number[nextseq[seq]].defend > 0:
                player_number[nextseq[seq]].defend -= 1
                player_number[nextseq[seq]].ab_attacked = 0

            if card == '조력자':
                if ab_helper == 0:
                    ab_helper = 1
                else:
                    ab_helper = 0
                player_number[seq].defend = 1
            if card == '키라X':
                player_number[nextseq[seq]].ab_attacked = 1
            if card == '마술사':
                player_number[nextseq[seq]].ab_magician = 1
            if card == '기자':
                pass
            if card == '해커':
                hack = 3  # 3
                # print("능력 on")
            if card == '테러리스트':
                player_number[nextseq[seq]].ab_attacked = 1
                player_number[nextseq[seq]].ab_terror = 1
            if card == '사제':
                player_number[nextseq[seq]].ab_priest = 1

    # 해커 능력 적용
        if hack == 2:
            if card == '의사' or card == '경찰B' or card == '경찰A':
                player_number[seq].ab_hacked = 2
                # print("해킹")
        if round % 4 == 0:
            if hack == 3:
                # print("해킹 능력 적용..") #2
                hack -= 1
            else:
                if hack == 2:
                    hack -= 1
                    # print("해킹 완료 종료") #1
                    for i in range(4):
                        if player_number[i].ab_hacked == 2:  # 형식적인 공격당함 표기
                            player_number[i].ab_hacked = 1
                            player_number[i].ab_attacked = 1
                # else:
                #     if hack == 1:
                #         hack = 0

    if card_type[round] == '버림':  # 카드 == '버림'
        player_number[seq].throw = 1

# 전광판 추가 메시지 설정


def add_point(card):
    global add_point_message, players, round

    add_point_message = ['', '', '', '']
    addextra = 0

    # 사신 관련
    def reaper_condition(x): return (
        roundcard == '사신' and card_type[round] == '일반' and card_land[round-1] == x and card_land[round-1] in avail(list(card_ab_exp)))

    if player_number[seq].neutra == 0:  # 무력화가 아니라면
        if card == '건달' or reaper_condition('건달'):  # 건달 능력 적용
            for i in range(4):
                if seq != i:
                    player_number[i].point -= 3
                    add_point_message[i] += '**(-3)**'

        if card_type[round] == '버림':  # 카드 == '버림'
            if card == '조커':
                for i in range(4):
                    if seq != i:
                        player_number[i].point -= 2
                        player_number[nextseq[seq]].ab_attacked = 1
                        add_point_message[i] += '**(-2)**'

        if card == '판사' and card_type[round-1] == '일반' or reaper_condition('판사'):
            print(f'판사 카드 전 카드 {
                  card_land[round-1]} 그리고 점수 {card_point[card_land[round-1]]}')
            addextra += card_point[card_land[round-1]]

        if card == '좀비' or reaper_condition('좀비'):
            rank()
            rank1 = find_player_by_rank(players, 1)
            addextra += int((rank1.point - player_number[seq].point)/2)

        if card == '신도':
            player_number[nextseq[seq]].point -= 3
            add_point_message[nextseq[seq]] += '(-3)'

        if card == '사신' and card_type[round-1] == '버림':
            addextra += card_point[card_land[round-1]]

    # 테러리스트 능력 적용
    if player_number[seq].ab_terror == 1:
        player_number[seq].ab_terror = 0
        if card_type[round] == '버림':
            player_number[lastseq[seq]].point += 4
            add_point_message[lastseq[seq]] += '**(+4)**'

    if card == '영매' or reaper_condition('사신'):
        if player_number[seq].ab_attacked == 1:
            addextra += 3

    if player_number[seq].ab_sorcerer == 1:  # 주술사 능력 발동
        extra = 12
        player_number[seq].ab_sorcerer = 0
    else:
        if player_number[seq].ab_magician == 1:  # 마술사
            extra = int(card_point[card]/2)  # 기본점수 1/2
            player_number[seq].ab_magician = 0
        else:
            if card_type[round] == '버림':
                extra = 0
            else:
                extra = card_point[card]+addextra

    # 전광판 출력
    if extra >= 0:
        add_point_message[seq] += f'**(+{extra})**'
        player_number[seq].point += extra
    else:
        add_point_message[seq] += f'**({extra})**'
        player_number[seq].point += extra

    # 표기
    for i in range(4):
        if player_number[i].defend > 0:  # 조력자 공격 면역
            add_point_message[i] += '(🛡)'

        # 용병 능력 적용
        if player_number[i].ab_mercenary > 0:
            add_point_message[i] += '(🪖)'

        # 마술사 능력 적용
        if player_number[i].ab_magician > 0:
            add_point_message[i] += '(🎩)'

        # 암살자 능력 적용
        if player_number[i].neutra > 0:
            add_point_message[i] += '(🚫)'

        # 테러리스트 능력 적용
        if player_number[i].ab_terror == 1:
            add_point_message[i] += '(🧨)'

        # 사제 능력 적용
        if player_number[i].ab_priest == 1:
            add_point_message[i] += '(🛐)'

        # 기자 능력 적용
        if player_number[i].ab_reporter != 0:
            add_point_message[i] += '(🧲)'

    # 엘 능력 적용 표시
    if card == '엘':
        add_point_message[nextseq[seq]] += '(🔍)'

    player_number[seq].ab_attacked = 0
    player_number[seq].neutra = 0

    if player_number[seq].ab_hacked == 1:
        player_number[seq].ab_attacked = 1
        player_number[seq].ab_hacked = 0

        # 상태이상 표시
    for i in range(4):
        if player_number[i].ab_attacked == 1:
            add_point_message[i] += '(🩸)'


# 조력자 능력
def helper():
    global player_number, playername
    # 값들을 역순으로 정렬하여 새로운 딕셔너리 생성
    player_number = {k: player_number[len(
        player_number) - 1 - k] for k in player_number}
    playername = playername[::-1]


# ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ


@client.command(name="게임시작")
async def wait(ctx):
    global gameworld, roundcard, seq, ab_reporter_user, ab_reporter_card, round, ab_helper, hack, nextseq, lastseq, add_point_message
    gameworld = ctx  # 게임을 생성한 채팅방을 게임메시지를 보내는 장소로 지정

    # 순서 정하기
    # random.shuffle(playername) #순서 셔플
    embed = discord.Embed(title='#게임을 시작합니다! ∥ 순서 공개',
                          description=f'<@!{playername[0]}> → <@!{playername[1]}> → <@!{playername[2]}> → <@!{playername[3]}>', color=discord.Color.random())
    await ctx.send(embed=embed)

    for round in range(1, 37):  # 라운드 진행
        print(f'라운드 {round} ㅡ')
        rank()  # 랭크 돌리기
        rank_players(player_number)  # 랭크 돌리기2

        if seq == 0 and ab_helper == 1:  # 조력자 능력
            helper()
            embed = discord.Embed(title='#조력자 능력발동! ∥ 순서가 거꾸로 진행됩니다',
                                  description=f'<@!{playername[0]}> → <@!{playername[1]}> → <@!{playername[2]}> → <@!{playername[3]}>', color=discord.Color.random())
            await gameworld.send(embed=embed)
            ab_helper = 0
            add_point_message = add_point_message[::-1]

        if seq == 0 and hack == 1:  # 해커 능력
            for i in range(4):
                if player_number[i].ab_hacked == 1:
                    player_number[i].ab_hacked = 0
                    player_number[i].ab_attacked = 1
            embed = discord.Embed(title='#해커 능력 발동! ∥ 이전 턴 "시민팀" 카드를 낸 유저들은 공격당합니다!',
                                  description=None, color=discord.Color.random())
            await gameworld.send(embed=embed)
            hack = 0

        user = await client.fetch_user(playername[seq])  # Dm 보낼 user 지정

        # DM 임베드 세팅
        embed_msg = '#당신의 차례!'
        embed_color = 0xff4747
        if len(avail(player_number[seq].deck)) == 0:  # 카드 ㅡ 버리기 상황일 경우
            embed_msg = '#카드 버리기!'
            embed_color = 0xffffff

        embed = discord.Embed(title=f"{embed_msg} {player_number[seq].point}점 {
                              add_point_message[seq]}", description="▼ 보유중인 카드 표시", color=embed_color)
        for i in range(len(player_number[seq].deck)):
            embed.add_field(name=f'• {player_number[seq].deck[i]}', value="")
        embed.set_footer(text="'카드를 선택해주세요!'를 눌러 제출할 카드를 선택해주세요. (60초 제한)")
        await user.send(embed=embed)
        # ―――――――――――――――――――――――――――――――

        # 종류 구분 ∥ 버리기 / 강제 선택 / 일반
        if len(avail(player_number[seq].deck)) == 0:  # 카드 ㅡ 버리기 상황일 경우
            d = await user.send(view=ThrowSelect())
        else:
            kira_dict = {'키라1': '키라2', '키라2': '키라1'}  # 키라 1 = 키라 2
            # ▼ 기자 ㅡ '강제 시전'일 경우
            # 기자 관련
            if player_number[seq].ab_reporter in avail(player_number[seq].deck) or kira_dict.get(player_number[seq].ab_reporter) in avail(player_number[seq].deck):
                def search_kira():  # 키라 갯수 확인
                    kira_number = 0
                    if '키라1' in avail(player_number[seq].deck):
                        kira_number += 1
                    if '키라2' in avail(player_number[seq].deck):
                        kira_number += 1
                    return kira_number
                print(search_kira())
                if search_kira() == 1 and player_number[seq].ab_reporter in ['키라1', '키라2']:
                    roundcard = list({'키라1', '키라2'} & set(
                        avail(player_number[seq].deck)))[0]
                else:
                    roundcard = player_number[seq].ab_reporter
                card_type.append("일반")
                # 강제시전 안내 문구 (피해자)
                embed = discord.Embed(
                    title=f"강제 사용됨 ∥  카드 - {roundcard}", description=None, color=0xfedf43)
                user = await client.fetch_user(playername[seq])
                await user.send(embed=embed)
            # ▼ 카드 ㅡ 일반
            else:
                d = await user.send(view=Select())

        embed_msg = '강제사용'  # 기자 관련
        # ▼ 기자 ㅡ '강제 시전'이 아닐 경우 ㅡ 정상 메시지 보낸 후 기다리기
        # 기자 관련
        if not player_number[seq].ab_reporter in avail(player_number[seq].deck) and not kira_dict.get(player_number[seq].ab_reporter) in avail(player_number[seq].deck):
            timeout = 60  # 기다릴 시간 정하기
            send_message = await ctx.send(f'**#라운드 {round}** 카드를 제출해주세요! ({timeout}초)')

            def check(m):  # check 메서드 정의
                # (m.author.id)
                return m.author.id == BotID and m.content == '―― 카드제출 완료! ――'

            try:  # 60초간 기다림
                msg = await client.wait_for('message', check=check, timeout=timeout)

            except asyncio.TimeoutError:  # 5초가 지나면 TimeoutError 발생 ㅡ 게임 유기 상황
                global for_reporter_z

                if roundcard == '기자':  # 라운드 카드를 기자로 낸 경우
                    try:
                        await for_reporter_z.delete()  # 기자 설렉트 메뉴를 삭제
                    except:
                        pass  # 아니면 패스

                if len(avail(player_number[seq].deck)) == 0:  # 버리기 상황이다면?
                    roundcard = random.choice(player_number[seq].deck)
                    card_type.append("버림")
                    player_number[seq].ab_attacked = 0
                    embed_msg = '게임 유기됨(버림)'

                else:  # 일반 상황이다면?
                    roundcard = random.choice(avail(player_number[seq].deck))
                    card_type.append("일반")
                    embed_msg = '게임 유기됨(일반)'

            else:  # 정상 제출인 경우
                if card_type[round] == '버림':
                    embed_msg = '카드버림'
                else:
                    embed_msg = '카드'

        # DM 메시지 지우기
        try:
            await d.delete()
        except:
            pass

        # 1. 이번 라운드 유저의 덱에서 선택된 카드 지우기
        player_number[seq].deck.remove(roundcard)

        if player_number[seq].ab_priest == 1:  # 사제의 신도 능력이 적용되었는가?
            roundcard = '신도'
            player_number[seq].ab_priest = 0

        card_land.append(roundcard)  # 2. 카드 로그 입력

        # 카드 ㅡ 사신이라면?
        if roundcard == '사신' and card_type[round] == '일반':
            if card_land[round-1] in avail(list(card_ab_exp)):
                print('사신 능력 발동..')
                effect_set(card_land[round-1])
            print(f'사신 전 카드 {card_land[round-1]}')
            add_point('사신')
            print(avail(list(card_ab_exp)))
        else:
            effect_set(roundcard)
            add_point(roundcard)

        rank_players(player_number)  # 랭크 함수
        rank_em = {0: '', 1: '🥇', 2: '🥈', 3: '🥉', 4: ''}  # 랭킹 이모지

        # 카드 제출 발표 메시지 보내기
        embed = discord.Embed(title=f'#{round} 라운드 ∥ {embed_msg} - **{roundcard}**',
                              description=f'카드 제출자 : <@!{playername[seq]}>', color=discord.Color.random())
        for i in range(4):
            if i == seq:
                embed.add_field(name=f'▶{rank_em[player_number[i].rank]} {gameplayer[playername[i]]}', value=f'{
                                player_number[i].point}점 {add_point_message[i]}', inline=False)
            else:
                embed.add_field(name=f'•{rank_em[player_number[i].rank]} {gameplayer[playername[i]]}', value=f'{
                                player_number[i].point}점 {add_point_message[i]}', inline=False)
        embed.set_footer(text='전체 진행상황 보기 ― "ㅎ 진행상황"')
        await ctx.send(embed=embed)

        # 엘의 특수능력
        if roundcard == '엘':
            user = await client.fetch_user(playername[seq])
            embed = discord.Embed(title=f"#🔍 엘 능력 발동!",
                                  description="▼ 다음 턴 유저의 덱", color=0xfedf43)
            for i in range(len(player_number[nextseq[seq]].deck)):
                embed.add_field(
                    name=f'• {player_number[nextseq[seq]].deck[i]}', value="")
            await user.send(embed=embed)

        # 기자 능력 종료
        player_number[seq].ab_reporter = 0

        # 순서 진행시키기
        if seq < 3:
            seq += 1
        else:
            seq = 0

    # 게임종료
    rank_players(player_number)
    embed = discord.Embed(title="#게임 종료", description="",
                          color=discord.Color.random())
    for ranks in range(1, 5):
        for i in range(4):
            if player_number[i].rank == ranks:
                embed.add_field(name=f"• {rank_em[ranks]}{ranks}등 ― {
                                player_number[i].point}점", value=f"<@!{player_number[i].name}>", inline=False)
    await gameworld.send(embed=embed)

# 카드 선택 ㅡ 일반


class SelectMenu(discord.ui.Select):
    def __init__(self):
        global roundcard
        round_deck = avail(player_number[seq].deck)
        deck_list = []
        for i in range(len(round_deck)):
            deck_list.append(discord.SelectOption(label=round_deck[i], emoji='🎴', description=f'(+{
                             card_point[round_deck[i]]}) {card_ab_exp[round_deck[i]]}'))
        options = deck_list
        super().__init__(placeholder="카드를 선택해주세요",
                         options=options, min_values=1, max_values=1)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(content=f"{self.values[0]}를 선택하셨습니다.")
        global roundcard
        roundcard = self.values[0]
        card_type.append('일반')
        if roundcard == '기자':
            user = await client.fetch_user(playername[seq])
            global for_reporter_z
            for_reporter_z = await user.send(view=ReporterMenuSelect())
        else:
            await gameworld.send('―― 카드제출 완료! ――')


class Select(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(SelectMenu())


# ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ

# 카드 선택 ㅡ 버리기
class ThrowMenu(discord.ui.Select):
    def __init__(self):
        deck_list = []
        round_deck = player_number[seq].deck
        for i in range(len(round_deck)):
            deck_list.append(discord.SelectOption(label=round_deck[i], emoji='🗑', description=f'(+{
                             card_point[round_deck[i]]}) {card_ab_exp[round_deck[i]]}'))
        options = deck_list
        super().__init__(placeholder="🗑 버릴 카드를 선택해주세요",
                         options=options, min_values=1, max_values=1)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(content=f"{self.values[0]}를 버리셨습니다.")
        global roundcard
        roundcard = self.values[0]
        card_type.append('버림')
        player_number[seq].ab_attacked = 0
        await gameworld.send('―― 카드제출 완료! ――')


class ThrowSelect(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(ThrowMenu())
# ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ

# 기자 특수능력 클래스 1


class ReporterMenu1(discord.ui.Select):
    def __init__(self):
        options = [discord.SelectOption(label=f'{int(lastseq[seq])+1}번 플레이어 ― {gameplayer[playername[lastseq[seq]]]}', description="", emoji="🔸"),
                   discord.SelectOption(label=f'{int(nextseq[seq])+1}번 플레이어 ― {gameplayer[playername[nextseq[seq]]]}', description="", emoji="🔸")]
        super().__init__(placeholder="[취재] 효과를 적용시킬 대상을 선택하세요.",
                         options=options, min_values=1, max_values=1)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(content=f"{self.values[0]}님을 선택하셨습니다.")
        user = await client.fetch_user(playername[seq])
        global for_reporter_z
        await for_reporter_z.delete()
        for_reporter_z = await user.send(view=ReporterMenuSelect2((int(self.values[0][:1]))-1))

        # [seq]


class ReporterMenuSelect(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(ReporterMenu1())

# 기자 특수능력 클래스 2


class ReporterMenu2(discord.ui.Select):
    def __init__(self, user):
        global for_reporter_user_in_def
        for_reporter_user_in_def = user
        deck_list1 = []
        card_list = list(card_ab_exp)
        for i in card_list:
            deck_list1.append(discord.SelectOption(
                label=i, description="", emoji="🔸"))
        options = deck_list1
        super().__init__(placeholder="강제 시전할 카드를 선택해주세요.",
                         options=options, min_values=1, max_values=1)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(content=f"**{gameplayer[player_number[for_reporter_user_in_def].name]}**님에게 강제시전 시킬 카드로 **{self.values[0]}**를 선택하셨습니다.")
        player_number[for_reporter_user_in_def].ab_reporter = self.values[0]
        await for_reporter_z.delete()
        await gameworld.send('―― 카드제출 완료! ――')


class ReporterMenuSelect2(discord.ui.View):
    def __init__(self, user):
        super().__init__()
        self.add_item(ReporterMenu2(user))


# ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ


# 잡다 명령어

# dm
@client.command(name="진행상황")
async def open_progress(ctx):
    user = await client.fetch_user(ctx.author.id)
    embed = discord.Embed(title="#🎮 게임 진행상황", color=0xff4747)
    iseq = 0
    forprogress = []
    playernames = playername
    for i in range(1, len(card_land)):
        embed.add_field(name=f'라운드 {i} ― {gameplayer[playernames[iseq]]}', value=f'{
                        card_land[i]}', inline=False)
        forprogress.append(card_land[i])
        if iseq < 3:
            iseq += 1
        else:
            iseq = 0
            if forprogress.count("조력자") % 2 != 0:
                embed.add_field(name=f'―――――순서 뒤집어짐­―――――',
                                value='', inline=False)
                playernames = playernames[::-1]
            else:
                embed.add_field(name=f'―――――――――――――――――――――――',
                                value='', inline=False)
                playernames = playername
            forprogress = []
    await user.send(embed=embed)

# 도감


@client.command(name="도감")
async def dictionary(ctx):
    await ctx.send()


@client.command(name="게임설명")
async def dictionary2(ctx):
    await ctx.send("- 순서를 정하고,돌아가면서 카드를 냅니다.\n- 조건으로 인해 카드를 낼 수 없을 경우 카드 1장을 버립니다.\n- 모든 유저가 가진 카드가 0장이 되면 게임이 끝납니다.\n- 게임이 끝난 뒤, 낸 카드의 점수의 합이 가장 높은 사람이 승리합니다.")

# 도감


@client.command(name="카드박스 열기")
async def open_box(ctx):
    pass

# 게임참여


@client.command(name="게임열기")
async def button(ctx):
    view = Menu()
    await ctx.reply(view=view)


class Menu(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label="👋 게임참가", style=discord.ButtonStyle.green)
    async def menu1(self, interaction: discord.Integration, button: discord.ui.button):
        await interaction.response.send_message("hi")

    @discord.ui.button(label="나가기", style=discord.ButtonStyle.danger)
    async def menu2(self, interaction: discord.Integration, button: discord.ui.button):
        await interaction.response.edit_message(content="exit")
# ㅡㅡㅡㅡ

# CREAT GAME.


@client.command(name="게임생성")
async def gamecreate(ctx):
    gameplayer1 = {}
    embed = discord.Embed(
        title="🎉 게임을 시작합니다!", description="게임에 참여하실 분들은 아래 버튼을 눌러주세요", color=0xfe3939)
    embed.set_footer(text="⚠ 상호작용 실패 메시지와 무관하게 정상 작동합니다.")
    messages = await ctx.send(embed=embed)

    async def button_callback(interaction):
        user = interaction.user
        if not user.id in list(gameplayer1):
            # 메시지를 수정해서 유저가 참여한 것을 표시
            await messages.edit(content=f"{user.mention}님이 게임에 참여하셨습니다")
            gameplayer1[user.id] = user
            chembed = discord.Embed(
                title="🎉 게임을 시작합니다!", description="게임에 참여하실 분들은 아래 버튼을 눌러주세요", color=0xfe3939)
            chembed.set_footer(text="⚠ 상호작용 실패 메시지와 무관하게 정상 작동합니다.")
            for i in range(len(list(gameplayer1))):
                chembed.add_field(name=f"{list(gameplayer1.values())[
                    i]}", value="", inline=True)
            await messages.edit(embed=chembed)
#        else:
#            await interaction.followup.send("이미 게임에 참여하셨습니다")

    async def button_callback2(interaction):
        user = interaction.user
        # 메시지를 수정해서 유저가 퇴장한 것을 표시
        await messages.edit(content=f"{user.mention}님이 퇴장하셨습니다")
        if user.id in list(gameplayer1):
            del gameplayer1[user.id]
            chembed = discord.Embed(
                title="🎉 게임을 시작합니다!", description="게임에 참여하실 분들은 아래 버튼을 눌러주세요", color=0xfe3939)
            for i in range(len(list(gameplayer1))):
                chembed.add_field(name=f"{list(gameplayer1.values())[
                    i]}", value="", inline=True)
            chembed.set_footer(text="⚠ 상호작용 실패 메시지와 무관하게 정상 작동합니다.")
            await messages.edit(embed=chembed)
#
#        else:
#            await interaction.followup.send("게임에 참여하지 않았습니다")

    button1 = Button(label='게임참가', style=discord.ButtonStyle.green, emoji='👋')
    button2 = Button(label='나가기', style=discord.ButtonStyle.danger, emoji='⛔')
    button1.callback = button_callback
    button2.callback = button_callback2

    view = View()
    view.add_item(button1)
    view.add_item(button2)
    m = await ctx.send(view=view)

    # 3초(원하는 시간) 후에 메시지 삭제
    await asyncio.sleep(3)
    await m.delete()
    await messages.delete()
    # 게임 완성후 여기다가 만드셈

client.run('봇 토큰 넣으세요')
