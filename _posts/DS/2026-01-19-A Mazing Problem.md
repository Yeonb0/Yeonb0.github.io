---
layout: single
title: "[DS] A Mazing Problem"
categories:
  - Data-Structure
tag: [DS, 자료구조, 격자 그래프]
---



# 3.5 A Mazing Problem

### 미로 표현 - 2차원 배열

- 1 : 막힌 길
- 0 : 통과 가능한 길

<img src="../../assets/images/posts/2026-01-19-A Mazing Problem/image.png" alt="image" style="zoom:67%;" />

- border-line 은? → 1로 둘러싸기.
    - (가로+2) * (세로+2)
    
    <img src="../../assets/images/posts/2026-01-19-A Mazing Problem/f22d4763-0782-4918-b0ab-cd7bf4048f8c.png" alt="f22d4763-0782-4918-b0ab-cd7bf4048f8c" style="zoom:67%;" />
    
    - 시작 위치 [1][1]
    - 출구 위치 [m][p]
- 8 방향으로 이동할 수 있음
    - 배열 `move` 에 가능한 방향 저장
    - <img src="../../assets/images/posts/2026-01-19-A Mazing Problem/6436bb7a-6969-4b8e-8a0d-3f3dd205f471.png" alt="6436bb7a-6969-4b8e-8a0d-3f3dd205f471" style="zoom:50%;" />
    
    
    
    ```cpp
    typedef struct {
    	short int vert; // 수직 방향
    	short int horiz; // 수평 방향
    } offsets; // 현재 위치(x)에서 어디로 이동해야 하는가?
    
    offsets move[8];
    ```
    
    → 8 방향에 대한 이동 정보 : 순서대로 이동 가능한지 확인
    
| 이름 | 방향 | move[dir].vert | move[dir].horiz |
| --- | --- | --- | --- |
| N ⬆️ | 0 | -1 | 0 |
| NE ↗️ | 1 | -1 | 1 |
| E ➡️ | 2 | 0 | 1 |
| SE ↘️ | 3 | 1 | 1 |
| S ⬇️ | 4 | 1 | 0 |
| SW ↙️ | 5 | 1 | -1 |
| W ⬅️ | 6 | 0 | -1 |
| NW ↖️ | 7 | -1 | -1 |

- 우리가 `maze[row][col]` 위치에 있다면

```cpp
nextRow = row + move[dir].vert;
nextCol = col + move[dir].horiz;
        
blue : 현재 위치
red : 이동할 값(offset)
```

`maze[nextRow][nextCol]` → 다음으로 이동할 위치
        
- `mark` : 2차원 배열, 이미 확인한 미로 위치 기록.
    - 출발 ~ 현 위치까지의 길 저장 by `stack`
    - 길 가다가 막히면 되돌아가기 위해.

### [Program 3.11] : Initial maze program

- Pseudo Code
  
    ```cpp
    미로의 입구 초기화;
    방향을 N(0)으로 초기화;
    while (stack is not empty) {  // 더 움직일 수 없을 때 까지
    	// stack 의 맨 위로 이동 
    	<row, col, dir> = stack 맨 위에서 삭제;
    	while (현 위치에서 더 움직일 수 있을 때) {
    		<nextRow, nextCol> = 다음 움직일 곳 좌표;
    		dir = 움직일 방향;
    		if ((nextRow == EXIT_ROW) && (nextCol == EXIT_COL)) // 다음 위치가 도착점이면
    			success; // 미로 탈출 성공
    		if((maze[nextRow][nextCol] == 0) && (mark[nextRow][nextCol] == 0)) {
    			// -> 다음 위치가 0이라 이동 가능 && -> 아직 안 가본 위치
    			mark[nextRow][nextCol] = 1; // mark 배열에 가본 위치라고 표시
    			// 현 위치 & 방향 저장
    			<row, col, dir> 을 stack 가장 위에 저장. // 되돌아갈 때 여기서부터만 체크하면 됨.
    			row = nextRow; col = nextCol; // 다음 위치 이동
    			dir = north; // 방향 초기화
    		} // if 문 끝
    	} // while 문 끝
    } // while 문 끝
    printf("No path found"); // 미로 탈출 실패
    ```
    
    <img src="../../assets/images/posts/2026-01-19-A Mazing Problem/73fc6054-bf23-4fca-8e6b-f53f549986c6.png" alt="73fc6054-bf23-4fca-8e6b-f53f549986c6" style="zoom:50%;" />
    
