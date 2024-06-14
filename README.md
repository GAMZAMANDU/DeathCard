# DeathCard
2020년 저희 서버의 이벤트제작자셨던 dtwz_님의 게임아이디어를 디스코드봇으로 구현했습니다

# 안내메시지
딕셔너리에 유저이름과 유저아이디, 유저덱제출을 자동으로 하는 기능이 만들어지지 않아 수동 기입해야합니다
<div style="width:70%;">
  <img src="https://github.com/GAMZAMANDU/DeathCard/assets/157395300/e0147c33-84d7-4b7d-b767-1390579a0310">
</div>
<div style="width:70%;">
  <img src="https://github.com/GAMZAMANDU/DeathCard/assets/157395300/9d8a3cab-066e-4b6c-84ca-4e88a9f59bba">
</div>

마지막으로 봇토큰을 넣어주세요 

# 진행방법
### `ㅎ 게임시작`으로 게임을 시작합니다
<div style="width:70%;">
  <img src="https://github.com/GAMZAMANDU/DeathCard/assets/157395300/2847af3f-62ed-4f4a-a828-8205ee9db4b4">
</div>

### 순서대로 사용자에게 카드제출을 요청하는 메시지가 DM으로 전송됩니다
<div style="width:70%;">
  <img src="https://github.com/GAMZAMANDU/DeathCard/assets/157395300/4f57b316-bf37-4d92-aa79-1aefb904cd19">
</div>

아래 설렉트바를 누르면 제출할 카드를 선택할 수 있습니다
- 제출조건에 부합하지 않는 카드는 노출되지 않습니다
- 카드제출 시간은 60초입니다, 시간내에 제출하지 않는다면 랜덤한 카드가 제출됩니다.
<div style="width:70%;">
  <img src="https://github.com/GAMZAMANDU/DeathCard/assets/157395300/510b7b6d-4e26-4631-bedf-a49f0ef662e9">
</div>

### 게임진행 상황이 게임을 시작한 채널에 전송됩니다
<div style="width:70%;">
  <img src="https://github.com/GAMZAMANDU/DeathCard/assets/157395300/e51662c3-bbc4-40f1-8884-899bcd609d53">
</div>

### 게임이 끝나면 종료됩니다
<div style="width:70%;">
  <img src="https://github.com/GAMZAMANDU/DeathCard/assets/157395300/e42d0a24-e3de-4210-8f9b-b4b0943de092">
</div>

# 추가적인 봇 명령어
1. `ㅎ 진행상황` ㅡ 게임의 모든 카드를 보여줍니다 (DM으로 전송됨)
<div style="width:70%;">
  <img src="https://github.com/GAMZAMANDU/DeathCard/assets/157395300/ed9cf546-2a21-453e-a9c7-0791ef79e1c5">
</div>

2. `ㅎ 게임설명`

- 간단한 게임 설명메시지가 전송됩니다

# 게임규칙

**< 데스노트 카드게임 >**

개인전입니다.

순서를 정하고,돌아가면서 카드를 냅니다. 조건으로 인해 카드를 낼 수 없을 경우 카드 1장을 버립니다. 모든 유저가 가진 카드가 0장이 되면 게임이 끝납니다.
게임이 끝난 뒤, 낸 카드의 점수의 합이 가장 높은 사람이 승리합니다.


필수 카드 : 무조건 넣어야 하는 카드입니다.

**키라 카드** `+7` (2장)
> 다음 유저를 공격합니다.
> 공격을 받은 경우, 공격을 막는(키라 뒤에 낼 수 있는) 카드 또는 아무 때나 낼 수 있는 카드만 낼 수 있습니다.

**의사 카드** `+3`
> 아무 때나 낼 수 있습니다.

시민팀 선택 카드 : 이 중 하나만 무조건 넣어야 하는 카드입니다.

**경찰A 카드** `+6`
> 키라가 공격했을 때에만 낼 수 있습니다.

**경찰B 카드** `+3`
> 키라가 공격했을 때에만 낼 수 있습니다.
> 다시 자신의 차례가 돌아올 때까지 키라 카드를 아무도 사용하지 못하게 합니다.

특수 카드 : 이 중 4장만 무조건 가지고 있어야 합니다.

**건달 카드** `+3`
> 다른 모든 유저의 점수를 3점씩 깎습니다.

**주술사 카드** `+0`
> 다음 턴에 내는 카드의 점수가 12점으로 고정됩니다. 
> (12점으로 고정된 카드의 점수는 변하지 않습니다 , __주술사 효과를 받는 카드는 추가 점수 획득 능력이 발동되지 않습니다__)

**용병 카드** `+5`
> 공격받았을 때만 사용 가능합니다.
> 다음 턴, 시전자가 공격을 하는 효과 발동 시 이전 유저에게 공격 효과가 적용됩니다.

**마술사 카드** `+4`
> 다음 상대가 내는 카드의 점수를 1/2로 변경합니다. (소수값 버림)

**기자 카드** `+4`
> 카드를 낼 때 자신의 이전 또는 다음의 유저 둘 중 한 명을 지정하고
> 카드를 하나 지정, 
> 지정된 유저가 지정된 카드를 가지고 있으며, 그 카드를 낼 수 있는 상황인 경우
> 지정된 유저의 의지와 상관 없이 다음 턴에 해당 카드를 내게 합니다.

# 미완성된 카드
해커의 효과가 다중적용 될 때 매끄럽지 못한 비정상적인 효과가 적용될 수 있습니다.
