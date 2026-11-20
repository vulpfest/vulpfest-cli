"""Skrip Tab completion untuk PowerShell, bash, dan zsh: `vulpfest completion <shell>`."""
import os
import sys

WORDS = "scan check leads gmaps links doctor update config completion menu --lang --version --help"

SCRIPTS = {
    "powershell": """Register-ArgumentCompleter -Native -CommandName vulpfest -ScriptBlock {
    param($wordToComplete, $commandAst, $cursorPosition)
    '%s'.Split(' ') | Where-Object { $_ -like "$wordToComplete*" } | ForEach-Object {
        [System.Management.Automation.CompletionResult]::new($_, $_, 'ParameterValue', $_)
    }
}""" % WORDS,
    "bash": """_vulpfest() { COMPREPLY=( $(compgen -W "%s" -- "${COMP_WORDS[COMP_CWORD]}") ); }
complete -F _vulpfest vulpfest""" % WORDS,
    "zsh": """_vulpfest() { compadd %s }
compdef _vulpfest vulpfest""" % WORDS,
}

HOWTO = {
    "powershell": "vulpfest completion powershell | Out-String | Invoke-Expression    (add to $PROFILE)",
    "bash": 'eval "$(vulpfest completion bash)"    (add to ~/.bashrc)',
    "zsh": 'eval "$(vulpfest completion zsh)"    (add to ~/.zshrc)',
}


def completion(args, t):
    shell = (args[0] if args else ("powershell" if os.name == "nt" else "bash")).lower()
    if shell not in SCRIPTS:
        print("Use: vulpfest completion powershell | bash | zsh")
        return 2
    print(SCRIPTS[shell])
    if sys.stdout.isatty():
        print("\n# " + t["comp_hint"] + "\n# " + HOWTO[shell], file=sys.stderr)
    return 0
