---
categories:
- Devlog
date: '2026-11-06T21:28:00.000+09:00'
layout: single
series: 공장 게임 개발일지
step: 0
tags:
- C#
- Godot
- .NET
- xUnit
- GitHub Actions
title: '[공장 게임] Phase 0 : 뼈대'
toc: true
toc_sticky: true
devlog_project: factory-game
devlog_phase: 0
---

## 이번 Phase의 목표

공장 게임은 Factorio · GregTech 계열의 자동화 게임이다. 플레이어가 기계를 "설계"하고 (외피에 부품을 순서대로 끼워 넣음), 그 기계들을 벨트로 이어 자동화 라인을 만든다. 게임 설계는 문서로 먼저 끝냈고, 이번 글부터 실제 구현 기록이다.

Phase 0의 목표는 게임 기능이 아니라 **뼈대**다. 앞으로 모든 코드가 올라갈 저장소 구조를 만들고, 그 구조가 실제로 동작하는지 세 가지로 확인한다.

1. Godot 에디터를 열지 않고 `dotnet test`가 통과한다
2. Godot로 게임을 실행하면, 게임 엔진과 분리된 라이브러리 (core)가 돌려준 문자열이 화면에 보인다
3. GitHub에 push하면 GitHub Actions (push할 때마다 자동으로 테스트를 돌려 주는 서비스)가 초록불을 띄운다

## 계획

개발 계획 문서에서 정한 저장소 구조는 이렇다.

```text
factory-game/
  core/    Factory.Core : 순수 C# 라이브러리 (Godot 참조 금지)
  tests/   Factory.Core.Tests : xUnit 테스트
  data/    게임 규칙 데이터 (JSON)
  game/    Godot 프로젝트 : core를 참조해서 화면만 담당
  .github/workflows/  CI
```

핵심은 **시뮬레이션 코어를 게임 엔진에서 떼어 내는 것**이다. 기계가 재료를 어떻게 바꾸는지, 한 틱 (게임 시간의 최소 단위)에 무엇이 어떤 순서로 일어나는지는 전부 `core`에 두고, Godot는 그것을 그리는 역할만 한다. 이렇게 하면 게임 규칙을 Godot 없이 단위 테스트로 검증할 수 있고, 같은 입력이면 같은 결과가 나오는지 (결정성) 확인하기도 쉽다.

시작할 때 모르는 것 (계획 문서의 "SP1") 이 세 가지 있었다.

- Godot 버전이 요구하는 .NET 대상 프레임워크에 core · tests를 어떻게 맞출지
- Godot가 자동으로 만드는 솔루션 (.sln) · 프로젝트 (.csproj) 파일에 다른 프로젝트를 넣으면 에디터가 덮어쓰지 않는지
- CI에서 Godot 프로젝트는 빼고 테스트만 돌릴 수 있는지

## 결정과 이유

### Godot 4.7.2 .NET 판으로 올렸다

처음에는 Godot 4.6을 쓰려 했다. 그런데 프로젝트 설정에서 C# 관련 항목 (`Dotnet`) 이 아예 보이지 않았다. 확인해 보니 받은 실행 파일 이름에 `mono`가 없었다. GDScript 전용인 **일반 판**이었던 것이다. Godot는 C#을 쓰려면 이름에 `mono`가 들어간 **.NET 판**을 따로 받아야 한다.

어차피 다시 받아야 해서 최신 안정판 4.7.2로 올렸다. 공식 문서의 `stable` 판이 4.7 기준이라 문서와 에디터 버전이 같아지는 것도 이유였다. 4.8은 아직 베타라 피했다.

### 대상 프레임워크를 net10.0으로 통일했다

.NET 프로젝트는 "어느 .NET 버전용으로 빌드할지" (대상 프레임워크, TFM) 를 정해야 한다. Godot의 C# 바인딩 패키지 (GodotSharp 4.7.2) 는 net8.0용으로만 배포된다. 하지만 낮은 버전용 라이브러리는 높은 버전에서 쓸 수 있으므로, 게임 프로젝트의 TFM을 net10.0으로 올려도 된다.

두 선택지를 비교했다.

| | 전부 net8.0 | 전부 net10.0 |
|---|---|---|
| 추가 설치 | .NET 8 런타임 필요 | 없음 (이미 SDK 10 설치됨) |
| Godot 기본값과 차이 | 없음 | game csproj 한 줄 수정 |
| 지원 기간 | .NET 8 LTS는 2026-11-10 지원 종료 | .NET 10 LTS |

추가 설치가 없고 지원 기간이 긴 net10.0으로 정했다. 실행이 안 되면 csproj 세 개만 고쳐 net8.0으로 내려가면 되므로 위험도 작았다. 결과적으로 Godot는 net10.0 게임을 문제없이 실행했다.

주의할 점이 하나 있다. game · core · tests의 TFM은 맞춰야 한다. game이 net8.0인데 core가 net10.0이면, game이 core를 참조할 수 없다.

### 솔루션 파일은 저장소 루트에 두었다

Godot는 C# 솔루션 (.sln) 을 기본으로 Godot 프로젝트 폴더 (`game/`) 안에 만든다. 그러면 core · tests를 같은 솔루션에 넣기가 어색해진다. 그래서 **C# 솔루션을 만들기 전에** 프로젝트 설정 `dotnet/project/solution_directory`를 `..`로 바꿨다. 이렇게 하면 .sln이 저장소 루트에 생긴다. 그다음 `dotnet sln add`로 core와 tests를 추가했다.

### CI는 테스트 프로젝트만 돌린다

