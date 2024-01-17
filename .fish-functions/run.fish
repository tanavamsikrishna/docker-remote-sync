function run
    switch "$argv[1]"
        case release
            set git_status (git status --porcelain | tr -d '\n' | tr -d ' ')
            test -n "$git_status"; and begin
                echo "Untracked/uncommited files exist"
                return 1
            end
            read -f -P "New tag (a.b.c): " tag; and \\
            sd '^version = ".*"' 'version = "'$tag'"' pyproject.toml; and \\
            git add .; and \\
            git commit -m "Bump up version to"$tag; and \\
            git push; and \\
            git tag $tag; and \\
            git push --tags; and \\
            gh release create v$tag
    end
end
