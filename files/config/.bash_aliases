# General
alias sk='nano ~/.bash_aliases && . ~/.bash_aliases && echo "Sourced new .bash_aliases"'
alias l='ls -lhX --group-directories-first'
alias la='ls -lhXa --group-directories-first'
alias c='clear'
alias ..='cd ..'
alias ...='cd ../..'
alias ....='cd ../../..'
alias path='echo $PATH | sed "s/:/\n/g"'
alias greps='ps aux | grep -v "grep" | grep'

# Galaxy
alias gxr='sudo service galaxy restart'
alias gxf='sudo journalctl -fu galaxy'
alias gxrf='sudo service galaxy restart && sudo journalctl -fu galaxy'
