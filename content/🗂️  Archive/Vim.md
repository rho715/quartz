---
title: _. Vim Keyboard Shortcut
---
## Vim 내용 정리 (for mac)

> `ctrl`: `control^`

### 입력모드
- `i`: abcd 에서 c 에 커서가 있다면 abicd
- `a`: abcd 에서 c 에 커서가 있다면 abcid
- `I`: abcd 에서 c 에 커서가 있어도 iabcd
- `A`: abcd 에서 c 에 커서가 있어도 abcdi
- [x] IntelliJ (IdeaVim)
- [x] VScode (Vim)
### Navigation
- `h, j, k, l`: 이동 커서
- `0`: 문장 앞으로 
- `$`: 문장 맨뒤로
- `w`: 단어 단위로 앞으로 이동
- `b`: 단어 단위로 백으로 이동
- `3w`: 3단어씩 이동
- `H`: **화면** 위
- `M`: **화면** 중간
- `L`: **화면** 끝
- `gg`: 파일 앞
- `G`: 파일 끝
- `20G`: 20번째 줄로 이동
- `ctrl + u`: 위로 스크롤 
- `ctrl + d`: 아래로 스크롤 
- `{`: 문단 시작 
- `}`: 문단 끝
- [x] IntelliJ (IdeaVim)
- [x] VScode (Vim)
### 명령모드
- `x`: 커서 아래 글자 삭제 
- `dd`: 문장 삭제 
- `yy`: 문장 복사
- `p`: 붙여넣기
- [x] IntelliJ (IdeaVim)
- [x] VScode (Vim)

- `*p`: 클립보드 붙여넣기 (VScode (Vim))
### command + object 
- `d` delete(cut), `y` yank(copy), `c` change 
- `d3w`: delete three words 
- `dit`: delete inner tags (works for html: `<p>vim is screen based </p>`)
- `dat`: delete at a tag
- `dap`: delete a paragraph 
- `das`: delete a sentence
- `.`: 반복
- `u`: undo 되감기
- `ctrl + R`: 앞감기 
- `d2j`: delete two rows below 
- `d3k`: delete three rows above
- `di{`: delete inside {} (ie. {hey hey hey hey asdfjasf})
- `di(`: delete inside () (ie. {hey hey hey hey asdfjasf})
- `da(`: delete all () (ie. {hey hey hey hey asdfjasf})
- `ci[`: change inside []; this puts you into insert mode (ie. [yoon, jung, rho])
- [x] IntelliJ (IdeaVim)
- [x] VScode (Vim)

### Smarter Usage
- `df(`: delete full "(" (ie. this is testing from [show , hello] (another parenthesis))
- `dt(`: delete til "(" (ie. this is testing from [show , hello] (another parenthesis)
- `d/[input keyword]`: delete search (ie. press `d/` and if you type [delete] it will delete everything that's infront of delete)
- `/`: search -> `n` next word 
- `?`: search -> `n` search backwards 
- `v`: select mode
- `vaw`: select a word 
- `ctrl + v`: block select 
- [x] IntelliJ (IdeaVim)
- [x] VScode (Vim)
### Frequently Used
- `shift + *`: find occurrence 
- `:%s/old/new/g`: to change every occurrence in the whole file.
- `:%s/old/new/gc`: to change every occurrence in the whole file with prompt.
- `shift + >/<`: indent
### Change VScode `keybinding.json` setting similar to IntelliJ
- my `keybinding.json` file

    ```json
    // Place your key bindings in this file to override the defaults
    [
    {
        "key": "ctrl+g",
        "command": "extension.vim_cmd+d",
        "when": "editorTextFocus && vim.active && vim.use<D-d> && !inDebugRepl"
    },
    {
        "key": "cmd+d",
        "command": "editor.action.copyLinesDownAction",
        "when": "editorTextFocus && !editorReadonly"
    },
    {
        "key": "shift+alt+down",
        "command": "editor.action.moveLinesDownAction",
        "when": "editorTextFocus && !editorReadonly"
    },
    {
        "key": "shift+alt+up",
        "command": "editor.action.moveLinesUpAction",
        "when": "editorTextFocus && !editorReadonly"
    },
    {
        "key": "ctrl+cmd+g", // 하.. 왜 IntelliJ 에서 처럼 똑같이 구동을 안하는걸까.. (@Intellij: "ctrl+cmd+g" -> Highlight mode -> esc -> Selection Mode -> i -> insert Mode)
        "command": "editor.action.selectHighlights"
    }
    ]

    ```

### if you want to know more 
- type [`vimtutor`](https://github.com/vim/vim/blob/master/runtime/tutor/tutor)



