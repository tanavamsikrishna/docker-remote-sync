function run
    switch "$argv[1]"
        case release
            set git_status (git status --porcelain | string trim)
            test -n $git_status; and begin
                echo "Untracked/uncommited files exist"
            end
            read -f -P "New tag: " tag
            rg $tag pyproject.toml >/dev/null; or begin
                echo "pyproject.toml doesn't have the correct version?"
                return 1
            end
            git tag $tag
            git push --tags
            gh release create v$tag
    end
end
