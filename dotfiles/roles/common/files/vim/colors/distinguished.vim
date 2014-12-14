" Author: Kim Silkebækken <kim.silkebaekken+vim@gmail.com>
" Source repository: https://github.com/Lokaltog/vim-distinguished

" Initialization {{{
set background=dark

hi clear
if exists('syntax_on')
    syntax reset
endif

let g:colors_name = 'distinguished'

if ! has('gui_running')
    if &t_Co != 256
        echoe 'The ' . g:colors_name . ' color scheme requires gvim or a 256-color terminal'

        finish
    endif
endif
" }}}
" Color dictionary parser {{{
function! s:ColorDictParser(color_dict)
    for [group, group_colors] in items(a:color_dict)
        exec 'hi ' . group
                    \ . ' ctermfg=' . (group_colors[0] == '' ? 'NONE' :       group_colors[0])
                    \ . ' ctermbg=' . (group_colors[1] == '' ? 'NONE' :       group_colors[1])
                    \ . '   cterm=' . (group_colors[2] == '' ? 'NONE' :       group_colors[2])
    endfor
endfunction
" }}}

"	   | Highlight group                |  CTFG |  CTBG |    CTAttributes | || |   GUIFG |    GUIBG |   GUIAttributes |
"	   |--------------------------------|-------|-------|-----------------| || |---------|----------|-----------------|
call s:ColorDictParser({
            \   'Normal'                      : [    231,     '',               '']
            \ , 'Visual'                      : [    240,    253,               '']
            \
            \ , 'Cursor'                      : [     '',     '',               '']
            \ , 'lCursor'                     : [     '',     '',               '']
            \
            \ , 'CursorLine'                  : [     16,    231,               '']
            \ , 'CursorColumn'                : [    231,    237,               '']
            \
            \ , 'Folded'                      : [    249,    234,               '']
            \ , 'FoldColumn'                  : [    243,    234,               '']
            \ , 'SignColumn'                  : [    231,    233,           'bold']
            \ , 'ColorColumn'                 : [      '',   233,               '']
            \
            \ , 'StatusLine'                  : [    231,    236,           'bold']
            \ , 'StatusLineNC'                : [    244,    232,               '']
            \
            \ , 'LineNr'                      : [    243,    235,               '']
            \ , 'VertSplit'                   : [    240,     '',               '']
            \
            \ , 'WildMenu'                    : [    234,    231,               '']
            \ , 'Directory'                   : [    143,     '',           'bold']
            \ , 'Underlined'                  : [    130,     '',               '']
            \
            \ , 'Question'                    : [     74,     '',           'bold']
            \ , 'MoreMsg'                     : [    214,     '',           'bold']
            \ , 'WarningMsg'                  : [    202,     '',           'bold']
            \ , 'ErrorMsg'                    : [    196,     '',           'bold']
            \
            \ , 'Comment'                     : [    243,    '',               '']
            \ , 'vimCommentTitleLeader'       : [    250,    233,               '']
            \ , 'vimCommentTitle'             : [    250,    233,               '']
            \ , 'vimCommentString'            : [    245,    233,               '']
            \
            \ , 'TabLine'                     : [    231,    238,               '']
            \ , 'TabLineSel'                  : [    255,     '',           'bold']
            \ , 'TabLineFill'                 : [    240,    238,               '']
            \ , 'TabLineNumber'               : [    160,    238,           'bold']
            \ , 'TabLineClose'                : [    245,    238,           'bold']
            \
            \ , 'SpellCap'                    : [    231,     31,           'bold']
            \
            \ , 'SpecialKey'                  : [    239,     '',               '']
            \ , 'NonText'                     : [     88,     '',               '']
            \ , 'MatchParen'                  : [    231,     25,           'bold']
            \
            \ , 'Constant'                    : [    137,     '',           'bold']
            \ , 'Special'                     : [    150,     '',               '']
            \ , 'Identifier'                  : [     66,     '',           'bold']
            \ , 'Statement'                   : [    186,     '',           'bold']
            \ , 'PreProc'                     : [    247,     '',               '']
            \ , 'Type'                        : [     67,     '',           'bold']
            \ , 'String'                      : [    143,     '',               '']
            \ , 'Number'                      : [    173,     '',               '']
            \ , 'Define'                      : [    173,     '',               '']
            \ , 'Error'                       : [    208,    124,               '']
            \ , 'Function'                    : [    179,     '',               '']
            \ , 'Include'                     : [    173,     '',               '']
            \ , 'PreCondit'                   : [    173,     '',               '']
            \ , 'Keyword'                     : [    173,     '',               '']
            \ , 'Search'                      : [    231,    131,               '']
            \ , 'Title'                       : [    231,     '',               '']
            \ , 'Delimiter'                   : [    246,     '',               '']
            \ , 'StorageClass'                : [    187,     '',               '']
            \
            \ , 'TODO'                        : [    228,     94,           'bold']
            \
            \ , 'SyntasticWarning'            : [    220,     94,               '']
            \ , 'SyntasticError'              : [    202,     52,               '']
            \
            \ , 'Pmenu'                       : [    248,    240,               '']
            \ , 'PmenuSel'                    : [    253,    245,               '']
            \ , 'PmenuSbar'                   : [    253,    248,               '']
            \
            \ , 'phpEOL'                      : [    245,     '',               '']
            \ , 'phpStringDelim'              : [     94,     '',               '']
            \ , 'phpDelimiter'                : [    160,     '',               '']
            \ , 'phpFunctions'                : [    221,     '',           'bold']
            \ , 'phpBoolean'                  : [    172,     '',           'bold']
            \ , 'phpOperator'                 : [    215,     '',               '']
            \ , 'phpMemberSelector'           : [    138,     '',           'bold']
            \ , 'phpParent'                   : [    227,     '',               '']
            \
            \ , 'PHPClassTag'                 : [    253,     '',               '']
            \ , 'PHPInterfaceTag'             : [    253,     '',               '']
            \ , 'PHPFunctionTag'              : [    222,     '',           'bold']
            \
            \ , 'pythonDocString'             : [    240,    233,               '']
            \ , 'pythonDocStringTitle'        : [    245,    233,               '']
            \ , 'pythonRun'                   : [     65,     '',               '']
            \ , 'pythonBuiltinObj'            : [     67,     '',           'bold']
            \ , 'pythonSelf'                  : [    250,     '',           'bold']
            \ , 'pythonFunction'              : [    179,     '',           'bold']
            \ , 'pythonClass'                 : [    221,     '',           'bold']
            \ , 'pythonExClass'               : [    130,     '',               '']
            \ , 'pythonException'             : [    130,     '',           'bold']
            \ , 'pythonOperator'              : [    186,     '',               '']
            \ , 'pythonPreCondit'             : [    152,     '',           'bold']
            \ , 'pythonDottedName'            : [    166,     '',               '']
            \ , 'pythonDecorator'             : [    124,     '',           'bold']
            \
            \ , 'PythonInterfaceTag'          : [    109,     '',               '']
            \ , 'PythonClassTag'              : [    221,     '',               '']
            \ , 'PythonFunctionTag'           : [    109,     '',               '']
            \ , 'PythonVariableTag'           : [    253,     '',               '']
            \ , 'PythonMemberTag'             : [    145,     '',               '']
            \
            \ , 'CTagsImport'                 : [    109,     '',               '']
            \ , 'CTagsClass'                  : [    221,     '',               '']
            \ , 'CTagsFunction'               : [    109,     '',               '']
            \ , 'CTagsGlobalVariable'         : [    253,     '',               '']
            \ , 'CTagsMember'                 : [    145,     '',               '']
            \
            \ , 'xmlTag'                      : [    149,     '',           'bold']
            \ , 'xmlTagName'                  : [    250,     '',               '']
            \ , 'xmlEndTag'                   : [    209,     '',           'bold']
            \
            \ , 'cssImportant'                : [    166,     '',           'bold']
            \
            \ , 'DiffAdd'                     : [    112,     22,               '']
            \ , 'DiffChange'                  : [    220,     94,               '']
            \ , 'DiffDelete'                  : [    160,     '',               '']
            \ , 'DiffText'                    : [    220,     94,   'reverse,bold']
            \
            \ , 'diffLine'                    : [     68,     '',           'bold']
            \ , 'diffFile'                    : [    242,     '',               '']
            \ , 'diffNewFile'                 : [    242,     '',               '']
            \ })

hi link htmlTag            xmlTag
hi link htmlTagName        xmlTagName
hi link htmlEndTag         xmlEndTag

hi link phpCommentTitle    vimCommentTitle
hi link phpDocTags         vimCommentString
hi link phpDocParam        vimCommentTitle

hi link diffAdded          DiffAdd
hi link diffChanged        DiffChange
hi link diffRemoved        DiffDelete

" Regular text color (default was too bright!)
hi Normal ctermfg=243