CI (지속적 통합 : push마다 자동으로 빌드 · 테스트를 돌리는 것) 는 솔루션 전체가 아니라 `tests/Factory.Core.Tests.csproj`만 지정했다. 테스트 프로젝트를 빌드하면 core도 같이 빌드되기 때문이다. 이렇게 하면 Godot 쪽 사정으로 CI가 깨질 일이 없다.

### 들여쓰기 규칙을 파일로 고정했다

내 코드 규칙은 2칸 들여쓰기다. 그런데 Godot가 만든 스크립트 템플릿은 탭이고, xUnit 템플릿은 4칸이다. 그래서 루트에 `.editorconfig`를 두어 2칸으로 고정했다. Godot가 `game/.editorconfig`를 따로 만들면서 `root = true`를 넣어 두었는데, 이 한 줄 때문에 루트 설정이 game 폴더에 적용되지 않았다. 그래서 이 줄을 지웠다.

## 구현

참조 관계는 단방향 두 줄뿐이다.

```text
tests → core ← game
```

core는 아무것도 참조하지 않는다. 그래서 core에 Godot 타입이 들어갈 길이 처음부터 없다.

확인용 코드는 일부러 작게 만들었다. core에는 버전 문자열을 돌려주는 정적 메서드 하나를 두었다.

{% raw %}
```csharp
namespace Factory.Core;

public static class CoreInfo
{
  public const string Version = "0.1.0";

  public static string GetVersion() => Version;
}
```
{% endraw %}

Godot 쪽에서는 Label 노드에 C# 스크립트를 붙였다. Godot에서 스크립트를 노드에 붙인다는 것은, 스크립트 클래스가 **그 노드 타입을 상속**한다는 뜻이다. 그래서 `Text`를 바로 쓸 수 있다. `_Ready()`는 노드가 화면 트리에 들어갔을 때 한 번 호출된다.

{% raw %}
```csharp
using Factory.Core;
using Godot;

public partial class VersionLabel : Label
{
  public override void _Ready()
  {
    Text = CoreInfo.GetVersion();
  }
}
```
{% endraw %}

`partial`은 꼭 필요하다. Godot의 소스 생성기가 클래스의 나머지 부분을 자동으로 만들어 붙이기 때문이다.

## 막혔던 점

- **일반 판 Godot** : 증상은 프로젝트 설정에 Dotnet 항목이 없는 것이었다. 원인은 실행 파일이 .NET 판이 아니었던 것이고, 파일 이름에 `mono`가 들어간 판으로 바꿔 해결했다.
- **루트 노드를 Node2D로 만듦** : UI용 루트 (`Control`) 를 고르는 버튼은 씬이 비어 있을 때만 보인다. 이미 만든 Node2D를 지우고 다시 골랐다.
- **C# 첫 사용** : Java와 비슷하지만 다른 점에서 막혔다.
  - `namespace Factory.Core;` 끝의 `;`를 빼면 파일 범위 네임스페이스가 되지 않는다
  - 변수에는 타입을 반드시 써야 하고, `return`은 메서드 안에서만 쓸 수 있다
  - `CoreInfo.GetVersion`처럼 괄호 없이 쓰면 메서드를 호출하지 않고 메서드 자체를 가리킨다
  - 클래스 이름을 `Version`으로 지으면 .NET의 `System.Version`과 겹친다
- **자동 완성이 몰래 넣은 using** : `System.Security.Cryptography.X509Certificates`가 들어가 있었다. 쓰지 않는 using은 지웠고, 비어 있는 `_Process`도 지웠다. 비어 있어도 오버라이드해 두면 매 프레임 호출되기 때문이다.
- **Actions가 시작조차 안 됨** : 첫 push의 결과는 `Startup failure`였다. 코드 문제가 아니라 GitHub 계정의 결제 정보가 잠겨 있었던 것이다. 잠금이 풀린 뒤 다시 push하니 19초 만에 초록불이 떴다.

## 결과와 배운 점

완료 기준 세 가지를 모두 충족했다.

1. `dotnet test` (Godot 없이) : 통과
2. Godot 실행 화면 왼쪽 위에 core가 돌려준 `0.1.0` 표시
3. GitHub Actions `core-tests` 초록불

처음에 모르던 세 가지의 답도 얻었다.

- Godot 4.7.2 .NET + net10.0 조합은 문제없이 동작한다 (GodotSharp는 net8.0용이지만 상위 TFM에서 쓸 수 있음)
- Godot는 이미 있는 .sln을 덮어쓰지 않는다. core · tests를 추가한 뒤 Godot에서 다시 빌드해도 프로젝트 3개가 그대로였다
- CI에서 테스트 프로젝트만 지정하면 Godot 없이 돈다. 덧붙여 `dotnet build FactoryGame.sln`도 Godot 에디터 없이 게임 프로젝트까지 빌드된다

다음 Phase 1은 **공정 코어**다. 재료와 변환 규칙을 데이터 (JSON) 로 정의하고, 기계 슬롯의 순서를 바꾸면 결과가 바뀌는지 검증하는 골든 테스트 (정답이 정해진 입력 · 출력 쌍 테스트) 를 먼저 둔다. 그다음 그 테스트를 통과하는 `ProcessResolver`를 core에 구현한다.

---

<sub>이 글은 커밋 · PR · 계획 문서 · 세션 기록을 바탕으로 초안을 만든 뒤 직접 다듬었습니다. 근거 기록 : 커밋 2개, PR 0개, 세션 기록 0개, 메모 0개 (이번 Phase에는 저장된 세션 기록 · 메모가 없어, 결정과 이유는 구현 세션의 대화와 계획 문서를 근거로 썼습니다)</sub>