- Stack 정의

```cpp
#define MAX_STACK_SIZE 100  // PATH_MAX 최대 미로 이동 횟수
typedef struct {
	short int row;
	short int col;
	short int dir; // 그 다음 체크할 dir
} element;

element stack[MAX_STACK_SIZE];

```

### [Program 3.12] : Maze search function

- 전역 변수
    - 배열
        - `maze` : 미로 모양 (0, 1 로 구성)
        - `mark` : 이동한 위치 저장 (이동 안한 곳이면 0, 이동 했던 곳이면 1)
        - `move` : [8방향의 이동 위치 저장한 배열](https://www.notion.so/3-5-A-Mazing-Problem-134149f183d9802d85aee54374fd4313?pvs=21)
        - `stack` : 미로 이동 위치 저장한 배열
    - 상수
        - `EXIT_ROW` , `EXIT_COL` : 도착 위치
        - `TRUE` , `FALSE`
    - 변수
        - `top` : stack의 top

```cpp
void path(void) {
	// 미로의 길이 존재하면 길을 출력
	int row, col, dir;
	int nextRow, nextCol;
	int found = FALSE;
	int i; // for 루프 용
	element position; // row, col, dir 구조체
	
	// 초기 값 설정
	mark[1][1] = 1; top = 0; 
	stack[0].row = 1; stack[0].col = 1;
	stack[0].dir = 0; // 초기 방향은 N
	
	// 미로 탐색
	while (top > -1 && !found) { // found가 TRUE가 될 때 까지
		position = pop(); // stack에서 pop 해서 저장
		row = position.row; col = position.col; dir = position.dir; // stack에서 값 저장
		while (dir < 8 && !found) { // found 찾을 때까지 이동
			// dir 위치로 이동 
			nextRow = row + move[dir].vert;
			nextCol = col + move[dir].horiz;
			if (nextRow == EXIT_ROW && nextCol == EXIT_COL) {
				found = TRUE; // 다음 이동할 값이 도착점이면
			} else if (!maze[nextRow][nextCol] && !mark[nextRow][nextCol]) { // 이동 가능하면
				mark[nextRow][nextCol] = 1; // 이동하니 mark 표시
				position.row = row; position.col = col; // 지금 위치 저장
				position.dir = ++dir; // 이동 가능한 방향 저장
				push(position); // stack에 현 위치 & 방향 저장
				row = nextRow; col = nextCol; dir = 0; // 현 위치 변경(한 칸 앞으로)
			} // else if 문 끝
			else ++dir; // 이동 못하면 방향 증가
			// 8 방향 모두 시도했는데 안되면 while 문 탈출 후 stack에서 새로 pop
		} // while 문 끝
	} // while 문 끝 -> 모든 이동 경우의 수 다 해본 후
	
	// 결과 출력
	if (found) { // 찾아냈을 때
		printf("The path is : \n");
		printf("row col \n");
		for (i = 0; i <= top; i++) // push 하면 자동 top 증가.
			printf("%2d%5d\n", stack[i].row, stack[i].col); // 입구부터 출구까지 순서대로
		printf("%2d%5d\n", row, col); // 현재 위치 (도착 직전)
		printf("%2d%5d\n", EXIT_ROW, EXIT_COL); // 도착점 = nextRow, nextCol
	} else // 못 찾았을 때
		printf("The maze does not have a path \n");
} // 함수 끝
```

- 미로에서 starting position은 1, 1 → stack[0]에 저장

<img src="../../assets/images/posts/2026-01-19-A Mazing Problem/bd3f98f5-41d7-4736-9673-b69f2af31d10.png" alt="bd3f98f5-41d7-4736-9673-b69f2af31d10" style="zoom:67%;" />

<img src="../../assets/images/posts/2026-01-19-A Mazing Problem/bc164c3a-cbb0-496b-b3a2-3b725311ec59.png" alt="bc164c3a-cbb0-496b-b3a2-3b725311ec59" style="zoom: 67%;" />